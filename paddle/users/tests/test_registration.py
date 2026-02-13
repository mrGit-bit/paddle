from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from games.models import Player

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
        

    def test_register_user_without_required_fields(self):
        """Test that user registration fails if required fields are missing."""
        data = {
            "password": "testpassword"
        }
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
