from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    # Include the URLs from the frontend app
    path('', include('frontend.urls')),
    # Include the URLs from the americano app
    path('americano/', include('americano.urls')),
]
