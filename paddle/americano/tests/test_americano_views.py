# absolute path: /workspaces/paddle/paddle/americano/tests/test_americano_views.py
# pytest /workspaces/paddle/paddle/americano/tests/test_americano_views.py -q

import pytest
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import User

from games.models import Player
from americano.models import (
    AmericanoTournament,
    AmericanoRound,
    AmericanoMatch,
    AmericanoPlayerStats,
)

pytestmark = pytest.mark.django_db


# -----------------------
# Helpers / fixtures
# -----------------------

@pytest.fixture
def user():
    return User.objects.create_user(username="u1", password="pass1234")


@pytest.fixture
def other_user():
    return User.objects.create_user(username="u2", password="pass1234")


@pytest.fixture
def staff_user():
    return User.objects.create_user(username="admin", password="pass1234", is_staff=True)


@pytest.fixture
def player_user(user):
    # Linked player to user
    return Player.objects.create(name="PlayerUser", registered_user=user)


@pytest.fixture
def player_other(other_user):
    return Player.objects.create(name="PlayerOther", registered_user=other_user)


@pytest.fixture
def players_pool():
    # A pool of existing registered/unregistered players
    return [
        Player.objects.create(name="Americano1"),
        Player.objects.create(name="Americano2"),
        Player.objects.create(name="anselmo fuertes"),
        Player.objects.create(name="Marta_Varela"),
        Player.objects.create(name="fede_N"),
        Player.objects.create(name="fede_olea"),
        Player.objects.create(name="hashjk"),
        Player.objects.create(name="jaimito"),
    ]


def _create_tournament(
    *,
    creator: User,
    name="Torneo Test",
    play_date=None,
    players=None,
    num_players=None,
    is_active=True,
):
    if play_date is None:
        play_date = timezone.localdate()

    # If players are provided and num_players is not, derive it.
    if num_players is None and players:
        num_players = len(players)

    # Fallback (avoid NOT NULL constraint)
    if num_players is None:
        num_players = 4

    t = AmericanoTournament.objects.create(
        name=name,
        play_date=play_date,
        created_by=creator,
        is_active=is_active,
        num_players=num_players,
    )

    if players:
        t.players.set(players)

    # Ensure stats rows exist
    for p in t.players.all():
        AmericanoPlayerStats.objects.get_or_create(tournament=t, player=p)

    return t


def _create_round_with_matches(tournament: AmericanoTournament, number=1, matches_count=2):
    r = AmericanoRound.objects.create(tournament=tournament, number=number)
    for i in range(matches_count):
        AmericanoMatch.objects.create(round=r, court_number=i + 1)
    return r


# -----------------------
# Tests: create tournament
# -----------------------

def test_americano_new_requires_login(client):
    url = reverse("americano_new")
    res = client.get(url)
    # login_required usually redirects to login
    assert res.status_code in (302, 301)


def test_americano_new_preselects_creator_player_on_get(client, user, player_user):
    client.login(username="u1", password="pass1234")
    res = client.get(reverse("americano_new"))
    assert res.status_code == 200
    form = res.context["form"]
    # ModelMultipleChoiceField initial should include creator player pk
    assert player_user.pk in list(form.fields["players"].initial)


def test_americano_new_creates_new_players_and_round1(client, user, player_user, players_pool, monkeypatch):
    """
    - Creates tournament
    - Adds selected existing players + new players (textarea)
    """

    client.login(username="u1", password="pass1234")

    # select 7 from pool + user player => total 8 (multiple of 4)
    selected = players_pool[:7] + [player_user]
    payload = {
        "name": "with existing players only",  # fits your max length example
        "play_date": str(timezone.localdate()),
        "num_players": 10,
        "players": [p.pk for p in selected],  # 8 existing
        "new_players": "NewOne\nNewTwo\n",     # 2 new => total 10 (not multiple of 4)
    }
    # This should fail because num_players must be multiple of 4 per your form
    res = client.post(reverse("americano_new"), data=payload)
    assert res.status_code == 200
    assert "El número de jugadores debe ser múltiplo de 4." in res.content.decode("utf-8")

    # Now valid: total 12 and multiple of 4
    payload["num_players"] = 12
    payload["new_players"] = "NewOne\nNewTwo\nNewThree\nNewFour\n"  # +4 => total 12

    res = client.post(reverse("americano_new"), data=payload)
    assert res.status_code == 302  # redirect to detail

    t = AmericanoTournament.objects.get(name="with existing players only")
    assert t.created_by == user
    assert t.players.count() == 12

    assert Player.objects.filter(name__iexact="NewOne").exists()

    # No random rounds created automatically anymore
    assert t.rounds.count() == 0

# -----------------------
# Tests: permissions / edit
# -----------------------

def test_americano_detail_view_accessible_anonymous(client, user, players_pool):
    t = _create_tournament(creator=user, players=players_pool[:4])
    res = client.get(reverse("americano_detail", kwargs={"pk": t.pk}))
    assert res.status_code == 200


def test_only_participants_can_edit_rounds(client, user, other_user, players_pool):
    # Tournament with players not linked to other_user
    t = _create_tournament(creator=user, players=players_pool[:4])
    r = _create_round_with_matches(t, number=1, matches_count=1)

    client.login(username="u2", password="pass1234")
    payload = {
        f"match_{r.matches.first().id}_court": "1",
    }
    res = client.post(reverse("americano_assign_round", kwargs={"round_id": r.pk}), data=payload)
    # should redirect back without applying changes
    assert res.status_code == 302


# -----------------------
# Tests: partial saving round results
# -----------------------

def test_assign_round_allows_partial_results(client, user, player_user, players_pool):
    # user is a participant
    t_players = [player_user] + players_pool[:7]  # 8 players
    t = _create_tournament(creator=user, players=t_players)
    r = _create_round_with_matches(t, number=1, matches_count=2)  # 2 matches

    client.login(username="u1", password="pass1234")

    m1, m2 = list(r.matches.all())

    # Fill only match 1 players + scores; leave match 2 empty
    # Match 1 uses first 4 players
    p = t_players
    payload = {
        f"match_{m1.id}_court": "2",
        f"match_{m1.id}_t1p1": str(p[0].pk),
        f"match_{m1.id}_t1p2": str(p[1].pk),
        f"match_{m1.id}_t2p1": str(p[2].pk),
        f"match_{m1.id}_t2p2": str(p[3].pk),
        f"match_{m1.id}_score1": "15",
        f"match_{m1.id}_score2": "10",

        f"match_{m2.id}_court": "1",
        # no players, no scores
        f"match_{m2.id}_score1": "",
        f"match_{m2.id}_score2": "",
    }

    res = client.post(reverse("americano_assign_round", kwargs={"round_id": r.pk}), data=payload)
    assert res.status_code == 302

    m1.refresh_from_db()
    m2.refresh_from_db()

    assert m1.court_number == 2
    assert m1.team1_points == 15
    assert m1.team2_points == 10

    # Match 2 incomplete => scores cleared
    assert m2.team1_player1 is None
    assert m2.team1_points is None
    assert m2.team2_points is None

    # Standings recomputed: winners are team1 players (p0, p1)
    s0 = AmericanoPlayerStats.objects.get(tournament=t, player=p[0])
    s1 = AmericanoPlayerStats.objects.get(tournament=t, player=p[1])
    s2 = AmericanoPlayerStats.objects.get(tournament=t, player=p[2])
    s3 = AmericanoPlayerStats.objects.get(tournament=t, player=p[3])

    assert s0.wins == 1
    assert s1.wins == 1
    assert s2.wins == 0
    assert s3.wins == 0


def test_recompute_no_double_count_on_edit(client, user, player_user, players_pool):
    t_players = [player_user] + players_pool[:3]  # 4 players => 1 match
    t = _create_tournament(creator=user, players=t_players)
    r = _create_round_with_matches(t, number=1, matches_count=1)
    m = r.matches.first()

    client.login(username="u1", password="pass1234")

    def post_score(a, b):
        payload = {
            f"match_{m.id}_court": "1",
            f"match_{m.id}_t1p1": str(t_players[0].pk),
            f"match_{m.id}_t1p2": str(t_players[1].pk),
            f"match_{m.id}_t2p1": str(t_players[2].pk),
            f"match_{m.id}_t2p2": str(t_players[3].pk),
            f"match_{m.id}_score1": str(a),
            f"match_{m.id}_score2": str(b),
        }
        return client.post(reverse("americano_assign_round", kwargs={"round_id": r.pk}), data=payload)

    post_score(15, 10)
    s0 = AmericanoPlayerStats.objects.get(tournament=t, player=t_players[0])
    assert s0.wins == 1

    # flip result
    post_score(10, 15)
    s0.refresh_from_db()
    assert s0.wins == 0  # must not be 1+0 or 2; recompute from scratch


# -----------------------
# Tests: delete round / create after delete
# -----------------------

def test_delete_last_round_then_can_create_new_round(client, user, player_user, players_pool):
    t_players = [player_user] + players_pool[:3]  # 4 players => 1 match
    t = _create_tournament(creator=user, players=t_players)
    r1 = _create_round_with_matches(t, number=1, matches_count=1)

    client.login(username="u1", password="pass1234")

    # delete round 1
    res = client.post(reverse("americano_delete_round", kwargs={"round_id": r1.pk}))
    assert res.status_code == 302
    assert t.rounds.count() == 0

    # create new round
    res = client.get(reverse("americano_new_round", kwargs={"pk": t.pk}))
    assert res.status_code == 302
    assert t.rounds.count() == 1


# -----------------------
# Tests: delete tournament permissions
# -----------------------

def test_delete_tournament_only_creator_or_staff(client, user, other_user, staff_user, players_pool):
    t = _create_tournament(creator=user, players=players_pool[:4])

    # other_user cannot delete
    client.login(username="u2", password="pass1234")
    res = client.post(reverse("americano_delete_tournament", kwargs={"pk": t.pk}))
    assert res.status_code == 302
    assert AmericanoTournament.objects.filter(pk=t.pk).exists()

    # staff can delete
    client.logout()
    client.login(username="admin", password="pass1234")
    res = client.post(reverse("americano_delete_tournament", kwargs={"pk": t.pk}))
    assert res.status_code == 302
    assert not AmericanoTournament.objects.filter(pk=t.pk).exists()


# -----------------------
# Tests: tie display positions (Option B)
# -----------------------

def test_standings_tie_position_shown_once(client, user, players_pool):
    # Create tournament with 4 players => 1 match; force a tie in standings by leaving scores None
    t = _create_tournament(creator=user, players=players_pool[:4])

    client.login(username="u1", password="pass1234")
    res = client.get(reverse("americano_detail", kwargs={"pk": t.pk}))
    assert res.status_code == 200

    standings = list(res.context["standings"])
    # With no results, all players have wins=0, diff=0, for=0 (tie group)
    # Option B: only first should show_position = True
    assert standings[0].show_position is True
    for row in standings[1:]:
        assert row.show_position is False
        assert row.display_position == standings[0].display_position

def test_americano_list_page_renders(client, user, players_pool):
    # one ongoing, one finished
    today = timezone.localdate()
    t1 = _create_tournament(creator=user, name="Ongoing", play_date=today, players=players_pool[:4])
    t2 = _create_tournament(creator=user, name="Finished", play_date=today - timezone.timedelta(days=1), players=players_pool[:4])

    res = client.get(reverse("americano_list"))
    assert res.status_code == 200
    content = res.content.decode("utf-8")
    assert "Ongoing" in content
    assert "Finished" in content


def test_americano_new_round_denied_for_non_participant(client, user, other_user, players_pool):
    t = _create_tournament(creator=user, players=players_pool[:4])
    client.login(username="u2", password="pass1234")

    res = client.get(reverse("americano_new_round", kwargs={"pk": t.pk}))
    assert res.status_code == 302

    # no rounds created
    assert t.rounds.count() == 0


def test_delete_round_denied_for_non_participant(client, user, other_user, players_pool):
    t = _create_tournament(creator=user, players=players_pool[:4])
    r = _create_round_with_matches(t, number=1, matches_count=1)

    client.login(username="u2", password="pass1234")
    res = client.post(reverse("americano_delete_round", kwargs={"round_id": r.pk}))
    assert res.status_code == 302

    # round still exists
    assert AmericanoRound.objects.filter(pk=r.pk).exists()


def test_assign_round_rejects_player_outside_tournament(client, user, player_user, players_pool):
    t_players = [player_user] + players_pool[:3]  # 4 players -> 1 match
    t = _create_tournament(creator=user, players=t_players)
    r = _create_round_with_matches(t, number=1, matches_count=1)
    m = r.matches.first()

    outsider = Player.objects.create(name="OUTSIDER_X")

    client.login(username="u1", password="pass1234")

    payload = {
        f"match_{m.id}_court": "1",
        f"match_{m.id}_t1p1": str(t_players[0].pk),
        f"match_{m.id}_t1p2": str(t_players[1].pk),
        f"match_{m.id}_t2p1": str(t_players[2].pk),
        f"match_{m.id}_t2p2": str(outsider.pk),  # invalid
        f"match_{m.id}_score1": "10",
        f"match_{m.id}_score2": "5",
    }
    res = client.post(reverse("americano_assign_round", kwargs={"round_id": r.pk}), data=payload)
    assert res.status_code == 302

    # session error set
    res2 = client.get(reverse("americano_detail", kwargs={"pk": t.pk}))
    assert "Selección inválida" in res2.content.decode("utf-8")


def test_assign_round_rejects_duplicate_within_match(client, user, player_user, players_pool):
    t_players = [player_user] + players_pool[:3]  # 4 players -> 1 match
    t = _create_tournament(creator=user, players=t_players)
    r = _create_round_with_matches(t, number=1, matches_count=1)
    m = r.matches.first()

    client.login(username="u1", password="pass1234")

    payload = {
        f"match_{m.id}_court": "1",
        f"match_{m.id}_t1p1": str(t_players[0].pk),
        f"match_{m.id}_t1p2": str(t_players[0].pk),  # duplicate in same match
        f"match_{m.id}_t2p1": str(t_players[2].pk),
        f"match_{m.id}_t2p2": str(t_players[3].pk),
        f"match_{m.id}_score1": "10",
        f"match_{m.id}_score2": "5",
    }
    res = client.post(reverse("americano_assign_round", kwargs={"round_id": r.pk}), data=payload)
    assert res.status_code == 302

    res2 = client.get(reverse("americano_detail", kwargs={"pk": t.pk}))
    assert "no puede repetirse" in res2.content.decode("utf-8").lower()


def test_assign_round_invalid_court_is_ignored(client, user, player_user, players_pool):
    t_players = [player_user] + players_pool[:3]
    t = _create_tournament(creator=user, players=t_players)
    r = _create_round_with_matches(t, number=1, matches_count=1)
    m = r.matches.first()

    client.login(username="u1", password="pass1234")

    payload = {
        f"match_{m.id}_court": "abc",  # invalid
        f"match_{m.id}_t1p1": str(t_players[0].pk),
        f"match_{m.id}_t1p2": str(t_players[1].pk),
        f"match_{m.id}_t2p1": str(t_players[2].pk),
        f"match_{m.id}_t2p2": str(t_players[3].pk),
        f"match_{m.id}_score1": "10",
        f"match_{m.id}_score2": "5",
    }
    res = client.post(reverse("americano_assign_round", kwargs={"round_id": r.pk}), data=payload)
    assert res.status_code == 302

    m.refresh_from_db()
    # court stays default (created by fixture), i.e., not overwritten by invalid input
    assert m.court_number in (None, 1)


def test_assign_round_negative_score_is_ignored(client, user, player_user, players_pool):
    t_players = [player_user] + players_pool[:3]
    t = _create_tournament(creator=user, players=t_players)
    r = _create_round_with_matches(t, number=1, matches_count=1)
    m = r.matches.first()

    client.login(username="u1", password="pass1234")

    payload = {
        f"match_{m.id}_court": "1",
        f"match_{m.id}_t1p1": str(t_players[0].pk),
        f"match_{m.id}_t1p2": str(t_players[1].pk),
        f"match_{m.id}_t2p1": str(t_players[2].pk),
        f"match_{m.id}_t2p2": str(t_players[3].pk),
        f"match_{m.id}_score1": "-1",   # invalid => None
        f"match_{m.id}_score2": "10",
    }
    res = client.post(reverse("americano_assign_round", kwargs={"round_id": r.pk}), data=payload)
    assert res.status_code == 302

    m.refresh_from_db()
    # Your parse_score returns None for negatives
    assert m.team1_points is None
    assert m.team2_points == 10


def test_delete_tournament_requires_login(client, user, players_pool):
    t = _create_tournament(creator=user, players=players_pool[:4])
    res = client.post(reverse("americano_delete_tournament", kwargs={"pk": t.pk}))
    assert res.status_code in (301, 302)
    assert AmericanoTournament.objects.filter(pk=t.pk).exists()
    
def test_americano_list_with_no_tournaments(client):
    res = client.get(reverse("americano_list"))
    assert res.status_code == 200


def test_americano_new_post_invalid_renders_form(client, user):
    client.login(username="u1", password="pass1234")

    # Missing required fields => invalid form => should render same page (200)
    res = client.post(reverse("americano_new"), data={"name": ""})
    assert res.status_code == 200
    assert "form" in res.context


def test_assign_round_ignores_invalid_player_id_format(client, user, player_user, players_pool):
    # create tournament and round with 1 match
    t_players = [player_user] + players_pool[:3]
    t = _create_tournament(creator=user, players=t_players)
    r = _create_round_with_matches(t, number=1, matches_count=1)
    m = r.matches.first()

    client.login(username="u1", password="pass1234")

    # Put a non-integer player id in one field to hit ValueError branch.
    payload = {
        f"match_{m.id}_court": "1",
        f"match_{m.id}_t1p1": "abc",  # invalid
        f"match_{m.id}_t1p2": str(t_players[1].pk),
        f"match_{m.id}_t2p1": str(t_players[2].pk),
        f"match_{m.id}_t2p2": str(t_players[3].pk),
        f"match_{m.id}_score1": "10",
        f"match_{m.id}_score2": "5",
    }
    res = client.post(reverse("americano_assign_round", kwargs={"round_id": r.pk}), data=payload)
    assert res.status_code == 302

    # Should not crash; and because match isn't fully assigned, scores must be cleared
    m.refresh_from_db()
    assert m.team1_points is None
    assert m.team2_points is None


def test_assign_round_clears_scores_if_not_fully_assigned(client, user, player_user, players_pool):
    t_players = [player_user] + players_pool[:3]
    t = _create_tournament(creator=user, players=t_players)
    r = _create_round_with_matches(t, number=1, matches_count=1)
    m = r.matches.first()

    client.login(username="u1", password="pass1234")

    # Provide scores but leave one player empty => not fully assigned => scores cleared
    payload = {
        f"match_{m.id}_court": "1",
        f"match_{m.id}_t1p1": str(t_players[0].pk),
        f"match_{m.id}_t1p2": "",  # missing
        f"match_{m.id}_t2p1": str(t_players[2].pk),
        f"match_{m.id}_t2p2": str(t_players[3].pk),
        f"match_{m.id}_score1": "15",
        f"match_{m.id}_score2": "10",
    }
    res = client.post(reverse("americano_assign_round", kwargs={"round_id": r.pk}), data=payload)
    assert res.status_code == 302

    m.refresh_from_db()
    assert m.team1_player2 is None
    assert m.team1_points is None
    assert m.team2_points is None

def test_delete_round_renumbers_remaining_rounds_edge_case(client, user, player_user, players_pool):
    """
    Edge-case coverage: If rounds become non-contiguous (e.g. via admin/DB),
    deleting one triggers renumbering to keep 1..N.
    """
    client.login(username="u1", password="pass1234")

    t = _create_tournament(
        creator=user,
        name="Renumber edge case",
        players=players_pool[:7] + [player_user],
        num_players=8,
    )


    # Non-contiguous by construction (simulating admin/DB edits)
    r1 = AmericanoRound.objects.create(tournament=t, number=1)
    r3 = AmericanoRound.objects.create(tournament=t, number=3)

    # Call delete endpoint on r1 to force remaining (3) -> (1) renumber
    res = client.post(reverse("americano_delete_round", args=[r1.pk]))
    assert res.status_code == 302

    r3.refresh_from_db()
    assert r3.number == 1

def test_assign_round_blocks_duplicate_player_across_fully_assigned_matches(client, user, player_user, players_pool):
    """
    When two matches are fully assigned, the same player cannot appear in both.
    Hits:
    - 'if any(pid in used_in_fully_assigned for pid in pid_list):'
    """
    client.login(username="u1", password="pass1234")

    players = players_pool[:7] + [player_user]
    t = _create_tournament(creator=user, name="Dup across matches test", players=players, num_players=8)

    r = AmericanoRound.objects.create(tournament=t, number=1)
    m1 = AmericanoMatch.objects.create(round=r)
    m2 = AmericanoMatch.objects.create(round=r)


    # Use p0..p3 in match1, then reuse p0 in match2 (fully assigned)
    p0, p1, p2, p3, p4, p5, p6, p7 = players

    payload = {
        f"match_{m1.id}_t1p1": str(p0.id),
        f"match_{m1.id}_t1p2": str(p1.id),
        f"match_{m1.id}_t2p1": str(p2.id),
        f"match_{m1.id}_t2p2": str(p3.id),

        # Reuse p0 here (invalid across fully assigned matches)
        f"match_{m2.id}_t1p1": str(p0.id),
        f"match_{m2.id}_t1p2": str(p4.id),
        f"match_{m2.id}_t2p1": str(p5.id),
        f"match_{m2.id}_t2p2": str(p6.id),
    }

    res = client.post(reverse("americano_assign_round", args=[r.id]), data=payload)
    assert res.status_code == 302

    # Follow redirect to read session message rendered on detail
    detail = client.get(res["Location"])
    assert "Un jugador no puede repetirse en la misma ronda." in detail.content.decode("utf-8")

def test_assign_round_parse_score_value_error_results_in_none(client, user, player_user, players_pool):
    """
    Covers parse_score() ValueError branch by submitting a non-integer score.
    """
    client.login(username="u1", password="pass1234")

    players = players_pool[:3] + [player_user]
    t = _create_tournament(creator=user, name="Score valueerror test", players=players, num_players=4)

    r = AmericanoRound.objects.create(tournament=t, number=1)
    m = AmericanoMatch.objects.create(round=r)

    p0, p1, p2, p3 = players

    payload = {
        f"match_{m.id}_t1p1": str(p0.id),
        f"match_{m.id}_t1p2": str(p1.id),
        f"match_{m.id}_t2p1": str(p2.id),
        f"match_{m.id}_t2p2": str(p3.id),
        f"match_{m.id}_score1": "abc",   # triggers ValueError
        f"match_{m.id}_score2": "10",
    }

    res = client.post(reverse("americano_assign_round", args=[r.id]), data=payload)
    assert res.status_code == 302

    m.refresh_from_db()
    assert m.team1_points is None
    assert m.team2_points == 10
    
def test_assign_round_action_new_round_saves_and_creates_next_round(client, user, player_user, players_pool):
    """
    Posting to americano_assign_round with action=new_round should:
    - save the current round data (same as Guardar)
    - recompute standings
    - create the next round with empty matches
    """
    client.login(username="u1", password="pass1234")

    # 8 players => each round should have 2 matches (8/4)
    t_players = players_pool[:7] + [player_user]
    t = _create_tournament(creator=user, players=t_players, num_players=8)

    r1 = AmericanoRound.objects.create(tournament=t, number=1)
    m1 = AmericanoMatch.objects.create(round=r1)
    m2 = AmericanoMatch.objects.create(round=r1)

    p0, p1, p2, p3, p4, p5, p6, p7 = t_players

    payload = {
        "action": "new_round",

        # Match 1 (fully assigned + scored)
        f"match_{m1.id}_court": "1",
        f"match_{m1.id}_t1p1": str(p0.id),
        f"match_{m1.id}_t1p2": str(p1.id),
        f"match_{m1.id}_t2p1": str(p2.id),
        f"match_{m1.id}_t2p2": str(p3.id),
        f"match_{m1.id}_score1": "15",
        f"match_{m1.id}_score2": "10",

        # Match 2 (fully assigned, no score)
        f"match_{m2.id}_court": "",
        f"match_{m2.id}_t1p1": str(p4.id),
        f"match_{m2.id}_t1p2": str(p5.id),
        f"match_{m2.id}_t2p1": str(p6.id),
        f"match_{m2.id}_t2p2": str(p7.id),
        f"match_{m2.id}_score1": "",
        f"match_{m2.id}_score2": "",
    }

    res = client.post(reverse("americano_assign_round", args=[r1.id]), data=payload)
    assert res.status_code == 302

    # Current match saved
    m1.refresh_from_db()
    assert m1.court_number == 1
    assert m1.team1_points == 15
    assert m1.team2_points == 10

    # Second match allowed with null court and no score
    m2.refresh_from_db()
    assert m2.court_number is None
    assert m2.team1_points is None
    assert m2.team2_points is None

    # Standings updated from the one completed match
    s0 = AmericanoPlayerStats.objects.get(tournament=t, player=p0)
    s1 = AmericanoPlayerStats.objects.get(tournament=t, player=p1)
    assert s0.wins == 1
    assert s1.wins == 1

    # New round created
    t.refresh_from_db()
    assert t.rounds.count() == 2
    r2 = t.rounds.order_by("number").last()
    assert r2.number == 2
    assert r2.matches.count() == 8 // 4  # 2 empty matches
    assert r2.matches.filter(team1_player1__isnull=False).count() == 0


