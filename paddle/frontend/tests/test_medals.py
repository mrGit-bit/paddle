import re
from pathlib import Path

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from frontend.medals.config import MEDAL_DEFINITIONS, SCOPE_CONFIG
from frontend.services import medals as medal_service
from frontend.view_modules import ranking as ranking_views
from games.models import Group, Player


User = get_user_model()


def ranked_player(
    player_id,
    name,
    *,
    position,
    matches=1,
    win_rate=50.0,
    gender=Player.GENDER_MALE,
    group=None,
):
    player = Player(id=player_id, name=name, gender=gender, group=group)
    player.display_position = position
    player.display_matches = matches
    player.display_win_rate = win_rate
    player.display_wins = round((matches * win_rate) / 100)
    player.show_position = True
    return player


def patch_rankings(monkeypatch, players_by_scope):
    def fake_compute_rankings_for_scopes(scopes, *, group=None):
        return {
            scope: (players_by_scope.get(scope, []), [], scope)
            for scope in scopes
        }

    monkeypatch.setattr(medal_service, "compute_rankings_for_scopes", fake_compute_rankings_for_scopes)
    monkeypatch.setattr(
        medal_service,
        "build_pairs_ranking_sections",
        lambda group=None: {
            "top_pairs": [],
            "pairs_of_the_century": [],
            "catastrophic_pairs": [],
        },
    )


def medal_names(row):
    return [medal["name"] for medal in row["medals"]]


def medal_keys(row):
    return [medal["key"] for medal in row["medals"]]


def medal_scopes(row, medal_key):
    return [medal["scope"] for medal in row["medals"] if medal["key"] == medal_key]


def test_medal_config_defines_required_metadata():
    assert len(MEDAL_DEFINITIONS) == 13
    assert list(SCOPE_CONFIG.keys()) == ["all", "male", "female", "mixed", "pairs"]

    keys = [medal["key"] for medal in MEDAL_DEFINITIONS]
    assert len(keys) == len(set(keys))
    assert "pairs_century" in keys
    assert "pairs_catastrophic_diamond" not in keys

    required_medal_fields = {"key", "name", "icon", "description", "category", "scopes", "order"}
    for medal in MEDAL_DEFINITIONS:
        assert required_medal_fields <= set(medal)
        assert set(medal["scopes"]) <= set(SCOPE_CONFIG)

    individual_orders = [
        medal["order"] for medal in MEDAL_DEFINITIONS if "pairs" not in medal["scopes"]
    ]
    pair_orders = [
        medal["order"] for medal in MEDAL_DEFINITIONS if medal["scopes"] == ["pairs"]
    ]
    assert min(pair_orders) > max(individual_orders)

    orders_by_key = {medal["key"]: medal["order"] for medal in MEDAL_DEFINITIONS}
    assert orders_by_key["pairs_century"] < orders_by_key["pairs_catastrophic"]

    for scope in SCOPE_CONFIG.values():
        assert {"label", "css_class", "progress_color_class"} <= set(scope)
        assert scope["css_class"] == scope["progress_color_class"]

    assert SCOPE_CONFIG["pairs"]["css_class"] == "circular-progress-danger"
    assert SCOPE_CONFIG["pairs"]["progress_color_class"] == "circular-progress-danger"


def test_medal_scope_styles_cover_configured_scopes():
    styles = (
        Path(__file__).resolve().parents[1]
        / "static"
        / "frontend"
        / "css"
        / "styles.css"
    ).read_text()

    for scope in SCOPE_CONFIG.values():
        assert f".{scope['css_class']}" in styles
        assert f".{scope['progress_color_class']}" in styles
        assert f".medallero-medal-card.{scope['css_class']}" in styles


def test_medal_service_keeps_pair_scope_out_of_individual_ranking_batch(monkeypatch):
    players = [ranked_player(1, "Ranked Player", position=1)]
    calls = []

    def fake_compute_rankings_for_scopes(scopes, *, group=None):
        calls.append(tuple(scopes))
        return {
            scope: (players if scope == "all" else [], [], scope)
            for scope in scopes
            if scope != "pairs"
        }

    monkeypatch.setattr(medal_service, "compute_rankings_for_scopes", fake_compute_rankings_for_scopes)
    monkeypatch.setattr(
        medal_service,
        "build_pairs_ranking_sections",
        lambda group=None: {
            "top_pairs": [],
            "pairs_of_the_century": [],
            "catastrophic_pairs": [],
        },
    )

    rows_by_name = {row["player"].name: row for row in medal_service.build_medallero_rows()}

    assert "Ranked Player" in rows_by_name
    assert calls == [("all", "male", "female", "mixed")]


def test_medal_service_includes_top_12_display_positions_and_ties(monkeypatch):
    players = [
        ranked_player(1, "Player 1", position=1),
        ranked_player(2, "Player 12 A", position=12),
        ranked_player(3, "Player 12 B", position=12),
        ranked_player(4, "Player 13", position=13, matches=99, win_rate=100.0),
    ]
    patch_rankings(monkeypatch, {"all": players})

    rows = medal_service.build_medallero_rows()
    rows_by_name = {row["player"].name: row for row in rows}

    assert "Player 12 A" in rows_by_name
    assert "Player 12 B" in rows_by_name
    assert "Player 13" not in rows_by_name
    assert "Cuadro de honor" in medal_names(rows_by_name["Player 12 A"])
    assert medal_scopes(rows_by_name["Player 12 B"], "cuadro_honor") == ["all"]


def test_medal_service_awards_tied_position_medals(monkeypatch):
    players = [
        ranked_player(1, "Gold A", position=1),
        ranked_player(2, "Gold B", position=1),
        ranked_player(3, "Silver A", position=2),
        ranked_player(4, "Bronze A", position=3),
        ranked_player(5, "Bronze B", position=3),
    ]
    patch_rankings(monkeypatch, {"all": players})

    rows_by_name = {row["player"].name: row for row in medal_service.build_medallero_rows()}

    assert "Primer puesto" in medal_names(rows_by_name["Gold A"])
    assert "Primer puesto" in medal_names(rows_by_name["Gold B"])
    assert "Segundo puesto" in medal_names(rows_by_name["Silver A"])
    assert "Tercer puesto" in medal_names(rows_by_name["Bronze A"])
    assert "Tercer puesto" in medal_names(rows_by_name["Bronze B"])


def test_medal_service_performance_medals_include_cutoff_ties_only_for_eligible_players(monkeypatch):
    players = [
        ranked_player(1, "Efficiency 100", position=1, matches=3, win_rate=100.0),
        ranked_player(2, "Efficiency 90", position=2, matches=8, win_rate=90.0),
        ranked_player(3, "Efficiency 80 A", position=3, matches=10, win_rate=80.004),
        ranked_player(4, "Efficiency 80 B", position=4, matches=10, win_rate=80.003),
        ranked_player(5, "Efficiency Out", position=13, matches=50, win_rate=100.0),
        ranked_player(6, "Matches 8 Tie", position=5, matches=8, win_rate=10.0),
        ranked_player(7, "Matches 7", position=6, matches=7, win_rate=10.0),
    ]
    patch_rankings(monkeypatch, {"all": players})

    rows_by_name = {row["player"].name: row for row in medal_service.build_medallero_rows()}

    assert "Top 3 eficacia" in medal_names(rows_by_name["Efficiency 100"])
    assert "Top 3 eficacia" in medal_names(rows_by_name["Efficiency 90"])
    assert "Top 3 eficacia" in medal_names(rows_by_name["Efficiency 80 A"])
    assert "Top 3 eficacia" in medal_names(rows_by_name["Efficiency 80 B"])
    assert "Efficiency Out" not in rows_by_name
    assert "Top 3 partidos" in medal_names(rows_by_name["Efficiency 80 A"])
    assert "Top 3 partidos" in medal_names(rows_by_name["Efficiency 80 B"])
    assert "Top 3 partidos" in medal_names(rows_by_name["Efficiency 90"])
    assert "Top 3 partidos" in medal_names(rows_by_name["Matches 8 Tie"])
    assert "Top 3 partidos" not in medal_names(rows_by_name["Matches 7"])


def test_medal_service_includes_pair_medals_in_individual_rows(monkeypatch):
    players = [
        ranked_player(1, "Pair A", position=1),
        ranked_player(2, "Pair B", position=2),
        ranked_player(3, "Pair C", position=3),
        ranked_player(4, "Pair D", position=4),
        ranked_player(5, "Pair E", position=5),
        ranked_player(6, "Pair F", position=6),
        ranked_player(7, "Pair G", position=7),
    ]
    patch_rankings(monkeypatch, {"all": players})

    monkeypatch.setattr(
        medal_service,
        "build_pairs_ranking_sections",
        lambda group=None: {
            "top_pairs": [
                {"player1": players[0], "player2": players[1]},
                {"player1": players[2], "player2": players[3]},
                {"player1": players[4], "player2": players[5]},
                {"player1": players[6], "player2": players[0]},
                {"player1": players[1], "player2": players[2]},
            ],
            "pairs_of_the_century": [
                {"player1": players[0], "player2": players[1]},
            ],
            "catastrophic_pairs": [
                {"player1": players[2], "player2": players[3]},
            ],
        },
    )

    rows_by_name = {row["player"].name: row for row in medal_service.build_medallero_rows()}

    assert "pairs_first_place" in medal_keys(rows_by_name["Pair A"])
    assert "pairs_first_place" in medal_keys(rows_by_name["Pair B"])
    assert "pairs_second_place" in medal_keys(rows_by_name["Pair C"])
    assert "pairs_second_place" in medal_keys(rows_by_name["Pair D"])
    assert "pairs_third_place" in medal_keys(rows_by_name["Pair E"])
    assert "pairs_third_place" in medal_keys(rows_by_name["Pair F"])
    assert "pairs_fourth_place" in medal_keys(rows_by_name["Pair G"])
    assert "pairs_fifth_place" in medal_keys(rows_by_name["Pair B"])
    assert "pairs_catastrophic" in medal_keys(rows_by_name["Pair C"])
    assert "pairs_century" in medal_keys(rows_by_name["Pair A"])


def fake_medals():
    medal = {
        "key": "first_place",
        "name": "Primer puesto",
        "icon": "🥇",
        "description": "Ocupa la primera posición de su ranking.",
        "category": "position",
        "order": 1,
        "scope": "all",
        "scope_label": "Todos",
        "scope_css_class": "circular-progress-primary",
        "progress_color_class": "circular-progress-primary",
    }
    return [medal]


def fake_medallero_rows(group=None, medals=None):
    player = ranked_player(1, "Medal Player", position=1, group=group)
    medals = medals or fake_medals()
    medal_rows = [medals[index:index + 3] for index in range(0, len(medals), 3)]
    medal_rows[-1] = medal_rows[-1] + [None] * (3 - len(medal_rows[-1]))
    return [
        {
            "player": player,
            "medals": medals,
            "total_medals": len(medals),
            "first_place_medals": 1,
            "position_medals": len(medals),
            "performance_medals": 0,
            "medal_rows": medal_rows,
        }
    ]


@pytest.mark.django_db
def test_medallero_page_renders_publicly_with_metadata_and_empty_slots(client, monkeypatch):
    monkeypatch.setattr(ranking_views, "build_medallero_rows", fake_medallero_rows)
    monkeypatch.setattr(ranking_views, "get_player_page_in_scope", lambda scope, player_id, page_size=12, *, group=None: 4)

    response = client.get(reverse("medallero"))
    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert re.search(r'<h1 class="display-5">[^<]*Medallero[^<]*</h1>', content)
    assert "Medal Player" in content
    assert 'class="accordion medallero-list" id="medalleroAccordion"' in content
    assert "accordion-button medallero-player-toggle collapsed" in content
    assert 'data-bs-toggle="collapse"' in content
    assert 'data-bs-target="#medalleroPlayer1"' in content
    assert 'aria-expanded="false"' in content
    assert 'data-bs-parent="#medalleroAccordion"' in content
    assert re.search(
        r'class="h4 mb-0 medallero-player-name">Medal Player</span>\s*'
        r'<span class="badge medallero-total"[^>]*>1</span>',
        content,
    )
    assert "1 medallas" not in content
    assert content.count("medallero-medal-icon-small") == 1
    assert "Primer puesto" in content
    assert "Todos" in content
    assert "circular-progress-primary" in content
    assert "medallero-scope-ribbon" in content
    assert 'href="/?page=4#top"' in content
    assert "medallero-medal-icon-large" in content
    assert "Ocupa la primera posición de su ranking." not in content
    assert "medallero-medal-wheel" not in content
    assert content.count("medallero-empty-slot") == 2


@pytest.mark.django_db
def test_medallero_summary_icon_strip_renders_every_player_medal(client, monkeypatch):
    medals = []
    for index, icon in enumerate(["🥇", "🥈", "🥉", "🏅"], start=1):
        medal = fake_medals()[0].copy()
        medal["key"] = f"medal_{index}"
        medal["name"] = f"Medalla {index}"
        medal["icon"] = icon
        medals.append(medal)

    monkeypatch.setattr(
        ranking_views,
        "build_medallero_rows",
        lambda group=None: fake_medallero_rows(group=group, medals=medals),
    )

    response = client.get(reverse("medallero"))
    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert re.search(r'class="badge medallero-total"[^>]*>4</span>', content)
    assert "medallero-icon-strip" in content
    assert content.count("medallero-medal-icon-small") == 4


def test_medallero_summary_icon_strip_uses_dynamic_overlap_only_when_needed():
    styles = (
        Path(__file__).resolve().parents[1]
        / "static"
        / "frontend"
        / "css"
        / "styles.css"
    ).read_text()
    script = (
        Path(__file__).resolve().parents[1]
        / "static"
        / "frontend"
        / "js"
        / "medalleroIconStrip.js"
    ).read_text()

    icon_strip_rule = re.search(r"\.medallero-icon-strip\s*\{(?P<body>[^}]+)\}", styles)
    small_icon_rule = re.search(r"\.medallero-medal-icon-small\s*\{(?P<body>[^}]+)\}", styles)

    assert icon_strip_rule is not None
    assert small_icon_rule is not None
    assert "flex-wrap: nowrap" in icon_strip_rule.group("body")
    assert "gap: 0.2rem" in icon_strip_rule.group("body")
    assert "var(--medallero-icon-overlap, 0px)" in small_icon_rule.group("body")
    assert "Math.max(0, fullWidth - availableWidth)" in script
    assert "--medallero-icon-overlap" in script


@pytest.mark.django_db
def test_medallero_navbar_link_appears_after_parejas_and_before_torneos(client, monkeypatch):
    monkeypatch.setattr(ranking_views, "build_medallero_rows", fake_medallero_rows)

    response = client.get(reverse("medallero"))
    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert re.search(r">Parejas<.*>Medallero<.*Torneos", content, re.S)
    assert f'href="{reverse("medallero")}"' in content


@pytest.mark.django_db
def test_medallero_uses_aggregate_for_anonymous_and_user_group_for_linked_user(client, monkeypatch):
    calls = []
    aggregate_row_group = Group.objects.create(name="Aggregate Row Group")

    def fake_build_medallero_rows(*, group=None):
        calls.append(group)
        row_group = aggregate_row_group if group is None else group
        return fake_medallero_rows(group=row_group)

    monkeypatch.setattr(ranking_views, "build_medallero_rows", fake_build_medallero_rows)

    anonymous_response = client.get(reverse("medallero"))
    anonymous_content = anonymous_response.content.decode("utf-8")
    assert anonymous_response.status_code == 200
    assert calls[-1] is None
    assert "Aggregate Row Group" not in anonymous_content
    assert "text-muted small d-block" not in anonymous_content

    group = Group.objects.create(name="Grupo Medallero")
    user = User.objects.create_user(username="medallero", password="pass")
    Player.objects.create(name="Linked Medallero", registered_user=user, group=group)
    client.login(username="medallero", password="pass")

    linked_response = client.get(reverse("medallero"))
    assert linked_response.status_code == 200
    assert calls[-1] == group
