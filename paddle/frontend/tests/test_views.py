import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from games.models import Player, Match
from datetime import date, timedelta,datetime
from django.test import Client
import json
from frontend import views

User = get_user_model()

@pytest.mark.django_db
class TestFrontendViews:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass", email="test@example.com")
        self.player = Player.objects.create(name="testuser", registered_user=self.user, ranking_position=1)
        self.other_player = Player.objects.create(name="other", ranking_position=2)
        # Create matches to reflect wins
        self.match = Match.objects.create(
            team1_player1=self.player,
            team1_player2=self.other_player,
            team2_player1=self.other_player,
            team2_player2=self.player,
            winning_team=1,
            date_played=date.today()
        )
        # If you want to simulate more wins, create more matches where self.player is on the winning team

    def test_hall_of_fame_view(self):
        url = reverse("hall_of_fame")
        response = self.client.get(url)
        assert response.status_code == 200
        

    def test_register_view_get(self):
        url = reverse("register")
        response = self.client.get(url)
        assert response.status_code == 200
        assert b"nuevo jugador" in response.content

    def test_register_view_post_new_player(self):
        url = reverse("register")
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass",
            "confirm_password": "newpass",
            "player_id": "",
            "gender": "F",
        }
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200
        assert User.objects.filter(username="newuser").exists()

    def test_register_view_post_existing_player(self):
        url = reverse("register")
        player = Player.objects.create(name="unlinked", ranking_position=3)
        data = {
            "username": "linkeduser",
            "email": "linked@example.com",
            "password": "linkedpass",
            "confirm_password": "linkedpass",
            "player_id": str(player.id),
            "gender": "F",
        }
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200
        assert User.objects.filter(username="linkeduser").exists()
        player.refresh_from_db()
        assert player.registered_user.username == "linkeduser"


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

    def test_match_view_post_duplicate_match(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("match")
        p2 = Player.objects.create(name="player2", ranking_position=2)
        p3 = Player.objects.create(name="player3", ranking_position=3)
        p4 = Player.objects.create(name="player4", ranking_position=4)

        match_data = {
            "team1_player2_choice": str(p2.id),
            "team2_player1_choice": str(p3.id),
            "team2_player2_choice": str(p4.id),
            "winning_team": 1,
            "date_played": date.today().isoformat(),
        }

        # First post should succeed
        response = self.client.post(url, match_data, follow=True)
        assert response.status_code == 200

        # Second post should fail due to duplicate
        response = self.client.post(url, match_data, follow=True)        
        messages = list(response.context["messages"])
        assert any("error" in str(m).lower() for m in messages)

    def test_match_view_no_player(self):
        user = User.objects.create_user(username="noplayer", password="nopass")
        self.client.login(username="noplayer", password="nopass")
        url = reverse("match")
        response = self.client.get(url, follow=True)
        messages = list(response.context["messages"])
        assert any("no está asociado a ningún jugador" in str(m).lower() for m in messages)

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
            POST = {"username": "a", "email": "b", "password": "1", "confirm_password": "2", "player_id": "", "gender": "M"}
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
            "gender": "M",
        }
        response = self.client.post(url, data, follow=True)
        messages = list(response.context["messages"])
        # check error response
        assert response.status_code == 200
        assert any("error" in str(m).lower() for m in messages)

    def test_register_view_post_linked_player(self):
        # Covers lines 246-247
        url = reverse("register")
        linked_user = User.objects.create_user(username="linked", password="pass", email="linked@example.com")
        linked_player = Player.objects.create(name="linked", registered_user=linked_user, ranking_position=3)
        data = {
            "username": "newuser2",
            "email": "new2@example.com",
            "password": "pass",
            "confirm_password": "pass",
            "player_id": str(linked_player.id),
            "gender": "M",
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
        p2 = Player.objects.create(name="player2", ranking_position=2)
        p3 = Player.objects.create(name="player3", ranking_position=3)
        p4 = Player.objects.create(name="player4", ranking_position=4)
        data = {
            "team1_player2_choice": str(p2.id),
            "team2_player1_choice": str(p3.id),
            "team2_player2_choice": str(p4.id),
            "winning_team": "1",
            "date_played": "not-a-date",
        }
        response = self.client.post(url, data, follow=True)
        messages = list(response.context["messages"])
        assert any(m.tags == "error" for m in messages)

    def test_match_view_post_future_date(self):
        # Covers lines 367-368
        self.client.login(username="testuser", password="testpass")
        url = reverse("match")
        p2 = Player.objects.create(name="player2", ranking_position=2)
        p3 = Player.objects.create(name="player3", ranking_position=3)
        p4 = Player.objects.create(name="player4", ranking_position=4)
        future = (date.today() + timedelta(days=10)).isoformat()
        data = {
            "team1_player2_choice": str(p2.id),
            "team2_player1_choice": str(p3.id),
            "team2_player2_choice": str(p4.id),
            "winning_team": "1",
            "date_played": future,
        }
        response = self.client.post(url, data, follow=True)
        messages = list(response.context["messages"])
        assert any(m.tags == "error" for m in messages)

    def test_match_view_post_missing_winning_team(self):
        # Covers lines 384-385
        self.client.login(username="testuser", password="testpass")
        url = reverse("match")
        p2 = Player.objects.create(name="player2", ranking_position=2)
        p3 = Player.objects.create(name="player3", ranking_position=3)
        p4 = Player.objects.create(name="player4", ranking_position=4)
        data = {
            "team1_player2_choice": str(p2.id),
            "team2_player1_choice": str(p3.id),
            "team2_player2_choice": str(p4.id),
            "date_played": date.today().isoformat(),
        }
        response = self.client.post(url, data, follow=True)
        messages = list(response.context["messages"])
        # check error response        
        assert any("error" in str(m).lower() for m in messages)

    def test_match_view_delete_unauthorized(self):        
        self.client.login(username="testuser", password="testpass")
        url = reverse("match")
        # Try to delete a match as a non-participant/non-admin        
        p1 = Player.objects.create(name="p_del_1")
        p2 = Player.objects.create(name="p_del_2")
        p3 = Player.objects.create(name="p_del_3")
        p4 = Player.objects.create(name="p_del_4")
        match = Match.objects.create(
            team1_player1=p1,
            team1_player2=p2,
            team2_player1=p3,
            team2_player2=p4,
            winning_team=1,
            date_played=date.today()
        )        
        response = self.client.post(url, data={"action": "delete", "match_id": match.id}, follow=True)
        # Must still exist because user is not participant nor staff
        assert Match.objects.filter(id=match.id).exists()
        messages_list = list(response.context["messages"])
        assert any("No estás autorizado para borrar este partido." in str(m) for m in messages_list)

    def test_match_view_delete_success(self):
        # Covers lines 453
        self.client.login(username="testuser", password="testpass")
        url = reverse("match")    
        # Ensure 4 distinct players and make testuser a participant
        p2 = Player.objects.create(name="p_ok_2")
        p3 = Player.objects.create(name="p_ok_3")
        p4 = Player.objects.create(name="p_ok_4")
        match = Match.objects.create(
            team1_player1=self.player,
            team1_player2=p2,
            team2_player1=p3,
            team2_player2=p4,
            winning_team=1,
            date_played=date.today()
        )
        response = self.client.post(url, data={"action": "delete", "match_id": match.id}, follow=True)

        assert not Match.objects.filter(id=match.id).exists()
        msgs = list(response.context["messages"])
        assert any("Partido borrado correctamente" in str(m) for m in msgs)
    
    def test_match_view_delete_exception(self):
        # Simulate exception in DELETE 
        user = User.objects.create_user(username="admin", password="pass", is_staff=True)
        Player.objects.create(name="admin", registered_user=user, ranking_position=1)
        self.client.login(username="admin", password="pass")
        url = reverse("match")
        resp = self.client.post(url, data={"action": "delete", "match_id": 999999}, follow=True)
        assert any("Error: el partido no existe." in str(m) for m in list(resp.context["messages"]))
        
    def test_about_view_context(self):
        url = reverse("about")
        resp = self.client.get(url)
        assert resp.status_code == 200
        # context should include counts
        ctx = resp.context
        assert "num_users" in ctx
        assert "num_players" in ctx
        assert "num_matches" in ctx