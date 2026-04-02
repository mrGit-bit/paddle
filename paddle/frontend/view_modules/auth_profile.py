"""Auth, profile, registration, and about views."""

from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.db.models.functions import Lower

from games.models import Match, Player
from frontend.forms import EMAIL_WARNING_TEXT, ProfileUpdateForm, RegistrationForm

from .common import compute_player_stats

User = get_user_model()

def register_view(request):
    player_queryset = (
        Player.objects.filter(registered_user__isnull=True)
        .select_related("group")
        .order_by(Lower("group__name"), Lower("name"))
    )

    if request.method == "POST":
        form = RegistrationForm(request.POST, player_queryset=player_queryset)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("hall_of_fame")
    else:
        initial = {}
        if request.GET.get("create_group") == "1":
            initial["group_mode"] = RegistrationForm.GROUP_MODE_CREATE
        form = RegistrationForm(player_queryset=player_queryset, initial=initial)

    return render(
        request,
        "frontend/register.html",
        {
            "form": form,
            "email_warning_text": EMAIL_WARNING_TEXT,
        },
    )


def _build_user_page_context(request, form):
    user_player = Player.objects.filter(registered_user=request.user).first()
    total_players = Player.objects.count()
    player_stats = compute_player_stats(user_player)

    return {
        "profile_form": form,
        "email_warning_text": EMAIL_WARNING_TEXT,
        "user_player": user_player,
        "total_players": total_players,
        "wins": player_stats["wins"],
        "matches": player_stats["matches"],
        "win_rate": player_stats["win_rate"],
    }


@login_required
def user_view(request, id):
    if request.user.id != id:
        return HttpResponseForbidden("No tienes permiso para editar este perfil.")

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Tus datos se han actualizado correctamente.")
            return redirect("user", id=request.user.id)
    else:
        form = ProfileUpdateForm(user=request.user)

    context = _build_user_page_context(request, form)
    return render(request, "frontend/user.html", context)


@login_required
def user_delete_view(request, id):
    if request.user.id != id:
        return HttpResponseForbidden("No tienes permiso para eliminar esta cuenta.")

    user_player = Player.objects.filter(registered_user=request.user).first()

    if request.method == "POST":
        with transaction.atomic():
            if user_player:
                user_player.registered_user = None
                user_player.save(update_fields=["registered_user"])
            request.user.delete()
        logout(request)
        messages.success(request, "Tu cuenta se ha eliminado correctamente. Hasta pronto.")
        return redirect("hall_of_fame")

    return render(
        request,
        "frontend/user_confirm_delete.html",
        {
            "user_player": user_player,
        },
    )


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
