# absolute path: /workspaces/paddle/paddle/frontend/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from games.models import Player

User = get_user_model()


class PlayerInline(admin.StackedInline):
    """
    Admin-only inline to view/edit the Player linked to a User.
    This improves traceability and allows setting gender without navigating away.
    """
    model = Player
    fk_name = "registered_user"
    extra = 0
    can_delete = False

    # Keep username/player name alignment stable: name is shown but not edited here.
    fields = ("name", "gender", "ranking_position")
    readonly_fields = ("name", "ranking_position")

# Unregister default User admin (registered by django.contrib.auth)
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    inlines = [PlayerInline]
