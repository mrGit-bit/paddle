# games/tests/test_matches.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from games.models import Player, Match
from datetime import date, timedelta


class MatchEdgeCasesTests(APITestCase):
    def setUp(self):
        # Create test players
        self.player1 = Player.objects.create(name="Player 1")
        self.player2 = Player.objects.create(name="Player 2")
        self.player3 = Player.objects.create(name="Player 3")
        self.player4 = Player.objects.create(name="Player 4")

        # Link the authenticated user to Player 1
        self.user = User.objects.create_user(username="player1_user", password="testpassword")
        self.player1.name = "player1_user"  # Update the name to match the user
        self.player1.registered_user = self.user
        self.player1.save()  # Save changes to ensure proper linking

        self.client.force_authenticate(user=self.user)

    def test_create_match_with_valid_data(self):
        data = {
            "team1_player1": "player1_user", # Authenticated user
            "team1_player2": "Player 2",
            "team2_player1": "Player 3",
            "team2_player2": "Player 4",
            "winning_team": 1,
            "date_played": "2024-12-01"
        }
        response = self.client.post('/api/games/matches/', data, format='json')
        # Debugging
        print ("Logged in user:", self.user)
        print ("Logged in user name:", self.user.username)
        print ("Response status code:", response.status_code)
        print("Response data:", response.data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_participants_can_only_update_own_match(self):
        data = {
            "team1_player1": "player1_user",
            "team1_player2": "Player 2",
            "team2_player1": "Player 3",
            "team2_player2": "Player 4",
            "winning_team": 1,
            "date_played": "2024-12-01"
        }
        # Create a valid match
        response = self.client.post('/api/games/matches/', data)
        match_id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Try to update the match as a participant
        update_data = {
            "team1_player1": "player1_user",
            "team1_player2": "Player 2",
            "team2_player1": "Player 3",
            "team2_player2": "Player 4",
            "winning_team": 2, # Update the winning team
            "date_played": "2024-12-01"
        }
        response = self.client.put(f'/api/games/matches/{match_id}/', update_data, format='json')
        print("Update Response status code:", response.status_code)
        print("Update Response data:", response.data)        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Try to update the match as a non-participant
        # Log with other user
        self.client.logout()
        other_user = User.objects.create_user(username="other_user", password="testpassword")
        self.client.force_authenticate(user=other_user)
                
        response = self.client.put(f'/api/games/matches/{match_id}/', update_data)
        print("Non-Participant Update Response status code:", response.status_code)
        print("Non-Participant Update Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Check the error message in the `detail` field
        self.assertIn("You do not have permission to perform this action.", str(response.data.get('detail', '')))
        
                
    
    def test_create_match_with_duplicate_players(self):
        """Test that match creation fails if the same player is in both teams."""
        data = {
            "team1_player1": "player1_user",
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
            "team1_player1": "player1_user",
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
            "team1_player2": "", # Missing field
            "team2_player1": "Player 3",
            "team2_player2": "Player 4",
            "winning_team": 1,
            "date_played": "2024-12-01"
        }
        response = self.client.post('/api/games/matches/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("team1_player2", response.data)

    def test_create_duplicate_match(self):
        """Test that creating a duplicate match fails."""
        data = {
            "team1_player1": "player1_user",
            "team1_player2": "Player 2",
            "team2_player1": "Player 3",
            "team2_player2": "Player 4",
            "winning_team": 1,
            "date_played": "2024-12-01"
        }
        # Create a valid match
        response = self.client.post('/api/games/matches/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Attempt to create the same match again
        response = self.client.post('/api/games/matches/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A match with the same teams and date already exists.", response.data['non_field_errors'][0])
    
    def test_create_duplicate_match_different_order(self):
        """Test that creating a duplicate match fails even if the order of players
        is different but teams, date and winning team are the same."""
        data = {
            "team1_player1": "player1_user",
            "team1_player2": "Player 2",
            "team2_player1": "Player 3",
            "team2_player2": "Player 4",
            "winning_team": 1,
            "date_played": "2024-12-01"
        }
        response = self.client.post('/api/games/matches/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "team1_player1": "Player 4",
            "team1_player2": "Player 3",
            "team2_player1": "Player 2",
            "team2_player2": "player1_user",
            "winning_team": 2,
            "date_played": "2024-12-01"
        }
        response = self.client.post('/api/games/matches/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A match with the same teams and date already exists.", response.data['non_field_errors'][0])
    
    def test_create_match_with_invalid_future_date(self):
        """Test that creating a match with a future date fails."""        
        future_date = date.today() + timedelta(days=1)
        data = {
            "team1_player1": "player1_user",
            "team1_player2": "Player 2",
            "team2_player1": "Player 3",
            "team2_player2": "Player 4",
            "winning_team": 1,
            "date_played": future_date
        }
        response = self.client.post('/api/games/matches/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Date cannot be in the future.", response.data['non_field_errors'][0])
    
    def test_create_match_by_non_participant(self):
        """Test that creating a match by a non-participant fails."""
        data = {
            "team1_player1": "Player 1",
            "team1_player2": "Player 2",
            "team2_player1": "Player 3",
            "team2_player2": "Player 4",
            "winning_team": 1,
            "date_played": "2024-12-01"
        }
        response = self.client.post('/api/games/matches/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You are only allowed to create or update your own matches.", response.data['non_field_errors'][0])
