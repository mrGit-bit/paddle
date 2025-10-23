# tests/test_login.py
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_login_with_email_or_username_case_insensitive(client):
    user = User.objects.create_user(
        username='john',
        email='John.Doe@Example.com',
        password='s3cr3tpass'
    )

    url = reverse('login')  # adjust to your URL name if different

    # Login via email (mixed case)
    resp = client.post(url, {'username': 'john.doe@example.COM', 'password': 's3cr3tpass'})
    assert resp.status_code == 302  # redirected on success

    client.logout()

    # Login via username (mixed case)
    resp = client.post(url, {'username': 'JOHN', 'password': 's3cr3tpass'})
    assert resp.status_code == 302


@pytest.mark.django_db
def test_login_invalid_user(client):
    url = reverse('login')

    # Nonexistent username
    resp = client.post(url, {'username': 'nosuchuser', 'password': 'irrelevant'})
    assert resp.status_code == 200
    assert "Nombre o contraseña no válidos." in resp.content.decode()

    # Nonexistent email
    resp = client.post(url, {'username': 'noone@example.com', 'password': 'irrelevant'})
    assert resp.status_code == 200
    assert "Nombre o contraseña no válidos." in resp.content.decode()


@pytest.mark.django_db
def test_login_invalid_password(client):
    user = User.objects.create_user(
        username='jane',
        email='jane@example.com',
        password='correctpass'
    )

    url = reverse('login')

    # Correct username, wrong password
    resp = client.post(url, {'username': 'jane', 'password': 'wrongpass'})
    assert resp.status_code == 200
    assert "Nombre o contraseña no válidos." in resp.content.decode()

    # Correct email, wrong password
    resp = client.post(url, {'username': 'jane@example.com', 'password': 'wrongpass'})
    assert resp.status_code == 200
    assert "Nombre o contraseña no válidos." in resp.content.decode()

@pytest.mark.django_db
def test_logout_view_get_redirects(client):
    user = User.objects.create_user(username="logoutget", password="pass")
    client.login(username="logoutget", password="pass")
    url = reverse("logout")
    resp = client.get(url)
    assert resp.status_code == 302
    assert resp.url == reverse("login")
    

