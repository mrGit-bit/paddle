from rest_framework import serializers
from django.contrib.auth.models import User
from games.models import Player

class UserSerializer(serializers.ModelSerializer):
    player_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'player_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Extract player_id from validated_data if provided
        player_id = validated_data.pop('player_id', None)
        password = validated_data.pop('password')

        # Create the user
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # If a player_id is provided, link this user with the player
        if player_id is not None:
            try:
                player = Player.objects.get(id=player_id, registered_user=None)
                player.registered_user = user
                player.save()
            except Player.DoesNotExist:
                raise serializers.ValidationError("Invalid player_id or player is already linked.")

        return user

