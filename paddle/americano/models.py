# americano/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone

from games.models import Player  


class AmericanoTournament(models.Model):
    name = models.CharField(max_length=100)
    play_date = models.DateField(default=timezone.localdate)
    num_players = models.PositiveIntegerField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="americano_tournaments",
    )
    players = models.ManyToManyField(Player, related_name="americano_tournaments")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.play_date})"

    @property
    def is_open_for_edit(self) -> bool:
        """
        Editable only until the tournament day (inclusive).
        """
        today = timezone.localdate()
        return self.is_active and self.play_date >= today

    @property
    def is_finished(self) -> bool:
        """
        Finished after tournament day.
        """
        today = timezone.localdate()
        return self.play_date < today


class AmericanoPlayerStats(models.Model):
    tournament = models.ForeignKey(
        AmericanoTournament,
        on_delete=models.CASCADE,
        related_name="player_stats",
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="americano_stats",
    )

    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    matches_played = models.PositiveIntegerField(default=0)
    points_for = models.PositiveIntegerField(default=0)
    points_against = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("tournament", "player")

    def __str__(self):
        return f"{self.tournament.name} - {self.player.name}"


class AmericanoRound(models.Model):
    tournament = models.ForeignKey(
        AmericanoTournament,
        on_delete=models.CASCADE,
        related_name="rounds",
    )
    number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("tournament", "number")
        ordering = ["number"]

    def __str__(self):
        return f"{self.tournament.name} - Ronda {self.number}"


class AmericanoMatch(models.Model):
    round = models.ForeignKey(
        AmericanoRound,
        on_delete=models.CASCADE,
        related_name="matches",
    )
    court_number = models.PositiveIntegerField(null=True, blank=True)

    team1_player1 = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True, blank=True, related_name="americano_t1p1"
    )
    team1_player2 = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True, blank=True, related_name="americano_t1p2"
    )
    team2_player1 = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True, blank=True, related_name="americano_t2p1"
    )
    team2_player2 = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True, blank=True, related_name="americano_t2p2"
    )

    team1_points = models.PositiveIntegerField(null=True, blank=True)
    team2_points = models.PositiveIntegerField(null=True, blank=True)

    winner_team = models.PositiveSmallIntegerField(
        choices=((1, "Team 1"), (2, "Team 2")),
        null=True,
        blank=True,
    )

    def __str__(self):
        court = self.court_number if self.court_number is not None else "—"
        return f"{self.round.tournament.name} - R{self.round.number} - Court {court}"

    # Stats are recomputed from saved matches in views.py to remain idempotent.
    # Idempotent means that updating or re‑saving a match does not double‑count its stats.
