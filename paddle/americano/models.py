# americano/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone

from games.models import Player  # adjust if your Player model lives elsewhere


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

    def get_standings(self):
        """
        Ordered by wins desc, then points_diff desc.
        Returns list of dict rows ready for template.
        """
        standings = []
        for stats in self.player_stats.select_related("player").all():
            points_diff = stats.points_for - stats.points_against
            standings.append(
                {
                    "player": stats.player,
                    "wins": stats.wins,
                    "points_for": stats.points_for,
                    "points_against": stats.points_against,
                    "points_diff": points_diff,
                }
            )

        return sorted(
            standings,
            key=lambda s: (s["wins"], s["points_diff"]),
            reverse=True,
        )


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

    class Meta:
        ordering = ["court_number"]

    def __str__(self):
        return f"{self.round.tournament.name} - R{self.round.number} - Court {self.court_number}"

    def update_player_stats(self):
        """
        Adds match points + win/loss to AmericanoPlayerStats.
        Note: for now this is additive and assumes results are entered once.
        We'll harden it later (idempotent updates) once UI is stable.
        """
        if self.winner_team is None:
            return
        if self.team1_points is None or self.team2_points is None:
            return

        tournament = self.round.tournament

        team1_players = [self.team1_player1, self.team1_player2]
        team2_players = [self.team2_player1, self.team2_player2]

        for player in team1_players:
            stats, _ = AmericanoPlayerStats.objects.get_or_create(tournament=tournament, player=player)
            stats.points_for += self.team1_points
            stats.points_against += self.team2_points
            if self.winner_team == 1:
                stats.wins += 1
            else:
                stats.losses += 1
            stats.save()

        for player in team2_players:
            stats, _ = AmericanoPlayerStats.objects.get_or_create(tournament=tournament, player=player)
            stats.points_for += self.team2_points
            stats.points_against += self.team1_points
            if self.winner_team == 2:
                stats.wins += 1
            else:
                stats.losses += 1
            stats.save()
