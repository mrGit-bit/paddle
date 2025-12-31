# americano/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.americano_list, name="americano_list"),
    path("nuevo/", views.americano_new, name="americano_new"),
    path("<int:pk>/", views.americano_detail, name="americano_detail"),
    path("<int:pk>/nueva-ronda/", views.americano_new_round, name="americano_new_round"),
    path("round/<int:round_id>/assign/", views.americano_assign_round, name="americano_assign_round"),
    path("round/<int:round_id>/delete/", views.americano_delete_round, name="americano_delete_round"),
    path("delete/<int:pk>/", views.americano_delete_tournament, name="americano_delete_tournament"),        
]
