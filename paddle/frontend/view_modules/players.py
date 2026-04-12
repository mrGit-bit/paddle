"""Public players pages and player insights logic.

Responsibilities:
- `/players/` selector page and `/players/<id>/` detail page.
- Player match-query helpers and insights computation (trend/partner/rivals).

Integration:
- Consumes shared helpers from `common.py` and ranking lookup helpers from `ranking.py`.
- Exported through `frontend.views` facade.
"""

from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from games.models import Match, Player

from .common import (
    build_all_players,
    build_player_participation_queryset,
    fetch_paginated_data,
    get_new_match_ids,
    get_request_group_context,
)
from .ranking import get_scoped_player_and_page


def build_player_matches_queryset(player):
    """
    Returns matches where player participates, ordered latest first.
    """
    return build_player_participation_queryset(player).order_by("-date_played")


def _compute_win_rate_percent(wins: int, matches: int) -> int:
    if matches <= 0:
        return 0
    return round((wins / matches) * 100)


def _mark_distinct_trend_progress(trend_rows):
    seen_results = set()
    for row in trend_rows:
        result_key = (row["wins"], row["losses"], row["matches"], row["win_rate_percent"])
        row["show_progress_stroke"] = result_key not in seen_results
        seen_results.add(result_key)
    return trend_rows


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
    color_classes = ["bg-primary", "bg-success", "bg-warning"]
    for index, row in enumerate(partner_rows[:3]):
        distribution_rows.append(
            {
                "label": row["player"].name,
                "player": row["player"],
                "matches": row["matches_together"],
                "color_class": color_classes[index],
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

    results = []
    partner_stats = {}
    rival_stats = {}

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

        results.append(is_win)

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

    def build_trend_row(label: str, slice_size=None):
        scoped_results = results if slice_size is None else results[:slice_size]
        wins = sum(1 for is_win in scoped_results if is_win)
        matches_count = len(scoped_results)
        losses = matches_count - wins
        return {
            "label": label,
            "wins": wins,
            "losses": losses,
            "matches": matches_count,
            "win_rate_percent": _compute_win_rate_percent(wins, matches_count),
        }

    trend_rows = [
        build_trend_row("Últimos 5", slice_size=5),
        build_trend_row("Últimos 10", slice_size=10),
        build_trend_row("Total", slice_size=None),
    ]
    _mark_distinct_trend_progress(trend_rows)

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

    return {
        "trend_rows": trend_rows,
        "top_partners": partner_rows[:3],
        "partner_distribution": _build_partner_distribution(partner_rows),
        "top_rivals": rival_rows[:3],
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

    for row in scope_rows:
        scoped_player, page = get_scoped_player_and_page(
            row["scope"],
            profile_player.id,
            group=profile_player.group,
        )
        row["scoped_player"] = scoped_player
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
            "new_match_ids": [],
            "user_matches": [],
            "new_matches_number": len(new_match_ids),
            "group_display_name": profile_player.group.name if not group_context["aggregate"] else f"{profile_player.group.name} · Hall of Fame",
        },
    )
