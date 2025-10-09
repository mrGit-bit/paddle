# frontend/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from datetime import date, datetime
from games.models import Player, Match
import json
import logging

User = get_user_model()

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
    Helper to paginate a queryset.
    """
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1

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

def hall_of_fame_view(request):
    """
    Renders the Hall of Fame page with paginated players.
    """
    players_qs = Player.objects.exclude(ranking_position=0).order_by('ranking_position')
    players, pagination = fetch_paginated_data(players_qs, request)

    user_page, user_player, previous_player, following_player = None, None, None, None
    new_match_ids = []

    if request.user.is_authenticated:
        new_match_ids = get_new_match_ids(request) or []
        try:
            user_player = Player.objects.get(registered_user=request.user)
            user_player_rank = user_player.ranking_position
            current_page = int(request.GET.get("page", 1))
            user_page = ((user_player_rank - 1) // 12) + 1
        except Player.DoesNotExist:
            user_player = None

        if user_player and user_page != current_page:
            previous_player = Player.objects.filter(ranking_position=user_player_rank - 1).first()
            following_player = Player.objects.filter(ranking_position=user_player_rank + 1).first()
        else:
            previous_player, following_player = None, None

    return render(request, "frontend/hall_of_fame.html", {
        "players": players,
        "pagination": pagination,
        "new_matches_number": len(new_match_ids),
        "user_page": user_page,
        "user_player": user_player,
        "previous_player": previous_player,
        "following_player": following_player,
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
        }
        required_fields = ["username", "email", "password", "confirm_password"]
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
                player.save()
            else:
                messages.error(request, "Selected player is already linked or does not exist.")
                user.delete()
                return redirect('register')
        else:
            Player.objects.create(
                name=user.username,
                registered_user=user
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

@login_required
def match_view(request, client=None):
    """
    Handles both GET and POST requests for match.html.

    GET: Renders the match page with a form to add new matches and a table of all matches.
    POST: Creates a new match if the data is valid and not duplicated, or updates an existing match if the match_id is provided.

    :param client: Not used
    :return: A rendered HTML page if GET, or a JSON response with a success message if POST
    """
    user_player = Player.objects.filter(registered_user=request.user).first()
    if not user_player:
        messages.error(request, "Error: el usuario no está asociado a ningún jugador.")
        return redirect('hall_of_fame')    

    if request.method == 'POST':
        match_data = request.POST.copy()
        match_data['team1_player1'] = request.user.username

        # Normalize names for case-insensitive duplicate check
        participants = [
            match_data.get('team1_player1', '').strip().lower(),
            match_data.get('team1_player2', '').strip().lower(),
            match_data.get('team2_player1', '').strip().lower(),
            match_data.get('team2_player2', '').strip().lower()
        ]
        if len(set(participants)) != 4:
            messages.error(request, "Jugadores repetidos! Inténtalo de nuevo.")
            return redirect('match')

        def get_or_create_player(name):
            player = Player.objects.filter(name__iexact=name.strip()).first()
            if not player:
                player = Player.objects.create(name=name.strip())
            return player

        team1_player1 = get_or_create_player(match_data['team1_player1'])
        team1_player2 = get_or_create_player(match_data['team1_player2'])
        team2_player1 = get_or_create_player(match_data['team2_player1'])
        team2_player2 = get_or_create_player(match_data['team2_player2'])

        try:
            date_played = datetime.strptime(match_data.get('date_played'), "%Y-%m-%d").date()
        except Exception:
            messages.error(request, "Invalid date format.")
            return redirect('match')

        if date_played > date.today():
            messages.error(request, "Date cannot be in the future.")
            return redirect('match')

        # Check for duplicate match on same date (skip if editing the same match)
        team1_sorted = sorted([team1_player1.name.lower(), team1_player2.name.lower()])
        team2_sorted = sorted([team2_player1.name.lower(), team2_player2.name.lower()])
        existing_matches = Match.objects.filter(date_played=date_played)
        match_id = match_data.get('match_id')
        for match in existing_matches:
            if match_id and str(match.id) == str(match_id):
                continue  # skip self when editing
            existing_team1_sorted = sorted([match.team1_player1.name.lower(), match.team1_player2.name.lower()])
            existing_team2_sorted = sorted([match.team2_player1.name.lower(), match.team2_player2.name.lower()])
            if (team1_sorted == existing_team1_sorted and team2_sorted == existing_team2_sorted) or \
               (team1_sorted == existing_team2_sorted and team2_sorted == existing_team1_sorted):
                messages.error(request, "Error: el partido ya se había creado")
                return redirect('match')

        winning_team = match_data.get('winning_team')
        if winning_team not in ['1', '2']:
            messages.error(request, "Error: Por favor selecciona equipo ganador.")
            return redirect('match')

        if match_id:
            # Edit existing match
            match = Match.objects.get(id=match_id)
            match.update_match(
                team1_player1=team1_player1,
                team1_player2=team1_player2,
                team2_player1=team2_player1,
                team2_player2=team2_player2,
                winning_team=int(winning_team),
                date_played=date_played
            )
            messages.success(request, "Partido creado correctamente")
        else:
            # Create new match
            Match.objects.create(
                team1_player1=team1_player1,
                team1_player2=team1_player2,
                team2_player1=team2_player1,
                team2_player2=team2_player2,
                winning_team=int(winning_team),
                date_played=date_played
            )
            messages.success(request, "Partido creado correctamente")
        return redirect('match')

    # Fetch players for form
    registered_players, non_registered_players = fetch_available_players()
    all_players = sorted(
        list(registered_players) + list(non_registered_players),
        key=lambda p: p['name'].lower()
    )

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

    # Handle DELETE request: delete a specific match
    if request.method == 'DELETE':
        try:
            delete_data = json.loads(request.body)
            match_id = delete_data.get('match_id')
            match = Match.objects.get(id=match_id)
            # Only allow participants or admin to delete
            if not (request.user.is_staff or Player.objects.filter(registered_user=request.user, id__in=[
                match.team1_player1.id, match.team1_player2.id, match.team2_player1.id, match.team2_player2.id
            ]).exists()):
                return JsonResponse({"error": "You are not authorized to delete this match."}, status=403)
            match.delete()
            return JsonResponse({"message": "Partido borrado correctamente"}, status=200)
        except Exception as e:
            logging.exception("Error occurred while deleting match")
            return JsonResponse({"error": "An error occurred while deleting the match."}, status=400)

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


