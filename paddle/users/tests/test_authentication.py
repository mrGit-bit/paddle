from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class AuthenticationTests(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.login_url = "/api/users/login/"
        self.logout_url = "/api/users/logout/"

    def test_successful_login(self):
        """Test a successful login."""
        response = self.client.post(self.login_url, {"username": "testuser", "password": "testpassword"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Login successful.")
        self.assertIn("user_id", response.data)
        self.assertEqual(response.data["username"], "testuser")

    def test_unsuccessful_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post(self.login_url, {"username": "testuser", "password": "wrongpassword"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_unsuccessful_login_missing_fields(self):
        """Test login with missing fields."""
        response = self.client.post(self.login_url, {"username": "testuser"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_successful_logout(self):
        """Test a successful logout."""
        # First, log the user in
        self.client.login(username="testuser", password="testpassword")

        # Then, log out
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Logout successful.")

    def test_logout_without_login(self):
        """Test logout without being logged in."""
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")
