from datetime import date

import pytest

from games.models import Match, Player


pytestmark = pytest.mark.django_db


def test_update_player_rankings_uses_competition_ties_and_unranked_zero():
    a = Player.objects.create(name="A", gender=Player.GENDER_MALE)
    b = Player.objects.create(name="B", gender=Player.GENDER_MALE)
    c = Player.objects.create(name="C", gender=Player.GENDER_MALE)
    d = Player.objects.create(name="D", gender=Player.GENDER_MALE)
    e = Player.objects.create(name="E", gender=Player.GENDER_MALE)
    f = Player.objects.create(name="F", gender=Player.GENDER_MALE)
    z = Player.objects.create(name="Z", gender=Player.GENDER_MALE)  # no matches

    Match.objects.create(
        team1_player1=a,
        team1_player2=b,
        team2_player1=c,
        team2_player2=d,
        winning_team=1,
        date_played=date(2026, 3, 1),
    )
    Match.objects.create(
        team1_player1=c,
        team1_player2=d,
        team2_player1=a,
        team2_player2=b,
        winning_team=1,
        date_played=date(2026, 3, 2),
    )
    Match.objects.create(
        team1_player1=e,
        team1_player2=f,
        team2_player1=b,
        team2_player2=d,
        winning_team=1,
        date_played=date(2026, 3, 3),
    )

    a.refresh_from_db()
    b.refresh_from_db()
    c.refresh_from_db()
    d.refresh_from_db()
    e.refresh_from_db()
    f.refresh_from_db()
    z.refresh_from_db()

    assert e.ranking_position == 1
    assert f.ranking_position == 1
    assert a.ranking_position == 3
    assert c.ranking_position == 3
    assert b.ranking_position == 5
    assert d.ranking_position == 5
    assert z.ranking_position == 0
