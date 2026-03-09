"""Public players pages and player insights logic.

Responsibilities:
- `/players/` selector page and `/players/<id>/` detail page.
- Player match-query helpers and insights computation (trend/partner/rivals).

Integration:
- Consumes shared helpers from `common.py` and ranking lookup helpers from `ranking.py`.
- Exported through `frontend.views` facade.
"""

from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from games.models import Match, Player

from .common import (
    build_all_players,
    build_player_participation_queryset,
    fetch_paginated_data,
    get_new_match_ids,
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


def build_player_insights(player):
    """
    Build trend, top partner and top rivals insights for a player.
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
    top_partner = partner_rows[0] if partner_rows else None

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
        "top_partner": top_partner,
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
    _, _, all_players = build_all_players()
    new_match_ids = get_new_match_ids(request) or []
    return render(
        request,
        "frontend/players.html",
        {
            "all_players": all_players,
            "selected_player_id": None,
            "new_matches_number": len(new_match_ids),
        },
    )


def player_detail_view(request, player_id):
    """
    Public player profile page with scoped stats and match history.
    """
    profile_player = get_object_or_404(Player, id=player_id)
    _, _, all_players = build_all_players()

    scope_rows = [
        {"label": "Todos", "scope": "all", "url_name": "hall_of_fame"},
    ]
    if profile_player.gender == Player.GENDER_MALE:
        scope_rows.append({"label": "Masc.", "scope": "male", "url_name": "ranking_male"})
    elif profile_player.gender == Player.GENDER_FEMALE:
        scope_rows.append({"label": "Fem.", "scope": "female", "url_name": "ranking_female"})
    scope_rows.append({"label": "Mixtos", "scope": "mixed", "url_name": "ranking_mixed"})

    for row in scope_rows:
        scoped_player, page = get_scoped_player_and_page(row["scope"], profile_player.id)
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
        },
    )
