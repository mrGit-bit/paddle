# absolute path: /workspaces/paddle/paddle/frontend/services/ranking.py
# shared ranking service

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Tuple

from games.models import Match, Player


def apply_competition_ranking_with_ties(players: list[Player], key_fn: Callable[[Player], tuple]) -> None:
    """
    Applies competition ranking ("1224") with ties to an already-sorted list.

    Adds:
        - display_position (int)
        - show_position (bool): True only for first row of tie group
    """
    last_key = None
    last_position = None

    for index, p in enumerate(players, start=1):
        key = key_fn(p)
        if key != last_key:
            p.display_position = index
            p.show_position = True
            last_key = key
            last_position = index
        else:
            p.display_position = last_position
            p.show_position = False


def compute_ranking(scope: str) -> tuple[list[Player], list[Player], str]:
    """
    Compute ranking for a scope:
        - "all": all matches
        - "male": Match.GENDER_TYPE_MALE
        - "female": Match.GENDER_TYPE_FEMALE
        - "mixed": Match.GENDER_TYPE_MIXED

    Returns:
        ranked_players (with display_* + show_position),
        unranked_players (scoped population),
        normalized_scope
    """
    scope_map = {
        "all": None,
        "male": Match.GENDER_TYPE_MALE,
        "female": Match.GENDER_TYPE_FEMALE,
        "mixed": Match.GENDER_TYPE_MIXED,
    }
    if scope not in scope_map:
        scope = "all"

    gender_type = scope_map[scope]

    matches_qs = Match.objects.all()
    if gender_type:
        matches_qs = matches_qs.filter(match_gender_type=gender_type)

    matches_qs = matches_qs.select_related(
        "team1_player1", "team1_player2", "team2_player1", "team2_player2"
    )

    # stats[player_id] = {"matches": int, "wins": int}
    stats: dict[int, dict[str, int]] = {}

    for m in matches_qs:
        players = [m.team1_player1, m.team1_player2, m.team2_player1, m.team2_player2]
        for p in players:
            if p.id not in stats:
                stats[p.id] = {"matches": 0, "wins": 0}
            stats[p.id]["matches"] += 1

        winners = [m.team1_player1, m.team1_player2] if m.winning_team == 1 else [m.team2_player1, m.team2_player2]
        for w in winners:
            stats[w.id]["wins"] += 1

    # Scoped population for "unranked" list
    if scope == "male":
        population = list(Player.objects.filter(gender=Player.GENDER_MALE).order_by("name"))
    elif scope == "female":
        population = list(Player.objects.filter(gender=Player.GENDER_FEMALE).order_by("name"))
    else:
        population = list(Player.objects.all().order_by("name"))

    ranked_players: list[Player] = []
    unranked_players: list[Player] = []

    for p in population:
        row = stats.get(p.id)
        if not row or row["matches"] == 0:
            unranked_players.append(p)
            continue

        wins = row["wins"]
        matches = row["matches"]
        win_rate = (wins / matches) * 100 if matches else 0.0

        p.display_wins = wins
        p.display_matches = matches
        p.display_win_rate = win_rate
        ranked_players.append(p)

    # Order: wins desc, win_rate desc, matches asc, name asc
    ranked_players.sort(
        key=lambda p: (
            -p.display_wins,
            -round(p.display_win_rate, 2),
            p.display_matches,
            p.name.lower(),
        )
    )

    # Ties: wins + win_rate + matches (T1 + your untie rule)
    apply_competition_ranking_with_ties(
        ranked_players,
        key_fn=lambda p: (p.display_wins, round(p.display_win_rate, 2), p.display_matches),
    )

    return ranked_players, unranked_players, scope
