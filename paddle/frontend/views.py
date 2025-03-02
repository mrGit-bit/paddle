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

def hall_of_fame_view(request):
    url = urljoin(BASE_API_URL, "games/players/")
    print(f"{request.user} (Authenticated: {request.user.is_authenticated}) calling hall_of_fame_view...")    
    print(f"Requesting API url: {url}")
    # instead of using 'response = requests.get(url)' 
    # (that would work anyway because HoF is an open endpoint)
    # we use request.Session() for consistency with other endpoints
    session = requests.Session()
    session.cookies.update(request.COOKIES) # Maintain the session cookies from the request
    response = session.get(url)    
    # print("API response content:", response.json())
    
    if response.status_code == 200:
        # 'results' is the usual key wrapper for the JSON content
        # in the API response. Is used in DRF for the content
        # when using pagination functionality
        players = response.json().get('results', [])
    else:
        print(f"API request failed with status code: {response.status_code}")
        print("Falling back to an empty list of players")
        players = []  # Fallback in case of API failure

    return render(request, "frontend/hall_of_fame.html", {"players": players})

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
        # If a success callback is provided, process the response data
        if success_callback:
            return None, success_callback(response)
        # If no success callback is provided, return the response data
        # and None for the error message
        return None, response.json()
    
    # Handle error response
    try:
        errors = response.json()
        if isinstance(errors, dict):
            error_messages = [f"{field.capitalize()}: {', '.join(messages)}" if isinstance(messages, list) else f"{field.capitalize()}: {messages}"
                              for field, messages in errors.items()]
            return "\n".join(error_messages), None
        return str(errors), None
    except ValueError:
        return "An unexpected error occurred.", None

def fetch_available_players(session, request):
    """
    Fetch non-linked players from the API endpoint for names.
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

@login_required
def user_view(request, id):
    print(f"Received request for user {id}: {request.method}")
    session = requests.Session()
    session.cookies.update(request.COOKIES)
    
    # Ensure the user can only access their own profile
    if request.user.id != id:
        print(f"Unauthorized access attempt by {request.user.username} to user {id}")
        return JsonResponse({'error': 'You are not authorized to view this profile.'}, status=403)
    
    # GET DATA: Fetch user data from the API
    try:
        user = request.user  # Get the currently logged-in user
    except User.DoesNotExist:
        print(f"User {id} not found.")
        return JsonResponse({'error': 'User not found.'}, status=404)

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
        user.refresh_from_db()
        print(f"API response data: {data}")
        print(f"Updated user: {user}")
        # Return a JSON response instead of redirecting
        return JsonResponse({'success': 'User updated successfully.', 'user': data}, status=200)

    # For GET requests render the user profile page
    print(f"Rendering user profile page for user {id}")
    return render (request, 'frontend/user.html', {"user": user})

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

def match_view(request, client=None):
    # Debug requesting user
    print("Starting match_view")
    print(f"User calling match_view: {request.user} (Authenticated: {request.user.is_authenticated})")
        
    # Create a session and pre-configure it
    session = requests.Session()
    session.cookies.update(request.COOKIES)  # Update the session cookies from the request    
    csrf_token = request.COOKIES.get('csrftoken') or get_token(request)    
        
    # Fetch players to populate the input form
    players_url = urljoin(BASE_API_URL, "games/players/")
    print(f"Requesting players from API: {players_url}")
    players_response = session.get(players_url) # Use session instead of 'requests.get'
    _, players = handle_api_response(players_response, lambda res: res.json().get('results', []))
    
    # Separate registered and non-registered players
    registered_players = [player for player in players if player.get('registered_user')]
    existing_players = [player for player in players if not player.get('registered_user')]
    
    # Fetch all matches 
    matches_url = urljoin(BASE_API_URL, "games/matches/")
    print(f"Requesting matches from API: {matches_url}")    
    matches_response = session.get(matches_url) # Use session instead of 'requests.get'
    _, matches = handle_api_response(matches_response, lambda res: res.json().get('results', []))
    
    # Fetch only matches where the user has played
    user_matches_url = f"{matches_url}?player={request.user.username}"
    print(f"Requesting user matches from API: {user_matches_url}")
    user_matches_response = session.get(user_matches_url)
    _, user_matches = handle_api_response(user_matches_response, lambda res: res.json().get('results', []))
    
    # Add a Bootstrap icon for the current user and bold text 
    user_icon = mark_safe('<i class="bi bi-person-check-fill"></i><span class="fw-bold">' + request.user.username + '</span>')
    
    # Process matches
    matches = process_matches(matches, request.user.username, user_icon) # All matches processed
    user_matches = process_matches(user_matches, request.user.username, user_icon) # User matches processed
        
    # Add today's date to limit the date picker in the ISO format 'YYYY-MM-DD'
    today = date.today().isoformat()
    
    # Centralized context dictionary
    context = {
        "players": players,
        "registered_players": registered_players,
        "existing_players": existing_players,
        "matches": matches, # All matches
        "user_matches": user_matches, # Matches played by the user
        "today": today,
        "error": None
    }
        
    # Handle POST request: create a new match        
    if request.method == 'POST':
        # Create a mutable copy of the POST data and 
        match_data = request.POST.copy()
        # ensure team1_player1 is set to the current user
        match_data['team1_player1'] = request.user.username  # Ensure current user is in the match (as team1_player1)
                
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
            context["error"] = "Try again, you have introduced duplicated players!"
            return render(request, 'frontend/match.html', context)            
        
        # Send match data as JSON to the API        
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
            context["error"] = error_message
            # Log the API response error to the console
            print(f"API response error: {error_message}")        
            return render(request, 'frontend/match.html', context)
        # If the match is correctly created then redirect to the hall of fame
        print("Match created successfully, redirecting to the hall of fame")
        return redirect('hall_of_fame')       

    # Handle GET request: display the match form and a list of all matches played    
    print("Rendering match.html")
    return render(request, 'frontend/match.html', context)


@login_required
def delete_match_view(request, id):
    """
    View to delete a match by its ID. Only accessible to logged-in users.
    """
    # Debug the requesting user
    print(f"User calling delete_match_view: {request.user} (Authenticated: {request.user.is_authenticated})")

    # Create a session and pre-configure it
    session = requests.Session()
    session.cookies.update(request.COOKIES)  # Update the session cookies from the request    
    csrf_token = request.COOKIES.get('csrftoken') or get_token(request)
    
    # Build the API URL for deleting a specific match
    delete_url = urljoin(BASE_API_URL, f"games/matches/{id}/")
    print(f"Requesting deletion of match at URL: {delete_url}")

    # Send the DELETE request to the API
    response = session.delete(delete_url, headers={'X-CSRFToken': csrf_token})
    print(f"API Response Status: {response.status_code}")
    print(f"API Response Content: {response.content}")

    # Handle API response
    if response.status_code == 204:  # Successful deletion
        print("Match deleted successfully.")
        return redirect('match')
    elif response.status_code == 403:  # Forbidden, user not authorized
        print("Deletion forbidden: User not authorized to delete this match.")
        return HttpResponseForbidden("You are not authorized to delete this match.")
    else:
        error_message, _ = handle_api_response(response)
        print(f"Error deleting match: {error_message}")
        return render(request, 'frontend/match.html', {"error": error_message})

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


