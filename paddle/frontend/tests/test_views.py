import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from games.models import Player, Match
from datetime import date, timedelta
from django.test import Client
import json
from frontend import views

@pytest.mark.django_db
class TestFrontendViews:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass", email="test@example.com")
        self.player = Player.objects.create(name="testuser", registered_user=self.user, wins=5, ranking_position=1)
        self.other_player = Player.objects.create(name="other", wins=2, ranking_position=2)
        self.match = Match.objects.create(
            team1_player1=self.player,
            team1_player2=self.other_player,
            team2_player1=self.other_player,
            team2_player2=self.player,
            winning_team=1,
            date_played=date.today()
        )

    def test_hall_of_fame_view(self):
        url = reverse("hall_of_fame")
        response = self.client.get(url)
        assert response.status_code == 200
        assert b"Hall of Fame" in response.content

    def test_register_view_get(self):
        url = reverse("register")
        response = self.client.get(url)
        assert response.status_code == 200
        assert b"New Player" in response.content

    def test_register_view_post_new_player(self):
        url = reverse("register")
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass",
            "confirm_password": "newpass",
            "player_id": "",
        }
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200
        assert User.objects.filter(username="newuser").exists()

    def test_register_view_post_existing_player(self):
        url = reverse("register")
        player = Player.objects.create(name="unlinked", wins=0, ranking_position=3)
        data = {
            "username": "linkeduser",
            "email": "linked@example.com",
            "password": "linkedpass",
            "confirm_password": "linkedpass",
            "player_id": str(player.id),
        }
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200
        assert User.objects.filter(username="linkeduser").exists()
        player.refresh_from_db()
        assert player.registered_user.username == "linkeduser"

    def test_login_view_get(self):
        url = reverse("login")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_login_view_post_success(self):
        url = reverse("login")
        response = self.client.post(url, {"username": "testuser", "password": "testpass"}, follow=True)
        assert response.status_code == 200

    def test_login_view_post_fail(self):
        url = reverse("login")
        response = self.client.post(url, {"username": "testuser", "password": "wrongpass"})
        assert b"Invalid credentials" in response.content

    def test_logout_view(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("logout")
        response = self.client.post(url, follow=True)
        assert response.status_code == 200

    def test_user_view_get(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("user", args=[self.user.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert b"User Profile" in response.content

    def test_user_view_patch(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("user", args=[self.user.id])
        response = self.client.patch(url, data='{"email": "newmail@example.com"}', content_type="application/json")
        assert response.status_code == 200
        self.user.refresh_from_db()
        assert self.user.email == "newmail@example.com"

    def test_user_view_forbidden(self):
        other = User.objects.create_user(username="otheruser", password="otherpass")
        self.client.login(username="otheruser", password="otherpass")
        url = reverse("user", args=[self.user.id])
        response = self.client.get(url)
        assert response.status_code == 403

    def test_match_view_get(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("match")
        response = self.client.get(url)
        assert response.status_code == 200
        assert b"Matches" in response.content

    def test_match_view_post(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("match")
        data = {
            "team1_player1": "testuser",
            "team1_player2": "other",
            "team2_player1": "other",
            "team2_player2": "testuser",
            "winning_team": "1",
            "date_played": date.today().isoformat(),
        }
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_match_view_post_duplicate(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("match")
        # Create two more players for a valid match
        player3 = Player.objects.create(name="player3", wins=0, ranking_position=3)
        player4 = Player.objects.create(name="player4", wins=0, ranking_position=4)
        data = {
            "team1_player1": "testuser",
            "team1_player2": "other",
            "team2_player1": "player3",
            "team2_player2": "player4",
            "winning_team": "1",
            "date_played": date.today().isoformat(),
        }
        # First post should succeed
        self.client.post(url, data, follow=True)
        # Second post should fail due to duplicate
        response = self.client.post(url, data, follow=True)
        messages = list(response.context["messages"])
        assert any("already exists" in str(m) for m in messages)

    def test_match_view_no_player(self):
        user = User.objects.create_user(username="noplayer", password="nopass")
        self.client.login(username="noplayer", password="nopass")
        url = reverse("match")
        response = self.client.get(url, follow=True)
        messages = list(response.context["messages"])
        assert any("not associated with any player" in str(m) for m in messages)

    def test_get_player_stats_no_player(self):
        # Covers lines 21-51
        url = reverse("hall_of_fame")
        self.client.login(username="testuser", password="testpass")
        # Call get_player_stats directly
        
        stats = views.get_player_stats(self.client.request().wsgi_request, player_id=9999)
        assert stats["wins"] == 0

    def test_get_new_match_ids_not_authenticated(self):
        # Covers line 59
        
        request = self.client.request().wsgi_request
        request.user = type("Anon", (), {"is_authenticated": False})()
        assert views.get_new_match_ids(request) == []

    def test_get_new_match_ids_no_player(self):
        # Covers lines 87-88
        
        self.client.login(username="testuser", password="testpass")
        request = self.client.request().wsgi_request
        request.user = User.objects.create_user(username="no_player", password="pass")
        assert views.get_new_match_ids(request) == []

    def test_fetch_paginated_data_invalid_page(self):
        # Covers lines 123-124
        
        qs = Player.objects.all()
        class DummyRequest:
            GET = {"page": "notanint"}
        items, pagination = views.fetch_paginated_data(qs, DummyRequest())
        assert pagination["current_page"] == 1

    def test_fetch_available_players(self):
        # Covers lines 167, 169
        
        registered, non_registered = views.fetch_available_players()
        assert isinstance(registered, list)
        assert isinstance(non_registered, list)

    def test_process_form_data_post_missing_fields(self):
        # Covers lines 181-182
        
        class DummyRequest:
            method = "POST"
            POST = {}
        data, error = views.process_form_data(DummyRequest())
        assert error is not None

    def test_process_form_data_post_password_mismatch(self):
        # Covers lines 196-197
        
        class DummyRequest:
            method = "POST"
            POST = {"username": "a", "email": "b", "password": "1", "confirm_password": "2", "player_id": ""}
        data, error = views.process_form_data(DummyRequest())
        assert "Passwords do not match" in error

    def test_process_form_data_patch_invalid_json(self):
        # Covers lines 201-202
        
        class DummyRequest:
            method = "PATCH"
            body = b"{invalid"
        data, error = views.process_form_data(DummyRequest())
        assert "Invalid JSON" in error

    def test_register_view_post_existing_username(self):
        # Covers lines 218-220
        url = reverse("register")
        User.objects.create_user(username="dupe", password="pass", email="dupe@example.com")
        data = {
            "username": "dupe",
            "email": "dupe@example.com",
            "password": "pass",
            "confirm_password": "pass",
            "player_id": "",
        }
        response = self.client.post(url, data, follow=True)
        messages = list(response.context["messages"])
        assert any("already taken" in str(m) for m in messages)

    def test_register_view_post_linked_player(self):
        # Covers lines 246-247
        url = reverse("register")
        linked_user = User.objects.create_user(username="linked", password="pass", email="linked@example.com")
        linked_player = Player.objects.create(name="linked", registered_user=linked_user, wins=0, ranking_position=3)
        data = {
            "username": "newuser2",
            "email": "new2@example.com",
            "password": "pass",
            "confirm_password": "pass",
            "player_id": str(linked_player.id),
        }
        response = self.client.post(url, data, follow=True)
        messages = list(response.context["messages"])
        assert any("already linked" in str(m) for m in messages)

    def test_user_view_patch_invalid_json(self):
        # Covers line 251
        self.client.login(username="testuser", password="testpass")
        url = reverse("user", args=[self.user.id])
        response = self.client.patch(url, data="{invalid", content_type="application/json")
        assert response.status_code == 400

    def test_user_view_patch_no_valid_fields(self):
        # Covers line 264
        self.client.login(username="testuser", password="testpass")
        url = reverse("user", args=[self.user.id])
        response = self.client.patch(url, data=json.dumps({}), content_type="application/json")
        assert response.status_code == 400

    def test_process_matches_handles_none(self):
        # Covers lines 288, 290
        
        dummy_match = type("Dummy", (), {"team1_player1": None, "team1_player2": None, "team2_player1": None, "team2_player2": None, "date_played": date.today()})()
        result = views.process_matches([dummy_match], "nobody", "<icon>")
        assert result

    def test_match_view_post_invalid_date(self):
        # Covers lines 362-364
        self.client.login(username="testuser", password="testpass")
        url = reverse("match")
        data = {
            "team1_player1": "testuser",
            "team1_player2": "other",
            "team2_player1": "player3",
            "team2_player2": "player4",
            "winning_team": "1",
            "date_played": "not-a-date",
        }
        response = self.client.post(url, data, follow=True)
        messages = list(response.context["messages"])
        assert any("Invalid date format" in str(m) for m in messages)

    def test_match_view_post_future_date(self):
        # Covers lines 367-368
        self.client.login(username="testuser", password="testpass")
        url = reverse("match")
        future = (date.today() + timedelta(days=10)).isoformat()
        data = {
            "team1_player1": "testuser",
            "team1_player2": "other",
            "team2_player1": "player3",
            "team2_player2": "player4",
            "winning_team": "1",
            "date_played": future,
        }
        response = self.client.post(url, data, follow=True)
        messages = list(response.context["messages"])
        assert any("Date cannot be in the future" in str(m) for m in messages)

    def test_match_view_post_missing_winning_team(self):
        # Covers lines 384-385
        self.client.login(username="testuser", password="testpass")
        url = reverse("match")
        data = {
            "team1_player1": "testuser",
            "team1_player2": "other",
            "team2_player1": "player3",
            "team2_player2": "player4",
            "date_played": date.today().isoformat(),
        }
        response = self.client.post(url, data, follow=True)
        messages = list(response.context["messages"])
        assert any("Please select the winning team" in str(m) for m in messages)

    def test_match_view_delete_unauthorized(self):
        # Covers lines 400-412
        self.client.login(username="testuser", password="testpass")
        url = reverse("match")
        # Try to delete a match as a non-participant/non-admin
        match = Match.objects.create(
            team1_player1=self.other_player,
            team1_player2=self.other_player,
            team2_player1=self.other_player,
            team2_player2=self.other_player,
            winning_team=1,
            date_played=date.today()
        )
        response = self.client.delete(url, data=json.dumps({"match_id": match.id}), content_type="application/json")
        assert response.status_code == 403

    def test_match_view_delete_success(self):
        # Covers lines 453
        self.client.login(username="testuser", password="testpass")
        url = reverse("match")
        # Make testuser a participant
        match = Match.objects.create(
            team1_player1=self.player,
            team1_player2=self.other_player,
            team2_player1=self.other_player,
            team2_player2=self.other_player,
            winning_team=1,
            date_played=date.today()
        )
        response = self.client.delete(url, data=json.dumps({"match_id": match.id}), content_type="application/json")
        assert response.status_code == 200