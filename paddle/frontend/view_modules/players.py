"""Public players pages and player insights logic.

Responsibilities:
- `/players/` selector page and `/players/<id>/` detail page.
- Player match-query helpers and insights computation (trend/partner/rivals).

Integration:
- Consumes shared helpers from `common.py` and ranking lookup helpers from `ranking.py`.
- Exported through `frontend.views` facade.
"""

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from games.models import Match, Player
from frontend.services.medals import build_player_medallero_row
from frontend.services.ranking import compute_ranking, compute_rankings_for_scopes

from .common import (
    build_all_players,
    build_player_participation_queryset,
    fetch_paginated_data,
    get_new_match_ids,
    get_request_group_context,
    get_user_player,
)


PARTNER_COLOR_CLASSES = ["bg-primary", "bg-success", "bg-warning"]
PARTNER_PROGRESS_COLOR_CLASSES = [
    "circular-progress-primary",
    "circular-progress-success",
    "circular-progress-warning",
]
NEMESIS_COLOR_CLASSES = [
    "bg-danger bg-opacity-100",
    "bg-danger bg-opacity-50",
    "bg-danger bg-opacity-25",
]
NEMESIS_PROGRESS_COLOR_STYLES = [
    "--progress-stroke: rgba(var(--bs-danger-rgb), 1);",
    "--progress-stroke: rgba(var(--bs-danger-rgb), 0.5);",
    "--progress-stroke: rgba(var(--bs-danger-rgb), 0.25);",
]
VICTIM_COLOR_CLASSES = [
    "bg-success bg-opacity-100",
    "bg-success bg-opacity-50",
    "bg-success bg-opacity-25",
]
VICTIM_PROGRESS_COLOR_STYLES = [
    "--progress-stroke: rgba(var(--bs-success-rgb), 1);",
    "--progress-stroke: rgba(var(--bs-success-rgb), 0.5);",
    "--progress-stroke: rgba(var(--bs-success-rgb), 0.25);",
]
SCOPE_COLOR_CLASSES = PARTNER_COLOR_CLASSES
SCOPE_PROGRESS_COLOR_CLASSES = PARTNER_PROGRESS_COLOR_CLASSES
SCOPE_STYLE_CLASSES = [
    "player-scope-primary",
    "player-scope-success",
    "player-scope-warning",
]
SCOPE_CLASS_BY_KEY = {
    "all": (SCOPE_COLOR_CLASSES[0], SCOPE_PROGRESS_COLOR_CLASSES[0], SCOPE_STYLE_CLASSES[0]),
    "male": (SCOPE_COLOR_CLASSES[1], SCOPE_PROGRESS_COLOR_CLASSES[1], SCOPE_STYLE_CLASSES[1]),
    "female": (SCOPE_COLOR_CLASSES[1], SCOPE_PROGRESS_COLOR_CLASSES[1], SCOPE_STYLE_CLASSES[1]),
    "gender": (SCOPE_COLOR_CLASSES[1], SCOPE_PROGRESS_COLOR_CLASSES[1], SCOPE_STYLE_CLASSES[1]),
    "mixed": (SCOPE_COLOR_CLASSES[2], SCOPE_PROGRESS_COLOR_CLASSES[2], SCOPE_STYLE_CLASSES[2]),
}
MEDAL_SCOPE_URL_NAMES = {
    "all": "hall_of_fame",
    "male": "ranking_male",
    "female": "ranking_female",
    "mixed": "ranking_mixed",
    "pairs": "ranking_pairs",
}


def build_player_matches_queryset(player):
    """
    Returns matches where player participates, ordered latest first.
    """
    return build_player_participation_queryset(player).order_by("-date_played")


def _compute_win_rate_percent(wins: int, matches: int) -> int:
    if matches <= 0:
        return 0
    return round((wins / matches) * 100)


def _add_scope_classes(row: dict, key: str) -> None:
    color_class, progress_color_class, style_class = SCOPE_CLASS_BY_KEY[key]
    row["color_class"] = color_class
    row["progress_color_class"] = progress_color_class
    row["style_class"] = style_class


def _mark_distinct_trend_progress(trend_rows):
    seen_results = set()
    for row in trend_rows:
        if not row.get("is_eligible", True):
            row["show_progress_stroke"] = False
            continue
        result_key = (row["wins"], row["losses"], row["matches"], row["win_rate_percent"])
        row["show_progress_stroke"] = result_key not in seen_results
        seen_results.add(result_key)
    return trend_rows


def _build_ranking_progress_fields(scoped_player, ranking_total: int) -> dict:
    if not scoped_player or ranking_total <= 0:
        return {
            "rank_label": "Sin datos",
            "rank_is_medal": False,
            "ranking_total": 0,
            "progress_percent": 0,
            "support_text": "Sin partidos",
            "record_label": "0🏆/0🏓",
            "progress_aria_label": "Sin partidos de ranking",
        }

    rank = scoped_player.display_position
    medal_map = {
        1: "🥇",
        2: "🥈",
        3: "🥉",
    }
    progress_percent = round(((ranking_total - rank + 1) / ranking_total) * 100)
    progress_percent = max(0, min(100, progress_percent))
    support_text = f"#{rank} de {ranking_total}"

    return {
        "rank_label": medal_map.get(rank, f"#{rank}"),
        "rank_is_medal": rank in medal_map,
        "ranking_total": ranking_total,
        "progress_percent": progress_percent,
        "support_text": support_text,
        "record_label": f"{scoped_player.display_wins}🏆/{scoped_player.display_matches}🏓",
        "progress_aria_label": support_text,
    }


def _add_medallero_card_hrefs(medal_row: dict | None, *, group=None) -> None:
    if not medal_row:
        return
    for medal in medal_row.get("medals", []):
        url_name = MEDAL_SCOPE_URL_NAMES.get(medal["scope"])
        if medal["scope"] == "pairs":
            medal["href"] = reverse(url_name) if url_name else None
            continue
        scoped_player, page, _ = _get_scoped_player_page_and_total(
            medal["scope"],
            medal_row["player"].id,
            group=group,
        )
        medal["href"] = None if not scoped_player or page is None or not url_name else f'{reverse(url_name)}?page={page}#top'


def _get_scoped_player_page_and_total(
    scope: str,
    player_id: int,
    page_size: int = 12,
    *,
    group=None,
    ranking_results=None,
):
    if ranking_results is None:
        ranked_players, _, _ = compute_ranking(scope, group=group)
    else:
        ranked_players, _, _ = ranking_results[scope]
    scoped_player = next((player for player in ranked_players if player.id == player_id), None)
    if not scoped_player:
        return None, None, len(ranked_players)
    ordinal_index = ranked_players.index(scoped_player) + 1
    page = ((ordinal_index - 1) // page_size) + 1
    return scoped_player, page, len(ranked_players)


def _build_efficiency_result_row(label: str, results: list[bool]) -> dict:
    wins = sum(1 for is_win in results if is_win)
    matches_count = len(results)
    losses = matches_count - wins
    return {
        "label": label,
        "wins": wins,
        "losses": losses,
        "matches": matches_count,
        "win_rate_percent": _compute_win_rate_percent(wins, matches_count),
    }


def _build_efficiency_scope(scope_key: str, label: str, match_results: list[dict]) -> dict:
    results = [row["is_win"] for row in match_results]
    selector_row = _build_efficiency_result_row(label, results)
    selector_row["show_progress_stroke"] = selector_row["matches"] > 0
    selector_row["display_value"] = "" if selector_row["matches"] > 0 else "--%"
    selector_row["is_inactive"] = selector_row["matches"] == 0
    selector_row["record_label"] = f"{selector_row['wins']}🏆/{selector_row['matches']}🏓"

    trend_rows = [
        _build_efficiency_result_row("5 últimos", results[:5]),
        _build_efficiency_result_row("10 últimos", results[:10]),
        _build_efficiency_result_row("20 últimos", results[:20]),
    ]
    total_matches = len(results)
    for row, minimum_matches in zip(trend_rows, [1, 6, 11]):
        row["is_eligible"] = total_matches >= minimum_matches
        row["is_inactive"] = not row["is_eligible"]
        row["display_value"] = "" if row["is_eligible"] else "--%"
    _mark_distinct_trend_progress(trend_rows)
    for row in trend_rows:
        row["record_label"] = f"{row['wins']}🏆/{row['matches']}🏓"

    return {
        "key": scope_key,
        "label": label,
        "selector": selector_row,
        "trend_rows": trend_rows,
    }


def _build_efficiency_scopes(player, match_results: list[dict]) -> list[dict]:
    from games.models import Match

    if player.gender == Player.GENDER_MALE:
        gender_label = "Masc."
        gender_type = Match.GENDER_TYPE_MALE
    elif player.gender == Player.GENDER_FEMALE:
        gender_label = "Fem."
        gender_type = Match.GENDER_TYPE_FEMALE
    else:
        gender_label = "Categoría"
        gender_type = None

    gender_results = (
        [row for row in match_results if row["match_gender_type"] == gender_type]
        if gender_type
        else []
    )

    scopes = [
        _build_efficiency_scope("all", "Todos", match_results),
        _build_efficiency_scope("gender", gender_label, gender_results),
        _build_efficiency_scope(
            "mixed",
            "Mixtos",
            [row for row in match_results if row["match_gender_type"] == Match.GENDER_TYPE_MIXED],
        ),
    ]
    for scope in scopes:
        _add_scope_classes(scope, scope["key"])
    return scopes


def _format_recent_form_balance_label(balance: int) -> str:
    if balance >= 5:
        return "Balance excelente"
    if balance >= 3:
        return "Balance muy positivo"
    if balance >= 1:
        return "Balance positivo"
    if balance == 0:
        return "Balance neutro"
    if balance <= -5:
        return "Balance crítico"
    if balance <= -3:
        return "Balance muy negativo"
    return "Balance negativo"


def _get_recent_form_summary_color_class(balance: int) -> str:
    if balance > 0:
        return "bg-success"
    if balance < 0:
        return "bg-danger"
    return "bg-secondary"


def _build_recent_form_chart(match_results: list[dict]) -> dict:
    recent_results = list(reversed(match_results[:10]))
    points = [{"x": 0, "y": 0}]
    cumulative_balance = 0
    wins = 0
    losses = 0

    for index, row in enumerate(recent_results, start=1):
        if row["is_win"]:
            cumulative_balance += 1
            wins += 1
        else:
            cumulative_balance -= 1
            losses += 1
        points.append({"x": index, "y": cumulative_balance})

    match_count = len(recent_results)
    axis_limit = max(1, max(abs(point["y"]) for point in points))
    balance_label = f"{cumulative_balance:+d}" if cumulative_balance else "0"
    return {
        "x_axis_min": 0,
        "x_axis_max": 10,
        "y_axis_min": -axis_limit,
        "y_axis_max": axis_limit,
        "match_count": match_count,
        "wins": wins,
        "losses": losses,
        "balance": cumulative_balance,
        "record_label": _format_recent_form_balance_label(cumulative_balance),
        "empty_label": "Sin partidos",
        "aria_label": (
            f"Últimos partidos: balance {balance_label} en {match_count} partidos"
        ),
        "points": points,
    }


def _compute_display_percents(rows, total_matches):
    if total_matches <= 0:
        return []

    percent_rows = []
    floor_total = 0
    for index, row in enumerate(rows):
        exact_percent = (row["matches"] / total_matches) * 100
        display_percent = int(exact_percent)
        floor_total += display_percent
        percent_rows.append(
            {
                "index": index,
                "display_percent": display_percent,
                "remainder": exact_percent - display_percent,
            }
        )

    points_to_assign = 100 - floor_total
    percent_rows.sort(key=lambda row: (-row["remainder"], row["index"]))
    for row in percent_rows[:points_to_assign]:
        row["display_percent"] += 1

    percent_rows.sort(key=lambda row: row["index"])
    return [row["display_percent"] for row in percent_rows]


def _format_css_percent(value):
    return f"{value:.4f}".rstrip("0").rstrip(".")


def _build_partner_distribution(partner_rows):
    total_matches = sum(row["matches_together"] for row in partner_rows)
    if total_matches <= 0:
        return []

    distribution_rows = []
    for index, row in enumerate(partner_rows[:3]):
        distribution_rows.append(
            {
                "label": row["player"].name,
                "player": row["player"],
                "matches": row["matches_together"],
                "color_class": PARTNER_COLOR_CLASSES[index],
                "is_empty_segment": False,
            }
        )

    other_matches = sum(row["matches_together"] for row in partner_rows[3:])
    if other_matches:
        distribution_rows.append(
            {
                "label": "Otros",
                "player": None,
                "matches": other_matches,
                "color_class": "",
                "is_empty_segment": True,
            }
        )

    display_percents = _compute_display_percents(distribution_rows, total_matches)
    for row, display_percent in zip(distribution_rows, display_percents):
        row["display_percent"] = display_percent
        row["width_percent"] = _format_css_percent((row["matches"] / total_matches) * 100)
        row["show_label"] = display_percent >= 10
        row["aria_label"] = f"{row['label']}: {display_percent}% de partidos"

    return distribution_rows


def _build_partner_efficiency_cards(partner_rows):
    if not partner_rows:
        return []

    card_rows = []
    for index in range(3):
        if index < len(partner_rows):
            row = partner_rows[index]
            label = row["player"].name
            card_rows.append(
                {
                    "label": label,
                    "player": row["player"],
                    "color_class": PARTNER_COLOR_CLASSES[index],
                    "progress_color_class": PARTNER_PROGRESS_COLOR_CLASSES[index],
                    "win_rate_percent": row["win_rate_percent"],
                    "display_value": "",
                    "record_label": f"{row['wins_together']}🏆/{row['matches_together']}🏓",
                    "show_progress_stroke": row["matches_together"] > 0,
                    "is_placeholder": False,
                    "is_inactive": False,
                    "aria_label": f"Efectividad con {label}: {row['win_rate_percent']}%",
                }
            )
        else:
            card_rows.append(
                {
                    "label": "Sin datos",
                    "player": None,
                    "color_class": "",
                    "progress_color_class": "",
                    "win_rate_percent": 0,
                    "display_value": "--%",
                    "record_label": "0🏆/0🏓",
                    "show_progress_stroke": False,
                    "is_placeholder": True,
                    "is_inactive": True,
                    "aria_label": "Efectividad sin datos: sin porcentaje",
                }
            )

    return card_rows


def _build_pair_label(player1, player2):
    return f"{player1.name} / {player2.name}"


def _build_rival_distribution(rival_rows):
    total_matches = sum(row["encounters"] for row in rival_rows)
    if total_matches <= 0:
        return []

    distribution_rows = []
    for index, row in enumerate(rival_rows[:3]):
        distribution_rows.append(
            {
                "label": _build_pair_label(row["player1"], row["player2"]),
                "player1": row["player1"],
                "player2": row["player2"],
                "matches": row["encounters"],
                "color_class": PARTNER_COLOR_CLASSES[index],
                "is_empty_segment": False,
            }
        )

    other_matches = sum(row["encounters"] for row in rival_rows[3:])
    if other_matches:
        distribution_rows.append(
            {
                "label": "Otros",
                "player1": None,
                "player2": None,
                "matches": other_matches,
                "color_class": "",
                "is_empty_segment": True,
            }
        )

    display_percents = _compute_display_percents(distribution_rows, total_matches)
    for row, display_percent in zip(distribution_rows, display_percents):
        row["display_percent"] = display_percent
        row["width_percent"] = _format_css_percent((row["matches"] / total_matches) * 100)
        row["show_label"] = display_percent >= 10
        row["aria_label"] = f"{row['label']}: {display_percent}% de partidos ante rivales"

    return distribution_rows


def _build_rival_efficiency_cards(rival_rows):
    if not rival_rows:
        return _build_empty_insight_cards("Efectividad sin datos: sin porcentaje")

    card_rows = []
    for index, row in enumerate(rival_rows[:3]):
        label = _build_pair_label(row["player1"], row["player2"])
        card_rows.append(
            {
                "label": label,
                "player1": row["player1"],
                "player2": row["player2"],
                "color_class": PARTNER_COLOR_CLASSES[index],
                "progress_color_class": PARTNER_PROGRESS_COLOR_CLASSES[index],
                "win_rate_percent": row["win_rate_percent"],
                "display_value": "",
                "record_label": f"{row['wins_vs_pair']}🏆/{row['encounters']}🏓",
                "show_progress_stroke": row["encounters"] > 0,
                "aria_label": f"Efectividad ante {label}: {row['win_rate_percent']}%",
            }
        )
    return card_rows


def _build_empty_insight_cards(aria_label):
    return [
        {
            "label": "Sin datos",
            "player": None,
            "player1": None,
            "player2": None,
            "color_class": "",
            "progress_color_class": "",
            "progress_color_style": "",
            "win_rate_percent": 0,
            "display_value": "--%",
            "record_label": "0🏆/0🏓",
            "show_progress_stroke": False,
            "is_placeholder": True,
            "is_inactive": True,
            "aria_label": aria_label,
        }
        for _ in range(3)
    ]


def _build_head_to_head_cards(opponent_rows, mode):
    if not opponent_rows:
        return _build_empty_insight_cards("Efectividad sin datos: sin porcentaje")

    card_rows = []
    is_nemesis = mode == "nemesis"
    color_classes = NEMESIS_COLOR_CLASSES if is_nemesis else VICTIM_COLOR_CLASSES
    progress_color_styles = (
        NEMESIS_PROGRESS_COLOR_STYLES if is_nemesis else VICTIM_PROGRESS_COLOR_STYLES
    )
    for index, row in enumerate(opponent_rows[:3]):
        label = row["player"].name
        win_rate_percent = (
            row["opponent_win_rate_percent"] if is_nemesis else row["player_win_rate_percent"]
        )
        record_label = (
            f"{row['opponent_wins']}🌴/{row['player_wins']}🏆"
            if is_nemesis
            else f"{row['player_wins']}🏆/{row['opponent_wins']}🌴"
        )
        aria_prefix = "Derrotas ante" if is_nemesis else "Victorias ante"
        card_rows.append(
            {
                "label": label,
                "player": row["player"],
                "matches_against": row["matches_against"],
                "player_wins": row["player_wins"],
                "opponent_wins": row["opponent_wins"],
                "player_win_rate_percent": row["player_win_rate_percent"],
                "opponent_win_rate_percent": row["opponent_win_rate_percent"],
                "color_class": color_classes[index],
                "progress_color_class": "",
                "progress_color_style": progress_color_styles[index],
                "win_rate_percent": win_rate_percent,
                "display_value": "",
                "record_label": record_label,
                "show_progress_stroke": row["matches_against"] > 0,
                "aria_label": f"{aria_prefix} {label}: {win_rate_percent}%",
            }
        )
    return card_rows


def _filter_summary_cards(card_rows):
    return [row for row in card_rows if row and not row.get("is_placeholder")]


def _first_summary_card(card_rows):
    return next(iter(_filter_summary_cards(card_rows)), None)


def _build_name_summary_badges(card_rows, empty_label="Sin datos"):
    summary_rows = [
        {
            "label": row["label"],
            "color_class": row.get("color_class") or "bg-secondary",
            "text_class": "text-dark" if row.get("color_class") == "bg-warning" else "",
        }
        for row in _filter_summary_cards(card_rows)
    ]
    if summary_rows:
        return summary_rows
    return [{"label": empty_label, "color_class": "bg-secondary", "text_class": ""}]


def _build_contender_summary_badges(nemesis_cards, victim_cards):
    summary_rows = []
    for row in [_first_summary_card(nemesis_cards)]:
        if not row:
            continue
        summary_rows.append(
            {
                "label": row["label"],
                "color_class": row.get("color_class") or "bg-danger",
                "text_class": "",
            }
        )
    for row in [_first_summary_card(victim_cards)]:
        if not row:
            continue
        summary_rows.append(
            {
                "label": row["label"],
                "color_class": row.get("color_class") or "bg-success",
                "text_class": "",
            }
        )
    if summary_rows:
        return summary_rows
    return [{"label": "Sin datos", "color_class": "bg-secondary", "text_class": ""}]


def _build_ranking_summary_badges(scope_rows, efficiency_scopes):
    efficiency_by_key = {
        ("gender" if scope["key"] in {"male", "female"} else scope["key"]): scope
        for scope in efficiency_scopes
    }
    summary_rows = []
    for row in scope_rows:
        if not row.get("scoped_player") or row.get("ranking_total", 0) <= 0:
            continue
        efficiency_key = "gender" if row["scope"] in {"male", "female"} else row["scope"]
        efficiency = efficiency_by_key.get(efficiency_key)
        if efficiency and efficiency["selector"]["matches"] > 0:
            efficiency_label = f"{efficiency['selector']['win_rate_percent']}%"
        else:
            efficiency_label = "--%"
        position_label = (
            str(row["scoped_player"].display_position)
            if row.get("scoped_player")
            else "--"
        )
        summary_rows.append(
            {
                "label": row["label"],
                "value": f"{position_label}/{efficiency_label}",
                "color_class": row["color_class"],
                "text_class": "text-dark" if row["color_class"] == "bg-warning" else "",
            }
        )
    return summary_rows


def _build_player_stats_summary(scope_rows, player_insights):
    recent_form_chart = player_insights["recent_form_chart"]
    return {
        "rankings": _build_ranking_summary_badges(
            scope_rows,
            player_insights["efficiency_scopes"],
        ),
        "recent_form": [
            {
                "label": recent_form_chart["record_label"],
                "color_class": _get_recent_form_summary_color_class(
                    recent_form_chart["balance"],
                ),
                "text_class": "",
            }
        ],
        "partners": _build_name_summary_badges(
            [_first_summary_card(player_insights["partner_efficiency_cards"])]
        ),
        "rivals": _build_name_summary_badges(
            [_first_summary_card(player_insights["rival_efficiency_cards"])]
        ),
        "contenders": _build_contender_summary_badges(
            player_insights["nemesis_cards"],
            player_insights["victim_cards"],
        ),
    }


def build_player_insights(player):
    """
    Build trend, top partners and top rivals insights for a player.
    """
    matches = list(
        build_player_matches_queryset(player).select_related(
            "team1_player1",
            "team1_player2",
            "team2_player1",
            "team2_player2",
        )
    )

    match_results = []
    partner_stats = {}
    rival_stats = {}
    opponent_stats = {}

    for match in matches:
        if match.team1_player1_id == player.id:
            teammate = match.team1_player2
            rivals = (match.team2_player1, match.team2_player2)
            is_win = match.winning_team == 1
        elif match.team1_player2_id == player.id:
            teammate = match.team1_player1
            rivals = (match.team2_player1, match.team2_player2)
            is_win = match.winning_team == 1
        elif match.team2_player1_id == player.id:
            teammate = match.team2_player2
            rivals = (match.team1_player1, match.team1_player2)
            is_win = match.winning_team == 2
        else:
            teammate = match.team2_player1
            rivals = (match.team1_player1, match.team1_player2)
            is_win = match.winning_team == 2

        match_results.append(
            {
                "is_win": is_win,
                "match_gender_type": match.match_gender_type,
            }
        )

        partner_row = partner_stats.setdefault(
            teammate.id,
            {
                "player": teammate,
                "matches_together": 0,
                "wins_together": 0,
                "last_date": match.date_played,
            },
        )
        partner_row["matches_together"] += 1
        partner_row["wins_together"] += 1 if is_win else 0
        if match.date_played > partner_row["last_date"]:
            partner_row["last_date"] = match.date_played

        rival_pair = tuple(sorted((rivals[0].id, rivals[1].id)))
        rival_row = rival_stats.setdefault(
            rival_pair,
            {
                "players_by_id": tuple(sorted(rivals, key=lambda p: p.id)),
                "encounters": 0,
                "wins_vs_pair": 0,
                "last_date": match.date_played,
            },
        )
        rival_row["encounters"] += 1
        rival_row["wins_vs_pair"] += 1 if is_win else 0
        if match.date_played > rival_row["last_date"]:
            rival_row["last_date"] = match.date_played

        for opponent in rivals:
            opponent_row = opponent_stats.setdefault(
                opponent.id,
                {
                    "player": opponent,
                    "matches_against": 0,
                    "player_wins": 0,
                    "opponent_wins": 0,
                    "last_date": match.date_played,
                },
            )
            opponent_row["matches_against"] += 1
            opponent_row["player_wins"] += 1 if is_win else 0
            opponent_row["opponent_wins"] += 0 if is_win else 1
            if match.date_played > opponent_row["last_date"]:
                opponent_row["last_date"] = match.date_played

    efficiency_scopes = _build_efficiency_scopes(player, match_results)
    trend_rows = efficiency_scopes[0]["trend_rows"]

    partner_rows = []
    for row in partner_stats.values():
        matches_together = row["matches_together"]
        wins_together = row["wins_together"]
        losses_together = matches_together - wins_together
        partner_rows.append(
            {
                "player": row["player"],
                "matches_together": matches_together,
                "wins_together": wins_together,
                "losses_together": losses_together,
                "win_rate_percent": _compute_win_rate_percent(wins_together, matches_together),
                "win_rate_value": (wins_together / matches_together) if matches_together else 0.0,
                "last_date": row["last_date"],
            }
        )

    partner_rows.sort(
        key=lambda row: (
            -row["matches_together"],
            -row["win_rate_value"],
            -row["last_date"].toordinal(),
            row["player"].id,
        )
    )
    rival_rows = []
    for rival_pair, row in rival_stats.items():
        encounters = row["encounters"]
        wins_vs_pair = row["wins_vs_pair"]
        losses_vs_pair = encounters - wins_vs_pair
        rival_rows.append(
            {
                "player1": row["players_by_id"][0],
                "player2": row["players_by_id"][1],
                "pair_ids": rival_pair,
                "encounters": encounters,
                "wins_vs_pair": wins_vs_pair,
                "losses_vs_pair": losses_vs_pair,
                "win_rate_percent": _compute_win_rate_percent(wins_vs_pair, encounters),
                "win_rate_value": (wins_vs_pair / encounters) if encounters else 0.0,
                "last_date": row["last_date"],
            }
        )

    rival_rows.sort(
        key=lambda row: (
            -row["encounters"],
            -row["win_rate_value"],
            -row["last_date"].toordinal(),
            row["pair_ids"][0],
            row["pair_ids"][1],
        )
    )

    opponent_rows = []
    for row in opponent_stats.values():
        matches_against = row["matches_against"]
        player_wins = row["player_wins"]
        opponent_wins = row["opponent_wins"]
        opponent_rows.append(
            {
                "player": row["player"],
                "matches_against": matches_against,
                "player_wins": player_wins,
                "opponent_wins": opponent_wins,
                "player_win_rate_percent": _compute_win_rate_percent(player_wins, matches_against),
                "opponent_win_rate_percent": _compute_win_rate_percent(
                    opponent_wins,
                    matches_against,
                ),
                "player_win_rate_value": (player_wins / matches_against) if matches_against else 0.0,
                "opponent_win_rate_value": (
                    opponent_wins / matches_against
                ) if matches_against else 0.0,
                "last_date": row["last_date"],
            }
        )

    nemesis_rows = [
        row
        for row in opponent_rows
        if row["matches_against"] >= 5 and row["opponent_win_rate_value"] > 0.6
    ]
    nemesis_rows.sort(
        key=lambda row: (
            -row["opponent_wins"],
            -row["opponent_win_rate_value"],
            -row["last_date"].toordinal(),
            row["player"].id,
        )
    )
    victim_rows = [
        row
        for row in opponent_rows
        if row["matches_against"] >= 5 and row["player_win_rate_value"] > 0.6
    ]
    victim_rows.sort(
        key=lambda row: (
            -row["player_wins"],
            -row["player_win_rate_value"],
            -row["last_date"].toordinal(),
            row["player"].id,
        )
    )

    return {
        "efficiency_scopes": efficiency_scopes,
        "recent_form_chart": _build_recent_form_chart(match_results),
        "trend_rows": trend_rows,
        "top_partners": partner_rows[:3],
        "partner_distribution": _build_partner_distribution(partner_rows),
        "partner_efficiency_cards": _build_partner_efficiency_cards(partner_rows),
        "rival_distribution": _build_rival_distribution(rival_rows),
        "rival_efficiency_cards": _build_rival_efficiency_cards(rival_rows),
        "top_rivals": rival_rows[:3],
        "nemesis_cards": _build_head_to_head_cards(nemesis_rows, "nemesis"),
        "victim_cards": _build_head_to_head_cards(victim_rows, "victim"),
    }


def process_matches_plain(matches):
    """
    Processes matches without current-user highlighting (public pages).
    """
    from datetime import datetime

    for match in matches:
        for key in ["team1_player1", "team1_player2", "team2_player1", "team2_player2"]:
            player = getattr(match, key)
            setattr(match, f"{key}_display", player.name if player else "")
        if isinstance(getattr(match, "date_played", None), str):
            match.date_played = datetime.strptime(match.date_played, "%Y-%m-%d").date()
    return matches


def players_view(request):
    """
    Public players landing page with selector.
    """
    user_player = get_user_player(request)
    if user_player:
        return redirect("player_detail", player_id=user_player.id)

    group_context = get_request_group_context(request)
    _, _, all_players = build_all_players(
        group=group_context["group"],
        include_group_labels=False,
    )
    new_match_ids = get_new_match_ids(request) or []
    return render(
        request,
        "frontend/players.html",
        {
            "all_players": all_players,
            "selected_player_id": None,
            "new_matches_number": len(new_match_ids),
            "group_display_name": group_context["display_name"],
        },
    )


def player_detail_view(request, player_id):
    """
    Public player profile page with scoped stats and match history.
    """
    profile_player = get_object_or_404(Player, id=player_id)
    group_context = get_request_group_context(request)
    if group_context["group"] is not None and profile_player.group_id != group_context["group"].id:
        raise Http404("Jugador no encontrado.")

    _, _, all_players = build_all_players(
        group=group_context["group"],
        include_group_labels=False,
    )

    scope_rows = [
        {"label": "Todos", "scope": "all", "url_name": "hall_of_fame"},
    ]
    if profile_player.gender == Player.GENDER_MALE:
        scope_rows.append({"label": "Masc.", "scope": "male", "url_name": "ranking_male"})
    elif profile_player.gender == Player.GENDER_FEMALE:
        scope_rows.append({"label": "Fem.", "scope": "female", "url_name": "ranking_female"})
    scope_rows.append({"label": "Mixtos", "scope": "mixed", "url_name": "ranking_mixed"})

    ranking_results = compute_rankings_for_scopes(
        [row["scope"] for row in scope_rows],
        group=profile_player.group,
    )

    for row in scope_rows:
        _add_scope_classes(row, row["scope"])
        scoped_player, page, ranking_total = _get_scoped_player_page_and_total(
            row["scope"],
            profile_player.id,
            group=profile_player.group,
            ranking_results=ranking_results,
        )
        row["scoped_player"] = scoped_player
        row.update(_build_ranking_progress_fields(scoped_player, ranking_total))
        if not scoped_player:
            row["href"] = None
            continue
        if page is None:
            row["href"] = None
            continue
        row["href"] = f'{reverse(row["url_name"])}?page={page}#top'

    profile_matches_qs = build_player_matches_queryset(profile_player)
    profile_matches, profile_pagination = fetch_paginated_data(profile_matches_qs, request)
    profile_matches = process_matches_plain(profile_matches)
    player_insights = build_player_insights(profile_player)
    player_stats_summary = _build_player_stats_summary(scope_rows, player_insights)
    profile_medal_row = build_player_medallero_row(profile_player, group=profile_player.group)
    _add_medallero_card_hrefs(profile_medal_row, group=profile_player.group)

    new_match_ids = get_new_match_ids(request) or []
    return render(
        request,
        "frontend/player_detail.html",
        {
            "profile_player": profile_player,
            "all_players": all_players,
            "selected_player_id": profile_player.id,
            "scope_rows": scope_rows,
            "profile_matches": profile_matches,
            "profile_pagination": profile_pagination,
            "player_insights": player_insights,
            "player_stats_summary": player_stats_summary,
            "profile_medal_row": profile_medal_row,
            "new_match_ids": [],
            "user_matches": [],
            "new_matches_number": len(new_match_ids),
            "group_display_name": profile_player.group.name if not group_context["aggregate"] else f"{profile_player.group.name} · Hall of Fame",
        },
    )
