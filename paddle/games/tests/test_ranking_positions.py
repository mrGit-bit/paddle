from datetime import date

import pytest
from django.core.exceptions import ValidationError

from games.models import Group, Match, Player


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


def test_invalid_match_update_preserves_existing_effects():
    group_a = Group.objects.create(name="Grupo A")
    group_b = Group.objects.create(name="Grupo B")
    a = Player.objects.create(name="A", gender=Player.GENDER_MALE, group=group_a)
    b = Player.objects.create(name="B", gender=Player.GENDER_MALE, group=group_a)
    c = Player.objects.create(name="C", gender=Player.GENDER_MALE, group=group_a)
    d = Player.objects.create(name="D", gender=Player.GENDER_MALE, group=group_a)
    outsider = Player.objects.create(
        name="Outsider",
        gender=Player.GENDER_MALE,
        group=group_b,
    )

    match = Match.objects.create(
        group=group_a,
        team1_player1=a,
        team1_player2=b,
        team2_player1=c,
        team2_player2=d,
        winning_team=1,
        date_played=date(2026, 3, 1),
    )

    original_player_ids = {a.id, b.id, c.id, d.id}
    assert set(match.players.values_list("id", flat=True)) == original_player_ids

    match.team1_player1 = outsider
    with pytest.raises(ValidationError):
        match.save()

    match.refresh_from_db()
    assert match.team1_player1_id == a.id
    assert set(match.players.values_list("id", flat=True)) == original_player_ids

    a.refresh_from_db()
    b.refresh_from_db()
    c.refresh_from_db()
    d.refresh_from_db()
    assert a.ranking_position == 1
    assert b.ranking_position == 1
    assert c.ranking_position == 3
    assert d.ranking_position == 3
