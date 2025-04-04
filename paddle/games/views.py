# games/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Player, Match
from .serializers import PlayerSerializer, MatchSerializer

def update_player_rankings():  
    """
    Calculate the ranking position of the player.
    Ranked by wins, then by win rate, and then by number of matches played.
    """
    players = Player.objects.all()
    sorted_players = sorted(
        players,
        key=lambda p: (-p.wins, -p.win_rate, -p.matches_played)
    )
    for index, player in enumerate(sorted_players, start=1):
        player.ranking_position = index
        player.save()

class PlayerViewSet(viewsets.ModelViewSet):
    
    queryset = Player.objects.all().order_by('ranking_position')
    serializer_class = PlayerSerializer    

    def get_permissions(self):
        """
        Returns the permissions for each action based on the type of request.
        """
        if self.action == 'player_names':
            permission_classes = [AllowAny] # Player names should be accessible because are used when registering 
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser] # only admin user can modify players        
        elif self.action == 'list':  # 'list' (Hall of Fame) action is open to anyone        
            permission_classes = [AllowAny]
        elif self.action == 'retrieve':  # 'retrieve' action is only for authenticated users
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated] # Default permission
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='player_names')    
    def player_names(self, request):
        """
        Custom endpoint to return a JSON dictionary with:
        - A list of registered users (players linked to a User account) with their ID and name.
        - A list of non-registered players with their ID and name.
        Results are sorted alphabetically case-insensitively.
        """
        print("Getting registered players names...")
        registered_players = Player.objects.filter(registered_user__isnull=False).values('id', 'name')
        
        print("Getting non-registered players names...")
        non_registered_players = Player.objects.filter(registered_user__isnull=True).values('id', 'name')
        
        registered_players = sorted(registered_players, key=lambda player: player['name'].lower())
        non_registered_players = sorted(non_registered_players, key=lambda player: player['name'].lower())
        
        return Response({
            'registered_players': list(registered_players),
            'non_registered_players': list(non_registered_players)
        })

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

    def get_permissions(self):
        """
        Define permissions for specific actions.
        """
        # Only participants can modify a match
        if self.action in ['update', 'partial_update', 'destroy']:        
            permission_classes = [IsMatchParticipant, IsAuthenticated]
        # Any authenticated users can 'create', 'list' and 'retrieve'
        elif self.action in ['create', 'list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated] # Default permission
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Allow filtering matches by a player's username using ?player=username.
        """
        queryset = Match.objects.all().order_by('-date_played')
        player_name = self.request.query_params.get('player', None)

        if player_name:
            queryset = queryset.filter(
                team1_player1__name__iexact=player_name
            ) | queryset.filter(
                team1_player2__name__iexact=player_name
            ) | queryset.filter(
                team2_player1__name__iexact=player_name
            ) | queryset.filter(
                team2_player2__name__iexact=player_name
            )

        return queryset
    
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
        old_winning_players = old_match.winning_players
        old_losing_players = old_match.losing_players
        
        # Reset stats for all players in the old match
        for player in old_winning_players + old_losing_players:
            player.matches.remove(old_match)
            if player in old_winning_players and player.wins > 0:
                player.wins -= 1
            player.save()

        # Update the match instance and stats
        match = serializer.save()        
        self.update_player_stats(match)

    def perform_destroy(self, instance):
        """
        Override the delete behavior to update players' stats before deleting the match.
        """
        self.update_player_stats_on_delete(instance)
        instance.delete()

    
    def update_player_stats(self, match):
        """
        Updates wins, matches of the players involved in the match and 
        updates player rankings for all players
        """
        # Retrieve the winning and losing players as objects
        winning_players = match.winning_players
        losing_players = match.losing_players

        # Update win/loss stats for winning players
        for player in winning_players:
            player.wins += 1
            player.matches.add(match)
            player.save()

        for player in losing_players:
            player.matches.add(match)
            player.save()
        
        update_player_rankings()
    
    def update_player_stats_on_delete(self, match):
        """
        Updates player stats when a match is deleted. 
        - Decrements wins for winning players.
        - Removes match from players' match history.
        - Updates all player rankings
        """
        winning_players = match.winning_players
        losing_players = match.losing_players

        for player in winning_players + losing_players:
            player.matches.remove(match)
            if player in winning_players and player.wins > 0:
                player.wins -= 1
            player.save()

        update_player_rankings()
    
    def get_serializer_context(self):
        """Add request context to the serializer."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

