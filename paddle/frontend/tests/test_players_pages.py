import pytest
from datetime import date
from django.urls import reverse

from games.models import Match, Player


pytestmark = pytest.mark.django_db


def test_players_list_is_public_200(client):
    Player.objects.create(name="Jugador Uno", gender=Player.GENDER_MALE)
    response = client.get(reverse("players"))
    assert response.status_code == 200
    assert "Jugador Uno" in response.content.decode("utf-8")


def test_player_detail_is_public_200(client):
    player = Player.objects.create(name="Jugador Perfil", gender=Player.GENDER_MALE)
    response = client.get(reverse("player_detail", args=[player.id]))
    assert response.status_code == 200
    assert "Jugador Perfil" in response.content.decode("utf-8")


def test_player_detail_404(client):
    response = client.get(reverse("player_detail", args=[999999]))
    assert response.status_code == 404


def test_player_detail_matches_filtered(client):
    player_a = Player.objects.create(name="Player A", gender=Player.GENDER_MALE)
    player_b = Player.objects.create(name="Player B", gender=Player.GENDER_MALE)
    player_c = Player.objects.create(name="Player C", gender=Player.GENDER_MALE)
    player_d = Player.objects.create(name="Player D", gender=Player.GENDER_MALE)
    player_e = Player.objects.create(name="Player E", gender=Player.GENDER_MALE)
    player_f = Player.objects.create(name="Player F", gender=Player.GENDER_MALE)
    player_g = Player.objects.create(name="Player G", gender=Player.GENDER_MALE)
    player_h = Player.objects.create(name="Player H", gender=Player.GENDER_MALE)

    involving_a = Match.objects.create(
        team1_player1=player_a,
        team1_player2=player_b,
        team2_player1=player_c,
        team2_player2=player_d,
        winning_team=1,
        date_played=date(2026, 1, 10),
    )
    not_involving_a = Match.objects.create(
        team1_player1=player_e,
        team1_player2=player_f,
        team2_player1=player_g,
        team2_player2=player_h,
        winning_team=2,
        date_played=date(2026, 1, 11),
    )

    response = client.get(reverse("player_detail", args=[player_a.id]))
    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert f"match-card-{involving_a.id}" in content
    assert f"match-card-{not_involving_a.id}" not in content


def test_player_detail_scope_rows_render_data_href_only_when_applicable(client):
    player_a = Player.objects.create(name="Scope A", gender=Player.GENDER_MALE)
    player_b = Player.objects.create(name="Scope B", gender=Player.GENDER_MALE)
    player_c = Player.objects.create(name="Scope C", gender=Player.GENDER_MALE)
    player_d = Player.objects.create(name="Scope D", gender=Player.GENDER_MALE)

    Match.objects.create(
        team1_player1=player_a,
        team1_player2=player_b,
        team2_player1=player_c,
        team2_player2=player_d,
        winning_team=1,
        date_played=date(2026, 1, 12),
    )

    response = client.get(reverse("player_detail", args=[player_a.id]))
    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert 'data-href="/?page=1#top"' in content
    assert 'data-href="/ranking/male/?page=1#top"' in content
    assert 'data-href="/ranking/mixed/' not in content
