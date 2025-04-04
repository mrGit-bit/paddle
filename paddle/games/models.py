# games/models.py

from django.db import models
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Unique player name enforced later
    registered_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True) # Optional link to a registered user
    wins = models.IntegerField(default=0)  # Tracks the number of wins    
    matches = models.ManyToManyField('Match', related_name='players', blank=True) # Store matches the player has participated in
    ranking_position = models.PositiveIntegerField(default=0)

    class Meta:
        """
        Forces the database to store and check names case-insensitively.
        For instance: prevents the creation of players like "john" and "John" separately.
        """
        constraints = [
            models.UniqueConstraint(
                Lower('name'), 
                name='unique_lower_name', 
                violation_error_message="Player name must be unique (case insensitive)"
            )
        ]
    
    def __str__(self):
        return self.name
    
    # ==== Calculated player stats ====
    @property
    def matches_played(self):
        if not self.id:
            return 0
        return self.matches.count()

    @property
    def win_rate(self):
        if self.matches_played == 0:
            return 0.0
        return (self.wins / self.matches_played) * 100
    
    @property
    def losses(self):
        return max(0, self.matches_played - self.wins)
    
    # Data integrity is enforced in views/serializers to avoid partial updates 
    # during cascading changes  (e.g., match deletions).



class Match(models.Model):    
    # For players, using ForeignKey to establish proper relationships with Player model
    # Team 1 players
    team1_player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='team1_player1')  
    team1_player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='team1_player2')
    # Team 2 players
    team2_player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='team2_player1')
    team2_player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='team2_player2')
    
    winning_team = models.IntegerField(choices=[(1, "Team 1"), (2, "Team 2")], null=False)  
    date_played = models.DateField()  # Date of the match

    def __str__(self):
        return f"Match on {self.date_played}"

    # ==== Calculated match properties ====
    @property
    def all_players(self):
        return [
            self.team1_player1,
            self.team1_player2,
            self.team2_player1,
            self.team2_player2,
        ]

    @property
    def winning_players(self):
        if self.winning_team == 1:
            return [self.team1_player1, self.team1_player2]
        elif self.winning_team == 2:
            return [self.team2_player1, self.team2_player2]
        return []

    @property
    def losing_players(self):
        return [p for p in self.all_players if p not in self.winning_players]
    


