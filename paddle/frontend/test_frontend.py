from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from games.models import Player, Match
from django.urls import reverse
from unittest.mock import patch
import json
import requests

class FrontendViewAPITests(APITestCase):
    def setUp(self):
        # Create test user and login
        self.user = User.objects.create_user(username="player1_user", password="testpassword")
        self.client.login(username="player1_user", password="testpassword")

        # Create test players
        self.player1 = Player.objects.create(name="player1_user", registered_user=self.user)
        self.player2 = Player.objects.create(name="Player 2")
        self.player3 = Player.objects.create(name="Player 3")
        self.player4 = Player.objects.create(name="Player 4")

        # Create test match
        self.match = Match.objects.create(
            team1_player1=self.player1,
            team1_player2=self.player2,
            team2_player1=self.player3,
            team2_player2=self.player4,
            winning_team=1,
            date_played="2019-12-01"
        )

    def mock_api_response(self, url, headers=None):
        """Return a mocked API response based on the requested URL."""
        response = requests.Response()
        response.status_code = 200

        if "games/matches" in url:
            matches_data = {
                "results": [
                    {
                        "team1_player1": self.player1.name,
                        "team1_player2": self.player2.name,
                        "team2_player1": self.player3.name,
                        "team2_player2": self.player4.name,
                        "winning_team": self.match.winning_team,
                        "date_played": str(self.match.date_played),
                    }
                ]
            }
            response._content = json.dumps(matches_data).encode("utf-8")
        elif "games/players" in url:
            players_data = {
                "results": [
                    {
                        "id": player.id,
                        "name": player.name,
                        "registered_user": player.registered_user.id if player.registered_user else None,
                    }
                    for player in Player.objects.all()
                ]
            }
            response._content = json.dumps(players_data).encode("utf-8")
        return response

    def perform_post(self, url, data, csrf_token, sessionid=None):
        headers = {"X-CSRFToken": csrf_token}
        if sessionid:
            headers["Cookie"] = f"sessionid={sessionid}"
        return self.client.post(url, data, headers=headers, cookies=self.client.cookies)

    @patch("requests.Session.get")
    def test_hall_of_fame_view_get_success(self, mock_get):                
        mock_get.side_effect = self.mock_api_response        
        response = self.client.get(reverse("hall_of_fame"))          
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Hall of Fame")
        self.assertContains(response, self.user.username)        
        self.assertContains(response, self.player2.name)
        self.assertContains(response, self.player3.name)
        self.assertContains(response, self.player4.name)
        # Check links for a logged in user
        self.assertContains(response, "Matches")
        self.assertContains(response, "Logged in")
        self.assertContains(response, "Logout")
        # Check links for a logged out user
        self.client.logout()
        response = self.client.get(reverse("hall_of_fame"))
        self.assertContains(response, "Register")
        self.assertContains(response, "Login")

    @patch("requests.Session.get")
    def test_hall_of_fame_view_get_API_error(self, mock_get):        
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 500  # Simulate an API failure            
        response = self.client.get(reverse("hall_of_fame"))        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Hall of Fame")
        self.assertContains(response, "Player")        

    @patch("requests.Session.get")
    def test_match_view_get_success(self, mock_get):        
        mock_get.side_effect = self.mock_api_response
        response = self.client.get(reverse("match"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Matches")
        self.assertContains(response, str(self.match.date_played))
        # Ensure players are found in match history
        self.assertContains(response, self.player1.name)
        self.assertContains(response, self.player2.name)
        self.assertContains(response, self.player3.name)
        self.assertContains(response, self.player4.name)

    @patch("requests.Session.get")
    @patch("requests.Session.post")
    def test_register_view_post_success(self, mock_post, mock_get):       
        unique_username = f"testuser_{self.user.id}"
        csrf_token = self.client.cookies.get('csrftoken') or "test_csrf_token"
        
        mock_get.side_effect = self.mock_api_response
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 201  # Simulate successful registration
        mock_post.return_value._content = json.dumps({"id": 1, "username": unique_username}).encode("utf-8")

        data = {
            "username": unique_username,
            "password": "securepassword",
            "confirm_password": "securepassword",
            "email": f"{unique_username}@example.com"
        }
        # Manually create the user in the test database
        User.objects.create_user(username=unique_username, password="securepassword")
        response = self.perform_post(reverse("register"), data, csrf_token)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse("hall_of_fame"))


    @patch("requests.Session.get")
    @patch("requests.Session.post")
    def test_register_view_post_password_mismatch(self, mock_post, mock_get):        
        csrf_token = self.client.cookies.get('csrftoken') or "test_csrf_token"
        mock_get.side_effect = self.mock_api_response
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 400  # Simulate password mismatch

        data = {
            "username": "testuser",
            "password": "password",
            "confirm_password": "different_password",
            "email": "B4dHt@example.com"
        }
        
        response = self.perform_post(reverse("register"), data, csrf_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Passwords do not match.")
        
    @patch("requests.Session.get")
    @patch("requests.Session.post")
    def test_register_view_post_api_error(self, mock_post, mock_get):
        """Ensure user registration fails with API error."""       
        mock_get.side_effect = self.mock_api_response        
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 500  # Simulate an API failure

        data = {
            "username": "testuser",
            "password": "password",
            "confirm_password": "password",
            "email": "B4dHt@example.com"
        }

        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "error")
    
    @patch("requests.Session.get")
    @patch("requests.Session.post")
    def test_register_view_post_duplicate_username(self, mock_post, mock_get):
        """Ensure user registration fails with duplicate username."""        
        csrf_token = self.client.cookies.get('csrftoken') or "test_csrf_token"        
        mock_get.side_effect = self.mock_api_response        
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 400  # Simulate duplicate username
        mock_post.return_value._content = json.dumps({"detail": "User with this Username already exists."}).encode("utf-8")

        data = {
            "username": "testuser",
            "password": "password",
            "confirm_password": "password",
            "email": "B4dHt@example.com"
        }       

        response = self.perform_post(reverse("register"), data, csrf_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "User with this Username already exists.")
    
    @patch("requests.Session.get")
    @patch("requests.Session.post")  
    def test_match_view_post_success(self, mock_post, mock_get):
        self.client.force_login(self.user)
        csrf_token = self.client.cookies.get("csrftoken") or "test_csrf_token"
        sessionid = self.client.cookies.get("sessionid").value  # Retrieve session ID

        mock_get.side_effect = self.mock_api_response
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 201  # Simulate successful match creation
        mock_post.return_value._content = b'{"id": 1, "message": "Match created successfully"}'  # Mock JSON response

        data = {
            "team1_player1": self.player1.name,
            "team1_player2": self.player2.name,
            "team2_player1": self.player3.name,
            "team2_player2": self.player4.name,
            "winning_team": 1,
            "date_played": "2024-01-01"
        }
        
        response = self.perform_post(reverse("match"), data, csrf_token, sessionid)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse("hall_of_fame"))


    @patch("requests.Session.get")
    def test_match_view_post_invalid_data(self, mock_get):
        """Ensure match creation fails with invalid data."""
        csrf_token = self.client.cookies.get('csrftoken') or "test_csrf_token"
        mock_get.side_effect = self.mock_api_response

        data = {
            "team1_player1": self.player1.name,
            "team1_player2": self.player1.name,  # Invalid: Duplicate player
            "team2_player1": self.player3.name,
            "team2_player2": self.player4.name,
            "winning_team": 1,
            "date_played": "2024-01-01"
        }
                
        response = self.perform_post(reverse("match"), data, csrf_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Should not redirect
        self.assertContains(response, "Try again, you have introduced duplicated players!")
    
    @patch("requests.Session.get")
    @patch("requests.Session.post")    
    def test_login_view_post_success(self, mock_get, mock_post):
        """Ensure successful login redirects to the Hall of Fame."""                
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 200  # Simulate successful login
        mock_post.return_value._content = json.dumps({"token": "fake_token"}).encode("utf-8")

        data = {"username": "player1_user", "password": "testpassword"}                
        response = self.client.post(reverse("login"), data)
        
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse("hall_of_fame"))

    @patch("requests.Session.get")
    @patch("requests.Session.post")
    def test_login_view_post_invalid_credentials(self, mock_get, mock_post):
        """Ensure login fails with incorrect credentials."""
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 401  # Simulate unauthorized login
        mock_post.return_value._content = json.dumps({"detail": "Invalid credentials"}).encode("utf-8")

        data = {"username": "wronguser", "password": "wrongpassword"}        
        response = self.client.post(reverse("login"), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Invalid credentials.")

