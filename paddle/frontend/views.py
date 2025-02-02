# frontend/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from games.models import Player
import requests
from urllib.parse import urljoin
from datetime import date
from django.middleware.csrf import get_token

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

def register_view(request):
    session = requests.Session()
    session.cookies.update(request.COOKIES) # Update the session cookies from the request
    
    if request.method == 'POST':        
        print(f"Data sent to API: {request.POST}")
        # Check if passwords match
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            print("Passwords do not match")
            return render(request, 'frontend/register.html', {"error": "Passwords do not match."})

        # Send registration data to the users app via API
        url = urljoin(BASE_API_URL, "users/")
        csrf_token = request.COOKIES.get('csrftoken') or get_token(request)
        session.headers.update({'X-CSRFToken': csrf_token})  # ✅ Ensure CSRF token is sent
        response = session.post(url, data=request.POST, headers={'X-CSRFToken': csrf_token})
        print(f"API response status: {response.status_code}")
        print(f"API response content: {response.content}")
        
        # Handle API response
        error_message, data = handle_api_response(response)
        print (f"API response error: {error_message}")
        print(f"API response data: {data}")
        
        if error_message:
            return render(request, 'frontend/register.html', {"error": error_message})

        
        # Authenticate and log in after successful registration
        username = request.POST.get("username")                
        user = User.objects.get(username=username)
        print (f"Created user: {user}")
        if user.check_password(password):
            login(request, user)  # Log in the user with session
            print(f"Authenticated user: {request.user}")
            return redirect('hall_of_fame')     
        # If authentication fails then return to the register page
        return render(request, 'frontend/register.html', {"error": error_message.strip()})

    # Fetch non-linked players from the API endpoint    
    print(f"{request.user} calling available players to populate the register_view...")
    url = urljoin(BASE_API_URL, "games/players/")
    print(f"is requesting API url: {url}")
    response = session.get(url) # Use session instead of 'requests.get
    _, data = handle_api_response(response)
    players = [
        (player['id'], player['name'])
        for player in data.get('results', []) if player.get('registered_user') is None
    ] if data else []
    
    # Render the registration form with available players context
    return render(request, 'frontend/register.html', {"players": players})

def match_view(request, client=None):
    # Debug requesting user
    print("Starting match_view")
    print(f"User calling match_view: {request.user} (Authenticated: {request.user.is_authenticated})")
        
    # Create a session and pre-configure it
    session = requests.Session()
    session.cookies.update(request.COOKIES)  # Update the session cookies from the request    
    csrf_token = request.COOKIES.get('csrftoken') or get_token(request)
    print(f"Retrieved CSRF token in cookies: {csrf_token}")    
        
    # Fetch players to populate the input form
    players_url = urljoin(BASE_API_URL, "games/players/")
    print(f"Requesting players from API: {players_url}")
    # players_response = session.get(players_url)
    players_response = session.get(players_url) # Use session instead of 'requests.get'
    _, players = handle_api_response(players_response, lambda res: res.json().get('results', []))
    # Separate registered and non-registered players
    registered_players = [player for player in players if player.get('registered_user')]
    existing_players = [player for player in players if not player.get('registered_user')]
    
    # Fetch all matches for the match.html GET template
    matches_url = urljoin(BASE_API_URL, "games/matches/")
    print(f"Requesting matches from API: {matches_url}")
    # matches_response = session.get(matches_url)
    matches_response = session.get(matches_url) # Use session instead of 'requests.get'
    _, matches = handle_api_response(matches_response, lambda res: res.json().get('results', []))
    
    # Add today's date to limit the date picker in the ISO format 'YYYY-MM-DD'
    today = date.today().isoformat()
    
    # Centralized context dictionary for all the possible rendering situations
    context = {
        "players": players,
        "registered_players": registered_players,
        "existing_players": existing_players,
        "matches": matches,
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
        print (f"CSRF Token sent to API: {csrf_token}")
        print (f"Cookies sent to API: {session.cookies}")
        print (f"Headers sent to API: {session.headers}")
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
    print("Rendering match.html template with context data and CSRF token")
    return render(request, 'frontend/match.html', context)

def user_view(request, id):
    session = requests.Session()
    session.cookies.update(request.COOKIES)  # Maintain session cookies
    if request.method == 'POST':
        url = urljoin(BASE_API_URL, f"users/{id}/")
        response = session.put(url, data=request.POST, headers={"Authorization": f"Bearer {request.session['user']['token']}"})
        if response.status_code == 200:
            return redirect('hall_of_fame')
        return render(request, 'frontend/user_details.html', {"error": response.json()})

    url = urljoin(BASE_API_URL, f"users/{id}/")
    response = requests.get(url)
    if response.status_code == 200:
        return render(request, 'frontend/user_details.html', {"user": response.json()})
    return render(request, 'frontend/user_details.html', {"error": "User not found."})

def handle_api_response(response, success_callback=None):
    """
    Handles API responses, extracting errors or passing the data to a callback.

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
        
        # Handle single-field errors (e.g., "detail": "C")
        if isinstance(errors, dict):
            # "detail" is a common error field in DRF error responses
            if "detail" in errors:  
                return errors["detail"], None
        
            # Generalize field-specific errors (e.g., "username": ["This field is required."])
            error_message = ""
            for field, messages in errors.items():
                if isinstance(messages, list):
                    error_message += f"{field.capitalize()}: {messages[0]} "
                else:
                    error_message += f"{field.capitalize()}: {messages} "
            return error_message.strip(), None        
        
        # Handle non-dict errors
        return str(errors), None
    
    # Handle non-JSON responses
    except ValueError:
        return "An error occurred.", None

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

# Endpoints for future functionalities
# def player_view(request, id):
#     url = urljoin(BASE_API_URL, f"games/players/{id}/")
#     response = requests.get(url)
#     if response.status_code == 200:
#         return render(request, 'frontend/player_details.html', {"player": response.json()})
#     return render(request, 'frontend/player_details.html', {"error": "Player not found."})

# def stats_view(request):
#     url = urljoin(BASE_API_URL, "games/stats/")
#     response = requests.get(url)
#     if response.status_code == 200:
#         return render(request, 'frontend/stats.html', {"stats": response.json()})
#     return render(request, 'frontend/stats.html', {"error": "Stats not available."})

