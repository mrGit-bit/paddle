"""Auth, profile, registration, and about views.

Responsibilities:
- Register/login/logout handlers.
- User profile update handler.
- About page handler and form-data parsing helper.

Integration:
- Uses shared helpers in `common.py`.
- In selected paths, resolves helpers via `frontend.views` facade to preserve
  monkeypatch compatibility expected by existing tests.
"""

import json
from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render

from games.models import Match, Player

from .common import fetch_available_players

User = get_user_model()


def process_form_data(request):
    """
    Extract and validate form data from the request.
    Supports both POST (for registration) and PATCH (for user profile updates).
    Ensures non-editable fields are set to None in PATCH requests.
    """
    form_data = {}

    if request.method == "POST":
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

    elif request.method == "PATCH":
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
    if request.method == "POST":
        form_data, form_error = process_form_data(request)
        if form_error:
            messages.error(request, form_error)
            return redirect("register")

        user_exists = User.objects.filter(username__iexact=form_data["username"]).exists()
        player_exists = (
            Player.objects.filter(
                name__iexact=form_data["username"], registered_user__isnull=True
            )
            .exclude(id=form_data.get("player_id"))
            .exists()
        )
        if user_exists or player_exists:
            messages.error(
                request,
                (
                    "Error: Ya existe un usuario o un jugador con el nombre "
                    f"'{form_data['username']}'. Cambia el nombre del usuario o selecciona "
                    "el jugador existente en el desplegable de jugadores."
                ),
            )
            return redirect("register")

        gender = form_data.get("gender")
        allowed_genders = {Player.GENDER_MALE, Player.GENDER_FEMALE}
        if gender not in allowed_genders:
            messages.error(request, "Error: por favor, selecciona un género válido.")
            return redirect("register")

        user = User(username=form_data["username"], email=form_data["email"])
        user.set_password(form_data["password"])
        user.save()

        player_id = form_data.get("player_id")
        if player_id:
            player = Player.objects.filter(id=player_id, registered_user__isnull=True).first()
            if player:
                player.registered_user = user
                player.name = user.username
                player.gender = gender
                player.save()
            else:
                messages.error(request, "Selected player is already linked or does not exist.")
                user.delete()
                return redirect("register")
        else:
            Player.objects.create(
                name=user.username,
                registered_user=user,
                gender=gender,
            )

        login(request, user)
        return redirect("match")

    registered_players, non_registered_players = fetch_available_players()
    players = [(p["id"], p["name"]) for p in non_registered_players]
    return render(request, "frontend/register.html", {"players": players})


@login_required
def user_view(request, id):
    if request.user.id != id:
        return JsonResponse({"error": "You are not authorized to view this profile."}, status=403)

    user_player = Player.objects.filter(registered_user=request.user).first()
    total_players = Player.objects.count()

    if request.method == "PATCH":
        try:
            json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body."}, status=400)

        from frontend import views as frontend_views

        form_data, form_error = frontend_views.process_form_data(request)
        if form_error:
            return JsonResponse({"error": form_error}, status=400)

        update_data = {k: v for k, v in form_data.items() if v is not None and k == "email"}
        if update_data.get("email"):
            request.user.email = update_data["email"]
            request.user.save()
            request.user.refresh_from_db()
            return JsonResponse(
                {
                    "success": "Datos actualizados",
                    "user": {
                        "id": request.user.id,
                        "username": request.user.username,
                        "email": request.user.email,
                    },
                },
                status=200,
            )
        return JsonResponse({"error": "No valid fields to update."}, status=400)

    context = {
        "user": request.user,
        "user_player": user_player,
        "total_players": total_players,
    }
    return render(request, "frontend/user.html", context)


def login_view(request):
    if request.method == "POST":
        raw_identifier = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""

        user_obj = None
        if "@" in raw_identifier:
            user_obj = User.objects.filter(email__iexact=raw_identifier).first()
        else:
            user_obj = User.objects.filter(username__iexact=raw_identifier).first()

        resolved_username = user_obj.username if user_obj else raw_identifier

        user = authenticate(request, username=resolved_username, password=password)

        if user:
            login(request, user)
            return redirect("hall_of_fame")

        return render(request, "frontend/login.html", {"error": "Nombre o contraseña no válidos."})

    return render(request, "frontend/login.html")


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("hall_of_fame")
    return redirect("login")


def about_view(request):
    """
    Renders the About page with stats: number of users, players, matches since 1 Sept 2025.
    """
    from frontend import views as frontend_views

    num_users = User.objects.count()
    num_players = Player.objects.count()
    num_matches = Match.objects.filter(date_played__gte=date(2025, 9, 1)).count()
    contact_email = "rankingdepadel.club@gmail.com"

    context = {
        "num_users": num_users,
        "num_players": num_players,
        "num_matches": num_matches,
        "contact_email": contact_email,
        "app_version_label": frontend_views.get_about_app_version_label(),
    }
    return render(request, "frontend/about.html", context)
