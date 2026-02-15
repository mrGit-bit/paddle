# absolute path: /workspaces/paddle/paddle/frontend/tests/test_about.py

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_favicon_link_present(client):
    response = client.get(reverse("hall_of_fame"))

    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert 'rel="icon"' in html
    assert "frontend/favicon.ico" in html
