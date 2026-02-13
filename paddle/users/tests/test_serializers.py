from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.http import Http404
from games.models import Player
from users.serializers import UserSerializer

class UserSerializerTests(APITestCase):
    def setUp(self):
        # Create a test player already linked to a user
        self.linked_user = User.objects.create_user(username="linked_user", password="testpassword")
        self.linked_player = Player.objects.create(name="Linked Player", registered_user=self.linked_user)

        # Create a test player not linked to any user
        self.unlinked_player = Player.objects.create(name="Unlinked Player")

    def test_register_user_with_unlinked_player(self):
        """Test creating a user with an unlinked player."""
        data = {
            "username": "new_user",
            "password": "newpassword",
            "email": "new_user@example.com",
            "player_id": self.unlinked_player.id  # Use unlinked player ID
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        # Retrieve the player object again after creating the new user
        player = Player.objects.get(id=self.unlinked_player.id)
        
        # Check if user was created and linked correctly
        # the player name should be changed to the user name
        self.assertEqual(player.name, "new_user")        
        self.assertEqual(user.player, player)
        self.assertEqual(user.player.registered_user, user)
        
    def test_register_user_with_already_linked_player(self):
        """Test creating a user with a player already linked to another user."""
        data = {
            "username": "new_user",
            "password": "newpassword",
            "email": "new_user@example.com",
            "player_id": self.linked_player.id  # Use already linked player ID
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("This player is already linked to another user.", str(serializer.errors))

    def test_register_user_without_player_id(self):
        """Test creating a user without providing a player_id."""
        data = {
            "username": "new_user",
            "password": "newpassword",
            "email": "new_user@example.com"
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        # Check if a new player was created for the user
        self.assertEqual(user.username, "new_user")
        self.assertEqual(user.player.name, "new_user")
        self.assertEqual(user.player.registered_user, user)

    def test_register_user_with_nonexistent_player_id(self):
        """Test creating a user with a nonexistent player_id."""
        data = {
            "username": "new_user",
            "password": "newpassword",
            "email": "new_user@example.com",
            "player_id": 9999  # Nonexistent player ID
        }
        serializer = UserSerializer(data=data)
        with self.assertRaises(Http404):
            serializer.is_valid(raise_exception=True)
