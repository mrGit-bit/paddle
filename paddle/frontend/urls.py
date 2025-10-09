# urls.py (frontend)
from django.urls import path
from django.views.generic import TemplateView
from . import views

# The frontend provides the following endpoints:
# - `/`: Endpoint for the Hall of Fame.
# - `/register/`: Endpoint for user registration.
# - `/matches/`: Endpoint for listing, adding, and deleting matches.
# - `/users/<id>/`: Endpoint for editing user details.
# - `/login/`: Endpoint for user login.
# - `/logout/`: Endpoint for user logout.
# - `/about/`: Endpoint for the About page.

urlpatterns = [
    path('', views.hall_of_fame_view, name='hall_of_fame'),    
    path('register/', views.register_view, name='register'),
    path('matches/', views.match_view, name='match'), # Handles listing, adding, deleting      
    path('users/<int:id>/', views.user_view, name='user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about_view, name='about'),    
]