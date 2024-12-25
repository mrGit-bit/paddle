from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    # Include the URLs from the games app
    path('api/games/', include('games.urls')),
    # Include the URLs from the users app
    path('api/users/', include('users.urls')),
    # Adds the login and logout endpoints for the browsable API    
    path('api-auth/', include('rest_framework.urls')),
]
