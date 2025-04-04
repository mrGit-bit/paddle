# frontend/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.utils.safestring import mark_safe
from django.http import HttpResponseForbidden, JsonResponse
from django.conf import settings
from datetime import date, datetime
from urllib.parse import urljoin
from games.models import Player
import requests
import json

BASE_API_URL = settings.BASE_API_URL

def get_new_match_ids(request):
    """
    Retrieves the list of new match IDs for the user.
    A match is considered "new" if the user is a participant but hasn't seen it yet.
    """

    # Fetch matches where the user participated
    matches_url = urljoin(BASE_API_URL, f"games/matches/?player={request.user.username}")
    print(f"Requesting user matches from API: {matches_url}")

    session = requests.Session()
    session.cookies.update(request.COOKIES)
    matches_response = session.get(matches_url)
    _, user_matches = handle_api_response(matches_response, lambda res: res.json().get('results', []))
    user_matches = user_matches or []  # Default to empty list if None
    
    # Get seen matches from session
    seen_matches = set(request.session.get('seen_matches', []))
    print(f"Seen matches from session: {seen_matches}")

    # Identify new matches the user hasn't seen
    new_match_ids = [match["id"] for match in user_matches if match["id"] not in seen_matches]
    print(f"New match IDs: {new_match_ids}")

    return new_match_ids  # Return the list of new match IDs

def fetch_paginated_api_data(request, endpoint, query_params=None):
    """    
    Fetch paginated data from an API endpoint, with optional query parameters.
    
    Args:
        request: Django request object.
        endpoint: Relative API path, e.g. 'games/matches/'.
        query_params: Optional dict like {'player': 'mario'}.

    Returns:
        (items, pagination) tuple where
            - items: A list of items for that page.
            - pagination: A context dictionary with next and previous page links, current page number
          a ranking offset to add to the player ranking in each page, and the total number of pages.
    """
    # Retrieves the requested page number from the query string in the URL
    try:
        page = int(request.GET.get("page", 1)) # default to page 1 if not provided
    except ValueError:
        page = 1  # fallback to page 1 if the value was invalid
    
    page_size = 12    
    ranking_offset = (page - 1) * page_size    
    
    # instead of using 'response = requests.get(url)' we use 'session.get(url)'
    session = requests.Session()
    session.cookies.update(request.COOKIES)

    # Build full query string
    query = f"?page={page}"
    if query_params:
        for key, value in query_params.items():
            query += f"&{key}={value}"

    full_url = urljoin(BASE_API_URL, f"{endpoint}{query}")
    print(f"Fetching paginated data from: {full_url}")
    response = session.get(full_url)

    
    error, data = handle_api_response(response)
    if error:
        print(f"Failed to fetch paginated data: {error}")
        return [], {}    
    
    items = data.get('results', [])        
    count = data.get('count', 0)
    total_pages = (count + page_size - 1) // page_size
    
    pagination = {            
        "next": data.get("next"),
        "previous": data.get("previous"),
        "current_page": page,
        "total_pages": total_pages,
        "ranking_offset": ranking_offset
    }
    return items, pagination
    

def hall_of_fame_view(request):
    """
    Displays the Hall of Fame (players ranking) and tracks unseen matches.
    """    
    print(f"{request.user} calling hall_of_fame_view...")
    # Call helper functions to fetch paginated data and not seen match IDs (in the session)
    players, pagination = fetch_paginated_api_data(request, "games/players/")    
    new_match_ids = get_new_match_ids(request) or []  # Matches the user hasn't seen in this session
    
    return render(request, "frontend/hall_of_fame.html", {
        "players": players,
        "pagination": pagination,
        "new_matches_number": len(new_match_ids),
        })

def handle_api_response(response, success_callback=None):
    """
    Handles API responses, extracting errors or passing the data to a callback.
    Returns errors from the API (e.g., duplicate username, server errors)
    Args:
        response: The API response object.
        success_callback: A function to call with the response data if successful.
    Returns:
        A tuple: (error_message, data).
    """
    if 200 <= response.status_code < 300:  # 2xx are successful responses
        
        # Handle 204 No Content response after deletion (no response body after successful deletion)
        if response.status_code == 204 or not response.content.strip():
            return None, {} # Return an empty dictionary        
        
        # If a success callback is provided, process the response data
        try:
            data = response.json()        
            return None, success_callback(response) if success_callback else data # No assumption of "results" key
        except ValueError:
            return "Unexpected empty response from the API.", {}
    
    # Handle error response
    try:
        errors = response.json()
        
        # If 'non_field_errors' exists, return only its message
        if "non_field_errors" in errors:
            return " ".join(errors["non_field_errors"]), None  # Just show the message, no prefix        
        
        if isinstance(errors, dict):
            error_messages = [f"{field.capitalize()}: {', '.join(messages)}" if isinstance(messages, list) else f"{field.capitalize()}: {messages}"
                              for field, messages in errors.items()]
            return "\n".join(error_messages), None
        return str(errors), None
    except ValueError: # Handle empty or malformed JSON
        return f"Unexpected API error (status {response.status_code}).", None

def fetch_available_players(session, request):
    """
    Fetch non-linked players from the API endpoint for names 
    ort alphabetically case-insensitively.
    """
    print(f"{request.user} fetching available players...")
    print("Requesting API url:", urljoin(BASE_API_URL, "games/players/player_names/"))
    response = session.get(urljoin(BASE_API_URL, "games/players/player_names/"))
    print("API response status code:", response.status_code)
    _, data = handle_api_response(response)    

    players = [
        (player['id'], player['name'])
        for player in data.get('non_registered_players',[]) 
    ] if data else []
    
    # Sort players alphabetically in a case-insensitive manner
    players.sort(key=lambda player: player[1].lower())

    return players

def process_form_data(request):
    """
    Extract and validate form data from the request.
    Supports both POST (for registration) and PATCH (for user profile updates).
    Ensures non-editable fields are set to None in PATCH requests.
    """
    form_data = {}

    # Handle POST (from registration)
    if request.method == 'POST':
        # Extract data from request.POST
        form_data = {
            "username": request.POST.get("username", "").strip(),
            "email": request.POST.get("email", "").strip(),
            "password": request.POST.get("password"),
            "confirm_password": request.POST.get("confirm_password"),
            "player_id": request.POST.get("player_id") or None, # Only player can be None
        }
        # Validate required fields
        required_fields = ["username", "email", "password", "confirm_password"]
        for field in required_fields:
            if not form_data.get(field):
                return None, f"The field '{field}' is required."
                    
        # Validate password match
        if form_data["password"] != form_data["confirm_password"]:
            return None, "Passwords do not match."
        
        # Remove confirm_password from final cleaned data
        form_data.pop("confirm_password", None)
    
    # Handle PATCH (for user profile updates)
    elif request.method == 'PATCH':
        # Parse JSON data from request.body
        try:
            data = json.loads(request.body)
            form_data = {
                # Fields that can not be updated
                "username": None,
                "password": None,
                "player_id": None,

                # Fields that can be updated
                "email": data.get("email", "").strip() or None,
            }
        except json.JSONDecodeError:
            return None, "Invalid JSON in request body."

    
    # Clean form data by removing unmodified or None fields
    cleaned_data = {
        "username": form_data.get("username"),
        "email": form_data.get("email"),
        "password": form_data.get("password"),
        "player_id": form_data.get("player_id"),
    }

    return cleaned_data, None

def register_view(request):
    session = requests.Session()
    session.cookies.update(request.COOKIES) # Update the session cookies from the request
    
    if request.method == 'POST':        
        print(f"Data before frontend processing: {request.POST}")
        
        # ERRORS: Handle client-side errors (form validation)
        form_data, form_error = process_form_data(request)        
        if form_error:
            print (f"Client-side error: {form_error}")
            # Use Django messages to pass error to the redirected GET request            
            messages.error(request, form_error)
            return redirect('register')  # Redirect to the register page using GET

        # API CALL: If not client side errors then sends registration data to API
        url = urljoin(BASE_API_URL, "users/")
        csrf_token = request.COOKIES.get('csrftoken') or get_token(request)
        session.headers.update({'X-CSRFToken': csrf_token})
        print(f"Data sent to API: {form_data}")
        response = session.post(url, data=form_data, headers={'X-CSRFToken': csrf_token})        
        
        # ERRORS: Handle server-side errors (API response)
        api_error, data = handle_api_response(response)
        if api_error:
            print (f"Server-side error(s):\n{api_error}")
            messages.error(request, api_error)
            return redirect('register')
        
        # Authenticate and log in after successful registration
        print(f"API response data: {data}")          
        username = form_data["username"]
        print (f"Created user: {username}")
        user = User.objects.get(username=username)
        if user.check_password(form_data["password"]):
            login(request, user)  # Log in the user with session
            print(f"Authenticated user: {request.user}")
            # Redirect to the match page after successful registration
            return redirect('match')     
        # If authentication fails then return to the register page
        return render(request, 'frontend/register.html', {"error": "Authentication failed", "players": players})
    
    # GET DATA: Fetch non-linked players from the API endpoint    
    players = fetch_available_players(session, request)
    # Render the registration form with available players context    
    return render(request, 'frontend/register.html', {"players": players})

def get_player_ranking(session, player_id):
    """Returns the player's rank and total number of players."""
    url = urljoin(BASE_API_URL, "games/players/")
    response = session.get(url)
    error, data = handle_api_response(response)

    if error or not data:
        print(f"Ranking API error: {error}")
        return None, None

    # Sort players by number of wins (descending), case-insensitive
    players = sorted(
        data.get("results", []),
        key=lambda p: (-p.get("wins", 0), p.get("name", "").lower())
    )

    total_players = len(players)

    # Find the index of the given player ID (1-based ranking)
    for index, player in enumerate(players, start=1):
        if player["id"] == player_id:
            return index, total_players # Player found, return its rank and total number of players

    return None, total_players  # Player not found, but return total number of players

@login_required
def user_view(request, id):
    print(f"Received request for user {id}: {request.method}")
    session = requests.Session()
    session.cookies.update(request.COOKIES)
    
    # Ensure the user can only access their own profile
    if request.user.id != id:
        print(f"Unauthorized access attempt by {request.user.username} to user {id}")
        return JsonResponse({'error': 'You are not authorized to view this profile.'}, status=403)
    
    # GET DATA: Fetch user id details and its player stats from player_id endpoint
    user_url = urljoin(BASE_API_URL, f"users/{id}/")
    response = session.get(user_url)
    user_error, user_data = handle_api_response(response)

    if user_error:
        print(f"Failed to fetch user details: {user_error}")
        return JsonResponse({'error': user_error}, status=response.status_code)

    player_id = user_data.get("player_id")

    # Fetch player stats if player_id exists
    wins, matches, win_rate = 0, 0, "0%"
    ranking_position, ranking_total = None, None
    if player_id:
        ranking_position, ranking_total = get_player_ranking(session, player_id)
        
        player_url = urljoin(BASE_API_URL, f"games/players/{player_id}/")
        player_error, player_data = handle_api_response(session.get(player_url))
        if player_error:
            print(f"Failed to fetch player details: {player_error}")
        else:
            wins = player_data.get("wins", 0)
            matches = player_data.get("matches_played", 0)
            win_rate = f"{player_data.get('win_rate', 0):.2f}%"
    
    # PATCH USER: Update user details
    if request.method == 'PATCH':
        print(f"PATCH data sent to API for user update: {request.body}")        
        # ERRORS: Parse PATCH data (since Django doesn't parse PATCH by default)
        try:
            form_data = json.loads(request.body)
        except json.JSONDecodeError:
            print(f"Invalid JSON in request body: {request.body}")
            return JsonResponse({'error': 'Invalid JSON in request body.'}, status=400)

        # ERRORS: Handle client-side errors (form validation)
        form_data, form_error = process_form_data(request)
        if form_error:
            print (f"Client-side error: {form_error}")
            return JsonResponse({'error': form_error}, status=400)
        print(f"Form data: {form_data}")
        
        # Prepare data for API update (only modified fields)
        update_data = {k: v for k, v in form_data.items() if v is not None}
        print(f"Update data: {update_data}")
        
        # API CALL: If not client side errors send PATCH data to API
        update_url = urljoin(BASE_API_URL, f"users/{id}/")
        csrf_token = request.COOKIES.get('csrftoken') or get_token(request)
        session.headers.update({'X-CSRFToken': csrf_token, 'Content-Type': 'application/json'})
        response = session.patch(update_url, data=json.dumps(update_data), headers={'X-CSRFToken': csrf_token})

        # ERRORS: Handle server-side errors (API response)
        api_error, data = handle_api_response(response)
        if api_error:
            print (f"Server-side error(s):\n{api_error}")
            # If server-side error then return to the user page
            return JsonResponse({'error': api_error}, status=response.status_code)

        # Refresh user data after successful update        
        request.user.refresh_from_db()
        print(f"API response data: {data}")
        print(f"Updated user: {request.user}")
        # Return a JSON response instead of redirecting
        return JsonResponse({'success': 'User updated successfully.', 'user': data}, status=200)

    # For GET requests render the user profile page
    print(f"Rendering user profile page for user {id}")
    context = {
        'user': request.user,
        'wins': wins,
        'matches': matches,
        'win_rate': win_rate,
        'ranking_position': ranking_position,
        'ranking_total': ranking_total,
    }
    print(f"Context: {context}")
    return render (request, 'frontend/user.html', context)

def process_matches(matches, current_user, user_icon):
    """
    Processes a list of matches by:
    - Highlighting the current user with an icon.
    - Converting date_played from string to date object.
    """
    for match in matches:
        for key in ["team1_player1", "team1_player2", "team2_player1", "team2_player2"]:
            if match[key] == current_user:
                match[key] = user_icon

        if isinstance(match.get("date_played"), str):
            match["date_played"] = datetime.strptime(match["date_played"], "%Y-%m-%d").date()
    
    return matches  # Ensure processed list is returned

@login_required
def match_view(request, client=None):
    """
    Handles match listing, creation, and deletion using PRG (Post/Redirect/Get).
    Tracks new matches involving the user.
    """    
    print(f"User calling match_view: {request.user}")
        
    # Create a session and pre-configure it
    session = requests.Session()
    session.cookies.update(request.COOKIES)  # Update the session cookies from the request    
    csrf_token = request.COOKIES.get('csrftoken') or get_token(request)    
        
    # Fetch players to populate the input form
    players_url = urljoin(BASE_API_URL, "games/players/player_names/")
    print(f"Requesting players names from API: {players_url}")
    players_response = session.get(players_url) # Use 'session.get' instead of 'requests.get'
    print(f"Players API response status code: {players_response.status_code}")      
    error_message, player_data = handle_api_response(players_response)
    print(f"Error message after handle_api_response: {error_message}")    
    
    # Extract registered and non-registered players
    registered_players = player_data.get("registered_players", [])    
    existing_players = player_data.get("non_registered_players", [])    
    # Merge both lists and sort alphabetically by name
    all_players = sorted(
        registered_players + existing_players, 
        key=lambda p: p['name'].lower()) # Case-insensitive sorting    

    # Fetch all matches and pagination
    matches, pagination = fetch_paginated_api_data(request, "games/matches/")
    
    # Fetch only user matches
    user_matches, user_pagination = fetch_paginated_api_data(request,"games/matches/",{"player": request.user.username})
    
    # Get list of new matches
    new_match_ids = get_new_match_ids(request)
    
    # Store new match IDs in session
    request.session['new_matches'] = new_match_ids
    request.session.modified = True  # Ensure session is saved
    
    # Add a Bootstrap icon for the current user and bold text 
    user_icon = mark_safe('<i class="bi bi-person-check-fill"></i><span class="fw-bold">' + request.user.username + '</span>')
    
    # Process matches
    matches = process_matches(matches, request.user.username, user_icon) # All matches processed
    user_matches = process_matches(user_matches, request.user.username, user_icon) # User matches processed
        
    # Add today's date to limit the date picker in the ISO format 'YYYY-MM-DD'
    today = date.today().isoformat()
        
    # Handle POST request: create a new match
    if request.method == 'POST':
        # Create a mutable copy of the POST data and 
        match_data = request.POST.copy()
        # Force team1_player1 to be set to the logged in user
        # ensuring current user is in the match
        match_data['team1_player1'] = request.user.username  
                
        # Check if we have four different participant players
        print ("Validating match data")
        participants = [
        match_data.get('team1_player1'),
        match_data.get('team1_player2'),
        match_data.get('team2_player1'),
        match_data.get('team2_player2')
        ]
        print (f"Participants: {participants}")
        print (f"Logged in user: {request.user.username}")
        if len(set(participants)) != 4:
            messages.error(request, "Try again, you have introduced duplicated players!")
            return redirect('match') # Redirect to the match page using GET
        
        # Send match data as JSON to the API        
        matches_url = urljoin(BASE_API_URL, "games/matches/")
        match_response = session.post(
            matches_url, # url must be the first positional argument
            json=match_data,
            headers={'X-CSRFToken': csrf_token})        
        
        # Log API response
        print(f"API Response Status: {match_response.status_code}")
        print(f"API Response Content: {match_response.content}")
        
        # Handle API response
        error_message, _ = handle_api_response(match_response)
        if error_message:
            messages.error(request, error_message)
            # Log the API response error to the console
            print(f"API response error: {error_message}")        
            return redirect('match') # Redirect to the match page using PRG (POST-Redirect-Get) 
        # If the match is correctly created
        print("Match created successfully")
        messages.success(request, "Match created successfully")
        return redirect('match') # Redirect to the match page using PRG (POST-Redirect-Get)        

    # Handle DELETE request: delete a specific match
    if request.method == 'DELETE':
        delete_data = json.loads(request.body)
        match_id = delete_data.get('match_id')
        if not match_id:
            return JsonResponse({"error": "Match ID not provided."}, status=400)        
    
    # Build the API URL for deleting a specific match
        delete_url = urljoin(BASE_API_URL, f"games/matches/{match_id}/")
        print(f"Requesting deletion of match at URL: {delete_url}")
    
    # Send the DELETE request to the API
        match_response = session.delete(delete_url, headers={'X-CSRFToken': csrf_token})
        print(f"API Response Status: {match_response.status_code}")
        print(f"API Response Content: {match_response.content}")
    
    # Handle API response
        error_message, _ = handle_api_response(match_response)
        if error_message:
            # Log the API response error to the console
            print(f"API response error: {error_message}")        
            return JsonResponse({"error": error_message}, status=400)
    
        # If the match is correctly deleted
        print("Match deleted successfully")
        return JsonResponse({"message": "Match deleted successfully"}, status=200)
        
    # Render the match page in GET requests    
    context = {
        "all_players": all_players,
        "registered_players": registered_players,
        "existing_players": existing_players,
        "matches": matches, # All matches
        "pagination": pagination,
        "user_matches": user_matches, # Matches played by the user
        "user_pagination": user_pagination,
        "new_match_ids": new_match_ids,  # Pass new match IDs to template
        "new_matches_number": len(new_match_ids), # Pass count for the navbar badge
        "today": today,
        "error": None
    }

    # Mark all matches as "seen" when user views match.html
    print("Add new matches as 'seen'")
    request.session['seen_matches'] = list(set(request.session.get('seen_matches', [])).union(new_match_ids))
    print(f"New seen matches: {request.session['seen_matches']}")
    request.session['new_matches'] = []  # Reset the new matches count
    print("Resetting new matches count")
    request.session.modified = True
    
    print("Rendering match.html")
    return render(request, 'frontend/match.html', context)

# Login / logout endpoints 
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)  # Use Django's default login
            return redirect('hall_of_fame')
        else:
            return render(request, 'frontend/login.html', {"error": "Invalid credentials."})
    return render(request, 'frontend/login.html')

@login_required  # The login_required decorator ensures the user is logged in 
# otherwise redirects him to the login page 
# (set in settings.py with LOGIN_URL='/login/')
def logout_view(request):
    if request.method == 'POST':
        logout(request)  # Use Django's default logout
        return redirect('hall_of_fame') # Redirect to the home page after logout   
    return redirect('login') # Redirect to the login page for GET requests to logout


