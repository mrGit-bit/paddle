import pytest
from django.contrib.auth import get_user_model
from datetime import date, timedelta

from django.db import connection
from django.test import Client
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from frontend import views
from games.models import Group, Match, Player

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

    def test_hall_of_fame_view_renders_ranking_sort_controls(self):
        url = reverse("hall_of_fame")
        response = self.client.get(url)
        content = response.content.decode("utf-8")

        assert response.status_code == 200
        assert 'data-ranking-sort-table' in content
        assert 'data-sort-key="position"' in content
        assert 'data-sort-key="wins"' in content
        assert 'data-sort-key="matches"' in content
        assert 'data-sort-key="win-rate"' in content
        assert 'frontend/js/rankingTableSort.js' in content
        assert 'data-canonical-show-position=' in content

    def test_hall_of_fame_view_renders_pairs_nav_link(self):
        response = self.client.get(reverse("hall_of_fame"))
        content = response.content.decode("utf-8")

        assert response.status_code == 200
        assert f'href="{reverse("ranking_pairs")}"' in content
        assert ">Parejas<" in content

    def test_hall_of_fame_view_renders_create_group_cta_for_anonymous_users(self):
        response = self.client.get(reverse("hall_of_fame"))
        content = response.content.decode("utf-8")

        assert response.status_code == 200
        assert f'href="{reverse("register")}?create_group=1"' in content
        assert "crea un grupo" in content

    def test_pairs_ranking_view_renders_requested_sections_and_two_line_pair_cell(self):
        pair_a = Player.objects.create(name="Pareja A", gender=Player.GENDER_MALE)
        pair_b = Player.objects.create(name="Pareja B", gender=Player.GENDER_MALE)
        rival_1 = Player.objects.create(name="Rival 1", gender=Player.GENDER_MALE)
        rival_2 = Player.objects.create(name="Rival 2", gender=Player.GENDER_MALE)

        for offset in range(4):
            Match.objects.create(
                team1_player1=pair_a,
                team1_player2=pair_b,
                team2_player1=rival_1,
                team2_player2=rival_2,
                winning_team=1,
                date_played=date.today() - timedelta(days=offset),
            )

        response = self.client.get(reverse("ranking_pairs"))
        content = response.content.decode("utf-8")

        assert response.status_code == 200
        assert "Ranking de parejas" in content
        assert "Parejas del siglo" in content
        assert "Parejas catastróficas" in content
        assert '<div>Pareja A</div>' in content
        assert '<div>Pareja B</div>' in content
        assert 'data-href=' not in content

    def test_pairs_ranking_view_hides_repeated_tie_positions(self):
        pair_a = Player.objects.create(name="Pareja A", gender=Player.GENDER_MALE)
        pair_b = Player.objects.create(name="Pareja B", gender=Player.GENDER_MALE)
        pair_c = Player.objects.create(name="Pareja C", gender=Player.GENDER_MALE)
        pair_d = Player.objects.create(name="Pareja D", gender=Player.GENDER_MALE)
        rival_1 = Player.objects.create(name="Rival 1", gender=Player.GENDER_MALE)
        rival_2 = Player.objects.create(name="Rival 2", gender=Player.GENDER_MALE)

        Match.objects.create(
            team1_player1=pair_a,
            team1_player2=pair_b,
            team2_player1=rival_1,
            team2_player2=rival_2,
            winning_team=1,
            date_played=date.today(),
        )
        Match.objects.create(
            team1_player1=pair_c,
            team1_player2=pair_d,
            team2_player1=rival_1,
            team2_player2=rival_2,
            winning_team=1,
            date_played=date.today() - timedelta(days=1),
        )

        response = self.client.get(reverse("ranking_pairs"))
        content = response.content.decode("utf-8")

        assert response.status_code == 200
        assert content.count('class="rank-1">🥇</strong>') == 1
        assert '&nbsp;' in content

    def test_deprecated_api_routes_are_not_available(self):
        for path in ("/api/games/", "/api/users/", "/api-auth/"):
            response = self.client.get(path)
            assert response.status_code == 404

    def test_register_view_get(self):
        url = reverse("register")
        response = self.client.get(url)
        assert response.status_code == 200
        assert b"nuevo jugador" in response.content

    def test_register_view_get_create_group_query_preselects_create_mode(self):
        url = reverse("register")
        response = self.client.get(f"{url}?create_group=1")

        assert response.status_code == 200
        assert response.context["form"].initial["group_mode"] == "create"

    def test_register_view_post_new_player(self):
        url = reverse("register")
        group = Group.objects.create(name="Grupo Registro")
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "confirm_email": "new@example.com",
            "password": "newpass12",
            "confirm_password": "newpass12",
            "group_choice": str(group.id),
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
            "confirm_email": "linked@example.com",
            "password": "linkedpass",
            "confirm_password": "linkedpass",
            "group_choice": str(player.group_id),
            "player_id": str(player.id),
            "gender": "F",
        }
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200
        assert User.objects.filter(username="linkeduser").exists()
        player.refresh_from_db()
        assert player.registered_user.username == "linkeduser"

    def test_register_view_requires_explicit_group_choice(self):
        url = reverse("register")
        response = self.client.post(
            url,
            {
                "username": "nogroup",
                "email": "nogroup@example.com",
                "confirm_email": "nogroup@example.com",
                "password": "pass12345",
                "confirm_password": "pass12345",
                "player_id": "",
                "gender": "F",
            },
        )

        assert response.status_code == 200
        assert "Selecciona un grupo/club o crea uno nuevo." in response.content.decode()
        assert not User.objects.filter(username="nogroup").exists()

    def test_register_view_rejects_invalid_email_format(self):
        url = reverse("register")
        group = Group.objects.create(name="Grupo Email")
        response = self.client.post(
            url,
            {
                "username": "badmailuser",
                "email": "texto-plano",
                "confirm_email": "texto-plano",
                "password": "pass12345",
                "confirm_password": "pass12345",
                "group_choice": str(group.id),
                "player_id": "",
                "gender": "F",
            },
        )

        assert response.status_code == 200
        assert "Introduce un correo electrónico válido." in response.content.decode()
        assert not User.objects.filter(username="badmailuser").exists()


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
        assert b"Cuenta de usuario" in response.content
        assert b'id="profile-confirm-email-container"' in response.content
        assert b'profile-confirm-email-container" class="mb-3 form-floating d-none"' in response.content

    def test_user_view_post_updates_username_and_email(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("user", args=[self.user.id])
        response = self.client.post(
            url,
            data={
                "username": "nuevo_usuario",
                "email": "newmail@example.com",
                "confirm_email": "newmail@example.com",
            },
            follow=True,
        )
        assert response.status_code == 200
        self.user.refresh_from_db()
        self.player.refresh_from_db()
        assert self.user.username == "nuevo_usuario"
        assert self.user.email == "newmail@example.com"
        assert self.player.name == "nuevo_usuario"

    def test_user_view_forbidden(self):
        other = User.objects.create_user(username="otheruser", password="otherpass")
        self.client.login(username="otheruser", password="otherpass")
        url = reverse("user", args=[self.user.id])
        response = self.client.get(url)
        assert response.status_code == 403

    def test_user_view_post_rejects_mismatched_changed_email(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("user", args=[self.user.id])
        response = self.client.post(
            url,
            data={
                "username": "testuser",
                "email": "nuevo@example.com",
                "confirm_email": "distinto@example.com",
            },
        )
        assert response.status_code == 200
        self.user.refresh_from_db()
        assert self.user.email == "test@example.com"
        assert b"Los correos electr" in response.content

    def test_user_view_post_allows_username_change_without_email_confirmation(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("user", args=[self.user.id])
        response = self.client.post(
            url,
            data={
                "username": "solo_nombre",
                "email": "test@example.com",
                "confirm_email": "",
            },
            follow=True,
        )
        assert response.status_code == 200
        self.user.refresh_from_db()
        assert self.user.username == "solo_nombre"

    def test_user_delete_view_unlinks_player_and_logs_out(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("user_delete", args=[self.user.id])
        response = self.client.post(url, follow=True)
        assert response.status_code == 200
        assert not User.objects.filter(id=self.user.id).exists()
        self.player.refresh_from_db()
        assert self.player.registered_user is None
        assert "_auth_user_id" not in self.client.session
        assert b"Tu cuenta se ha eliminado correctamente" in response.content

    def test_user_delete_view_forbidden_for_other_user(self):
        other = User.objects.create_user(username="otheruser", password="otherpass")
        self.client.login(username="otheruser", password="otherpass")
        url = reverse("user_delete", args=[self.user.id])
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

    def test_match_view_post_rejects_date_older_than_30_days(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("match")
        p2 = Player.objects.create(name="stale_p2", ranking_position=2)
        p3 = Player.objects.create(name="stale_p3", ranking_position=3)
        p4 = Player.objects.create(name="stale_p4", ranking_position=4)

        response = self.client.post(
            url,
            {
                "team1_player2_choice": str(p2.id),
                "team2_player1_choice": str(p3.id),
                "team2_player2_choice": str(p4.id),
                "winning_team": "1",
                "date_played": (date.today() - timedelta(days=31)).isoformat(),
            },
            follow=True,
        )

        messages = list(response.context["messages"])
        assert any("últimos 30 días" in str(m) for m in messages)
        assert not Match.objects.filter(
            team1_player1=self.player,
            team1_player2=p2,
            team2_player1=p3,
            team2_player2=p4,
        ).exists()

    def test_match_view_post_allows_date_exactly_30_days_old(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("match")
        p2 = Player.objects.create(name="border_p2", ranking_position=2)
        p3 = Player.objects.create(name="border_p3", ranking_position=3)
        p4 = Player.objects.create(name="border_p4", ranking_position=4)

        response = self.client.post(
            url,
            {
                "team1_player2_choice": str(p2.id),
                "team2_player1_choice": str(p3.id),
                "team2_player2_choice": str(p4.id),
                "winning_team": "1",
                "date_played": (date.today() - timedelta(days=30)).isoformat(),
            },
            follow=True,
        )

        messages = list(response.context["messages"])
        assert any("Partido creado correctamente" in str(m) for m in messages)
        assert Match.objects.filter(
            team1_player1=self.player,
            team1_player2=p2,
            team2_player1=p3,
            team2_player2=p4,
            date_played=date.today() - timedelta(days=30),
        ).exists()

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

    def test_register_view_post_existing_username(self):
        # Covers lines 218-220
        url = reverse("register")
        User.objects.create_user(username="dupe", password="pass", email="dupe@example.com")
        data = {
            "username": "dupe",
            "email": "fresh@example.com",
            "confirm_email": "fresh@example.com",
            "password": "pass1234",
            "confirm_password": "pass1234",
            "player_id": "",
            "gender": "M",
        }
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200
        assert b"Ya existe un usuario o un jugador con ese nombre" in response.content
        assert b'<div class="invalid-feedback d-block">Ya existe un usuario o un jugador con ese nombre.' in response.content
        assert b'<div class="invalid-feedback d-block">Los correos electr' not in response.content

    def test_register_view_post_linked_player(self):
        # Covers lines 246-247
        url = reverse("register")
        linked_user = User.objects.create_user(username="linked", password="pass", email="linked@example.com")
        linked_player = Player.objects.create(name="linked", registered_user=linked_user, ranking_position=3)
        data = {
            "username": "newuser2",
            "email": "new2@example.com",
            "confirm_email": "new2@example.com",
            "password": "pass1234",
            "confirm_password": "pass1234",
            "player_id": str(linked_player.id),
            "gender": "M",
        }
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200
        assert not User.objects.filter(username="newuser2").exists()
        assert b"El jugador seleccionado ya no est" in response.content

    def test_register_view_allows_linking_existing_unregistered_player_with_same_name(self):
        url = reverse("register")
        player = Player.objects.create(name="sameplayer", ranking_position=3, gender=Player.GENDER_MALE)
        data = {
            "username": "sameplayer",
            "email": "sameplayer@example.com",
            "confirm_email": "sameplayer@example.com",
            "password": "pass1234",
            "confirm_password": "pass1234",
            "group_choice": str(player.group_id),
            "player_id": str(player.id),
            "gender": "M",
        }

        response = self.client.post(url, data, follow=True)

        assert response.status_code == 200
        assert User.objects.filter(username="sameplayer").exists()
        player.refresh_from_db()
        assert player.registered_user is not None
        assert player.registered_user.username == "sameplayer"
        assert b"Ya existe un usuario o un jugador con ese nombre" not in response.content
        assert b'<div class="invalid-feedback d-block">Los correos electr' not in response.content

    def test_register_view_rejects_duplicate_player_name_from_other_group(self):
        url = reverse("register")
        first_group = Group.objects.create(name="Grupo Uno")
        second_group = Group.objects.create(name="Grupo Dos")
        Player.objects.create(
            name="globaldupe",
            ranking_position=3,
            gender=Player.GENDER_MALE,
            group=first_group,
        )

        response = self.client.post(
            url,
            data={
                "username": "globaldupe",
                "email": "globaldupe@example.com",
                "confirm_email": "globaldupe@example.com",
                "password": "pass1234",
                "confirm_password": "pass1234",
                "group_choice": str(second_group.id),
                "player_id": "",
                "gender": "M",
            },
            follow=True,
        )

        assert response.status_code == 200
        assert not User.objects.filter(username="globaldupe").exists()
        assert b"Ya existe un usuario o un jugador con ese nombre" in response.content

    def test_register_view_post_mismatched_emails(self):
        url = reverse("register")
        response = self.client.post(
            url,
            data={
                "username": "newuser3",
                "email": "one@example.com",
                "confirm_email": "two@example.com",
                "password": "12345678",
                "confirm_password": "12345678",
                "gender": "M",
            },
        )
        assert response.status_code == 200
        assert not User.objects.filter(username="newuser3").exists()
        assert b"Los correos electr" in response.content

    def test_register_view_post_duplicate_email_case_insensitive(self):
        url = reverse("register")
        User.objects.create_user(
            username="emailowner",
            password="pass1234",
            email="EmailOwner@Example.com",
        )
        response = self.client.post(
            url,
            data={
                "username": "newuser4",
                "email": "emailowner@example.com",
                "confirm_email": "emailowner@example.com",
                "password": "12345678",
                "confirm_password": "12345678",
                "gender": "M",
            },
        )
        assert response.status_code == 200
        assert b"Ya existe una cuenta con ese correo electr" in response.content
        assert not User.objects.filter(username="newuser4").exists()

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

    def test_match_view_delete_rejects_locked_match_for_participant(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("match")
        p2 = Player.objects.create(name="p_locked_2")
        p3 = Player.objects.create(name="p_locked_3")
        p4 = Player.objects.create(name="p_locked_4")
        match = Match.objects.create(
            team1_player1=self.player,
            team1_player2=p2,
            team2_player1=p3,
            team2_player2=p4,
            winning_team=1,
            date_played=date.today() - timedelta(days=31),
        )

        response = self.client.post(url, data={"action": "delete", "match_id": match.id}, follow=True)

        assert Match.objects.filter(id=match.id).exists()
        messages_list = list(response.context["messages"])
        assert any("aprobado automáticamente" in str(m) for m in messages_list)
    
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

    def test_register_view_get_query_count(self):
        Player.objects.create(name="free_a", ranking_position=4)
        Player.objects.create(name="free_b", ranking_position=5)
        url = reverse("register")

        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get(url)

        assert response.status_code == 200
        assert len(ctx) <= 4

    def test_user_view_get_query_count(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("user", args=[self.user.id])

        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get(url)

        assert response.status_code == 200
        assert len(ctx) <= 10

    def test_match_view_get_query_count(self):
        self.client.login(username="testuser", password="testpass")
        for idx in range(5):
            p2 = Player.objects.create(name=f"query_p2_{idx}", ranking_position=10 + idx)
            p3 = Player.objects.create(name=f"query_p3_{idx}", ranking_position=20 + idx)
            p4 = Player.objects.create(name=f"query_p4_{idx}", ranking_position=30 + idx)
            Match.objects.create(
                team1_player1=self.player,
                team1_player2=p2,
                team2_player1=p3,
                team2_player2=p4,
                winning_team=1,
                date_played=date.today() - timedelta(days=idx + 1),
            )

        url = reverse("match")
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get(url)

        assert response.status_code == 200
        assert len(ctx) <= 17
