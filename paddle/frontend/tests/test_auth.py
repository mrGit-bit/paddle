# absolute path: /workspaces/paddle/paddle/frontend/tests/test_auth.py
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

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
def test_register_rejects_duplicate_email_case_insensitive(client):
    User.objects.create_user(
        username="existing",
        email="Existing@Example.com",
        password="pass12345",
    )
    url = reverse("register")

    response = client.post(
        url,
        {
            "username": "newuser",
            "email": "existing@example.com",
            "confirm_email": "existing@example.com",
            "password": "pass12345",
            "confirm_password": "pass12345",
            "gender": "M",
        },
    )

    assert response.status_code == 200
    assert "Ya existe una cuenta con ese correo electrónico." in response.content.decode()
    assert 'invalid-feedback d-block">Ya existe una cuenta con ese correo electrónico.' in response.content.decode()
    assert not User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_profile_update_rejects_duplicate_email_case_insensitive(client):
    owner = User.objects.create_user(
        username="owner",
        email="owner@example.com",
        password="pass12345",
    )
    User.objects.create_user(
        username="taken",
        email="Taken@Example.com",
        password="pass12345",
    )

    client.login(username="owner", password="pass12345")
    url = reverse("user", args=[owner.id])
    response = client.post(
        url,
        {
            "username": "owner",
            "email": "taken@example.com",
            "confirm_email": "taken@example.com",
        },
    )

    assert response.status_code == 200
    assert "Ya existe una cuenta con ese correo electrónico." in response.content.decode()
    assert response.content.decode().count("Ya existe una cuenta con ese correo electrónico.") >= 2
    assert "Los correos electrónicos no coinciden." not in response.content.decode()
    owner.refresh_from_db()
    assert owner.email == "owner@example.com"


@pytest.mark.django_db
def test_logout_view_get_redirects(client):
    user = User.objects.create_user(username="logoutget", password="pass")
    client.login(username="logoutget", password="pass")
    url = reverse("logout")
    resp = client.get(url)
    assert resp.status_code == 302
    assert resp.url == reverse("login")
    
