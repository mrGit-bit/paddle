# users/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from games.models import Player

class UserSerializer(serializers.ModelSerializer):
    # Use a ChoiceField to display names of non-linked players as choices
    player_id = serializers.ChoiceField(
        choices=[],  # Will be dynamically populated in the `__init__` method
        required=False
    )
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 
                  'password', 'player_id']
        # Set password to write-only (input only not output)
        # extra_kwargs in DRF is a dict used to add additional options
        # without modifying the field itself
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate the player_id choices with names of non-linked players
        self.fields['player_id'].choices = [('', 'New Player')] + [
            (player.id, player.name) for player in Player.objects.filter(registered_user__isnull=True)
        ]
    
    def validate_username(self, value):
        """
        Case-insensitive validation to avoid duplicate usernames.
        """
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(f"Username '{value}' is already taken. Please choose another one.")
        return value
    
    def create(self, validated_data):
        # Extract (and remove) player_id and password from validated_data
        # with "None" result if not provided any player_id
        player_id = validated_data.pop('player_id', None)
        password = validated_data.pop('password')
        
        # Create the user without password and player_id
        # ** are used to unpack the dictionary
        user = User(**validated_data)
        # Hash the password and save the user instance
        user.set_password(password)
        user.save()

        # If a player_id is provided, link this user with the player
        if player_id is not None:
            try:
                player = Player.objects.get(id=player_id, registered_user=None)
                player.registered_user = user
                # Replace the player name with the user's username
                player.name = user.username
                player.save()
            except Player.DoesNotExist:
                raise serializers.ValidationError("Invalid player_id or player is already linked.")
        # If no player_id is provided, create a new player linked to the user
        else:
            # Create a new Player with default stats and link to the user
            player = Player.objects.create(
                name=user.username,
                registered_user=user,
                wins=0                
            )
            # Since `matches` is ManyToMany, ensure to use `.set()` if needed
            player.matches.set([])  # Optional: Clear any existing matches
            player.save()

        return user
    
    def update(self, instance, validated_data):
        # Handle password update separately to hash it properly
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

