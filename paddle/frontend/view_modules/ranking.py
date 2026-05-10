"""Ranking domain views and helpers.

Responsibilities:
- Ranking home redirect and hall of fame wrapper.
- Scoped ranking page rendering and scoped-player pagination helpers.

Integration:
- Uses ranking service (`frontend.services.ranking`) and shared helpers from `common.py`.
- Exported to URLconf through `frontend.views` facade.
"""

from django.shortcuts import render
from django.urls import reverse

from games.models import Player

from frontend.services.medals import build_medallero_rows
from frontend.services.ranking import build_pairs_ranking_sections, compute_ranking

from .common import get_new_match_ids, get_ranking_redirect, get_request_group_context, get_user_player, paginate_list


MEDAL_SCOPE_URL_NAMES = {
    "all": "hall_of_fame",
    "male": "ranking_male",
    "female": "ranking_female",
    "mixed": "ranking_mixed",
}


def _add_medallero_card_hrefs(rows: list[dict], *, group=None) -> None:
    for row in rows:
        player = row["player"]
        for medal in row.get("medals", []):
            page = get_player_page_in_scope(medal["scope"], player.id, group=group)
            url_name = MEDAL_SCOPE_URL_NAMES.get(medal["scope"])
            medal["href"] = None if page is None or not url_name else f'{reverse(url_name)}?page={page}#top'


def ranking_home_view(request):
    """
    Redirects to the last visited ranking scope.
    """
    scope = request.session.get("last_ranking_scope", "all")
    return get_ranking_redirect(scope)


def hall_of_fame_view(request):
    """Wrapper to avoid changing URLs."""
    return ranking_view(request, scope="all")


def ranking_view(request, scope):
    """
    Renders scoped ranking pages: all/male/female/mixed.
    """
    group_context = get_request_group_context(request)
    ranked_players, unranked_players, scope = compute_ranking(scope, group=group_context["group"])

    request.session["last_ranking_scope"] = scope

    players, pagination = paginate_list(ranked_players, request, page_size=12)

    new_match_ids = get_new_match_ids(request) or []
    new_matches_number = len(new_match_ids)

    user_page = None
    user_player = None
    previous_player = None
    following_player = None

    if request.user.is_authenticated:
        db_user_player = get_user_player(request)

        if db_user_player:
            scoped_user_player = next((p for p in ranked_players if p.id == db_user_player.id), None)

            if scoped_user_player:
                user_player = scoped_user_player
                ordinal_index = ranked_players.index(user_player) + 1

                current_page = int(request.GET.get("page", 1))
                user_page = ((ordinal_index - 1) // 12) + 1

                if user_page != current_page:
                    previous_player = ranked_players[ordinal_index - 2] if ordinal_index > 1 else None
                    following_player = (
                        ranked_players[ordinal_index] if ordinal_index < len(ranked_players) else None
                    )

    titles = {
        "all": f'{group_context["display_name"]} — Todos los partidos',
        "male": f'{group_context["display_name"]} — Partidos masculinos',
        "female": f'{group_context["display_name"]} — Partidos femeninos',
        "mixed": f'{group_context["display_name"]} — Partidos mixtos',
    }

    return render(
        request,
        "frontend/hall_of_fame.html",
        {
            "players": players,
            "pagination": pagination,
            "unranked_players": unranked_players,
            "new_matches_number": new_matches_number,
            "user_page": user_page,
            "user_player": user_player,
            "previous_player": previous_player,
            "following_player": following_player,
            "ranking_scope": scope,
            "page_title": titles.get(scope, titles["all"]),
            "group_display_name": group_context["display_name"],
            "is_aggregate_context": group_context["aggregate"],
        },
    )


def pairs_ranking_view(request):
    """
    Renders the all-matches pairs ranking page.
    """
    group_context = get_request_group_context(request)
    sections = build_pairs_ranking_sections(group=group_context["group"])
    new_match_ids = get_new_match_ids(request) or []

    return render(
        request,
        "frontend/pairs_ranking.html",
        {
            "top_pairs": sections["top_pairs"],
            "pairs_of_the_century": sections["pairs_of_the_century"],
            "catastrophic_pairs": sections["catastrophic_pairs"],
            "new_matches_number": len(new_match_ids),
            "page_title": "Parejas",
            "group_display_name": group_context["display_name"],
            "is_aggregate_context": group_context["aggregate"],
        },
    )


def medallero_view(request):
    """
    Renders the public medal board for the current ranking group context.
    """
    group_context = get_request_group_context(request)
    new_match_ids = get_new_match_ids(request) or []

    medallero_rows = build_medallero_rows(group=group_context["group"])
    _add_medallero_card_hrefs(medallero_rows, group=group_context["group"])

    return render(
        request,
        "frontend/medallero.html",
        {
            "medallero_rows": medallero_rows,
            "new_matches_number": len(new_match_ids),
            "page_title": "Medallero",
            "group_display_name": group_context["display_name"],
            "is_aggregate_context": group_context["aggregate"],
        },
    )


def get_scoped_player_row(scope: str, player_id: int, *, group=None):
    """
    Returns the scoped ranked player object with display_* fields or None.
    """
    ranked_players, _, _ = compute_ranking(scope, group=group)
    return next((player for player in ranked_players if player.id == player_id), None)


def get_player_page_in_scope(scope: str, player_id: int, page_size: int = 12, *, group=None):
    """
    Returns the pagination page number where player_id appears for a ranking scope.
    """
    ranked_players, _, _ = compute_ranking(scope, group=group)
    scoped_player = next((p for p in ranked_players if p.id == player_id), None)
    if not scoped_player:
        return None
    ordinal_index = ranked_players.index(scoped_player) + 1
    return ((ordinal_index - 1) // page_size) + 1


def get_scoped_player_and_page(scope: str, player_id: int, page_size: int = 12, *, group=None):
    """
    Returns (scoped_player, page) from a single ranking computation.
    """
    ranked_players, _, _ = compute_ranking(scope, group=group)
    scoped_player = next((p for p in ranked_players if p.id == player_id), None)
    if not scoped_player:
        return None, None
    ordinal_index = ranked_players.index(scoped_player) + 1
    page = ((ordinal_index - 1) // page_size) + 1
    return scoped_player, page
