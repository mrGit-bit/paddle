# users/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from games.models import Player
from django.shortcuts import get_object_or_404

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with optional linking to an existing player.
    """
    player_id = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email','password','player_id']
        # Avoid password being sent and exposed in the response
        extra_kwargs = {'password': {'write_only': True}}
        

    def __init__(self, *args, **kwargs):
        # Dynamically populate the player_id choices with names of non-linked players
        super().__init__(*args, **kwargs)
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
    
    def validate_player_id(self, value):
        """
        Validate that the player_id exists and is not already linked to another user.
        """
        if value is not None:
            player = get_object_or_404(Player, id=value)
            if player.registered_user is not None:
                raise serializers.ValidationError("This player is already linked to another user.")
        return value

    
    def create(self, validated_data):
        """
        Handles user creation with optional linking to an existing player.
        """
        # Debugging: Check validated_data content
        print("Full validated_data:", validated_data)        
        player_id = validated_data.pop('player_id', None)        
        print(f"passed player_id: {player_id}")
        
        password = validated_data.pop('password')
        
        # Create the user without password and player_id
        # ** are used to unpack the dictionary
        user = User(**validated_data)
        # Hash the password and save the user instance
        user.set_password(password)
        user.save()
        print(f"Created user: {user.username}")

        # If a player_id is provided, link this user with the player
        if player_id is not None:            
            player = get_object_or_404(Player, id=player_id, registered_user=None)  # Get the player by ID
            player.registered_user = user            
            player.name = user.username # Replace the player name with the user's username
            player.save()
            print(f"Linked user {user.username} with existing player {player_id}")
            
        # If no player_id is provided, create a new player linked to the user
        else:            
            player = Player.objects.create(
                name=user.username,
                registered_user=user,
                wins=0                
            )
            # Since `matches` is ManyToMany, ensure to use `.set()` if needed
            player.matches.set([])  # Clear any existing matches to ensure a clean start
            player.save()
            print(f"Created new player for user {user.username}")

        return user
    
    def update(self, instance, validated_data):
        # Handle password update separately to hash it properly
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """
        Add player_id in the API response.
        """
        response = super().to_representation(instance)
        response['player_id'] = getattr(instance.player, 'id', None)  # Get player ID if exists
        return response
