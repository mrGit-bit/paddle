# urls.py (users)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LoginView, LogoutView

# Create a router for standard CRUD actions
router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # Login endpoint
    path('logout/', LogoutView.as_view(), name='logout'), # Logout endpoint
    path('', include(router.urls)),  # Include router URLs at the end to avoid conflicts
]
