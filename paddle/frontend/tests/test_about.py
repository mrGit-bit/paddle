# absolute path: /workspaces/paddle/paddle/frontend/tests/test_about.py

import pytest
from django.template import engines
from django.urls import reverse
from frontend import context_processors


def _set_app_version_processor(monkeypatch, processor):
    django_engine = engines["django"].engine
    processors = list(django_engine.template_context_processors)
    replaced = False
    for index, existing in enumerate(processors):
        existing_module = getattr(existing, "__module__", None)
        existing_name = getattr(existing, "__name__", None)
        if existing_module == "frontend.context_processors" and existing_name == "app_version":
            processors[index] = processor
            replaced = True
            break
        if existing_module == __name__ and existing_name == "processor":
            processors[index] = processor
            replaced = True
            break
    if not replaced:
        processors.append(processor)
    monkeypatch.setattr(
        django_engine, "template_context_processors", tuple(processors), raising=False
    )


def _patch_app_version(monkeypatch, value):
    def processor(request):
        return {"app_version": value}

    monkeypatch.setattr(context_processors, "app_version", processor)
    _set_app_version_processor(monkeypatch, processor)


@pytest.mark.django_db
def test_about_page_shows_app_version(client, monkeypatch):
    _patch_app_version(monkeypatch, "1.2.1")

    response = client.get(reverse("about"))

    assert response.status_code == 200
    assert "1.2.1" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_about_page_shows_fallback_when_missing(client, monkeypatch):
    _patch_app_version(monkeypatch, "")

    response = client.get(reverse("about"))

    assert response.status_code == 200
    assert "—" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_favicon_link_present(client):
    response = client.get(reverse("hall_of_fame"))

    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert 'rel="icon"' in html
    assert "frontend/favicon.ico" in html
