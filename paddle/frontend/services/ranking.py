from __future__ import annotations

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


def _build_pair_rows():
    from games.models import Match

    matches_qs = Match.objects.select_related(
        "team1_player1", "team1_player2", "team2_player1", "team2_player2"
    )

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


def build_pairs_ranking_sections() -> dict[str, list[dict]]:
    pair_rows = _build_pair_rows()

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
    qualified_by_rate = [row for row in pair_rows if row["matches"] >= 3]

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
    from games.models import Match, Player

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

    # Canonical ordering policy.
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

    # Canonical tie policy (competition ranking).
    apply_competition_ranking_with_ties(
        ranked_players,
        key_fn=lambda p: canonical_ranking_tie_key(
            wins=p.display_wins,
            win_rate=p.display_win_rate,
            matches=p.display_matches,
        ),
    )

    return ranked_players, unranked_players, scope
