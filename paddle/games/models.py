from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensure player names are unique to avoid duplicates
    registered_user = models.OneToOneField('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)
    win_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class Match(models.Model):
    teams = models.JSONField()  # Dictionary with two lists: {"team_1": [player1_id, player2_id], "team_2": [player3_id, player4_id]}
    winning_team = models.IntegerField()  # 1 for team 1, 2 for team 2
    date_played = models.DateField()  # Date of the match without time, set manually

    def __str__(self):
        return f"Match on {self.date_played}"


