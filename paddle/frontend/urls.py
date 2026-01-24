# absolute path: /workspaces/paddle/paddle/frontend/urls.py

from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

# --- The frontend provides the following endpoints: ---
# - `/`: All ranking page
# - `/ranking/male/`: Male ranking page
# - `/ranking/female/`: Female ranking page
# - `/ranking/mixed/`: Mixed ranking page
# - `/register/`: User registration
# - `/matches/`: Matches list/add/delete
# - `/users/<id>/`: Edit user details
# - `/login/`: User login
# - `/logout/`: User logout
# - `/about/`: About page
# --- Password reset endpoints (built-in Django views, Spanish templates) ---
# - `/password_reset/`: Start password reset (Brevo mail)
# - `/password_reset/done/`: Confirmation that email was sent
# - `/reset/<uidb64>/<token>/`: Enter new password
# - `/reset/done/`: Password successfully changed

urlpatterns = [
    path('', views.hall_of_fame_view, name='hall_of_fame'),
    path('ranking/male/', views.ranking_view, {"scope": "male"}, name='ranking_male'),
    path('ranking/female/', views.ranking_view, {"scope": "female"}, name='ranking_female'),
    path('ranking/mixed/', views.ranking_view, {"scope": "mixed"}, name='ranking_mixed'),    
    path('register/', views.register_view, name='register'),
    path('matches/', views.match_view, name='match'), # Handles listing, adding, deleting      
    path('users/<int:id>/', views.user_view, name='user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about_view, name='about'),
    
    # --- Password reset flow (built-in Django views, Spanish templates) ---
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            form_class=views.EmailExistsPasswordResetForm,
            template_name="frontend/pass_reset/password_reset_form.html",
            email_template_name="frontend/pass_reset/password_reset_email.txt",
            subject_template_name="frontend/pass_reset/password_reset_subject.txt",
            success_url=reverse_lazy("password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="frontend/pass_reset/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="frontend/pass_reset/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="frontend/pass_reset/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),    
]