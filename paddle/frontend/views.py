# Absolute path: /workspaces/paddle/paddle/frontend/views.py
# Responsibility: compatibility facade.
# How it works:
# - Keeps the public `frontend.views` import path stable for urls/tests.
# - Re-exports callables implemented in `frontend.view_modules.*`.
# - Must remain thin (no business logic) so module boundaries stay clear.

from .view_modules.auth_profile import (
    about_view,
    login_view,
    logout_view,
    register_view,
    user_delete_view,
    user_view,
)
from .view_modules.common import (
    EmailExistsPasswordResetForm,
    build_all_players,
    fetch_available_players,
    fetch_paginated_data,
    get_about_app_version_label,
    get_new_match_ids,
    get_player_stats,
    get_ranking_redirect,
    paginate_list,
)
from .view_modules.matches import match_view, process_matches
from .view_modules.players import (
    _compute_win_rate_percent,
    build_player_insights,
    build_player_matches_queryset,
    player_detail_view,
    players_view,
    process_matches_plain,
)
from .view_modules.ranking import (
    get_player_page_in_scope,
    get_scoped_player_and_page,
    get_scoped_player_row,
    hall_of_fame_view,
    pairs_ranking_view,
    ranking_home_view,
    ranking_view,
)

__all__ = [
    "EmailExistsPasswordResetForm",
    "_compute_win_rate_percent",
    "about_view",
    "build_all_players",
    "build_player_insights",
    "build_player_matches_queryset",
    "fetch_available_players",
    "fetch_paginated_data",
    "get_about_app_version_label",
    "get_new_match_ids",
    "get_player_page_in_scope",
    "get_player_stats",
    "get_ranking_redirect",
    "get_scoped_player_and_page",
    "get_scoped_player_row",
    "hall_of_fame_view",
    "login_view",
    "logout_view",
    "match_view",
    "pairs_ranking_view",
    "paginate_list",
    "player_detail_view",
    "players_view",
    "process_matches",
    "process_matches_plain",
    "ranking_home_view",
    "ranking_view",
    "register_view",
    "user_delete_view",
    "user_view",
]
