from __future__ import annotations

from frontend.medals.config import MEDAL_DEFINITIONS, SCOPE_CONFIG
from frontend.services.ranking import canonical_rounded_win_rate, compute_rankings_for_scopes

MEDAL_BY_KEY = {medal["key"]: medal for medal in MEDAL_DEFINITIONS}
MEDAL_SCOPE_KEYS = list(SCOPE_CONFIG.keys())
TOP_PAGE_POSITION = 12


def _medal_instance(medal_key: str, scope: str) -> dict:
    medal = MEDAL_BY_KEY[medal_key]
    scope_config = SCOPE_CONFIG[scope]
    return {
        "key": medal["key"],
        "name": medal["name"],
        "icon": medal["icon"],
        "description": medal["description"],
        "category": medal["category"],
        "order": medal["order"],
        "scope": scope,
        "scope_label": scope_config["label"],
        "scope_css_class": scope_config["css_class"],
        "progress_color_class": scope_config["progress_color_class"],
    }


def _ensure_player_row(players_by_id: dict[int, dict], player) -> dict:
    row = players_by_id.setdefault(
        player.id,
        {
            "player": player,
            "medals": [],
            "total_medals": 0,
            "first_place_medals": 0,
            "position_medals": 0,
            "performance_medals": 0,
            "medal_rows": [],
        },
    )
    return row


def _award(players_by_id: dict[int, dict], player, medal_key: str, scope: str) -> None:
    row = _ensure_player_row(players_by_id, player)
    medal = _medal_instance(medal_key, scope)
    row["medals"].append(medal)
    row["total_medals"] += 1
    if medal_key == "first_place":
        row["first_place_medals"] += 1
    if medal["category"] == "position":
        row["position_medals"] += 1
    if medal["category"] == "performance":
        row["performance_medals"] += 1


def _players_at_or_above_third_metric_row(players: list, metric_fn) -> list:
    if not players:
        return []
    sorted_players = sorted(
        players,
        key=lambda player: (-metric_fn(player), player.name.lower(), player.id),
    )
    cutoff_index = min(2, len(sorted_players) - 1)
    cutoff_value = metric_fn(sorted_players[cutoff_index])
    return [player for player in sorted_players if metric_fn(player) >= cutoff_value]


def _pad_medal_rows(medals: list[dict]) -> list[list[dict | None]]:
    rows = []
    for index in range(0, len(medals), 3):
        row = medals[index:index + 3]
        rows.append(row + [None] * (3 - len(row)))
    return rows


def _finalize_rows(players_by_id: dict[int, dict]) -> list[dict]:
    rows = list(players_by_id.values())
    for row in rows:
        row["medals"].sort(key=lambda medal: (medal["order"], medal["scope"]))
        row["medal_rows"] = _pad_medal_rows(row["medals"])

    rows.sort(
        key=lambda row: (
            -row["total_medals"],
            -row["first_place_medals"],
            -row["position_medals"],
            -row["performance_medals"],
            row["player"].name.lower(),
            row["player"].id,
        )
    )
    return rows


def build_medallero_rows(*, group=None) -> list[dict]:
    ranking_results = compute_rankings_for_scopes(MEDAL_SCOPE_KEYS, group=group)
    players_by_id: dict[int, dict] = {}

    for scope in MEDAL_SCOPE_KEYS:
        ranked_players, _, _ = ranking_results[scope]
        eligible_players = [
            player for player in ranked_players
            if getattr(player, "display_position", None) is not None
            and player.display_position <= TOP_PAGE_POSITION
        ]

        for player in eligible_players:
            _award(players_by_id, player, "cuadro_honor", scope)
            if player.display_position == 1:
                _award(players_by_id, player, "first_place", scope)
            if player.display_position == 2:
                _award(players_by_id, player, "second_place", scope)
            if player.display_position == 3:
                _award(players_by_id, player, "third_place", scope)

        for player in _players_at_or_above_third_metric_row(
            eligible_players,
            lambda ranked_player: canonical_rounded_win_rate(ranked_player.display_win_rate),
        ):
            _award(players_by_id, player, "top3_efficiency", scope)

        for player in _players_at_or_above_third_metric_row(
            eligible_players,
            lambda ranked_player: ranked_player.display_matches,
        ):
            _award(players_by_id, player, "top3_matches", scope)

    return _finalize_rows(players_by_id)


def build_player_medallero_row(player, *, group=None) -> dict | None:
    for row in build_medallero_rows(group=group):
        if row["player"].id == player.id:
            return row
    return None
