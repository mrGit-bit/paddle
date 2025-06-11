# users/tests.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.http import Http404
from games.models import Player, Match
from users.serializers import UserSerializer

class UserManagementTests(APITestCase):
    def setUp(self):
        # Create existing non-registered player (remove wins=0)
        self.existing_player = Player.objects.create(name="Existing Player")

    def test_register_new_user_with_existing_player(self):
        """Test registering a user and linking to an existing player."""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "testpassword",
            "player_id": self.existing_player.id
        }
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.existing_player.refresh_from_db()
        self.assertEqual(self.existing_player.registered_user.username, "newuser")

    def test_register_new_user_without_linking(self):
        """Test registering a user without linking to an existing player."""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "testpassword"
        }
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        player = Player.objects.get(name="newuser")
        self.assertEqual(player.registered_user.username, "newuser")

class AuthenticationAndPermissionsTests(APITestCase):
    def setUp(self):
        # Create users and players
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpassword")
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.other_user = User.objects.create_user(username="otheruser", password="otherpassword")
        self.player = Player.objects.create(name="Test Player", registered_user=self.user)
        self.other_player = Player.objects.create(name="Other Player", registered_user=self.other_user)

    def test_admin_can_modify_any_match(self):
        """Test admin can modify or delete any match."""
        match = Match.objects.create(
            team1_player1=self.player,
            team1_player2=self.player,
            team2_player1=self.other_player,
            team2_player2=self.other_player,
            winning_team=1,
            date_played="2024-12-01"
        )
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/games/matches/{match.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Match.objects.filter(id=match.id).exists())

    """Test user can update or delete their own profile but not others'."""
    def test_user_can_modify_own_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/api/users/{self.user.id}/', {"username": "newusername"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "newusername")
        
    # User cannot modify another user's profile
    def test_user_cannot_modify_other_user_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/api/users/{self.other_user.id}/', {"username": "newusername"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserEdgeCasesTests(APITestCase):
    def setUp(self):
        # Create existing players
        self.player1 = Player.objects.create(name="Player 1")
        self.player2 = Player.objects.create(name="Player 2")

    def test_register_user_with_duplicate_username(self):
        """Test that user registration fails with a duplicate username."""
        User.objects.create_user(username="existinguser", password="testpassword")

        data = {
            "username": "existinguser",  # Duplicate username
            "password": "newpassword"
        }
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A user with that username already exists.", response.data['username'][0])

    def test_register_user_without_required_fields(self):
        """Test that user registration fails if required fields are missing."""
        data = {
            "password": "testpassword"
        }
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
    


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