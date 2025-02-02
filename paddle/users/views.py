# users/views.py
# with session based authentication

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get_permissions(self):
        # Custom permission logic for each action
        if self.action == 'create':
            # Allow anyone to register a new user
            permission_classes = [AllowAny]
        elif self.action == 'list':
            # Only authenticated users can view the list of users
            permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            # Only authenticated users can view, update, or delete profiles
            permission_classes = [IsAuthenticated]
        else: # Default permission
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_object(self):
        # Ensure that users can only update, retrieve, or delete their own profile
        # Admin users can update, retrieve, or delete any profile
        obj = super().get_object()
        if self.action in ['update', 'partial_update', 'destroy']:
            if obj != self.request.user and not self.request.user.is_staff:
                raise PermissionDenied("You do not have permission to modify this profile.")
        return obj
    
class LoginView(APIView):
    """
    Login endpoint for users to authenticate using session-based authentication.
    """
    permission_classes = [AllowAny]  # Allow anyone to access this endpoint

    
    def post(self, request, *args, **kwargs):
        # Use DRF's serializer to handle validation
        username = request.data.get("username")
        password = request.data.get("password")

        # Check if both fields are provided
        if not username or not password:
            # Rely on DRF's validation conventions
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_400_BAD_REQUEST)
        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)  # Log the user in and create a session
            return Response(
                {
                    "message": "Login successful.",
                    "user_id": user.id,
                    "username": user.username,
                },
                status=status.HTTP_200_OK,
            )
        # DRF convention for unauthorized access
        else:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    Logout endpoint to end the session of the authenticated user.
    """
    permission_classes = [IsAuthenticated] 
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)  # End the session
            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        # Use DRF's convention for unauthorized access
        else:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)
    
