"""Shared frontend view helpers and forms.

Responsibilities:
- Cross-module helpers (pagination, scope redirects, player utility lookups).
- Shared password reset form and about-version label helper.

Integration:
- Imported by domain modules (`ranking`, `players`, `matches`, `auth_profile`).
- Re-exported publicly via `frontend.views`.
"""

from functools import lru_cache

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.core.paginator import Paginator
from django.shortcuts import redirect

from games.models import Match, Player


@lru_cache(maxsize=1)
def get_about_app_version_label():
    try:
        from config import __version__
    except (ImportError, AttributeError):
        return None

    return __version__


class EmailExistsPasswordResetForm(PasswordResetForm):
    """Password reset form requires the email to exist in DB."""

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        user_model = get_user_model()
        exists = user_model._default_manager.filter(email__iexact=email).exists()
        if not exists:
            raise forms.ValidationError("No existe ninguna cuenta con este correo electrónico.")
        return email


def get_player_stats(request, player_id=None):
    """
    Returns a dictionary containing the player's stats
    (wins, matches, win rate, ranking position & ranking total).
    """
    if player_id is None and request.user.is_authenticated:
        try:
            player = Player.objects.get(registered_user=request.user)
            player_id = player.id
        except Player.DoesNotExist:
            player_id = None

    stats = {
        "player_id": player_id,
        "wins": 0,
        "matches": 0,
        "win_rate": "0%",
        "ranking_position": 0,
        "ranking_total": Player.objects.count(),
    }

    if not player_id:
        return stats

    try:
        player = Player.objects.get(id=player_id)
        stats.update(
            {
                "player_id": player.id,
                "wins": player.wins,
                "matches": player.matches_played,
                "win_rate": f"{player.win_rate:.2f}%",
                "ranking_position": player.ranking_position,
            }
        )
    except Player.DoesNotExist:
        pass
    return stats


def build_player_participation_queryset(player):
    """
    Returns matches where `player` participates in any of the four match slots.
    """
    return (
        Match.objects.filter(team1_player1=player)
        | Match.objects.filter(team1_player2=player)
        | Match.objects.filter(team2_player1=player)
        | Match.objects.filter(team2_player2=player)
    ).distinct()


def get_new_match_ids(request):
    """
    Retrieves the list of new match IDs for the user.
    A match is considered "new" if the user is a participant but hasn't seen it yet.
    """
    if not request.user.is_authenticated:
        return []

    user_player = Player.objects.filter(registered_user=request.user).first()
    if not user_player:
        return []

    matches = build_player_participation_queryset(user_player)
    seen_matches = set(request.session.get("seen_matches", []))
    new_match_ids = [match.id for match in matches if match.id not in seen_matches]
    return new_match_ids


def fetch_paginated_data(queryset, request, page_size=12):
    """
    Helper to paginate a queryset for DB-backed pagination.
    """
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1

    if getattr(queryset, "model", None) == Player:
        queryset = queryset.order_by("ranking_position", "id")

    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    items = list(page_obj.object_list)
    pagination = {
        "count": paginator.count,
        "next": page_obj.next_page_number() if page_obj.has_next() else None,
        "previous": page_obj.previous_page_number() if page_obj.has_previous() else None,
        "current_page": page,
        "total_pages": paginator.num_pages,
    }
    return items, pagination


def get_ranking_redirect(scope: str):
    """
    Returns a redirect() to the last visited ranking scope in session.
    """
    if scope == "male":
        return redirect("ranking_male")
    if scope == "female":
        return redirect("ranking_female")
    if scope == "mixed":
        return redirect("ranking_mixed")
    return redirect("hall_of_fame")


def paginate_list(items, request, page_size=12):
    """
    Helper to paginate an in-memory list (same pagination dict shape as fetch_paginated_data()).
    """
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1

    paginator = Paginator(items, page_size)
    page_obj = paginator.get_page(page)
    pagination = {
        "count": paginator.count,
        "next": page_obj.next_page_number() if page_obj.has_next() else None,
        "previous": page_obj.previous_page_number() if page_obj.has_previous() else None,
        "current_page": page,
        "total_pages": paginator.num_pages,
    }
    return list(page_obj.object_list), pagination


def fetch_available_players():
    """
    Fetch non-linked players and registered players, sorted alphabetically.
    """
    registered_players = Player.objects.filter(registered_user__isnull=False).values("id", "name")
    non_registered_players = Player.objects.filter(registered_user__isnull=True).values("id", "name")
    registered_players = sorted(registered_players, key=lambda player: player["name"].lower())
    non_registered_players = sorted(non_registered_players, key=lambda player: player["name"].lower())
    return list(registered_players), list(non_registered_players)


def build_all_players():
    """
    Returns the merged players list used in selects, sorted alphabetically.
    """
    registered_players, non_registered_players = fetch_available_players()
    all_players = sorted(
        list(registered_players) + list(non_registered_players),
        key=lambda p: p["name"].lower(),
    )
    return registered_players, non_registered_players, all_players
