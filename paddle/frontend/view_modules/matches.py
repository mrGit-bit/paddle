"""Authenticated match workflow views and helpers.

Responsibilities:
- `/matches/` page orchestration for list/create/delete flows.
- Match row display preparation for templates.

Integration:
- Reuses shared helpers from `common.py`.
- Exported through `frontend.views` facade.
"""

from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from games.models import Match, Player

from .common import (
    build_all_players,
    build_player_participation_queryset,
    fetch_paginated_data,
    filter_matches_for_group,
    get_new_match_ids,
    get_ranking_redirect,
    get_user_player,
)


def process_matches(matches, current_user, user_icon):
    """
    Processes a list of matches by:
    - Highlighting the current user with an icon (for display only).
    - Converting date_played from string to date object.
    """
    for match in matches:
        for key in ["team1_player1", "team1_player2", "team2_player1", "team2_player2"]:
            player = getattr(match, key)
            if player and player.name == current_user:
                setattr(match, f"{key}_display", user_icon)
            elif player:
                setattr(match, f"{key}_display", player.name)
            else:
                setattr(match, f"{key}_display", "")
        if isinstance(getattr(match, "date_played", None), str):
            match.date_played = datetime.strptime(match.date_played, "%Y-%m-%d").date()
    return matches


def _with_match_players(queryset):
    return queryset.select_related(
        "team1_player1",
        "team1_player2",
        "team2_player1",
        "team2_player2",
    )


def _match_window_floor():
    return Match.editable_date_floor()


@login_required
def match_view(request, client=None):
    """
    GET: Renders the match page with a form to add new matches and a table of all matches.
    POST: Creates a new match if the data is valid and not duplicated. Also manages deletion of matches.
    """
    user_player = get_user_player(request)

    if not user_player:
        messages.error(request, "Error: el usuario no está asociado a ningún jugador.")
        return redirect("hall_of_fame")

    if request.method == "POST":
        match_data = request.POST.copy()

        if match_data.get("action") == "delete":
            match_id = match_data.get("match_id")
            if not match_id:
                messages.error(request, "Error: falta el identificador del partido.")
                return redirect("match")

            try:
                match = Match.objects.get(id=match_id, group=user_player.group)
            except Match.DoesNotExist:
                messages.error(request, "Error: el partido no existe.")
                return redirect("match")

            is_participant = Player.objects.filter(
                registered_user=request.user,
                id__in=[
                    match.team1_player1.id,
                    match.team1_player2.id,
                    match.team2_player1.id,
                    match.team2_player2.id,
                ],
            ).exists()

            if not (request.user.is_staff or is_participant):
                messages.error(request, "No estás autorizado para borrar este partido.")
                return redirect("match")

            if match.is_locked():
                messages.error(
                    request,
                    "Este partido ya ha sido aprobado automáticamente y no se puede borrar.",
                )
                return redirect("match")

            match.delete()
            messages.success(request, "Partido borrado correctamente")
            return redirect("match")

        def resolve_player(choice_key: str, new_name_key: str):
            choice = (match_data.get(choice_key) or "").strip()
            new_name = (match_data.get(new_name_key) or "").strip()

            if not choice:
                return None, "Por favor, selecciona un jugador."

            if choice in ("NEW_M", "NEW_F"):
                if not new_name:
                    return None, "Por favor, introduce el nombre del nuevo jugador."
                existing = Player.objects.filter(name__iexact=new_name, group=user_player.group).first()
                if existing:
                    return existing, None

                gender = Player.GENDER_MALE if choice == "NEW_M" else Player.GENDER_FEMALE
                created = Player.objects.create(name=new_name, gender=gender, group=user_player.group)
                return created, None

            try:
                return Player.objects.get(id=int(choice), group=user_player.group), None
            except (ValueError, Player.DoesNotExist):
                return None, "Jugador seleccionado no válido."

        team1_player1 = user_player

        team1_player2, err = resolve_player("team1_player2_choice", "team1_player2_new_name")
        if err:
            messages.error(request, err)
            return redirect("match")

        team2_player1, err = resolve_player("team2_player1_choice", "team2_player1_new_name")
        if err:
            messages.error(request, err)
            return redirect("match")

        team2_player2, err = resolve_player("team2_player2_choice", "team2_player2_new_name")
        if err:
            messages.error(request, err)
            return redirect("match")

        participant_ids = [team1_player1.id, team1_player2.id, team2_player1.id, team2_player2.id]
        if len(set(participant_ids)) != 4:
            messages.error(request, "¡Jugadores repetidos! Inténtalo de nuevo.")
            return redirect("match")

        try:
            date_played = datetime.strptime(match_data.get("date_played"), "%Y-%m-%d").date()
        except Exception:
            messages.error(request, "Formato de fecha no válido.")
            return redirect("match")

        if date_played > date.today():
            messages.error(request, "La fecha no puede ser futura.")
            return redirect("match")

        min_date_allowed = _match_window_floor()
        if date_played < min_date_allowed:
            messages.error(
                request,
                "Solo se pueden añadir partidos jugados en los últimos 30 días.",
            )
            return redirect("match")

        team1_sorted = sorted([team1_player1.id, team1_player2.id])
        team2_sorted = sorted([team2_player1.id, team2_player2.id])

        existing_matches = Match.objects.filter(date_played=date_played, group=user_player.group)

        for match in existing_matches:
            existing_team1_sorted = sorted([match.team1_player1.id, match.team1_player2.id])
            existing_team2_sorted = sorted([match.team2_player1.id, match.team2_player2.id])

            if (team1_sorted == existing_team1_sorted and team2_sorted == existing_team2_sorted) or (
                team1_sorted == existing_team2_sorted and team2_sorted == existing_team1_sorted
            ):
                messages.error(request, "Error: el partido ya se había creado")
                return redirect("match")

        winning_team = match_data.get("winning_team")
        if winning_team not in ["1", "2"]:
            messages.error(request, "Error: Por favor selecciona equipo ganador.")
            return redirect("match")

        Match.objects.create(
            group=user_player.group,
            team1_player1=team1_player1,
            team1_player2=team1_player2,
            team2_player1=team2_player1,
            team2_player2=team2_player2,
            winning_team=int(winning_team),
            date_played=date_played,
        )
        messages.success(request, "Partido creado correctamente")
        scope = request.session.get("last_ranking_scope", "all")
        return get_ranking_redirect(scope)

    registered_players, non_registered_players, all_players = build_all_players(group=user_player.group)

    matches_qs = _with_match_players(filter_matches_for_group(group=user_player.group)).order_by("-date_played")
    matches, pagination = fetch_paginated_data(matches_qs, request)

    user_matches_qs = _with_match_players(
        build_player_participation_queryset(user_player)
    ).order_by("-date_played")
    user_matches, user_pagination = fetch_paginated_data(user_matches_qs, request)

    new_match_ids = get_new_match_ids(request)
    request.session["new_matches"] = new_match_ids
    request.session.modified = True

    user_icon = mark_safe(
        '<i class="bi bi-person-check-fill"></i><span class="fw-bold">'
        + request.user.username
        + "</span>"
    )

    matches = process_matches(matches, request.user.username, user_icon)
    user_matches = process_matches(user_matches, request.user.username, user_icon)

    today = date.today().isoformat()
    min_match_date = _match_window_floor().isoformat()

    context = {
        "all_players": all_players,
        "registered_players": registered_players,
        "existing_players": non_registered_players,
        "matches": matches,
        "pagination": pagination,
        "user_matches": user_matches,
        "user_pagination": user_pagination,
        "new_match_ids": new_match_ids,
        "new_matches_number": len(new_match_ids),
        "today": today,
        "min_match_date": min_match_date,
        "match_window_days": Match.APPROVAL_WINDOW_DAYS,
        "error": None,
    }

    request.session["seen_matches"] = list(
        set(request.session.get("seen_matches", [])).union(new_match_ids)
    )
    request.session["new_matches"] = []
    request.session.modified = True

    return render(request, "frontend/match.html", context)
