# games/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, BasePermission
from .models import Player, Match
from .serializers import PlayerSerializer, MatchSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations related to players.
    """
    queryset = Player.objects.all().order_by('-wins')
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated] # Default permission at view level    

    def get_permissions(self):
        """
        Returns the permissions for each action based on the type of request.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser] # only admin user can modify players        
        elif self.action == 'list':  # 'list' (Hall of Fame) action is open to anyone        
            permission_classes = [AllowAny]
        elif self.action == 'retrieve':  # 'retrieve' action is only for authenticated users
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated] # Default permission
        return [permission() for permission in permission_classes]

class IsMatchParticipant(BasePermission):
    """
    Custom permission to check if the user is a participant in the match.
    Admin users bypass this check.
    """
    def has_object_permission(self, request, view, obj):
        # Allow admin users unrestricted access
        if request.user.is_staff:
            return True

        # Check if the requesting user is a registered participant in the match
        players = [
            obj.team1_player1.registered_user,
            obj.team1_player2.registered_user,
            obj.team2_player1.registered_user,
            obj.team2_player2.registered_user,
        ]
        return request.user in players


class MatchViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations related to matches.
    """
    queryset = Match.objects.all().order_by('-date_played')
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated] # Default permission at view level    

    def get_permissions(self):
        """
        Define permissions for specific actions.
        """
        # Only match participants can modify an existing match
        if self.action in ['update', 'partial_update', 'destroy']:
        # All the permissions in the list must be true (behavior is AND)
            permission_classes = [IsAuthenticated, IsMatchParticipant]
        # Authenticated users can 'create', 'list' and 'retrieve'
        else: 
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """
        Override the default behavior of saving a new instance
        allowing us to update players' stats
        """
        match = serializer.save()
        # Update players' win & matches stats after the match has been saved
        self.update_player_stats(match)

    def perform_update(self, serializer):
        """
        Reset old players' stats before updating the match
        and update new players' stats
        """
        # Get the old state of the match before updating
        old_match = self.get_object()
        old_winning_players, old_losing_players = old_match.get_players_by_result()
        
        # Reset stats for all players in the old match
        for player_name in old_winning_players + old_losing_players:
            player = Player.objects.get(name__iexact=player_name)
            if old_match.id in player.matches.values_list('id', flat=True):
                player.matches.remove(old_match)
            if player_name in old_winning_players:
                player.wins -= 1
            player.save()

        # Update the match instance and stats
        match = serializer.save()        
        self.update_player_stats(match)

    def update_player_stats(self, match):
        """
        Updates only the wins and matches fields of the players involved in the match.
        because number of matches played, win rate, and losses are not fields in the Player model,
        and are calculated dynamically in PlayerSerializer.py
        """
        # Retrieve the winning and losing players using the model´s method
        winning_players, losing_players = match.get_players_by_result()

        # Update win/loss stats for winning players
        for player_name in winning_players:
            player = Player.objects.get(name__iexact=player_name)
            player.wins += 1
            if match.id not in player.matches.values_list('id', flat=True):
                player.matches.add(match)           
            player.save()

        # Update loss stats for losing players
        for player_name in losing_players:
            player = Player.objects.get(name__iexact=player_name)
            if match.id not in player.matches.values_list('id', flat=True):
                player.matches.add(match)
            player.save()
    
    

