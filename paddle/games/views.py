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
    Rank only players with at least one match played.
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
    """
    ViewSet for handling CRUD operations related to players.
    """
    queryset = Player.objects.exclude(ranking_position=0).order_by('ranking_position')
    serializer_class = PlayerSerializer

    def get_permissions(self):
        """
        Returns the permissions for each action based on the type of request.
        """
        if self.action == 'player_names':
            permission_classes = [AllowAny]  # Player names are public.
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]  # Only admin can modify players.
        elif self.action == 'list':  # Hall of Fame is public.
            permission_classes = [AllowAny]
        elif self.action == 'retrieve':  # Player details are for authenticated users.
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]  # Default permission.
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='player_names')
    def player_names(self, request):
        """
        Custom endpoint to return a JSON dictionary with:
        - A list of registered users (players linked to a User account) with their ID and name.
        - A list of non-registered players with their ID and name.
        Results are sorted alphabetically case-insensitively.
        """
        registered_players = Player.objects.filter(registered_user__isnull=False).values('id', 'name')
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
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsMatchParticipant, IsAuthenticated]  # Only participants can modify.
        elif self.action in ['create', 'list', 'retrieve']:
            permission_classes = [IsAuthenticated]  # Authenticated users can create, list, and retrieve.
        else:
            permission_classes = [IsAuthenticated]  # Default permission.
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
        self.update_player_stats(match)

    def perform_update(self, serializer):
        """
        Reset old players' stats before updating the match
        and update new players' stats
        """
        old_match = self.get_object()
        old_winning_players = old_match.winning_players
        old_losing_players = old_match.losing_players

        # Reset stats for all players in the old match
        for player in old_winning_players + old_losing_players:
            player.matches.remove(old_match)
            if player in old_winning_players and player.wins > 0:
                player.wins -= 1
            player.save()

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
        updates player rankings for all players.
        Ensures logical consistency by enforcing: wins ≥ 0 and wins ≤ matches.
        """
        winning_players = match.winning_players
        losing_players = match.losing_players

        for player in winning_players:
            player.wins = max(0, player.wins + 1)
            player.matches.add(match)
            player.wins = min(player.wins, player.matches.count())
            player.save()

        for player in losing_players:
            player.matches.add(match)
            player.wins = max(0, min(player.wins, player.matches.count()))
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
        winning_ids = {p.id for p in winning_players}
        losing_players = match.losing_players

        for player in winning_players + losing_players:
            player.matches.remove(match)
            if player.id in winning_ids:
                player.wins = max(0, player.wins - 1)
            player.wins = min(player.wins, player.matches.count())
            player.save()

        update_player_rankings()

    def get_serializer_context(self):
        """Add request context to the serializer."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
