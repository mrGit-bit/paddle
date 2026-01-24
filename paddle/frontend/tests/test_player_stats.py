import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from games.models import Player
from django.contrib.auth.models import AnonymousUser

from frontend.views import get_player_stats

User = get_user_model()

@pytest.mark.django_db
def test_get_player_stats_authenticated_user_without_player():
    rf = RequestFactory()
    user = User.objects.create_user(username="u1", password="pass")
    request = rf.get("/")
    request.user = user  # authenticated, but no Player linked

    stats = get_player_stats(request)

    assert stats["player_id"] is None
    assert stats["wins"] == 0
    assert stats["matches"] == 0
    assert stats["win_rate"] == "0%"
    assert stats["ranking_position"] == 0
    assert "ranking_total" in stats

@pytest.mark.django_db
def test_get_player_stats_returns_defaults_when_no_player_id():
    rf = RequestFactory()
    request = rf.get("/")
    request.user = AnonymousUser()  # <- FIX

    stats = get_player_stats(request, player_id=None)

    assert stats["player_id"] is None
    assert stats["wins"] == 0

@pytest.mark.django_db
def test_get_player_stats_invalid_player_id_returns_defaults():
    rf = RequestFactory()
    request = rf.get("/")
    request.user = User()  # user irrelevant because player_id provided

    stats = get_player_stats(request, player_id=999999)

    assert stats["player_id"] == 999999
    assert stats["wins"] == 0
    assert stats["matches"] == 0
    assert stats["win_rate"] == "0%"

@pytest.mark.django_db
def test_get_player_stats_valid_player_id_returns_computed_values():
    rf = RequestFactory()
    request = rf.get("/")
    request.user = User()

    p = Player.objects.create(name="P1", ranking_position=7)
    # With 0 matches, wins=0/matches=0 still, but update() is executed

    stats = get_player_stats(request, player_id=p.id)

    assert stats["player_id"] == p.id
    assert stats["ranking_position"] == 7
    assert stats["win_rate"].endswith("%")
