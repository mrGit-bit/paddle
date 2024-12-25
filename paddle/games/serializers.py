# games/serializers.py

from rest_framework import serializers
from .models import Player, Match


class PlayerSerializer(serializers.ModelSerializer):
    # Dynamically determine matches played, losses, and win rate
    matches_played = serializers.SerializerMethodField()
    losses = serializers.SerializerMethodField()
    win_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = Player
        fields = ['id', 'name', 'registered_user', 'matches_played', 'wins', 
                  'losses', 'win_rate', 'matches']

    def get_matches_played(self, obj):
        """Calculate the total number of matches the player has played."""
        # Use count() instead of len() for ManyToManyField
        return obj.matches.count()

    def get_losses(self, obj):
        """Calculate the total number of matches the player has lost."""
        matches_played = self.get_matches_played(obj)
        return matches_played - obj.wins

    def get_win_rate(self, obj):
        """Calculate the win rate of the player."""
        matches_played = self.get_matches_played(obj)
        if matches_played == 0:
            return 0.0
        return (obj.wins / matches_played) * 100


class MatchSerializer(serializers.ModelSerializer):
    # Accept player names as an input string   
    team1_player1 = serializers.CharField()
    team1_player2 = serializers.CharField()
    team2_player1 = serializers.CharField()
    team2_player2 = serializers.CharField()
        
    # Dynamically determine winning and losing players
    winning_players = serializers.SerializerMethodField()
    losing_players = serializers.SerializerMethodField()    
    
    class Meta:
        model = Match
        fields = [
            'id', 'team1_player1', 'team1_player2',
            'team2_player1', 'team2_player2',
            'winning_team', 'date_played', 'winning_players', 'losing_players'
        ]
    
    def validate(self, data):
        """Ensure no player appears more than once in the same match."""
        # Normalize player names to compare them
        players = {
            data['team1_player1'].strip().lower(),
            data['team1_player2'].strip().lower(),
            data['team2_player1'].strip().lower(),
            data['team2_player2'].strip().lower()
        }

        # Check for duplicates
        if len(players) < 4:
            raise serializers.ValidationError("A player cannot appear more than once in the same match.")

        return data
    
    def create_or_get_player(self, name):
        """Helper method to get an existing player or create a new one."""
        player, created = Player.objects.get_or_create(
            name__iexact=name.strip(),
            defaults={'name': name.strip()}
        )
        return player

    def create(self, validated_data):
        # Retrieve player names using pop
        team1_player1_name = validated_data.pop('team1_player1')
        team1_player2_name = validated_data.pop('team1_player2')
        team2_player1_name = validated_data.pop('team2_player1')
        team2_player2_name = validated_data.pop('team2_player2')

        # Get or create players
        team1_player1 = self.create_or_get_player(team1_player1_name)
        team1_player2 = self.create_or_get_player(team1_player2_name)
        team2_player1 = self.create_or_get_player(team2_player1_name)
        team2_player2 = self.create_or_get_player(team2_player2_name)

        # Create the match instance with player references
        match = Match.objects.create(
            team1_player1=team1_player1,
            team1_player2=team1_player2,
            team2_player1=team2_player1,
            team2_player2=team2_player2,
            winning_team=validated_data['winning_team'],
            date_played=validated_data['date_played']
        )

        return match

    def update(self, instance, validated_data):
        # Retrieve player names using pop with defaults
        team1_player1_name = validated_data.pop('team1_player1', instance.team1_player1.name)
        team1_player2_name = validated_data.pop('team1_player2', instance.team1_player2.name)
        team2_player1_name = validated_data.pop('team2_player1', instance.team2_player1.name)
        team2_player2_name = validated_data.pop('team2_player2', instance.team2_player2.name)

        # Get or create players
        instance.team1_player1 = self.create_or_get_player(team1_player1_name)
        instance.team1_player2 = self.create_or_get_player(team1_player2_name)
        instance.team2_player1 = self.create_or_get_player(team2_player1_name)
        instance.team2_player2 = self.create_or_get_player(team2_player2_name)

        # Update other fields
        instance.winning_team = validated_data.get('winning_team', instance.winning_team)
        instance.date_played = validated_data.get('date_played', instance.date_played)
        
        instance.save()
        return instance


    def get_winning_players(self, obj):
        """Retrieve the list of players who won the match."""
        # Call method from the model instance
        winning_players, _ = obj.get_players_by_result()
        return winning_players

    def get_losing_players(self, obj):
        """Retrieve the list of players who lost the match."""
        # Call method from the model instance
        _, losing_players = obj.get_players_by_result()
        return losing_players