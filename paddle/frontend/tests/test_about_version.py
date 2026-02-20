import pytest
from django.urls import reverse

from frontend import views

pytestmark = pytest.mark.django_db


def test_about_page_shows_configured_version_label(client):
    response = client.get(reverse("about"))

    assert response.status_code == 200
    assert "1.3.0" in response.content.decode("utf-8")


def test_about_page_shows_fallback_when_version_missing(client, monkeypatch):
    monkeypatch.setattr(views, "get_about_app_version_label", lambda: None)

    response = client.get(reverse("about"))

    assert response.status_code == 200
    assert "—" in response.content.decode("utf-8")
