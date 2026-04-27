from __future__ import annotations

from copy import copy
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from games.models import Player

# Canonical ranking policy (source of truth):
# - Sort key: wins desc, win_rate(2dp) desc, matches asc, name asc (case-insensitive).
# - Tie key: wins, win_rate(2dp), matches.
# - Position style: competition ranking ("1224"), with one displayed row per tie group.


def canonical_rounded_win_rate(win_rate: float) -> float:
    return round(win_rate, 2)


def canonical_ranking_sort_key(*, wins: int, win_rate: float, matches: int, name: str) -> tuple:
    return (
        -wins,
        -canonical_rounded_win_rate(win_rate),
        matches,
        name.lower(),
    )


def canonical_ranking_tie_key(*, wins: int, win_rate: float, matches: int) -> tuple:
    return (
        wins,
        canonical_rounded_win_rate(win_rate),
        matches,
    )


def _pair_player_tuple(player_a, player_b):
    if player_a.id <= player_b.id:
        return player_a, player_b
    return player_b, player_a


def _build_pair_rows(*, group=None):
    from games.models import Match

    matches_qs = Match.objects.select_related(
        "team1_player1", "team1_player2", "team2_player1", "team2_player2"
    )
    if group is not None:
        matches_qs = matches_qs.filter(group=group)

    stats = {}

    for match in matches_qs:
        for team_number, players in (
            (1, _pair_player_tuple(match.team1_player1, match.team1_player2)),
            (2, _pair_player_tuple(match.team2_player1, match.team2_player2)),
        ):
            pair_key = (players[0].id, players[1].id)
            row = stats.setdefault(
                pair_key,
                {
                    "player1": players[0],
                    "player2": players[1],
                    "wins": 0,
                    "matches": 0,
                },
            )
            row["matches"] += 1
            if match.winning_team == team_number:
                row["wins"] += 1

    pair_rows = []
    for row in stats.values():
        wins = row["wins"]
        matches = row["matches"]
        losses = matches - wins
        win_rate = (wins / matches) * 100 if matches else 0.0
        pair_rows.append(
            {
                "player1": row["player1"],
                "player2": row["player2"],
                "wins": wins,
                "matches": matches,
                "losses": losses,
                "win_rate": win_rate,
                "pair_sort_name": (
                    row["player1"].name.lower(),
                    row["player2"].name.lower(),
                ),
            }
        )

    return pair_rows


def _apply_competition_positions(rows: list[dict], key_fn) -> list[dict]:
    rows = [row.copy() for row in rows]
    last_key = None
    last_position = None

    for index, row in enumerate(rows, start=1):
        key = key_fn(row)
        if key != last_key:
            row["display_position"] = index
            row["show_position"] = True
            last_key = key
            last_position = index
        else:
            row["display_position"] = last_position
            row["show_position"] = False

    return rows


def build_pairs_ranking_sections(*, group=None) -> dict[str, list[dict]]:
    pair_rows = _build_pair_rows(group=group)

    by_wins = sorted(
        pair_rows,
        key=lambda row: (
            -row["wins"],
            -row["win_rate"],
            -row["matches"],
            row["pair_sort_name"][0],
            row["pair_sort_name"][1],
        ),
    )
    qualified_by_rate = [row for row in pair_rows if row["matches"] >= 5]

    best_rate = sorted(
        qualified_by_rate,
        key=lambda row: (
            -row["win_rate"],
            -row["wins"],
            -row["matches"],
            row["pair_sort_name"][0],
            row["pair_sort_name"][1],
        ),
    )
    worst_rate = sorted(
        qualified_by_rate,
        key=lambda row: (
            row["win_rate"],
            -row["losses"],
            -row["matches"],
            row["pair_sort_name"][0],
            row["pair_sort_name"][1],
        ),
    )
    return {
        "top_pairs": _apply_competition_positions(
            by_wins[:5],
            key_fn=lambda row: (row["wins"], canonical_rounded_win_rate(row["win_rate"]), row["matches"]),
        ),
        "pairs_of_the_century": _apply_competition_positions(
            best_rate[:3],
            key_fn=lambda row: (
                canonical_rounded_win_rate(row["win_rate"]),
                row["wins"],
                row["matches"],
            ),
        ),
        "catastrophic_pairs": _apply_competition_positions(
            worst_rate[:3],
            key_fn=lambda row: (
                canonical_rounded_win_rate(row["win_rate"]),
                row["losses"],
                row["matches"],
            ),
        ),
    }


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


def _normalize_scope(scope: str) -> str:
    return scope if scope in {"all", "male", "female", "mixed"} else "all"


def _population_for_scope(scope: str, population: list[Player]) -> list[Player]:
    from games.models import Player

    if scope == "male":
        return [player for player in population if player.gender == Player.GENDER_MALE]
    if scope == "female":
        return [player for player in population if player.gender == Player.GENDER_FEMALE]
    return list(population)


def _apply_ranking_stats(population: list[Player], stats: dict[int, dict[str, int]]):
    ranked_players: list[Player] = []
    unranked_players: list[Player] = []

    for source_player in population:
        row = stats.get(source_player.id)
        player = copy(source_player)
        if not row or row["matches"] == 0:
            unranked_players.append(player)
            continue

        wins = row["wins"]
        matches = row["matches"]
        win_rate = (wins / matches) * 100 if matches else 0.0

        player.display_wins = wins
        player.display_matches = matches
        player.display_win_rate = win_rate
        ranked_players.append(player)

    ranked_players.sort(
        key=lambda p: (
            canonical_ranking_sort_key(
                wins=p.display_wins,
                win_rate=p.display_win_rate,
                matches=p.display_matches,
                name=p.name,
            )
        )
    )

    apply_competition_ranking_with_ties(
        ranked_players,
        key_fn=lambda p: canonical_ranking_tie_key(
            wins=p.display_wins,
            win_rate=p.display_win_rate,
            matches=p.display_matches,
        ),
    )

    return ranked_players, unranked_players


def compute_rankings_for_scopes(scopes: list[str], *, group=None) -> dict[str, tuple[list[Player], list[Player], str]]:
    """
    Compute multiple ranking scopes from one match scan for the same group.
    """
    from games.models import Match, Player

    requested_scopes = []
    for scope in scopes:
        normalized = _normalize_scope(scope)
        if normalized not in requested_scopes:
            requested_scopes.append(normalized)

    if not requested_scopes:
        return {}

    scope_map = {
        "all": None,
        "male": Match.GENDER_TYPE_MALE,
        "female": Match.GENDER_TYPE_FEMALE,
        "mixed": Match.GENDER_TYPE_MIXED,
    }
    gender_scope_by_type = {
        Match.GENDER_TYPE_MALE: "male",
        Match.GENDER_TYPE_FEMALE: "female",
        Match.GENDER_TYPE_MIXED: "mixed",
    }

    matches_qs = Match.objects.all()
    if group is not None:
        matches_qs = matches_qs.filter(group=group)
    if "all" not in requested_scopes:
        gender_types = [scope_map[scope] for scope in requested_scopes if scope_map[scope]]
        matches_qs = matches_qs.filter(match_gender_type__in=gender_types)

    matches_qs = matches_qs.select_related(
        "team1_player1", "team1_player2", "team2_player1", "team2_player2"
    )

    stats_by_scope: dict[str, dict[int, dict[str, int]]] = {
        scope: {} for scope in requested_scopes
    }

    for match in matches_qs:
        match_scopes = []
        if "all" in stats_by_scope:
            match_scopes.append("all")
        gender_scope = gender_scope_by_type.get(match.match_gender_type)
        if gender_scope in stats_by_scope:
            match_scopes.append(gender_scope)
        if not match_scopes:
            continue

        players = [match.team1_player1, match.team1_player2, match.team2_player1, match.team2_player2]
        winners = [match.team1_player1, match.team1_player2] if match.winning_team == 1 else [
            match.team2_player1,
            match.team2_player2,
        ]
        winner_ids = {winner.id for winner in winners}

        for scope in match_scopes:
            scope_stats = stats_by_scope[scope]
            for player in players:
                row = scope_stats.setdefault(player.id, {"matches": 0, "wins": 0})
                row["matches"] += 1
                if player.id in winner_ids:
                    row["wins"] += 1

    if group:
        population = list(Player.objects.filter(group=group).order_by("name"))
    else:
        population = list(Player.objects.select_related("group").all().order_by("name", "group__name"))

    results = {}
    for scope in requested_scopes:
        ranked_players, unranked_players = _apply_ranking_stats(
            _population_for_scope(scope, population),
            stats_by_scope[scope],
        )
        results[scope] = (ranked_players, unranked_players, scope)
    return results


def compute_ranking(scope: str, *, group=None) -> tuple[list[Player], list[Player], str]:
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
    normalized_scope = _normalize_scope(scope)
    return compute_rankings_for_scopes([normalized_scope], group=group)[normalized_scope]
