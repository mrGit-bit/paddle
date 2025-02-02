# urls.py (frontend)
from django.urls import path
from django.views.generic import TemplateView
from . import views

# The frontend provides the following endpoints:
# - `/`: Endpoint for the Hall of Fame.
# - `/register/`: Endpoint for user registration.
# - `/login/`: Endpoint for user login.
# - `/logout/`: Endpoint for user logout.
# - `/players/<id>/`: Endpoint for player details and stats.
# - `/users/<id>/`: Endpoint for editing user details.
# - `/matches/`: Endpoint for adding match results.
# - `/stats/`: Endpoint for statistics.

urlpatterns = [
    path('', views.hall_of_fame_view, name='hall_of_fame'),    
    path('register/', views.register_view, name='register'),
    path('matches/', views.match_view, name='match'),
    path('users/<int:id>/', views.user_view, name='user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Future Endpoints with new functionalities
    # path('stats/', views.stats_view, name='stats'),
    # path('players/<int:id>/', views.player_view, name='player'),
]
