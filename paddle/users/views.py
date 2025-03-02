# users/views.py
# with session based authentication

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission

from .serializers import UserSerializer

class IsUserOrAdmin(BasePermission):
    # Custom permission: Users can view and update only their own profile,
    # and Admin users can access any profile
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users:
    - Regular users can retrieve and update only their own profile.
    - Admin are the only ones who can list and delete users.
    """    
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get_permissions(self):
        # Custom permission logic for each action
        if self.action == 'create':            
            permission_classes = [AllowAny] # Allow anyone to register a new user
        elif self.action in ['list', 'destroy']:            
            permission_classes = [IsAdminUser] # Only admin users can list and delete users
        elif self.action in ['retrieve', 'update', 'partial_update']:            
            permission_classes = [IsAuthenticated, IsUserOrAdmin] # Users can access & edit only their own profile
        else: # Default permission
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
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
        logout(request)  # End the session
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        
