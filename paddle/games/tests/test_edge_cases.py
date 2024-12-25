# games/tests/test_edge_cases.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from games.models import Player, Match


class MatchEdgeCasesTests(APITestCase):
    def setUp(self):
        # Create test players
        self.player1 = Player.objects.create(name="Player 1")
        self.player2 = Player.objects.create(name="Player 2")
        self.player3 = Player.objects.create(name="Player 3")
        self.player4 = Player.objects.create(name="Player 4")

        # Link a user to one of the players
        self.user = User.objects.create_user(username="player1_user", password="testpassword")
        self.player1.registered_user = self.user
        self.player1.save()

        self.client.force_authenticate(user=self.user)

    def test_create_match_with_duplicate_players(self):
        """Test that match creation fails if the same player is in both teams."""
        data = {
            "team1_player1": "Player 1",
            "team1_player2": "Player 2",
            "team2_player1": "Player 2",  # Duplicate player
            "team2_player2": "Player 3",
            "winning_team": 1,
            "date_played": "2024-12-01"
        }
        response = self.client.post('/api/games/matches/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A player cannot appear more than once in the same match.", response.data['non_field_errors'][0])

    def test_update_match_with_duplicate_players(self):
        """Test updating a match with duplicate players raises an error."""
        data = {
            "team1_player1": "Player 1",
            "team1_player2": "Player 2",
            "team2_player1": "Player 3",
            "team2_player2": "Player 4",
            "winning_team": 1,
            "date_played": "2024-12-01"
        }
        # Create a valid match
        response = self.client.post('/api/games/matches/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Update the match to include a duplicate player
        match_id = response.data['id']
        update_data = {
            "team1_player1": "Player 1",
            "team1_player2": "Player 2",
            "team2_player1": "Player 2",  # Duplicate
            "team2_player2": "Player 4",
            "winning_team": 2,
            "date_played": "2024-12-02"
        }
        response = self.client.put(f'/api/games/matches/{match_id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A player cannot appear more than once in the same match.", response.data['non_field_errors'])
    
    def test_create_match_with_missing_team_data(self):
        """Test that match creation fails if a team is incomplete."""
        data = {
            "team1_player1": "Player 1",
            "team1_player2": "",
            "team2_player1": "Player 3",
            "team2_player2": "Player 4",
            "winning_team": 1,
            "date_played": "2024-12-01"
        }
        response = self.client.post('/api/games/matches/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("team1_player2", response.data)

    
