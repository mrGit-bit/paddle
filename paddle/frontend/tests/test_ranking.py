import pytest
from datetime import date, timedelta
from django.urls import reverse
from django.test import RequestFactory

from games.models import Player, Match
from frontend.services.ranking import compute_ranking
from frontend.views import get_ranking_redirect
from frontend.views import paginate_list

pytestmark = pytest.mark.django_db


def test_get_ranking_redirect_male():
    resp = get_ranking_redirect("male")
    assert resp.status_code == 302
    assert resp.url == reverse("ranking_male")


def test_get_ranking_redirect_female():
    resp = get_ranking_redirect("female")
    assert resp.status_code == 302
    assert resp.url == reverse("ranking_female")


def test_get_ranking_redirect_mixed():
    resp = get_ranking_redirect("mixed")
    assert resp.status_code == 302
    assert resp.url == reverse("ranking_mixed")


def test_get_ranking_redirect_default_all_or_unknown():
    resp = get_ranking_redirect("all")
    assert resp.status_code == 302
    assert resp.url == reverse("hall_of_fame")

    resp2 = get_ranking_redirect("unknown")
    assert resp2.status_code == 302
    assert resp2.url == reverse("hall_of_fame")


def test_ranking_home_redirects_to_last_scope_male(client):
    session = client.session
    session["last_ranking_scope"] = "male"
    session.save()

    resp = client.get(reverse("ranking_home"))
    assert resp.status_code == 302
    assert resp.url == reverse("ranking_male")


def test_ranking_home_redirects_to_last_scope_female(client):
    session = client.session
    session["last_ranking_scope"] = "female"
    session.save()

    resp = client.get(reverse("ranking_home"))
    assert resp.status_code == 302
    assert resp.url == reverse("ranking_female")


def test_ranking_home_redirects_to_last_scope_mixed(client):
    session = client.session
    session["last_ranking_scope"] = "mixed"
    session.save()

    resp = client.get(reverse("ranking_home"))
    assert resp.status_code == 302
    assert resp.url == reverse("ranking_mixed")


def test_ranking_home_redirects_default_to_all(client):
    resp = client.get(reverse("ranking_home"))
    assert resp.status_code == 302
    assert resp.url == reverse("hall_of_fame")


@pytest.mark.django_db
def test_paginate_list_invalid_page_defaults_to_1():
    rf = RequestFactory()
    request = rf.get("/", {"page": "not-an-int"})

    items = list(range(30))  # 30 items, page_size=12 -> 3 pages
    page_items, pagination = paginate_list(items, request, page_size=12)

    assert pagination["current_page"] == 1
    assert pagination["total_pages"] == 3
    assert len(page_items) == 12
    assert page_items[0] == 0


def mk_player(name: str, gender: str):
    return Player.objects.create(name=name, gender=gender)


def mk_match(p1, p2, p3, p4, winning_team: int, d: date):
    """
    Create a 2v2 match.
    Team1: p1+p2 vs Team2: p3+p4
    """
    return Match.objects.create(
        team1_player1=p1,
        team1_player2=p2,
        team2_player1=p3,
        team2_player2=p4,
        winning_team=winning_team,
        date_played=d,
    )


def test_tie_positions_show_only_once_and_skip_numbers():
    """
    Two players tie (same wins, same win_rate, same matches) -> 1224 style
    - First in tie group: show_position=True
    - Second in tie group: show_position=False, same display_position
    - Next player position skips (e.g., 1,2,2,4)
    """
    # all male for simplicity
    a = mk_player("A", "M")
    b = mk_player("B", "M")
    c = mk_player("C", "M")
    d = mk_player("D", "M")
    e = mk_player("E", "M")
    f = mk_player("F", "M")

    base = date.today() - timedelta(days=10)

    # Make A and B tie at 1 win / 2 matches = 50%
    # Match1: A wins, B loses
    mk_match(a, c, b, d, winning_team=1, d=base)
    # Match2: B wins, A loses
    mk_match(b, e, a, f, winning_team=1, d=base + timedelta(days=1))

    ranked, unranked, scope = compute_ranking("all")

    # Find A and B in ranked list
    pa = next(p for p in ranked if p.name == "A")
    pb = next(p for p in ranked if p.name == "B")

    assert pa.display_wins == 1 and pa.display_matches == 2
    assert pb.display_wins == 1 and pb.display_matches == 2
    assert round(pa.display_win_rate, 2) == 50.0
    assert round(pb.display_win_rate, 2) == 50.0

    # They must share the same competition rank
    assert pa.display_position == pb.display_position

    # Exactly one of them should show the position (first row of tie group)
    assert {pa.show_position, pb.show_position} == {True, False}

    # Verify competition ranking skip after the tie group:
    # If a tie group of size k starts at ordinal index i, the next distinct rank is i+k.
    tie_pos = pa.display_position
    tie_group = [p for p in ranked if p.display_position == tie_pos]
    assert len(tie_group) >= 2  # at least A and B

    # Find the first occurrence of that tie group in the ordered list
    first_idx = next(i for i, p in enumerate(ranked, start=1) if p.display_position == tie_pos)
    k = len(tie_group)

    # The next player after the tie group (if any) must have position first_idx + k
    if first_idx + k <= len(ranked):
        next_after_group = ranked[first_idx + k - 1]  # convert to 0-based
        assert next_after_group.display_position == first_idx + k


def test_untie_by_matches_fewer_matches_ranks_higher_when_wins_and_rate_equal():
    """
    If wins and win_rate are equal, fewer matches ranks higher.
    Example: both 0 wins and 0%:
      - player with 1 match should rank above player with 5 matches
    """
    # all male for simplicity
    one = mk_player("ONE", "M")
    five = mk_player("FIVE", "M")

    t1 = mk_player("T1", "M")
    t2 = mk_player("T2", "M")
    o1 = mk_player("O1", "M")
    o2 = mk_player("O2", "M")

    base = date.today() - timedelta(days=20)

    # ONE loses 1 match
    mk_match(one, t1, o1, o2, winning_team=2, d=base)

    # FIVE loses 5 matches (always on losing team)
    for i in range(5):
        mk_match(five, t2, o1, o2, winning_team=2, d=base + timedelta(days=i + 1))

    ranked, _, _ = compute_ranking("all")

    p_one = next(p for p in ranked if p.name == "ONE")
    p_five = next(p for p in ranked if p.name == "FIVE")

    assert p_one.display_wins == 0 and round(p_one.display_win_rate, 2) == 0.0
    assert p_five.display_wins == 0 and round(p_five.display_win_rate, 2) == 0.0

    # Matches differ
    assert p_one.display_matches == 1
    assert p_five.display_matches == 5

    # ONE must appear before FIVE in ranked list
    idx_one = ranked.index(p_one)
    idx_five = ranked.index(p_five)
    assert idx_one < idx_five


def test_unranked_population_is_scoped_by_gender_for_female():
    """
    In female scope:
    - unranked list must include only female players (even if males exist in DB)
    """
    f1 = mk_player("F1", "F")
    f2 = mk_player("F2", "F")
    m1 = mk_player("M1", "M")
    m2 = mk_player("M2", "M")

    ranked, unranked, scope = compute_ranking("female")

    assert scope == "female"
    assert all(p.gender == "F" for p in unranked)
    assert all(p.gender == "F" for p in ranked)

    # With no matches, all female players should be unranked
    assert {p.name for p in unranked} == {"F1", "F2"}
    assert len(ranked) == 0
