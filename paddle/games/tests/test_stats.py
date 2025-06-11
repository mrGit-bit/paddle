# games/tests/test_stats.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from games.models import Player, Match


class MatchStatsUpdateTests(APITestCase):
    def setUp(self):
        # Create test players (remove wins=0)
        self.player1 = Player.objects.create(name="Player 1")
        self.player2 = Player.objects.create(name="Player 2")
        self.player3 = Player.objects.create(name="Player 3")
        self.player4 = Player.objects.create(name="Player 4")

        # Link a user to one of the players
        self.user = User.objects.create_user(username="player1_user", password="testpassword")
        self.player1.registered_user = self.user
        self.player1.save()

        self.client.force_authenticate(user=self.user)

    def test_stats_update_on_match_creation(self):
        """Test that player stats are correctly updated when creating a match."""
        data = {
            "team1_player1": "Player 1",
            "team1_player2": "Player 2",
            "team2_player1": "Player 3",
            "team2_player2": "Player 4",
            "winning_team": 1,
            "date_played": "2024-12-01"
        }

        # Create a new match
        response = self.client.post('/api/games/matches/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check player stats
        self.player1.refresh_from_db()
        self.player2.refresh_from_db()
        self.player3.refresh_from_db()
        self.player4.refresh_from_db()

        self.assertEqual(self.player1.wins, 1)
        self.assertEqual(self.player2.wins, 1)
        self.assertEqual(self.player3.wins, 0)
        self.assertEqual(self.player4.wins, 0)

        # Check match participation
        self.assertEqual(self.player1.matches.count(), 1)
        self.assertEqual(self.player3.matches.count(), 1)

    def test_stats_update_on_match_update(self):
        """Test that player stats are correctly updated when modifying a match result."""
        # Step 1: Create an initial match via the endpoint
        initial_data = {
            "team1_player1": "Player 1",
            "team1_player2": "Player 2",
            "team2_player1": "Player 3",
            "team2_player2": "Player 4",
            "winning_team": 1,
            "date_played": "2024-12-01"
        }
        response = self.client.post('/api/games/matches/', initial_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        match_id = response.data['id']

        # Step 2: Verify initial stats for players
        self.player1.refresh_from_db()
        self.player2.refresh_from_db()
        self.player3.refresh_from_db()
        self.player4.refresh_from_db()

        self.assertEqual(self.player1.wins, 1)
        self.assertEqual(self.player2.wins, 1)
        self.assertEqual(self.player3.wins, 0)
        self.assertEqual(self.player4.wins, 0)

        # Step 3: Update the match result (Team 2 wins)
        updated_data = {
            "team1_player1": "Player 1",
            "team1_player2": "Player 2",
            "team2_player1": "Player 3",
            "team2_player2": "Player 4",
            "winning_team": 2,
            "date_played": "2024-12-01"
        }
        response = self.client.put(f'/api/games/matches/{match_id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Step 4: Verify updated stats for players
        self.player1.refresh_from_db()
        self.player2.refresh_from_db()
        self.player3.refresh_from_db()
        self.player4.refresh_from_db()

        self.assertEqual(self.player1.wins, 0)  # Removed win
        self.assertEqual(self.player2.wins, 0)
        self.assertEqual(self.player3.wins, 1)  # New win for team 2
        self.assertEqual(self.player4.wins, 1)

        # Check match participation remains correct
        self.assertEqual(self.player1.matches.count(), 1)
        self.assertEqual(self.player3.matches.count(), 1)
    
    def test_stats_win_rate(self):
        """Test that the win rate is correctly calculated and returned by the API."""
        # Create a match using the POST endpoint
        match_data = {
            "team1_player1": self.player1.name,
            "team1_player2": self.player2.name,
            "team2_player1": self.player3.name,
            "team2_player2": self.player4.name,
            "winning_team": 1,
            "date_played": "2024-12-01"
        }
        response = self.client.post('/api/games/matches/', match_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Retrieve player data from the players endpoint
        response = self.client.get('/api/games/players/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        players = response.json()['results']

        # Check win rate is correct for all the players in the match
        for player in players:
            if player['name'] == self.player1.name:
                self.assertEqual(player['win_rate'], 100.0)
            elif player['name'] == self.player2.name:
                self.assertEqual(player['win_rate'], 100.0)
            elif player['name'] == self.player3.name:
                self.assertEqual(player['win_rate'], 0.0)
            elif player['name'] == self.player4.name:
                self.assertEqual(player['win_rate'], 0.0)


