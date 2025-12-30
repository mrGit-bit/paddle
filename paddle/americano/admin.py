from django.contrib import admin

from .models import (
    AmericanoTournament,
    AmericanoRound,
    AmericanoMatch,
    AmericanoPlayerStats,
)

class AmericanoRoundInline(admin.TabularInline):
    model = AmericanoRound
    extra = 0
    fields = ("number",)
    show_change_link = True


class AmericanoMatchInline(admin.TabularInline):
    model = AmericanoMatch
    extra = 0
    fields = (
        "court_number",
        "team1_player1",
        "team1_player2",
        "team2_player1",
        "team2_player2",
        "team1_points",
        "team2_points",
    )
    show_change_link = True


@admin.register(AmericanoTournament)
class AmericanoTournamentAdmin(admin.ModelAdmin):
    inlines = [AmericanoRoundInline]
    list_display = ("name", "play_date", "is_active", "created_by", "players_count")
    list_filter = ("is_active", "play_date")
    search_fields = ("name", "created_by__username", "players__name")
    filter_horizontal = ("players",)
    ordering = ("-play_date", "name")

    @admin.display(description="Players")
    def players_count(self, obj):
        return obj.players.count()


@admin.register(AmericanoRound)
class AmericanoRoundAdmin(admin.ModelAdmin):
    inlines = [AmericanoMatchInline]
    list_display = ("tournament", "number", "matches_count")
    list_filter = ("tournament",)
    ordering = ("tournament", "number")

    @admin.display(description="Matches")
    def matches_count(self, obj):
        return obj.matches.count()

@admin.register(AmericanoPlayerStats)
class AmericanoPlayerStatsAdmin(admin.ModelAdmin):
    list_display = ("tournament", "player", "wins", "points_for", "points_against")
    list_filter = ("tournament",)
    search_fields = ("tournament__name", "player__name")
    ordering = ("tournament", "-wins", "-points_for")
