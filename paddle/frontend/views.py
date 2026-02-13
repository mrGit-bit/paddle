# Absolute path: /workspaces/paddle/paddle/frontend/views.py

from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from datetime import date, datetime
from games.models import Player, Match
import json

from .services.ranking import compute_ranking

User = get_user_model()

class EmailExistsPasswordResetForm(PasswordResetForm):
    """Password reset form requires the email to exist in DB."""
    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        User = get_user_model()
        exists = User._default_manager.filter(email__iexact=email).exists()
        if not exists:
            # Spanish, plain and helpful; shown under the field.
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
        stats.update({
            "player_id": player.id,
            "wins": player.wins,
            "matches": player.matches_played,
            "win_rate": f"{player.win_rate:.2f}%",
            "ranking_position": player.ranking_position,
        })
    except Player.DoesNotExist:
        pass
    return stats

def get_new_match_ids(request):
    """
    Retrieves the list of new match IDs for the user.
    A match is considered "new" if the user is a participant but hasn't seen it yet.
    """
    if not request.user.is_authenticated:
        return []

    # Find matches where the user is a participant
    user_player = Player.objects.filter(registered_user=request.user).first()
    if not user_player:
        return []

    matches = Match.objects.filter(
        team1_player1=user_player
    ) | Match.objects.filter(
        team1_player2=user_player
    ) | Match.objects.filter(
        team2_player1=user_player
    ) | Match.objects.filter(
        team2_player2=user_player
    )
    matches = matches.distinct()

    seen_matches = set(request.session.get('seen_matches', []))
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
    return redirect("hall_of_fame")  # "all" or unknown


def ranking_home_view(request):
    """
    Redirects to the last visited ranking scope.
    """
    scope = request.session.get("last_ranking_scope", "all")
    return get_ranking_redirect(scope)


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

def hall_of_fame_view(request):
    """ Wrapper to avoid changing URLs"""
    return ranking_view(request, scope="all")

def ranking_view(request, scope):
    """
    Renders scoped ranking pages: all/male/female/mixed.
    """
    ranked_players, unranked_players, scope = compute_ranking(scope)
    
    # store the current scope
    request.session["last_ranking_scope"] = scope

    # Paginate ranked players only
    players, pagination = paginate_list(ranked_players, request, page_size=12)

    # New matches badge number (navbar)
    new_match_ids = get_new_match_ids(request) or []
    new_matches_number = len(new_match_ids)

    # User mini-table logic (scoped) for hof_user_snippet.html
    user_page = None
    user_player = None
    previous_player = None
    following_player = None

    if request.user.is_authenticated:
        db_user_player = Player.objects.filter(registered_user=request.user).first()

        if db_user_player:
            # Find the scoped player object of the user (has display_* attributes)
            scoped_user_player = next((p for p in ranked_players if p.id == db_user_player.id), None)

            # Only show mini-table if the user has matches in this scope
            if scoped_user_player:
                user_player = scoped_user_player  # IMPORTANT: use scoped object for template
                # Ordinal index in the sorted list (1..N). Needed for pagination/neighbors under ties.
                ordinal_index = ranked_players.index(user_player) + 1

                current_page = int(request.GET.get("page", 1))
                user_page = ((ordinal_index - 1) // 12) + 1

                if user_page != current_page:
                    previous_player = ranked_players[ordinal_index - 2] if ordinal_index > 1 else None
                    following_player = ranked_players[ordinal_index] if ordinal_index < len(ranked_players) else None

    titles = {
        "all": "Ranking — Todos los partidos",
        "male": "Ranking — Partidos masculinos",
        "female": "Ranking — Partidos femeninos",
        "mixed": "Ranking — Partidos mixtos",
    }

    return render(request, "frontend/hall_of_fame.html", {
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
    })

def fetch_available_players():
    """
    Fetch non-linked players and registered players, sorted alphabetically.
    """
    registered_players = Player.objects.filter(registered_user__isnull=False).values('id', 'name')
    non_registered_players = Player.objects.filter(registered_user__isnull=True).values('id', 'name')
    registered_players = sorted(registered_players, key=lambda player: player['name'].lower())
    non_registered_players = sorted(non_registered_players, key=lambda player: player['name'].lower())
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


def build_player_matches_queryset(player):
    """
    Returns matches where player participates, ordered latest first.
    """
    profile_matches_qs = Match.objects.filter(
        team1_player1=player
    ) | Match.objects.filter(
        team1_player2=player
    ) | Match.objects.filter(
        team2_player1=player
    ) | Match.objects.filter(
        team2_player2=player
    )
    return profile_matches_qs.distinct().order_by("-date_played")


def get_scoped_player_row(scope: str, player_id: int):
    """
    Returns the scoped ranked player object with display_* fields or None.
    """
    ranked_players, _, _ = compute_ranking(scope)
    return next((player for player in ranked_players if player.id == player_id), None)

def process_form_data(request):
    """
    Extract and validate form data from the request.
    Supports both POST (for registration) and PATCH (for user profile updates).
    Ensures non-editable fields are set to None in PATCH requests.
    """
    form_data = {}

    if request.method == 'POST':
        form_data = {
            "username": request.POST.get("username", "").strip(),
            "email": request.POST.get("email", "").strip(),
            "password": request.POST.get("password"),
            "confirm_password": request.POST.get("confirm_password"),
            "player_id": request.POST.get("player_id") or None,
            "gender": (request.POST.get("gender") or "").strip().upper() or None,
        }

        required_fields = ["username", "email", "password", "confirm_password", "gender"]
        for field in required_fields:
            if not form_data.get(field):
                return None, f"The field '{field}' is required."
        if form_data["password"] != form_data["confirm_password"]:
            return None, "Passwords do not match."
        form_data.pop("confirm_password", None)

    elif request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            form_data = {
                "username": None,
                "password": None,
                "player_id": None,
                "email": data.get("email", "").strip() or None,
            }
        except json.JSONDecodeError:
            return None, "Invalid JSON in request body."

    cleaned_data = {
        "username": form_data.get("username"),
        "email": form_data.get("email"),
        "password": form_data.get("password"),
        "player_id": form_data.get("player_id"),
        "gender": form_data.get("gender"),
    }
    return cleaned_data, None

def register_view(request):
    if request.method == 'POST':
        form_data, form_error = process_form_data(request)
        if form_error:
            messages.error(request, form_error)
            return redirect('register')

        # Check for duplicate username or player name        
        user_exists = User.objects.filter(username__iexact=form_data["username"]).exists()
        player_exists = Player.objects.filter(
            name__iexact=form_data["username"], registered_user__isnull=True
        ).exclude(id=form_data.get("player_id")).exists()
        if user_exists or player_exists:
            messages.error(request, f"Error: Ya existe un usuario o un jugador con el nombre '{form_data['username']}'. Cambia el nombre del usuario o selecciona el jugador existente en el desplegable de jugadores.")
            return redirect('register')

        # Validate gender (server-side)
        gender = form_data.get("gender")
        allowed_genders = {Player.GENDER_MALE, Player.GENDER_FEMALE}
        if gender not in allowed_genders:
            messages.error(request, "Error: por favor, selecciona un género válido.")
            return redirect('register')
        
        # Create user
        user = User(username=form_data["username"], email=form_data["email"])
        user.set_password(form_data["password"])
        user.save()

        # Link to player or create new player
        player_id = form_data.get("player_id")
        if player_id:
            player = Player.objects.filter(id=player_id, registered_user__isnull=True).first()
            if player:
                player.registered_user = user
                player.name = user.username
                player.gender = gender # Update gender based on user input registration form
                player.save()
            else:
                messages.error(request, "Selected player is already linked or does not exist.")
                user.delete()
                return redirect('register')
        else:
            Player.objects.create(
                name=user.username,
                registered_user=user,
                gender=gender,
            )

        login(request, user)
        return redirect('match')

    registered_players, non_registered_players = fetch_available_players()
    players = [(p['id'], p['name']) for p in non_registered_players]
    return render(request, 'frontend/register.html', {"players": players})

@login_required
def user_view(request, id):
    if request.user.id != id:
        return JsonResponse({'error': 'You are not authorized to view this profile.'}, status=403)

    user_player = Player.objects.filter(registered_user=request.user).first()
    total_players = Player.objects.count()

    if request.method == 'PATCH':
        try:
            form_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body.'}, status=400)

        form_data, form_error = process_form_data(request)
        if form_error:
            return JsonResponse({'error': form_error}, status=400)

        update_data = {k: v for k, v in form_data.items() if v is not None and k == "email"}
        if update_data.get("email"):
            request.user.email = update_data["email"]
            request.user.save()
            request.user.refresh_from_db()
            return JsonResponse({'success': 'Datos actualizados', 'user': {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
            }}, status=200)
        else:
            return JsonResponse({'error': 'No valid fields to update.'}, status=400)

    context = {
        'user': request.user,
        'user_player': user_player,
        'total_players': total_players
    }
    return render(request, 'frontend/user.html', context)

def process_matches(matches, current_user, user_icon):
    """
    Processes a list of matches by:
    - Highlighting the current user with an icon (for display only).
    - Converting date_played from string to date object.
    """
    for match in matches:
        for key in ["team1_player1", "team1_player2", "team2_player1", "team2_player2"]:
            player = getattr(match, key)
            # Add a display attribute for the template
            if player and player.name == current_user:
                setattr(match, f"{key}_display", user_icon)
            elif player:
                setattr(match, f"{key}_display", player.name)
            else:
                setattr(match, f"{key}_display", "")
        if isinstance(getattr(match, "date_played", None), str):
            match.date_played = datetime.strptime(match.date_played, "%Y-%m-%d").date()
    return matches


def process_matches_plain(matches):
    """
    Processes matches without current-user highlighting (public pages).
    """
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
    return render(request, "frontend/players.html", {
        "all_players": all_players,
        "selected_player_id": None,
        "new_matches_number": len(new_match_ids),
    })


def player_detail_view(request, player_id):
    """
    Public player profile page with scoped stats and match history.
    """
    profile_player = get_object_or_404(Player, id=player_id)
    _, _, all_players = build_all_players()

    scope_rows = [
        {"label": "Todos", "scoped_player": get_scoped_player_row("all", profile_player.id)},
    ]
    if profile_player.gender == Player.GENDER_MALE:
        scope_rows.append({"label": "Masc.", "scoped_player": get_scoped_player_row("male", profile_player.id)})
    elif profile_player.gender == Player.GENDER_FEMALE:
        scope_rows.append({"label": "Fem.", "scoped_player": get_scoped_player_row("female", profile_player.id)})
    scope_rows.append({"label": "Mixtos", "scoped_player": get_scoped_player_row("mixed", profile_player.id)})

    profile_matches_qs = build_player_matches_queryset(profile_player)
    profile_matches, profile_pagination = fetch_paginated_data(profile_matches_qs, request)
    profile_matches = process_matches_plain(profile_matches)

    new_match_ids = get_new_match_ids(request) or []
    return render(request, "frontend/player_detail.html", {
        "profile_player": profile_player,
        "all_players": all_players,
        "selected_player_id": profile_player.id,
        "scope_rows": scope_rows,
        "profile_matches": profile_matches,
        "profile_pagination": profile_pagination,
        "new_match_ids": [],
        "user_matches": [],
        "new_matches_number": len(new_match_ids),
    })

@login_required
def match_view(request, client=None):
    """    
    GET: Renders the match page with a form to add new matches and a table of all matches.
    POST: Creates a new match if the data is valid and not duplicated. Also manages deletion of matches.    
    """
    user_player = Player.objects.filter(registered_user=request.user).first()      
    
    if not user_player:
        messages.error(request, "Error: el usuario no está asociado a ningún jugador.")
        return redirect('hall_of_fame')    

    if request.method == 'POST':
        match_data = request.POST.copy()
        
        # Delete action (handled via normal POST + redirect + messages)
        if match_data.get("action") == "delete":
            match_id = match_data.get("match_id")
            if not match_id:
                messages.error(request, "Error: falta el identificador del partido.")
                return redirect("match")

            try:
                match = Match.objects.get(id=match_id)
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

            match.delete()
            messages.success(request, "Partido borrado correctamente")
            return redirect("match")

        def resolve_player(choice_key: str, new_name_key: str):
            """
            Resolves a player from the match form.

            - If choice is an existing Player ID -> returns that Player.
            - If choice is NEW_M / NEW_F -> requires a name, and:
                - if name exists case-insensitively -> returns existing Player (Option 1)
                - else -> creates a new Player with gender set, registered_user NULL
            """
            choice = (match_data.get(choice_key) or "").strip()
            new_name = (match_data.get(new_name_key) or "").strip()

            if not choice:
                return None, "Por favor, selecciona un jugador."

            if choice in ("NEW_M", "NEW_F"):
                if not new_name:
                    return None, "Por favor, introduce el nombre del nuevo jugador."
                existing = Player.objects.filter(name__iexact=new_name).first()
                if existing:
                    # Option 1: auto-resolve to existing player (do not change gender here)
                    return existing, None

                gender = Player.GENDER_MALE if choice == "NEW_M" else Player.GENDER_FEMALE
                created = Player.objects.create(name=new_name, gender=gender)
                return created, None

            # Existing player by ID
            try:
                return Player.objects.get(id=int(choice)), None
            except (ValueError, Player.DoesNotExist):
                return None, "Jugador seleccionado no válido."

        # Current user is always team1_player1
        team1_player1 = user_player

        team1_player2, err = resolve_player("team1_player2_choice", "team1_player2_new_name")
        if err:
            messages.error(request, err)
            return redirect('match')

        team2_player1, err = resolve_player("team2_player1_choice", "team2_player1_new_name")
        if err:
            messages.error(request, err)
            return redirect('match')

        team2_player2, err = resolve_player("team2_player2_choice", "team2_player2_new_name")
        if err:
            messages.error(request, err)
            return redirect('match')

        # No repeated players in the same match
        participant_ids = [team1_player1.id, team1_player2.id, team2_player1.id, team2_player2.id]
        if len(set(participant_ids)) != 4:
            messages.error(request, "¡Jugadores repetidos! Inténtalo de nuevo.")
            return redirect('match')
        
        try:
            date_played = datetime.strptime(match_data.get('date_played'), "%Y-%m-%d").date()
        except Exception:
            messages.error(request, "Formato de fecha no válido.")
            return redirect('match')

        if date_played > date.today():
            messages.error(request, "La fecha no puede ser futura.")
            return redirect('match')

        # Check for duplicate match on same date (skip if editing the same match)
        team1_sorted = sorted([team1_player1.id, team1_player2.id])
        team2_sorted = sorted([team2_player1.id, team2_player2.id])

        existing_matches = Match.objects.filter(date_played=date_played)

        for match in existing_matches:
            existing_team1_sorted = sorted([match.team1_player1.id, match.team1_player2.id])
            existing_team2_sorted = sorted([match.team2_player1.id, match.team2_player2.id])

            if (team1_sorted == existing_team1_sorted and team2_sorted == existing_team2_sorted) or \
            (team1_sorted == existing_team2_sorted and team2_sorted == existing_team1_sorted):
                messages.error(request, "Error: el partido ya se había creado")
                return redirect('match')

        winning_team = match_data.get('winning_team')
        if winning_team not in ['1', '2']:
            messages.error(request, "Error: Por favor selecciona equipo ganador.")
            return redirect('match')

        Match.objects.create(
            team1_player1=team1_player1,
            team1_player2=team1_player2,
            team2_player1=team2_player1,
            team2_player2=team2_player2,
            winning_team=int(winning_team),
            date_played=date_played
        )
        messages.success(request, "Partido creado correctamente")
        scope = request.session.get('last_ranking_scope', 'all')
        return get_ranking_redirect(scope)

    # GET option renders the match page (form + table of matches)
    # Fetch players for form
    registered_players, non_registered_players, all_players = build_all_players()

    # Fetch all matches and paginated
    matches_qs = Match.objects.all().order_by('-date_played')
    matches, pagination = fetch_paginated_data(matches_qs, request)

    # Fetch only user matches
    user_matches_qs = Match.objects.filter(
        team1_player1=user_player
    ) | Match.objects.filter(
        team1_player2=user_player
    ) | Match.objects.filter(
        team2_player1=user_player
    ) | Match.objects.filter(
        team2_player2=user_player
    )
    user_matches_qs = user_matches_qs.distinct().order_by('-date_played')
    user_matches, user_pagination = fetch_paginated_data(user_matches_qs, request)

    # Get list of new matches
    new_match_ids = get_new_match_ids(request)
    request.session['new_matches'] = new_match_ids
    request.session.modified = True

    user_icon = mark_safe('<i class="bi bi-person-check-fill"></i><span class="fw-bold">' + request.user.username + '</span>')

    matches = process_matches(matches, request.user.username, user_icon)
    user_matches = process_matches(user_matches, request.user.username, user_icon)

    today = date.today().isoformat()    

    # Render the match page in GET requests
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
        "error": None
    }

    # Mark all matches as "seen" when user views match.html
    request.session['seen_matches'] = list(set(request.session.get('seen_matches', [])).union(new_match_ids))
    request.session['new_matches'] = []
    request.session.modified = True

    return render(request, 'frontend/match.html', context)

def login_view(request):
    if request.method == 'POST':
        raw_identifier = (request.POST.get('username') or '').strip()        
        password = request.POST.get('password') or ''
        
        # Resolve identifier to an actual username (case-insensitive for username & email)
        user_obj = None
        if '@' in raw_identifier:
            # Treat as email
            user_obj = User.objects.filter(email__iexact=raw_identifier).first()
        else:
            # Treat as username
            user_obj = User.objects.filter(username__iexact=raw_identifier).first()

        resolved_username = user_obj.username if user_obj else raw_identifier  # fallback keeps existing behavior       
        
        user = authenticate(request, username=resolved_username, password=password)
        
        if user:
            login(request, user)
            return redirect('hall_of_fame')
        # Generic error (don't reveal whether it's username, email or password)    
        return render(request, 'frontend/login.html', {"error": "Nombre o contraseña no válidos."})
    
    return render(request, 'frontend/login.html')

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('hall_of_fame')
    return redirect('login')

def about_view(request):
    """
    Renders the About page with stats: number of users, players, matches since 1 Sept 2025.
    """
    num_users = User.objects.count()
    num_players = Player.objects.count()
    num_matches = Match.objects.filter(date_played__gte=date(2025, 9, 1)).count()
    contact_email = "rankingdepadel.club@gmail.com"

    context = {
        "num_users": num_users,
        "num_players": num_players,
        "num_matches": num_matches,
        "contact_email": contact_email,
    }
    return render(request, "frontend/about.html", context)
