from django.shortcuts import render

from rest_framework import viewsets
from .models import Player, Match
from .serializers import PlayerSerializer, MatchSerializer
from rest_framework.permissions import IsAuthenticated

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all().order_by('-wins')
    serializer_class = PlayerSerializer
  
    def perform_update(self, serializer):
        player = serializer.instance
        player.matches_played = player.wins + player.losses
        player.win_rate = player.wins / player.matches_played if player.matches_played > 0 else 0.0
        serializer.save()

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        match = serializer.save()
        self.update_player_stats(match)

    def perform_update(self, serializer):
        match = serializer.save()
        self.update_player_stats(match)
    
    def update_player_stats(self, match):
        # Update players' stats based on match outcome
        team_1_players = match.teams.get('team_1', [])
        team_2_players = match.teams.get('team_2', [])

        # Determine the winning and losing teams
        if match.winning_team == 1:
            winning_players = team_1_players
            losing_players = team_2_players
        else:
            winning_players = team_2_players
            losing_players = team_1_players

        # Update win/loss stats for each player
        for player_id in winning_players:
            player = Player.objects.get(id=player_id)
            player.wins += 1
            player.matches_played += 1
            player.win_rate = player.wins / player.matches_played if player.matches_played > 0 else 0.0
            player.save()

        for player_id in losing_players:
            player = Player.objects.get(id=player_id)
            player.losses += 1
            player.matches_played += 1
            player.win_rate = player.wins / player.matches_played if player.matches_played > 0 else 0.0
            player.save()

