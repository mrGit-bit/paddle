# games/models.py

from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Unique player name
    # Optional link to a registered user
    registered_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)  
    wins = models.IntegerField(default=0)  # Tracks the number of wins
    # Store matches the player participated in
    matches = models.ManyToManyField('Match', related_name='players', blank=True)

    def __str__(self):
        return self.name


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

    def get_players_by_result(self):
        """Retrieve lists of winning and losing players.
        Keeps the model logic separated from the serializer logic, 
        inside the Match model, where it belongs.        
        """
        
        if self.winning_team == 1:
            winning_players = [self.team1_player1.name, self.team1_player2.name]
            losing_players = [self.team2_player1.name, self.team2_player2.name]

        elif self.winning_team == 2:
            winning_players = [self.team2_player1.name, self.team2_player2.name]
            losing_players = [self.team1_player1.name, self.team1_player2.name]
        
        # not applicable because winning_team is not null and only 1 or 2 is allowed
        # else:
        #     winning_players = []
        #     losing_players = []

        return winning_players, losing_players

    


