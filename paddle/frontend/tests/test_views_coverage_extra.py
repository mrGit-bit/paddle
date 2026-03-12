import json
import pytest
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.urls import reverse

from games.models import Player, Match
from frontend.views import get_player_stats, process_matches
from frontend.view_modules.common import build_player_participation_queryset

from django.test import Client

client = Client()

User = get_user_model()


pytestmark = pytest.mark.django_db


def mk_user_with_player(username="testuser", gender="M"):
    user = User.objects.create_user(username=username, password="pass")
    player = Player.objects.create(name=username, registered_user=user, gender=gender)
    return user, player


def mk_match(p1, p2, p3, p4, winning_team=1, d=None):
    return Match.objects.create(
        team1_player1=p1, team1_player2=p2,
        team2_player1=p3, team2_player2=p4,
        winning_team=winning_team,
        date_played=d or date.today(),
    )


def test_build_player_participation_queryset_includes_all_slots_without_duplicates():
    p = Player.objects.create(name="Q_MAIN", gender=Player.GENDER_MALE)
    a = Player.objects.create(name="Q_A", gender=Player.GENDER_MALE)
    b = Player.objects.create(name="Q_B", gender=Player.GENDER_MALE)
    c = Player.objects.create(name="Q_C", gender=Player.GENDER_MALE)
    d = Player.objects.create(name="Q_D", gender=Player.GENDER_MALE)
    e = Player.objects.create(name="Q_E", gender=Player.GENDER_MALE)
    f = Player.objects.create(name="Q_F", gender=Player.GENDER_MALE)

    m1 = mk_match(p, a, b, c, winning_team=1, d=date(2026, 3, 1))  # team1_player1
    m2 = mk_match(a, p, b, c, winning_team=1, d=date(2026, 3, 2))  # team1_player2
    m3 = mk_match(a, b, p, c, winning_team=1, d=date(2026, 3, 3))  # team2_player1
    m4 = mk_match(a, b, c, p, winning_team=1, d=date(2026, 3, 4))  # team2_player2
    mk_match(d, e, f, a, winning_team=1, d=date(2026, 3, 5))  # unrelated

    qs = build_player_participation_queryset(p)
    ids = set(qs.values_list("id", flat=True))

    assert ids == {m1.id, m2.id, m3.id, m4.id}


def test_get_player_stats_authenticated_with_linked_player_covers_line_39():
    # Covers line 39 (Player.objects.get(registered_user=request.user) success path)
    rf = RequestFactory()
    user, player = mk_user_with_player("u_stats", "M")
    request = rf.get("/")
    request.user = user

    stats = get_player_stats(request)

    assert stats["player_id"] == player.id


def test_ranking_view_sets_previous_following_when_user_is_off_page():
    # Covers lines 193-194 in ranking_view (previous_player/following_player set)
    # We need >12 ranked players so user is on page 2 while we request page 1.
    user, user_player = mk_user_with_player("u_rank", "M")

    # Create 13 additional male players and give each at least 1 match
    others = [Player.objects.create(name=f"P{i}", gender="M") for i in range(1, 14)]
    filler1 = Player.objects.create(name="FILL1", gender="M")
    filler2 = Player.objects.create(name="FILL2", gender="M")

    # Make sure everyone (including user) appears in ranking at least once:
    # Create matches pairing each other with fillers
    base = date.today() - timedelta(days=30)
    for idx, p in enumerate(others, start=1):
        mk_match(p, filler1, filler2, user_player, winning_team=1, d=base + timedelta(days=idx))

    # Give user one win so they are not last (ensures following_player exists)
    mk_match(user_player, filler1, filler2, others[0], winning_team=1, d=base + timedelta(days=100))

    client.login(username="u_rank", password="pass")

    url = reverse("ranking_male")  # any scope is fine; male is stable here
    resp = client.get(url + "?page=1")
    assert resp.status_code == 200

    # user_page should be 2 (off current page 1), and prev/follow should exist
    assert resp.context["user_page"] == 2
    assert resp.context["previous_player"] is not None
    assert resp.context["following_player"] is not None


def test_register_view_form_error_branch_covers_277_278():
    # Covers invalid registration form re-rendering on missing fields.

    url = reverse("register")

    resp = client.post(url, data={"username": "x"}, follow=False)
    assert resp.status_code == 200
    assert "Este campo es obligatorio" in resp.content.decode("utf-8")


def test_register_view_invalid_gender_branch_covers_293_294():
    # Covers invalid registration gender choice re-rendering.
    
    url = reverse("register")

    data = {
        "username": "newuser",
        "email": "new@ex.com",
        "confirm_email": "new@ex.com",
        "password": "12345678",
        "confirm_password": "12345678",
        "gender": "X",  # invalid
    }
    resp = client.post(url, data=data, follow=False)
    assert resp.status_code == 200
    assert "Por favor, selecciona un género válido." in resp.content.decode("utf-8")


def test_user_view_post_requires_confirmation_for_changed_email():
    user = User.objects.create_user(username="u_patch", password="pass")

    client.login(username="u_patch", password="pass")

    url = reverse("user", kwargs={"id": user.id})
    resp = client.post(
        url,
        data={
            "username": "u_patch",
            "email": "x@x.com",
            "confirm_email": "",
        },
    )

    assert resp.status_code == 200
    assert "Confirma tu correo electrónico si quieres cambiarlo." in resp.content.decode("utf-8")


def test_process_matches_converts_string_date_covers_383():
    # Covers line 383: convert date_played from string to date
    u, p = mk_user_with_player("u_match", "M")
    p2 = Player.objects.create(name="p2x", gender="M")
    p3 = Player.objects.create(name="p3x", gender="M")
    p4 = Player.objects.create(name="p4x", gender="M")
    m = mk_match(p, p2, p3, p4)

    # Force string date (simulates non-ORM serialization cases)
    m.date_played = "2026-01-01"

    out = process_matches([m], current_user="nope", user_icon="*")
    assert str(out[0].date_played) == "2026-01-01"


def test_match_view_delete_missing_match_id_covers_405_406():
    # Covers 405-406: delete action with missing match_id
    user, player = mk_user_with_player("u_del", "M")
    
    client.login(username="u_del", password="pass")
    url = reverse("match")

    resp = client.post(url, data={"action": "delete"}, follow=True)
    msgs = list(resp.context["messages"])
    assert any("falta el identificador" in str(m) for m in msgs)


def test_match_view_resolve_player_new_missing_name_covers_448_449():
    # Covers 448-449: NEW_* chosen but missing name
    user, player = mk_user_with_player("u_newmiss", "M")
    
    client.login(username="u_newmiss", password="pass")
    url = reverse("match")

    data = {
        "team1_player2_choice": "NEW_M",
        "team1_player2_new_name": "",  # missing
        "team2_player1_choice": "NEW_M",
        "team2_player1_new_name": "X1",
        "team2_player2_choice": "NEW_M",
        "team2_player2_new_name": "X2",
        "winning_team": "1",
        "date_played": "2026-01-01",
    }
    resp = client.post(url, data=data, follow=True)
    msgs = list(resp.context["messages"])
    assert any("introduce el nombre" in str(m) for m in msgs)


def test_match_view_resolve_player_creates_new_player_covers_455_457():
    # Covers 455-457: create new player on NEW_M
    user, player = mk_user_with_player("u_newcreate", "M")
    
    client.login(username="u_newcreate", password="pass")
    url = reverse("match")

    data = {
        "team1_player2_choice": "NEW_M",
        "team1_player2_new_name": "NEW_CREATED",
        "team2_player1_choice": "NEW_M",
        "team2_player1_new_name": "NEW_CREATED2",
        "team2_player2_choice": "NEW_M",
        "team2_player2_new_name": "NEW_CREATED3",
        "winning_team": "1",
        "date_played": "2026-01-02",
    }
    resp = client.post(url, data=data, follow=True)

    assert Player.objects.filter(name="NEW_CREATED").exists()


def test_match_view_invalid_player_id_covers_462_463():
    # Covers 462-463: invalid player id (ValueError/DoesNotExist)
    user, player = mk_user_with_player("u_badid", "M")
    
    client.login(username="u_badid", password="pass")
    url = reverse("match")

    data = {
        "team1_player2_choice": "abc",  # invalid int
        "team2_player1_choice": "NEW_M",
        "team2_player1_new_name": "X1",
        "team2_player2_choice": "NEW_M",
        "team2_player2_new_name": "X2",
        "winning_team": "1",
        "date_played": "2026-01-03",
    }
    resp = client.post(url, data=data, follow=True)
    msgs = list(resp.context["messages"])
    assert any("no válido" in str(m) for m in msgs)


def test_match_view_team2_player1_error_covers_475_476():
    # Covers 475-476: err on team2_player1 -> messages.error + redirect
    user, player = mk_user_with_player("u_t2p1", "M")
    p2 = Player.objects.create(name="P2_T2P1", gender="M")

    
    client.login(username="u_t2p1", password="pass")
    url = reverse("match")

    data = {
        "team1_player2_choice": str(p2.id),
        "team2_player1_choice": "",  # triggers err
        "team2_player2_choice": "NEW_M",
        "team2_player2_new_name": "X2",
        "winning_team": "1",
        "date_played": "2026-01-04",
    }
    resp = client.post(url, data=data, follow=True)
    msgs = list(resp.context["messages"])
    assert any("selecciona un jugador" in str(m) for m in msgs)


def test_match_view_team2_player2_error_covers_480_481():
    # Covers 480-481: err on team2_player2 -> messages.error + redirect
    user, player = mk_user_with_player("u_t2p2", "M")
    p2 = Player.objects.create(name="P2_T2P2", gender="M")
    p3 = Player.objects.create(name="P3_T2P2", gender="M")

    
    client.login(username="u_t2p2", password="pass")
    url = reverse("match")

    data = {
        "team1_player2_choice": str(p2.id),
        "team2_player1_choice": str(p3.id),
        "team2_player2_choice": "",  # triggers err
        "winning_team": "1",
        "date_played": "2026-01-05",
    }
    resp = client.post(url, data=data, follow=True)
    msgs = list(resp.context["messages"])
    assert any("selecciona un jugador" in str(m) for m in msgs)


def test_match_view_duplicate_players_covers_486_487():
    # Covers 486-487: duplicate participants
    user, player = mk_user_with_player("u_dup", "M")
    p2 = Player.objects.create(name="P2_DUP", gender="M")
    p3 = Player.objects.create(name="P3_DUP", gender="M")

    
    client.login(username="u_dup", password="pass")
    url = reverse("match")

    # team1_player2 == team2_player1 -> duplicate
    data = {
        "team1_player2_choice": str(p2.id),
        "team2_player1_choice": str(p2.id),
        "team2_player2_choice": str(p3.id),
        "winning_team": "1",
        "date_played": "2026-01-06",
    }
    resp = client.post(url, data=data, follow=True)
    msgs = list(resp.context["messages"])
    assert any("Jugadores repetidos" in str(m) for m in msgs)


def test_login_view_get_covers_614():
    
    url = reverse("login")
    resp = client.get(url)
    assert resp.status_code == 200
