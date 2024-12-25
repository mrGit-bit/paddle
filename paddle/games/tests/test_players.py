# games/tests/test_players.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from games.models import Player, Match


class HallOfFameTests(APITestCase):
    def setUp(self):
        # Create sample players
        Player.objects.create(name="Player 1", wins=5)
        Player.objects.create(name="Player 2", wins=3)
        Player.objects.create(name="Player 3", wins=7)

    def test_hall_of_fame_rankings(self):
        """Test that Hall of Fame rankings are ordered by wins and accessible without authentication."""
        response = self.client.get('/api/games/players/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        players = response.json()['results']
        self.assertEqual(players[0]['name'], "Player 3")  # Highest wins
        self.assertEqual(players[1]['name'], "Player 1")  # Second highest wins
        self.assertEqual(players[2]['name'], "Player 2")  # Lowest wins


class MatchResultTests(APITestCase):
    def setUp(self):
        # Create sample players
        self.player1 = Player.objects.create(name="Player 1")
        self.player2 = Player.objects.create(name="Player 2")
        self.player3 = Player.objects.create(name="Player 3")
        self.player4 = Player.objects.create(name="Player 4")
        
        # Create and authenticate a test user
        self.user = User.objects.create_user(username="player1_user", password="testpassword")
        self.player1.registered_user = self.user  # Link user to Player 1
        self.player1.save()

        # Force authentication for this user
        self.client.force_authenticate(user=self.user)

    def test_create_match_with_new_players(self):
        """Test creating a match with new players."""
        data = {
            "team1_player1": self.player1.name,  # Linked player
            "team1_player2": self.player2.name,
            "team2_player1": "Player 5",  # New player
            "team2_player2": "Player 6",  # New player
            "winning_team": 1,
            "date_played": "2024-12-01"
        }
        response = self.client.post('/api/games/matches/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Player.objects.filter(name="Player 5").exists())
        self.assertTrue(Player.objects.filter(name="Player 6").exists())

    def test_update_match_results_as_participant(self):
        """Test updating match results as a participant."""
        match = Match.objects.create(
            team1_player1=self.player1,  # Linked player
            team1_player2=self.player2,
            team2_player1=self.player3,
            team2_player2=self.player4,
            winning_team=1,
            date_played="2024-12-01"
        )
        data = {
            "team1_player1": self.player1.name,
            "team1_player2": self.player2.name,
            "team2_player1": self.player3.name,
            "team2_player2": self.player4.name,
            "winning_team": 2,
            "date_played": "2024-12-01"  # Ensure all data are present
        }
        response = self.client.put(f'/api/games/matches/{match.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        match.refresh_from_db()
        self.assertEqual(match.winning_team, 2)


    def test_update_match_results_as_non_participant(self):
        """Test updating match results as a non-participant."""
        match = Match.objects.create(
            team1_player1=self.player3,
            team1_player2=self.player4,
            team2_player1=self.player1,
            team2_player2=self.player2,
            winning_team=1,
            date_played="2024-12-01"
        )
        other_user = User.objects.create_user(username="otheruser", password="testpassword")
        self.client.force_authenticate(user=other_user)
        data = {
            "team1_player1": self.player3.name,
            "team1_player2": self.player4.name,
            "team2_player1": self.player2.name,
            "team2_player2": self.player1.name,
            "winning_team": 2,
            "date_played": "2024-12-01"  # Ensure all data are present
        }
        response = self.client.put(f'/api/games/matches/{match.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_match_str_method(self):
        """Test the __str__ method of the Match model."""
        match = Match.objects.create(
            team1_player1=self.player1,
            team1_player2=self.player2,
            team2_player1=self.player3,
            team2_player2=self.player4,
            winning_team=1,
            date_played="2024-12-01"
        )
        self.assertEqual(str(match), "Match on 2024-12-01")