import pytest
from django.urls import reverse
from django.test import RequestFactory
from frontend.views import get_ranking_redirect
from frontend.views import paginate_list

pytestmark = pytest.mark.django_db


def test_get_ranking_redirect_male():
    resp = get_ranking_redirect("male")
    assert resp.status_code == 302
    assert resp.url == reverse("ranking_male")


def test_get_ranking_redirect_female():
    resp = get_ranking_redirect("female")
    assert resp.status_code == 302
    assert resp.url == reverse("ranking_female")


def test_get_ranking_redirect_mixed():
    resp = get_ranking_redirect("mixed")
    assert resp.status_code == 302
    assert resp.url == reverse("ranking_mixed")


def test_get_ranking_redirect_default_all_or_unknown():
    resp = get_ranking_redirect("all")
    assert resp.status_code == 302
    assert resp.url == reverse("hall_of_fame")

    resp2 = get_ranking_redirect("unknown")
    assert resp2.status_code == 302
    assert resp2.url == reverse("hall_of_fame")

@pytest.mark.django_db
def test_paginate_list_invalid_page_defaults_to_1():
    rf = RequestFactory()
    request = rf.get("/", {"page": "not-an-int"})

    items = list(range(30))  # 30 items, page_size=12 -> 3 pages
    page_items, pagination = paginate_list(items, request, page_size=12)

    assert pagination["current_page"] == 1
    assert pagination["total_pages"] == 3
    assert len(page_items) == 12
    assert page_items[0] == 0