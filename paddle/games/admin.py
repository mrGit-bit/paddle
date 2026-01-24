# absolute path: /workspaces/paddle/paddle/games/admin.py

from django.contrib import admin
from .models import Player, Match
from django.utils.html import format_html

class GenderMissingFilter(admin.SimpleListFilter):
    title = "gender missing"
    parameter_name = "gender_missing"

    def lookups(self, request, model_admin):
        return [("1", "Yes")]

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(gender__isnull=True)
        return queryset

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "gender", "registered_user", "ranking_position")
    list_filter = ("gender", GenderMissingFilter)
    search_fields = ("name", "registered_user__username", "registered_user__email")
    ordering = ("ranking_position", "name")
    actions = ("set_gender_male", "set_gender_female")

    @admin.action(description="Set gender to Male (M)")
    def set_gender_male(self, request, queryset):
        queryset.update(gender=Player.GENDER_MALE)

    @admin.action(description="Set gender to Female (F)")
    def set_gender_female(self, request, queryset):
        queryset.update(gender=Player.GENDER_FEMALE)



@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        "date_played",
        "match_gender_type",
        "winning_team",
        "team1_player1",
        "team1_player2",
        "team2_player1",
        "team2_player2",
        "players_with_gender",
    )
    list_filter = ("match_gender_type", "date_played", "winning_team")
    search_fields = (
        "team1_player1__name",
        "team1_player2__name",
        "team2_player1__name",
        "team2_player2__name",
    )
    ordering = ("-date_played",)

    @admin.display(description="Players (gender)")
    def players_with_gender(self, obj):
        def fmt(p):
            if not p:
                return "-"
            g = p.gender or "?"
            return f"{p.name} ({g})"

        return format_html(
            "{} / {}  vs  {} / {}",
            fmt(obj.team1_player1),
            fmt(obj.team1_player2),
            fmt(obj.team2_player1),
            fmt(obj.team2_player2),
        )


