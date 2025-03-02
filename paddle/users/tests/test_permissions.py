from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from games.models import Player

class UserViewSetPermissionsTests(APITestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username="user1", password="password1", email="user1@example.com")
        self.user2 = User.objects.create_user(username="user2", password="password2", email="user2@example.com")
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpassword", email="admin@example.com")

        # Ensure each user has a linked Player 
        self.player1 = Player.objects.create(name=self.user1.username, registered_user=self.user1, wins=0)
        self.player2 = Player.objects.create(name=self.user2.username, registered_user=self.user2, wins=0)
        self.admin_player = Player.objects.create(name=self.admin_user.username, registered_user=self.admin_user, wins=0)
        
    def test_create_user_permission(self):
        """Test that anyone can create a user."""
        data = {"username": "new_user", "password": "newpassword", "email": "new_user@example.com"}
        response = self.client.post("/api/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_users_permission_admin(self):
        """Test that only admin users can view the list of users."""
        self.client.login(username="admin", password="adminpassword")
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users_permission_not_admin(self):
        """Test that regular users cannot view the list of users."""
        self.client.login(username="user1", password="password1")
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_permission(self):
        """Test that authenticated users can retrieve their profile."""
        self.client.login(username="user1", password="password1")
        response = self.client.get(f"/api/users/{self.user1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_other_user_permission(self):
        """Test that a regular user can not retrieve other user's profile."""
        self.client.login(username="user1", password="password1")
        response = self.client.get(f"/api/users/{self.user2.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_permission(self):
        """Test that authenticated users can update their own profile."""
        self.client.login(username="user1", password="password1")
        data = {"username": "updated_user1", "email": "updated_user1@example.com"}
        response = self.client.patch(f"/api/users/{self.user1.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_other_user_permission(self):
        """Test that authenticated users cannot update another user's profile."""
        self.client.login(username="user1", password="password1")
        data = {"username": "updated_user2"}
        response = self.client.patch(f"/api/users/{self.user2.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_permissions(self):
        """Test that an admin user can view, update, and delete any profile."""
        self.client.login(username="admin", password="adminpassword")
        
        # Admin can view any profile
        response = self.client.get(f"/api/users/{self.user1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Admin can update any profile
        data = {"username": "admin_updated_user1"}
        response = self.client.patch(f"/api/users/{self.user1.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Admin can delete any profile
        response = self.client.delete(f"/api/users/{self.user1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_own_user_permission(self):
        """Test that regular users cannot delete their own user's profile."""
        self.client.login(username="user1", password="password1")
        response = self.client.delete(f"/api/users/{self.user1.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_other_user_permission(self):
        """Test that authenticated users cannot delete another user's profile."""
        self.client.login(username="user1", password="password1")
        response = self.client.delete(f"/api/users/{self.user2.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
