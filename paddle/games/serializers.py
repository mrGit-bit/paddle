from rest_framework import serializers
from .models import Player, Match
from django.core.exceptions import ValidationError

class PlayerSerializer(serializers.ModelSerializer):
    matches = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['id', 'name', 'registered_user', 'wins', 'losses', 
                  'matches_played', 'win_rate', 'matches']

    def get_matches(self, obj):
        matches = Match.objects.filter(teams__icontains=obj.id)
        return MatchSerializer(matches, many=True).data

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'teams', 'winning_team', 'date_played']

    def validate(self, validated_data):
        all_players = self.extract_players(validated_data)

        # Ensure no player is repeated across both teams
        if len(set(all_players)) != 4:
            raise ValidationError("Error selecting players: Player repeated!")

        return validated_data

    def create(self, validated_data):
        all_players = self.extract_players(validated_data)

        # Create new players if they do not exist
        for player_name in all_players:
            Player.objects.get_or_create(name=player_name)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        all_players = self.extract_players(validated_data, instance.teams)

        # Create new players if they do not exist
        for player_name in all_players:
            Player.objects.get_or_create(name=player_name)

        return super().update(instance, validated_data)

    def extract_players(self, validated_data, default_teams=None):
        teams = validated_data.get('teams', default_teams)
        team_1_players = teams.get('team_1', [])
        team_2_players = teams.get('team_2', [])
        return team_1_players + team_2_players
