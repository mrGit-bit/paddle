from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from games.models import Player, Match


class PlayerPermissionsTests(APITestCase):
    def setUp(self):
        # Create admin and regular users
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpassword")
        self.regular_user = User.objects.create_user(username="user", password="userpassword")

        # Create test players
        self.player1 = Player.objects.create(name="Player 1")
        self.player2 = Player.objects.create(name="Player 2")
        self.player3 = Player.objects.create(name="Player 3")
        self.player4 = Player.objects.create(name="Player 4")

        # Create a match
        self.match = Match.objects.create(
            team1_player1=self.player1,
            team1_player2=self.player2,
            team2_player1=self.player3,
            team2_player2=self.player4,
            winning_team=1,
            date_played="2024-12-01"
        )

    """Permissions tests for players endpoints."""
    def test_list_players_permissions(self):
        """Test that the 'list' action is open to anyone."""
        response = self.client.get('/api/games/players/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_player_permissions_authenticated_user(self):
        """Test that only authenticated users can retrieve player details."""
        # Unauthenticated user
        response = self.client.get(f'/api/games/players/{self.player1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Authenticated user
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(f'/api/games/players/{self.player1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_player_permissions_admin_user(self):
        """Test that only admin users can create players."""
        player_data = {"name": "New Player", "wins": 0}
        # Authenticated user
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post('/api/games/players/', player_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Admin user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post('/api/games/players/', player_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_player_permissions_admin_user(self):
        """Test that only admin users can update player details."""
        update_data = {"name": "Updated Player"}
        # Authenticated user
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.put(f'/api/games/players/{self.player1.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Admin user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(f'/api/games/players/{self.player1.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_player_permissions_admin_user(self):
        """Test that only admin users can delete players."""
        # Authenticated user
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f'/api/games/players/{self.player1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Admin user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/games/players/{self.player1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    """Permissions tests for matches endpoints."""
    def test_list_matches_permissions(self):
        """Test that the 'list' action is restricted to authenticated users."""
        # Unauthenticated user
        response = self.client.get('/api/games/matches/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Authenticated user
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/api/games/matches/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_match_permissions_authenticated_user(self):
        """Test that only authenticated users can create matches."""
        match_data = {
            "team1_player1": "Player 1",
            "team1_player2": "Player 2",
            "team2_player1": "Player 3",
            "team2_player2": "Player 4",
            "winning_team": 1,
            "date_played": "2024-12-01"
        }
        # Unauthenticated user
        response = self.client.post('/api/games/matches/', match_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Authenticated user
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post('/api/games/matches/', match_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_match_permissions(self):
        """Test that only participants or admin users can update matches."""
        self.participant_user = User.objects.create_user(username="participant", password="password")
        self.player1.registered_user = self.participant_user
        self.player1.save()

        match_data = {
            "team1_player1": "Player 1",
            "team1_player2": "Player 2",
            "team2_player1": "Player 3",
            "team2_player2": "Player 4",
            "winning_team": 2,
            "date_played": "2024-12-02"
        }
        # Non participant user
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.put(f'/api/games/matches/{self.match.id}/', match_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Participant user
        self.client.force_authenticate(user=self.participant_user)
        response = self.client.put(f'/api/games/matches/{self.match.id}/', match_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Admin user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(f'/api/games/matches/{self.match.id}/', match_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_match_permissions(self):
        """Test that only participants or admin users can delete matches."""
        self.participant_user = User.objects.create_user(username="participant", password="password")
        self.player1.registered_user = self.participant_user
        self.player1.save()
        # Non participant user
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f'/api/games/matches/{self.match.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Participant user
        self.client.force_authenticate(user=self.participant_user)
        response = self.client.delete(f'/api/games/matches/{self.match.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Admin user
        # Recreate the deleted match for the admin user test
        self.match = Match.objects.create(
            team1_player1=self.player1,
            team1_player2=self.player2,
            team2_player1=self.player3,
            team2_player2=self.player4,
            winning_team=1,
            date_played="2024-12-01"
        )
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/games/matches/{self.match.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
