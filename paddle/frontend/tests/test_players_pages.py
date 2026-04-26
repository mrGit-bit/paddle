import re
from datetime import date, timedelta
from pathlib import Path

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from games.models import Group, Match, Player


pytestmark = pytest.mark.django_db
User = get_user_model()


def create_match(
    player,
    partner,
    rival_1,
    rival_2,
    *,
    winning_team,
    played_on,
    player_on_team1=True,
):
    if player_on_team1:
        return Match.objects.create(
            team1_player1=player,
            team1_player2=partner,
            team2_player1=rival_1,
            team2_player2=rival_2,
            winning_team=winning_team,
            date_played=played_on,
        )
    return Match.objects.create(
        team1_player1=rival_1,
        team1_player2=rival_2,
        team2_player1=player,
        team2_player2=partner,
        winning_team=winning_team,
        date_played=played_on,
    )


def count_trend_wheels(content):
    return len(re.findall(r'class="circular-progress(?:\s|")', content))


def scope_by_key(insights, key):
    return next(scope for scope in insights["efficiency_scopes"] if scope["key"] == key)


def test_players_list_is_public_200(client):
    Player.objects.create(name="Jugador Uno", gender=Player.GENDER_MALE)
    response = client.get(reverse("players"))
    content = response.content.decode("utf-8")
    assert response.status_code == 200
    assert "Jugador Uno" in content
    assert "<h1 class=\"display-5\">Jugadores</h1>" in content


def test_players_list_anonymous_selector_shows_player_names_without_groups(client):
    group_a = Group.objects.create(name="Club Norte")
    group_b = Group.objects.create(name="Club Sur")
    Player.objects.create(name="Jugador Norte", gender=Player.GENDER_MALE, group=group_a)
    Player.objects.create(name="Jugador Sur", gender=Player.GENDER_FEMALE, group=group_b)

    response = client.get(reverse("players"))
    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert re.search(r"<option[^>]*>\s*Jugador Norte\s*</option>", content)
    assert re.search(r"<option[^>]*>\s*Jugador Sur\s*</option>", content)
    assert "Jugador Norte — Club Norte" not in content
    assert "Jugador Sur — Club Sur" not in content


def test_players_list_redirects_authenticated_user_to_linked_player_detail(client):
    user = User.objects.create_user(username="perfil", password="pass")
    player = Player.objects.create(
        name="Perfil Propio",
        gender=Player.GENDER_MALE,
        registered_user=user,
    )

    client.login(username="perfil", password="pass")
    response = client.get(reverse("players"))

    assert response.status_code == 302
    assert response.url == reverse("player_detail", args=[player.id])


def test_players_list_authenticated_user_without_player_keeps_empty_selector(client):
    User.objects.create_user(username="sinperfil", password="pass")
    Player.objects.create(name="Jugador Disponible", gender=Player.GENDER_MALE)

    client.login(username="sinperfil", password="pass")
    response = client.get(reverse("players"))
    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "<h1 class=\"display-5\">Jugadores</h1>" in content
    assert "Jugador Disponible" in content


def test_player_detail_is_public_200(client):
    player = Player.objects.create(name="Jugador Perfil", gender=Player.GENDER_MALE)
    response = client.get(reverse("player_detail", args=[player.id]))
    content = response.content.decode("utf-8")
    assert response.status_code == 200
    assert "Jugador Perfil" in content
    assert f"<h1 class=\"display-5\">{player.name}</h1>" in content


def test_player_detail_anonymous_selector_shows_player_names_without_groups(client):
    group_a = Group.objects.create(name="Club Alfa")
    group_b = Group.objects.create(name="Club Beta")
    selected_player = Player.objects.create(
        name="Perfil Alfa",
        gender=Player.GENDER_MALE,
        group=group_a,
    )
    Player.objects.create(name="Perfil Beta", gender=Player.GENDER_FEMALE, group=group_b)

    response = client.get(reverse("player_detail", args=[selected_player.id]))
    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert re.search(r"<option[^>]*>\s*Perfil Alfa\s*</option>", content)
    assert re.search(r"<option[^>]*>\s*Perfil Beta\s*</option>", content)
    assert "Perfil Alfa — Club Alfa" not in content
    assert "Perfil Beta — Club Beta" not in content


def test_player_detail_404(client):
    response = client.get(reverse("player_detail", args=[999999]))
    assert response.status_code == 404


def test_player_detail_matches_filtered(client):
    player_a = Player.objects.create(name="Player A", gender=Player.GENDER_MALE)
    player_b = Player.objects.create(name="Player B", gender=Player.GENDER_MALE)
    player_c = Player.objects.create(name="Player C", gender=Player.GENDER_MALE)
    player_d = Player.objects.create(name="Player D", gender=Player.GENDER_MALE)
    player_e = Player.objects.create(name="Player E", gender=Player.GENDER_MALE)
    player_f = Player.objects.create(name="Player F", gender=Player.GENDER_MALE)
    player_g = Player.objects.create(name="Player G", gender=Player.GENDER_MALE)
    player_h = Player.objects.create(name="Player H", gender=Player.GENDER_MALE)

    involving_a = Match.objects.create(
        team1_player1=player_a,
        team1_player2=player_b,
        team2_player1=player_c,
        team2_player2=player_d,
        winning_team=1,
        date_played=date(2026, 1, 10),
    )
    not_involving_a = Match.objects.create(
        team1_player1=player_e,
        team1_player2=player_f,
        team2_player1=player_g,
        team2_player2=player_h,
        winning_team=2,
        date_played=date(2026, 1, 11),
    )

    response = client.get(reverse("player_detail", args=[player_a.id]))
    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert f"match-card-{involving_a.id}" in content
    assert f"match-card-{not_involving_a.id}" not in content


def test_player_detail_scope_rows_render_data_href_only_when_applicable(client):
    player_a = Player.objects.create(name="Scope A", gender=Player.GENDER_MALE)
    player_b = Player.objects.create(name="Scope B", gender=Player.GENDER_MALE)
    player_c = Player.objects.create(name="Scope C", gender=Player.GENDER_MALE)
    player_d = Player.objects.create(name="Scope D", gender=Player.GENDER_MALE)

    Match.objects.create(
        team1_player1=player_a,
        team1_player2=player_b,
        team2_player1=player_c,
        team2_player2=player_d,
        winning_team=1,
        date_played=date(2026, 1, 12),
    )

    response = client.get(reverse("player_detail", args=[player_a.id]))
    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "player-ranking-progress-list" in content
    assert '<th scope="col">Rkg.</th>' not in content
    assert 'href="/?page=1#top"' in content
    assert 'href="/ranking/male/?page=1#top"' in content
    assert 'data-href="/?page=1#top"' in content
    assert 'data-href="/ranking/male/?page=1#top"' in content
    assert 'data-href="/ranking/mixed/' not in content
    assert "Todos" in content
    assert "Masc." in content
    assert "Mixtos" in content
    assert "#1 de 4" in content
    assert 'aria-label="#1 de 4"' in content
    assert '<div class="progress-bar bg-primary" style="width: 100%;"></div>' in content
    assert '<div class="progress-bar bg-success" style="width: 100%;"></div>' in content
    assert "--player-ranking-progress-percent: 100%;" in content
    assert "1🏆/1🏓" in content
    assert "0🏆/0🏓" in content
    assert "player-ranking-cards" not in content
    assert "player-ranking-card" not in content
    assert "player-scope-primary" in content
    assert "player-scope-success" in content
    assert "player-scope-warning" in content
    assert "player-scope-danger" not in content
    assert "player-ranking-bar-labels" in content
    assert "player-ranking-bar-labels-track" in content
    assert "player-ranking-bar-labels-fill" in content
    assert "player-ranking-rank" not in content
    assert "player-ranking-medal" not in content
    assert "🥇" not in content
    assert "Sin datos" in content


def test_player_detail_ranking_progress_uses_display_rank_and_ranked_total(client):
    player_a = Player.objects.create(name="Progress A", gender=Player.GENDER_MALE)
    player_b = Player.objects.create(name="Progress B", gender=Player.GENDER_MALE)
    player_c = Player.objects.create(name="Progress C", gender=Player.GENDER_MALE)
    player_d = Player.objects.create(name="Progress D", gender=Player.GENDER_MALE)

    Match.objects.create(
        team1_player1=player_a,
        team1_player2=player_b,
        team2_player1=player_c,
        team2_player2=player_d,
        winning_team=1,
        date_played=date(2026, 1, 13),
    )

    response = client.get(reverse("player_detail", args=[player_c.id]))
    content = response.content.decode("utf-8")
    scope_rows = response.context["scope_rows"]
    all_scope = next(row for row in scope_rows if row["scope"] == "all")

    assert response.status_code == 200
    assert all_scope["scoped_player"].display_position == 3
    assert all_scope["ranking_total"] == 4
    assert all_scope["rank_label"] == "🥉"
    assert all_scope["rank_is_medal"] is True
    assert all_scope["progress_percent"] == 50
    assert all_scope["support_text"] == "#3 de 4"
    assert "🥉" not in content
    assert "#3 de 4" in content
    assert 'aria-valuenow="50"' in content
    assert 'style="width: 50%;"' in content
    assert "--player-ranking-progress-percent: 50%;" in content


def test_player_detail_insights_defaults_with_zero_matches(client):
    player = Player.objects.create(name="Zero Insights", gender=Player.GENDER_MALE)

    response = client.get(reverse("player_detail", args=[player.id]))
    content = response.content.decode("utf-8")
    css = Path("paddle/frontend/static/frontend/css/styles.css").read_text()
    insights = response.context["player_insights"]

    assert response.status_code == 200
    assert '<h4 class="mb-4">Estadísticas</h4>' in content
    assert "Rankings" in content
    assert "Últimos partidos" in content
    assert "Balance acumulado" in content
    for title in [
        "Rankings",
        "Últimos partidos",
        "Pareja habitual",
        "Parejas rivales frecuentes",
        "Contendientes",
    ]:
        assert re.search(
            rf'<div class="card shadow mb-4">\s*'
            rf'<div class="card-body">\s*'
            rf'<h4 class="mb-2">{title}</h4>',
            content,
        )
    assert "Balance neutro" in content
    assert "Balance = 0🏆 - 0🌴 = 0" not in content
    assert "recent-form-record-label text-muted small" in content
    assert ".recent-form-record-label {\n  margin: 0;" in css
    assert "recent-form-chart-data" in content
    assert "buildSmoothPathData" in content
    assert "buildAreaPathData" in content
    assert "var(--bs-success)" in content
    assert "var(--bs-danger-bg-subtle)" in content
    assert "recent-form-positive-clip" in content
    assert "recent-form-negative-clip" in content
    assert "createSvgElement(\"circle\"" not in content
    assert "Balance positivo: más victorias que derrotas" not in content
    assert "Balance negativo: más derrotas que victorias" not in content
    assert "Posición" in content
    assert "Posición en los rankings" not in content
    assert "Eficacia por ranking" in content
    assert "Tendencias" not in content
    assert "Sin datos" in content
    assert "Sin partidos" in content
    assert insights["top_partners"] == []
    assert insights["recent_form_chart"] == {
        "x_axis_min": 0,
        "x_axis_max": 10,
        "y_axis_min": -1,
        "y_axis_max": 1,
        "match_count": 0,
        "wins": 0,
        "losses": 0,
        "balance": 0,
        "record_label": "Balance neutro",
        "empty_label": "Sin partidos",
        "aria_label": "Últimos partidos: balance 0 en 0 partidos",
        "points": [{"x": 0, "y": 0}],
    }
    assert insights["partner_distribution"] == []
    assert insights["partner_efficiency_cards"] == []
    assert insights["rival_distribution"] == []
    assert len(insights["rival_efficiency_cards"]) == 3
    assert [row["label"] for row in insights["rival_efficiency_cards"]] == [
        "Sin datos",
        "Sin datos",
        "Sin datos",
    ]
    assert all(row["is_placeholder"] for row in insights["rival_efficiency_cards"])
    assert all(row["is_inactive"] for row in insights["rival_efficiency_cards"])
    assert insights["top_rivals"] == []
    assert len(insights["nemesis_cards"]) == 3
    assert len(insights["victim_cards"]) == 3
    assert [row["label"] for row in insights["nemesis_cards"]] == [
        "Sin datos",
        "Sin datos",
        "Sin datos",
    ]
    assert [row["label"] for row in insights["victim_cards"]] == [
        "Sin datos",
        "Sin datos",
        "Sin datos",
    ]
    assert all(row["is_placeholder"] for row in insights["nemesis_cards"])
    assert all(row["is_placeholder"] for row in insights["victim_cards"])
    assert [scope["key"] for scope in insights["efficiency_scopes"]] == ["all", "gender", "mixed"]
    assert [scope["label"] for scope in insights["efficiency_scopes"]] == ["Todos", "Masc.", "Mixtos"]
    assert insights["trend_rows"] == [
        {
            "label": "5 últimos",
            "wins": 0,
            "losses": 0,
            "matches": 0,
            "win_rate_percent": 0,
            "is_eligible": False,
            "display_value": "--%",
            "is_inactive": True,
            "show_progress_stroke": False,
            "record_label": "0🏆/0🏓",
        },
        {
            "label": "10 últimos",
            "wins": 0,
            "losses": 0,
            "matches": 0,
            "win_rate_percent": 0,
            "is_eligible": False,
            "display_value": "--%",
            "is_inactive": True,
            "show_progress_stroke": False,
            "record_label": "0🏆/0🏓",
        },
        {
            "label": "20 últimos",
            "wins": 0,
            "losses": 0,
            "matches": 0,
            "win_rate_percent": 0,
            "is_eligible": False,
            "display_value": "--%",
            "is_inactive": True,
            "show_progress_stroke": False,
            "record_label": "0🏆/0🏓",
        },
    ]
    assert all(scope["selector"]["is_inactive"] for scope in insights["efficiency_scopes"])
    assert count_trend_wheels(content) == 21
    assert "circular-progress-active" not in content
    assert content.count("--%") >= 21
    assert content.count("player-efficiency-card-disabled") >= 21
    assert content.count('aria-disabled="true"') == 3
    assert len(re.findall(r"<button[^>]*\sdisabled(?:\s|>|=)", content)) == 3
    assert content.count("0🏆/0🏓") >= 6
    assert "circular-progress-primary" in content
    assert "circular-progress-success" in content
    assert "circular-progress-warning" in content
    assert "circular-progress-danger" not in content
    assert "player-partner-card-title" in content
    assert "player-partner-name" in content
    assert "player-partner-swatch bg-primary" in content
    assert "player-partner-swatch bg-success" in content
    assert "player-partner-swatch bg-warning" in content
    assert 'data-efficiency-scope="all"' in content
    assert 'data-efficiency-scope="gender"' in content
    assert 'data-efficiency-scope="mixed"' in content
    assert 'aria-pressed="true"' in content
    contendientes_content = content.split('<h4 class="mb-2">Contendientes</h4>', 1)[1].split(
        "Partidos jugados",
        1,
    )[0]
    assert "Némesis: más puntos perdidos contra..." not in contendientes_content
    assert "Víctimas: más puntos ganados contra..." not in contendientes_content
    assert "Rivales que más veces han ganado contra este jugador." not in contendientes_content
    assert "Rivales a los que este jugador más veces ha ganado." not in contendientes_content
    assert "Némesis: efic&gt;60% y más derrotas" in contendientes_content
    assert "Víctimas: efic&gt;60% y más victorias" in contendientes_content
    assert contendientes_content.count("Sin datos") == 6
    assert contendientes_content.count("player-partner-card-empty") == 6
    assert contendientes_content.count("circular-progress") >= 6
    rival_content = content.split('<h4 class="mb-2">Parejas rivales frecuentes</h4>', 1)[1].split(
        '<h4 class="mb-2">Contendientes</h4>',
        1,
    )[0]
    assert rival_content.count("Sin datos") == 3
    assert rival_content.count("player-partner-card-empty") == 3
    assert "Eficacia ante rivales" in rival_content
    assert re.search(
        r'class="[^"]*player-efficiency-selector-card-active[^"]*"[^>]*data-efficiency-scope="all"',
        content,
    )
    assert "Seleccionado" not in content
    assert content.count(">Ver<") == 3
    assert "player-efficiency-title-stack" not in content
    assert "text-bg-success player-efficiency-selector-card" not in content
    assert "player-efficiency-card text-bg-success" not in content
    assert 'aria-valuenow="0"' in content
    assert "player-trend-meta" not in content
    assert (
        ".player-efficiency-selector-card {\n"
        "  appearance: none;\n"
        "  cursor: pointer;\n"
        "  text-align: inherit;\n"
        "  align-items: stretch;\n"
        "  padding: 0;\n"
        "  font-family: inherit;"
    ) in css
    assert ".player-efficiency-selector-card .card-body {\n  display: block;\n}" not in css


def test_player_detail_recent_form_chart_uses_available_matches_in_oldest_first_order(client):
    player = Player.objects.create(name="Recent Partial", gender=Player.GENDER_MALE)
    partner = Player.objects.create(name="Recent Partner", gender=Player.GENDER_MALE)
    rival_1 = Player.objects.create(name="Recent Rival 1", gender=Player.GENDER_MALE)
    rival_2 = Player.objects.create(name="Recent Rival 2", gender=Player.GENDER_MALE)

    results = [False, True, True, False]
    for index, won in enumerate(results, start=1):
        player_on_team1 = index % 2 == 1
        winning_team = 1 if (won and player_on_team1) or (not won and not player_on_team1) else 2
        create_match(
            player,
            partner,
            rival_1,
            rival_2,
            winning_team=winning_team,
            played_on=date(2026, 2, index),
            player_on_team1=player_on_team1,
        )

    response = client.get(reverse("player_detail", args=[player.id]))
    chart = response.context["player_insights"]["recent_form_chart"]

    assert response.status_code == 200
    assert chart == {
        "x_axis_min": 0,
        "x_axis_max": 10,
        "y_axis_min": -1,
        "y_axis_max": 1,
        "match_count": 4,
        "wins": 2,
        "losses": 2,
        "balance": 0,
        "record_label": "Balance neutro",
        "empty_label": "Sin partidos",
        "aria_label": "Últimos partidos: balance 0 en 4 partidos",
        "points": [
            {"x": 0, "y": 0},
            {"x": 1, "y": -1},
            {"x": 2, "y": 0},
            {"x": 3, "y": 1},
            {"x": 4, "y": 0},
        ],
    }


def test_player_detail_recent_form_chart_uses_latest_ten_matches_only(client):
    player = Player.objects.create(name="Recent Latest Ten", gender=Player.GENDER_MALE)
    partner = Player.objects.create(name="Recent Latest Partner", gender=Player.GENDER_MALE)
    rival_1 = Player.objects.create(name="Recent Latest Rival 1", gender=Player.GENDER_MALE)
    rival_2 = Player.objects.create(name="Recent Latest Rival 2", gender=Player.GENDER_MALE)

    results_by_day = {
        1: False,
        2: False,
        3: True,
        4: True,
        5: False,
        6: True,
        7: False,
        8: True,
        9: True,
        10: False,
        11: True,
        12: True,
    }

    for day in range(1, 13):
        won = results_by_day[day]
        create_match(
            player,
            partner,
            rival_1,
            rival_2,
            winning_team=1 if won else 2,
            played_on=date(2026, 3, day),
        )

    response = client.get(reverse("player_detail", args=[player.id]))
    content = response.content.decode("utf-8")
    chart = response.context["player_insights"]["recent_form_chart"]

    assert response.status_code == 200
    assert chart["x_axis_min"] == 0
    assert chart["x_axis_max"] == 10
    assert chart["y_axis_min"] == -4
    assert chart["y_axis_max"] == 4
    assert chart["match_count"] == 10
    assert chart["wins"] == 7
    assert chart["losses"] == 3
    assert chart["balance"] == 4
    assert chart["record_label"] == "Balance muy positivo"
    assert chart["points"] == [
        {"x": 0, "y": 0},
        {"x": 1, "y": 1},
        {"x": 2, "y": 2},
        {"x": 3, "y": 1},
        {"x": 4, "y": 2},
        {"x": 5, "y": 1},
        {"x": 6, "y": 2},
        {"x": 7, "y": 3},
        {"x": 8, "y": 2},
        {"x": 9, "y": 3},
        {"x": 10, "y": 4},
    ]
    assert "Últimos partidos" in content
    assert "Balance muy positivo" in content
    assert "Balance = 7🏆 - 3🌴 = +4" not in content


def test_player_detail_recent_form_chart_uses_negative_balance_labels(client):
    player = Player.objects.create(name="Recent Negative", gender=Player.GENDER_MALE)
    partner = Player.objects.create(name="Recent Negative Partner", gender=Player.GENDER_MALE)
    rival_1 = Player.objects.create(name="Recent Negative Rival 1", gender=Player.GENDER_MALE)
    rival_2 = Player.objects.create(name="Recent Negative Rival 2", gender=Player.GENDER_MALE)

    results = [False, False, False, True, False, False]
    for index, won in enumerate(results, start=1):
        create_match(
            player,
            partner,
            rival_1,
            rival_2,
            winning_team=1 if won else 2,
            played_on=date(2026, 4, index),
        )

    response = client.get(reverse("player_detail", args=[player.id]))
    content = response.content.decode("utf-8")
    chart = response.context["player_insights"]["recent_form_chart"]

    assert response.status_code == 200
    assert chart["wins"] == 1
    assert chart["losses"] == 5
    assert chart["balance"] == -4
    assert chart["record_label"] == "Balance muy negativo"
    assert chart["aria_label"] == "Últimos partidos: balance -4 en 6 partidos"
    assert "Balance muy negativo" in content
    assert "Balance = 1🏆 - 5🌴 = -4" not in content


def test_player_detail_trend_windows_use_available_matches_and_round_percent(client):
    player = Player.objects.create(name="Trend Player", gender=Player.GENDER_MALE)
    partner = Player.objects.create(name="Trend Partner", gender=Player.GENDER_MALE)
    rival_1 = Player.objects.create(name="Trend Rival 1", gender=Player.GENDER_MALE)
    rival_2 = Player.objects.create(name="Trend Rival 2", gender=Player.GENDER_MALE)

    base_day = date(2026, 2, 1)
    results_by_day = {
        1: False,
        2: False,
        3: True,
        4: True,
        5: False,
        6: True,
        7: False,
        8: True,
        9: True,
        10: False,
        11: True,
        12: True,
    }

    for day in range(1, 13):
        player_on_team1 = day % 2 == 0
        won = results_by_day[day]
        winning_team = 1 if (won and player_on_team1) or (not won and not player_on_team1) else 2
        create_match(
            player,
            partner,
            rival_1,
            rival_2,
            winning_team=winning_team,
            played_on=base_day + timedelta(days=day - 1),
            player_on_team1=player_on_team1,
        )

    response = client.get(reverse("player_detail", args=[player.id]))
    insights = response.context["player_insights"]

    assert response.status_code == 200
    assert insights["trend_rows"] == [
        {
            "label": "5 últimos",
            "wins": 4,
            "losses": 1,
            "matches": 5,
            "win_rate_percent": 80,
            "is_eligible": True,
            "is_inactive": False,
            "display_value": "",
            "show_progress_stroke": True,
            "record_label": "4🏆/5🏓",
        },
        {
            "label": "10 últimos",
            "wins": 7,
            "losses": 3,
            "matches": 10,
            "win_rate_percent": 70,
            "is_eligible": True,
            "is_inactive": False,
            "display_value": "",
            "show_progress_stroke": True,
            "record_label": "7🏆/10🏓",
        },
        {
            "label": "20 últimos",
            "wins": 7,
            "losses": 5,
            "matches": 12,
            "win_rate_percent": 58,
            "is_eligible": True,
            "is_inactive": False,
            "display_value": "",
            "show_progress_stroke": True,
            "record_label": "7🏆/12🏓",
        },
    ]
    content = response.content.decode("utf-8")
    assert count_trend_wheels(content) == 22
    assert "Total" not in content
    assert "20 últimos" in content
    assert "4🏆/5🏓" in content
    assert "7🏆/10🏓" in content
    assert "7🏆/12🏓" in content
    assert "circular-progress-primary" in content
    assert 'aria-valuenow="80"' in content
    assert 'aria-valuenow="70"' in content
    assert 'aria-valuenow="58"' in content


def test_player_detail_trend_wheels_mute_duplicate_result_windows(client):
    player = Player.objects.create(name="Duplicate Trend Player", gender=Player.GENDER_MALE)
    partner = Player.objects.create(name="Duplicate Trend Partner", gender=Player.GENDER_MALE)
    rival_1 = Player.objects.create(name="Duplicate Trend Rival 1", gender=Player.GENDER_MALE)
    rival_2 = Player.objects.create(name="Duplicate Trend Rival 2", gender=Player.GENDER_MALE)

    base_day = date(2026, 2, 1)
    results = [False, True, False, True, False]
    for index, won in enumerate(results, start=1):
        create_match(
            player,
            partner,
            rival_1,
            rival_2,
            winning_team=1 if won else 2,
            played_on=base_day + timedelta(days=index - 1),
        )

    response = client.get(reverse("player_detail", args=[player.id]))
    content = response.content.decode("utf-8")
    css = Path("paddle/frontend/static/frontend/css/styles.css").read_text()
    insights = response.context["player_insights"]

    assert response.status_code == 200
    assert [row["show_progress_stroke"] for row in insights["trend_rows"]] == [True, False, False]
    assert [row["is_eligible"] for row in insights["trend_rows"]] == [True, False, False]
    assert [row["is_inactive"] for row in insights["trend_rows"]] == [False, True, True]
    assert [row["display_value"] for row in insights["trend_rows"]] == ["", "--%", "--%"]
    assert count_trend_wheels(content) == 22
    assert [row["win_rate_percent"] for row in insights["trend_rows"]] == [40, 40, 40]
    assert content.count("player-efficiency-card-disabled") >= 2
    assert "--%" in content


def test_player_detail_partial_history_marks_total_duplicate_of_last_10(client):
    player = Player.objects.create(name="Partial Trend Player", gender=Player.GENDER_MALE)
    partner = Player.objects.create(name="Partial Trend Partner", gender=Player.GENDER_MALE)
    rival_1 = Player.objects.create(name="Partial Trend Rival 1", gender=Player.GENDER_MALE)
    rival_2 = Player.objects.create(name="Partial Trend Rival 2", gender=Player.GENDER_MALE)

    base_day = date(2026, 2, 1)
    results = [False, False, False, True, True, True, True, True]
    for index, won in enumerate(results, start=1):
        create_match(
            player,
            partner,
            rival_1,
            rival_2,
            winning_team=1 if won else 2,
            played_on=base_day + timedelta(days=index - 1),
        )

    response = client.get(reverse("player_detail", args=[player.id]))
    content = response.content.decode("utf-8")
    insights = response.context["player_insights"]

    assert response.status_code == 200
    assert insights["trend_rows"][0]["win_rate_percent"] == 100
    assert insights["trend_rows"][1]["win_rate_percent"] == 62
    assert insights["trend_rows"][2]["win_rate_percent"] == 62
    assert [row["show_progress_stroke"] for row in insights["trend_rows"]] == [True, True, False]
    assert [row["is_eligible"] for row in insights["trend_rows"]] == [True, True, False]
    assert [row["is_inactive"] for row in insights["trend_rows"]] == [False, False, True]
    assert [row["display_value"] for row in insights["trend_rows"]] == ["", "", "--%"]
    assert count_trend_wheels(content) == 21
    assert "--%" in content


def test_player_detail_efficiency_scopes_use_gender_and_mixed_matches(client):
    player = Player.objects.create(name="Scoped Efficiency", gender=Player.GENDER_MALE)
    male_partner = Player.objects.create(name="Male Partner", gender=Player.GENDER_MALE)
    male_rival_1 = Player.objects.create(name="Male Rival 1", gender=Player.GENDER_MALE)
    male_rival_2 = Player.objects.create(name="Male Rival 2", gender=Player.GENDER_MALE)
    female_partner = Player.objects.create(name="Female Partner", gender=Player.GENDER_FEMALE)
    female_rival = Player.objects.create(name="Female Rival", gender=Player.GENDER_FEMALE)

    create_match(
        player,
        male_partner,
        male_rival_1,
        male_rival_2,
        winning_team=1,
        played_on=date(2026, 3, 1),
    )
    create_match(
        player,
        male_partner,
        male_rival_1,
        male_rival_2,
        winning_team=2,
        played_on=date(2026, 3, 2),
    )
    create_match(
        player,
        female_partner,
        male_rival_1,
        female_rival,
        winning_team=1,
        played_on=date(2026, 3, 3),
    )
    create_match(
        player,
        female_partner,
        male_rival_2,
        female_rival,
        winning_team=2,
        played_on=date(2026, 3, 4),
    )
    create_match(
        player,
        female_partner,
        male_rival_1,
        female_rival,
        winning_team=1,
        played_on=date(2026, 3, 5),
    )

    response = client.get(reverse("player_detail", args=[player.id]))
    insights = response.context["player_insights"]
    all_scope = scope_by_key(insights, "all")
    gender_scope = scope_by_key(insights, "gender")
    mixed_scope = scope_by_key(insights, "mixed")

    assert response.status_code == 200
    assert all_scope["selector"]["matches"] == 5
    assert all_scope["selector"]["win_rate_percent"] == 60
    assert gender_scope["label"] == "Masc."
    assert gender_scope["selector"]["matches"] == 2
    assert gender_scope["selector"]["win_rate_percent"] == 50
    assert mixed_scope["selector"]["matches"] == 3
    assert mixed_scope["selector"]["win_rate_percent"] == 67
    assert [row["label"] for row in mixed_scope["trend_rows"]] == [
        "5 últimos",
        "10 últimos",
        "20 últimos",
    ]
    assert mixed_scope["trend_rows"][0]["matches"] == 3
    assert mixed_scope["trend_rows"][0]["win_rate_percent"] == 67


def test_player_detail_efficiency_gender_labels_and_unknown_fallback(client):
    female_player = Player.objects.create(name="Female Efficiency", gender=Player.GENDER_FEMALE)
    unknown_player = Player.objects.create(name="Unknown Efficiency", gender=None)

    female_response = client.get(reverse("player_detail", args=[female_player.id]))
    unknown_response = client.get(reverse("player_detail", args=[unknown_player.id]))

    female_scopes = female_response.context["player_insights"]["efficiency_scopes"]
    unknown_scopes = unknown_response.context["player_insights"]["efficiency_scopes"]

    assert female_response.status_code == 200
    assert unknown_response.status_code == 200
    assert [scope["label"] for scope in female_scopes] == ["Todos", "Fem.", "Mixtos"]
    assert [scope["label"] for scope in unknown_scopes] == ["Todos", "Categoría", "Mixtos"]
    assert [scope["style_class"] for scope in unknown_scopes] == [
        "player-scope-primary",
        "player-scope-success",
        "player-scope-warning",
    ]
    assert [row["style_class"] for row in unknown_response.context["scope_rows"]] == [
        "player-scope-primary",
        "player-scope-warning",
    ]
    assert scope_by_key(unknown_response.context["player_insights"], "gender")["selector"][
        "win_rate_percent"
    ] == 0
    unknown_content = unknown_response.content.decode("utf-8")
    assert re.search(
        r'data-efficiency-scope="gender"[\s\S]*?'
        r'aria-pressed="false"[\s\S]*?'
        r'aria-disabled="true" disabled',
        unknown_content,
    )
    assert re.search(
        r'if \(button\.disabled \|\| button\.getAttribute\("aria-disabled"\) === "true"\) return;',
        unknown_content,
    )


def test_player_detail_partner_and_rivals_tiebreakers_and_clickable_links(client):
    player = Player.objects.create(name="Insights Main", gender=Player.GENDER_MALE)
    partner_a = Player.objects.create(name="Partner A", gender=Player.GENDER_MALE)
    partner_b = Player.objects.create(name="Partner B", gender=Player.GENDER_MALE)
    partner_c = Player.objects.create(name="Partner C", gender=Player.GENDER_MALE)

    rival_1 = Player.objects.create(name="Rival 1", gender=Player.GENDER_MALE)
    rival_2 = Player.objects.create(name="Rival 2", gender=Player.GENDER_MALE)
    rival_3 = Player.objects.create(name="Rival 3", gender=Player.GENDER_MALE)
    rival_4 = Player.objects.create(name="Rival 4", gender=Player.GENDER_MALE)
    rival_5 = Player.objects.create(name="Rival 5", gender=Player.GENDER_MALE)
    rival_6 = Player.objects.create(name="Rival 6", gender=Player.GENDER_MALE)

    create_match(player, partner_a, rival_1, rival_2, winning_team=1, played_on=date(2026, 1, 1))
    create_match(player, partner_a, rival_2, rival_1, winning_team=2, played_on=date(2026, 1, 2))
    create_match(player, partner_a, rival_1, rival_2, winning_team=1, played_on=date(2026, 1, 3))

    create_match(player, partner_b, rival_3, rival_4, winning_team=1, played_on=date(2026, 1, 4))
    create_match(player, partner_b, rival_4, rival_3, winning_team=2, played_on=date(2026, 1, 5))
    create_match(player, partner_b, rival_3, rival_4, winning_team=1, played_on=date(2026, 1, 6))

    create_match(player, partner_a, rival_5, rival_6, winning_team=2, played_on=date(2026, 1, 7))
    create_match(player, partner_a, rival_6, rival_5, winning_team=1, played_on=date(2026, 1, 8))
    create_match(player, partner_c, rival_1, rival_3, winning_team=1, played_on=date(2026, 1, 9))
    create_match(player, partner_c, rival_2, rival_4, winning_team=2, played_on=date(2026, 1, 10))

    response = client.get(reverse("player_detail", args=[player.id]))
    content = response.content.decode("utf-8")
    insights = response.context["player_insights"]

    assert response.status_code == 200
    top_partners = insights["top_partners"]
    assert len(top_partners) == 3
    assert top_partners[0]["player"].id == partner_a.id
    assert top_partners[0]["matches_together"] == 5
    assert top_partners[0]["win_rate_percent"] == 60
    assert top_partners[1]["player"].id == partner_b.id
    assert top_partners[1]["matches_together"] == 3
    assert top_partners[1]["win_rate_percent"] == 67
    assert top_partners[2]["player"].id == partner_c.id
    assert top_partners[2]["matches_together"] == 2
    assert top_partners[2]["win_rate_percent"] == 50
    assert insights["partner_distribution"] == [
        {
            "label": "Partner A",
            "player": partner_a,
            "matches": 5,
            "color_class": "bg-primary",
            "is_empty_segment": False,
            "display_percent": 50,
            "width_percent": "50",
            "show_label": True,
            "aria_label": "Partner A: 50% de partidos",
        },
        {
            "label": "Partner B",
            "player": partner_b,
            "matches": 3,
            "color_class": "bg-success",
            "is_empty_segment": False,
            "display_percent": 30,
            "width_percent": "30",
            "show_label": True,
            "aria_label": "Partner B: 30% de partidos",
        },
        {
            "label": "Partner C",
            "player": partner_c,
            "matches": 2,
            "color_class": "bg-warning",
            "is_empty_segment": False,
            "display_percent": 20,
            "width_percent": "20",
            "show_label": True,
            "aria_label": "Partner C: 20% de partidos",
        },
    ]
    assert insights["partner_efficiency_cards"] == [
        {
            "label": "Partner A",
            "player": partner_a,
            "color_class": "bg-primary",
            "progress_color_class": "circular-progress-primary",
            "win_rate_percent": 60,
            "display_value": "",
            "record_label": "3🏆/5🏓",
            "show_progress_stroke": True,
            "is_placeholder": False,
            "is_inactive": False,
            "aria_label": "Efectividad con Partner A: 60%",
        },
        {
            "label": "Partner B",
            "player": partner_b,
            "color_class": "bg-success",
            "progress_color_class": "circular-progress-success",
            "win_rate_percent": 67,
            "display_value": "",
            "record_label": "2🏆/3🏓",
            "show_progress_stroke": True,
            "is_placeholder": False,
            "is_inactive": False,
            "aria_label": "Efectividad con Partner B: 67%",
        },
        {
            "label": "Partner C",
            "player": partner_c,
            "color_class": "bg-warning",
            "progress_color_class": "circular-progress-warning",
            "win_rate_percent": 50,
            "display_value": "",
            "record_label": "1🏆/2🏓",
            "show_progress_stroke": True,
            "is_placeholder": False,
            "is_inactive": False,
            "aria_label": "Efectividad con Partner C: 50%",
        },
    ]

    top_rivals = insights["top_rivals"]
    assert len(top_rivals) == 3
    assert top_rivals[0]["pair_ids"] == tuple(sorted((rival_3.id, rival_4.id)))
    assert top_rivals[0]["encounters"] == 3
    assert top_rivals[0]["win_rate_percent"] == 67

    assert top_rivals[1]["pair_ids"] == tuple(sorted((rival_1.id, rival_2.id)))
    assert top_rivals[1]["encounters"] == 3
    assert top_rivals[1]["win_rate_percent"] == 67

    assert top_rivals[2]["pair_ids"] == tuple(sorted((rival_5.id, rival_6.id)))
    assert top_rivals[2]["encounters"] == 2
    assert top_rivals[2]["win_rate_percent"] == 50
    assert insights["rival_distribution"] == [
        {
            "label": "Rival 3 / Rival 4",
            "player1": rival_3,
            "player2": rival_4,
            "matches": 3,
            "color_class": "bg-primary",
            "is_empty_segment": False,
            "display_percent": 30,
            "width_percent": "30",
            "show_label": True,
            "aria_label": "Rival 3 / Rival 4: 30% de partidos ante rivales",
        },
        {
            "label": "Rival 1 / Rival 2",
            "player1": rival_1,
            "player2": rival_2,
            "matches": 3,
            "color_class": "bg-success",
            "is_empty_segment": False,
            "display_percent": 30,
            "width_percent": "30",
            "show_label": True,
            "aria_label": "Rival 1 / Rival 2: 30% de partidos ante rivales",
        },
        {
            "label": "Rival 5 / Rival 6",
            "player1": rival_5,
            "player2": rival_6,
            "matches": 2,
            "color_class": "bg-warning",
            "is_empty_segment": False,
            "display_percent": 20,
            "width_percent": "20",
            "show_label": True,
            "aria_label": "Rival 5 / Rival 6: 20% de partidos ante rivales",
        },
        {
            "label": "Otros",
            "player1": None,
            "player2": None,
            "matches": 2,
            "color_class": "",
            "is_empty_segment": True,
            "display_percent": 20,
            "width_percent": "20",
            "show_label": True,
            "aria_label": "Otros: 20% de partidos ante rivales",
        },
    ]
    assert insights["rival_efficiency_cards"] == [
        {
            "label": "Rival 3 / Rival 4",
            "player1": rival_3,
            "player2": rival_4,
            "color_class": "bg-primary",
            "progress_color_class": "circular-progress-primary",
            "win_rate_percent": 67,
            "display_value": "",
            "record_label": "2🏆/3🏓",
            "show_progress_stroke": True,
            "aria_label": "Efectividad ante Rival 3 / Rival 4: 67%",
        },
        {
            "label": "Rival 1 / Rival 2",
            "player1": rival_1,
            "player2": rival_2,
            "color_class": "bg-success",
            "progress_color_class": "circular-progress-success",
            "win_rate_percent": 67,
            "display_value": "",
            "record_label": "2🏆/3🏓",
            "show_progress_stroke": True,
            "aria_label": "Efectividad ante Rival 1 / Rival 2: 67%",
        },
        {
            "label": "Rival 5 / Rival 6",
            "player1": rival_5,
            "player2": rival_6,
            "color_class": "bg-warning",
            "progress_color_class": "circular-progress-warning",
            "win_rate_percent": 50,
            "display_value": "",
            "record_label": "1🏆/2🏓",
            "show_progress_stroke": True,
            "aria_label": "Efectividad ante Rival 5 / Rival 6: 50%",
        },
    ]

    assert f'href="/players/{partner_a.id}/"' in content
    assert f'href="/players/{partner_b.id}/"' in content
    assert f'href="/players/{partner_c.id}/"' in content
    assert "progress-stacked player-partner-progress" in content
    assert 'style="width: 50%;"' in content
    assert 'style="width: 30%;"' in content
    assert 'style="width: 20%;"' in content
    assert 'aria-label="Partner A: 50% de partidos"' in content
    assert 'aria-label="Partner B: 30% de partidos"' in content
    assert 'aria-label="Partner C: 20% de partidos"' in content
    assert "Frecuencia de juego" in content
    assert "Eficacia por pareja" in content
    assert "player-partner-cards" in content
    assert content.count('class="card h-100 player-trend-card player-partner-card') == 11
    assert (
        f'<a href="/players/{partner_a.id}/" '
        'class="card h-100 player-trend-card player-partner-card '
        'player-partner-card-link text-body text-decoration-none">'
    ) in content
    assert (
        f'<a href="/players/{partner_b.id}/" '
        'class="card h-100 player-trend-card player-partner-card '
        'player-partner-card-link text-body text-decoration-none">'
    ) in content
    assert (
        f'<a href="/players/{partner_c.id}/" '
        'class="card h-100 player-trend-card player-partner-card '
        'player-partner-card-link text-body text-decoration-none">'
    ) in content
    assert 'aria-label="Efectividad con Partner A: 60%"' in content
    assert 'aria-label="Efectividad con Partner B: 67%"' in content
    assert 'aria-label="Efectividad con Partner C: 50%"' in content
    assert "3🏆/5🏓" in content
    assert "2🏆/3🏓" in content
    assert "1🏆/2🏓" in content
    assert "circular-progress-primary" in content
    assert "circular-progress-success" in content
    assert "circular-progress-warning" in content
    assert "Parejas rivales frecuentes" in content
    assert content.index("Parejas rivales frecuentes") < content.index("Contendientes")
    assert content.index("Contendientes") < content.index("Partidos jugados")
    assert "Némesis: más puntos perdidos contra..." not in content
    assert "Víctimas: más puntos ganados contra..." not in content
    assert "Rivales que más veces han ganado contra este jugador." not in content
    assert "Rivales a los que este jugador más veces ha ganado." not in content
    assert "Némesis: efic&gt;60% y más derrotas" in content
    assert "Víctimas: efic&gt;60% y más victorias" in content
    assert "Rivales frecuentes" not in content
    assert "Volver al ranking" not in content
    assert 'href="/#top"' not in content
    assert "Frecuencia de partidos" in content
    assert "Frecuencia de oposición" not in content
    assert "Eficacia ante rivales" in content
    assert '<th scope="col">Pareja</th>' not in content
    assert '<th scope="col" class="text-center">🎯</th>' not in content
    assert "Otros" in content
    assert 'aria-label="Rival 3 / Rival 4: 30% de partidos ante rivales"' in content
    assert 'aria-label="Rival 1 / Rival 2: 30% de partidos ante rivales"' in content
    assert 'aria-label="Rival 5 / Rival 6: 20% de partidos ante rivales"' in content
    assert 'aria-label="Otros: 20% de partidos ante rivales"' in content
    assert 'aria-label="Efectividad ante Rival 3 / Rival 4: 67%"' in content
    assert 'aria-label="Efectividad ante Rival 1 / Rival 2: 67%"' in content
    assert 'aria-label="Efectividad ante Rival 5 / Rival 6: 50%"' in content
    assert "2🏆/3🏓" in content
    assert "1🏆/2🏓" in content
    assert "player-rival-card" in content
    assert "player-rival-player-row" in content
    assert "player-rival-legend" not in content
    assert "player-partner-legend\">" not in content
    assert content.count("player-partner-legend-item") >= 3
    assert '<span class="text-muted">50%</span>' not in content
    assert '<span class="text-muted">30%</span>' not in content
    assert '<span class="text-muted">20%</span>' not in content
    assert f'href="/players/{rival_1.id}/"' in content
    assert f'href="/players/{rival_2.id}/"' in content
    assert f'href="/players/{rival_3.id}/"' in content
    assert f'href="/players/{rival_4.id}/"' in content
    assert f'href="/players/{rival_5.id}/"' in content
    assert f'href="/players/{rival_6.id}/"' in content
    assert "/\n" not in content


def test_player_detail_contendientes_cards_use_individual_head_to_head_sorting(client):
    player = Player.objects.create(name="Contendientes Main", gender=Player.GENDER_MALE)
    partner = Player.objects.create(name="Contendientes Partner", gender=Player.GENDER_MALE)
    loss_more_a = Player.objects.create(name="Loss More A", gender=Player.GENDER_MALE)
    loss_more_b = Player.objects.create(name="Loss More B", gender=Player.GENDER_MALE)
    loss_recent_a = Player.objects.create(name="Loss Recent A", gender=Player.GENDER_MALE)
    loss_recent_b = Player.objects.create(name="Loss Recent B", gender=Player.GENDER_MALE)
    win_more_a = Player.objects.create(name="Win More A", gender=Player.GENDER_MALE)
    win_more_b = Player.objects.create(name="Win More B", gender=Player.GENDER_MALE)
    win_recent_a = Player.objects.create(name="Win Recent A", gender=Player.GENDER_MALE)
    win_recent_b = Player.objects.create(name="Win Recent B", gender=Player.GENDER_MALE)
    boundary_partner = Player.objects.create(name="Boundary Partner", gender=Player.GENDER_MALE)
    loss_boundary = Player.objects.create(name="Loss Boundary", gender=Player.GENDER_MALE)
    loss_above = Player.objects.create(name="Loss Above", gender=Player.GENDER_MALE)
    loss_boundary_support = Player.objects.create(name="Loss Boundary Support", gender=Player.GENDER_MALE)
    loss_above_support = Player.objects.create(name="Loss Above Support", gender=Player.GENDER_MALE)
    win_boundary = Player.objects.create(name="Win Boundary", gender=Player.GENDER_MALE)
    win_above = Player.objects.create(name="Win Above", gender=Player.GENDER_MALE)
    win_boundary_support = Player.objects.create(name="Win Boundary Support", gender=Player.GENDER_MALE)
    win_above_support = Player.objects.create(name="Win Above Support", gender=Player.GENDER_MALE)

    create_match(player, partner, loss_more_a, loss_more_b, winning_team=2, played_on=date(2026, 7, 1))
    create_match(player, partner, loss_more_a, loss_more_b, winning_team=2, played_on=date(2026, 7, 2))
    create_match(player, partner, loss_more_a, loss_more_b, winning_team=2, played_on=date(2026, 7, 3))
    create_match(player, partner, loss_more_a, loss_more_b, winning_team=1, played_on=date(2026, 7, 4))
    create_match(player, partner, loss_recent_a, loss_recent_b, winning_team=2, played_on=date(2026, 7, 5))
    create_match(player, partner, loss_recent_a, loss_recent_b, winning_team=2, played_on=date(2026, 7, 6))
    create_match(
        player,
        boundary_partner,
        loss_boundary,
        loss_boundary_support,
        winning_team=2,
        played_on=date(2026, 7, 13),
    )
    create_match(
        player,
        boundary_partner,
        loss_boundary,
        loss_boundary_support,
        winning_team=2,
        played_on=date(2026, 7, 14),
    )
    create_match(
        player,
        boundary_partner,
        loss_boundary,
        loss_boundary_support,
        winning_team=2,
        played_on=date(2026, 7, 15),
    )
    create_match(
        player,
        boundary_partner,
        loss_boundary,
        loss_boundary_support,
        winning_team=1,
        played_on=date(2026, 7, 16),
    )
    create_match(
        player,
        boundary_partner,
        loss_boundary,
        loss_boundary_support,
        winning_team=1,
        played_on=date(2026, 7, 17),
    )
    create_match(
        player,
        boundary_partner,
        loss_above,
        loss_above_support,
        winning_team=2,
        played_on=date(2026, 7, 18),
    )
    create_match(
        player,
        boundary_partner,
        loss_above,
        loss_above_support,
        winning_team=2,
        played_on=date(2026, 7, 19),
    )
    create_match(
        player,
        boundary_partner,
        loss_above,
        loss_above_support,
        winning_team=1,
        played_on=date(2026, 7, 20),
    )

    create_match(player, partner, win_more_a, win_more_b, winning_team=1, played_on=date(2026, 7, 7))
    create_match(player, partner, win_more_a, win_more_b, winning_team=1, played_on=date(2026, 7, 8))
    create_match(player, partner, win_more_a, win_more_b, winning_team=1, played_on=date(2026, 7, 9))
    create_match(player, partner, win_more_a, win_more_b, winning_team=2, played_on=date(2026, 7, 10))
    create_match(player, partner, win_recent_a, win_recent_b, winning_team=1, played_on=date(2026, 7, 11))
    create_match(player, partner, win_recent_a, win_recent_b, winning_team=1, played_on=date(2026, 7, 12))
    create_match(
        player,
        boundary_partner,
        win_boundary,
        win_boundary_support,
        winning_team=1,
        played_on=date(2026, 7, 21),
    )
    create_match(
        player,
        boundary_partner,
        win_boundary,
        win_boundary_support,
        winning_team=1,
        played_on=date(2026, 7, 22),
    )
    create_match(
        player,
        boundary_partner,
        win_boundary,
        win_boundary_support,
        winning_team=1,
        played_on=date(2026, 7, 23),
    )
    create_match(
        player,
        boundary_partner,
        win_boundary,
        win_boundary_support,
        winning_team=2,
        played_on=date(2026, 7, 24),
    )
    create_match(
        player,
        boundary_partner,
        win_boundary,
        win_boundary_support,
        winning_team=2,
        played_on=date(2026, 7, 25),
    )
    create_match(
        player,
        boundary_partner,
        win_above,
        win_above_support,
        winning_team=1,
        played_on=date(2026, 7, 26),
    )
    create_match(
        player,
        boundary_partner,
        win_above,
        win_above_support,
        winning_team=1,
        played_on=date(2026, 7, 27),
    )
    create_match(
        player,
        boundary_partner,
        win_above,
        win_above_support,
        winning_team=2,
        played_on=date(2026, 7, 28),
    )

    response = client.get(reverse("player_detail", args=[player.id]))
    content = response.content.decode("utf-8")
    contendientes_content = content.split('<h4 class="mb-2">Contendientes</h4>', 1)[1].split(
        "Partidos jugados",
        1,
    )[0]
    insights = response.context["player_insights"]

    assert response.status_code == 200
    assert [row["player"] for row in insights["nemesis_cards"]] == [
        loss_more_a,
        loss_more_b,
        loss_recent_a,
    ]
    assert [row["opponent_wins"] for row in insights["nemesis_cards"]] == [3, 3, 2]
    assert [row["opponent_win_rate_percent"] for row in insights["nemesis_cards"]] == [75, 75, 100]
    assert [row["record_label"] for row in insights["nemesis_cards"]] == [
        "3🌴/1🏆",
        "3🌴/1🏆",
        "2🌴/0🏆",
    ]
    assert [row["win_rate_percent"] for row in insights["nemesis_cards"]] == [75, 75, 100]
    assert [row["color_class"] for row in insights["nemesis_cards"]] == [
        "bg-danger bg-opacity-100",
        "bg-danger bg-opacity-50",
        "bg-danger bg-opacity-25",
    ]
    assert [row["progress_color_style"] for row in insights["nemesis_cards"]] == [
        "--progress-stroke: rgba(var(--bs-danger-rgb), 1);",
        "--progress-stroke: rgba(var(--bs-danger-rgb), 0.5);",
        "--progress-stroke: rgba(var(--bs-danger-rgb), 0.25);",
    ]

    assert [row["player"] for row in insights["victim_cards"]] == [
        win_more_a,
        win_more_b,
        win_recent_a,
    ]
    assert [row["player_wins"] for row in insights["victim_cards"]] == [3, 3, 2]
    assert [row["player_win_rate_percent"] for row in insights["victim_cards"]] == [75, 75, 100]
    assert [row["record_label"] for row in insights["victim_cards"]] == [
        "3🏆/1🌴",
        "3🏆/1🌴",
        "2🏆/0🌴",
    ]
    assert [row["win_rate_percent"] for row in insights["victim_cards"]] == [75, 75, 100]
    assert [row["color_class"] for row in insights["victim_cards"]] == [
        "bg-success bg-opacity-100",
        "bg-success bg-opacity-50",
        "bg-success bg-opacity-25",
    ]
    assert [row["progress_color_style"] for row in insights["victim_cards"]] == [
        "--progress-stroke: rgba(var(--bs-success-rgb), 1);",
        "--progress-stroke: rgba(var(--bs-success-rgb), 0.5);",
        "--progress-stroke: rgba(var(--bs-success-rgb), 0.25);",
    ]

    assert f'href="/players/{loss_more_a.id}/"' in contendientes_content
    assert f'href="/players/{loss_more_b.id}/"' in contendientes_content
    assert f'href="/players/{loss_recent_a.id}/"' in contendientes_content
    assert f'href="/players/{loss_recent_b.id}/"' not in contendientes_content
    assert f'href="/players/{loss_boundary.id}/"' not in contendientes_content
    assert f'href="/players/{loss_above.id}/"' not in contendientes_content
    assert f'href="/players/{win_more_a.id}/"' in contendientes_content
    assert f'href="/players/{win_more_b.id}/"' in contendientes_content
    assert f'href="/players/{win_recent_a.id}/"' in contendientes_content
    assert f'href="/players/{win_recent_b.id}/"' not in contendientes_content
    assert f'href="/players/{win_boundary.id}/"' not in contendientes_content
    assert f'href="/players/{win_above.id}/"' not in contendientes_content
    assert "player-trend-card player-partner-card player-partner-card-link" in contendientes_content
    assert "player-partner-swatch bg-danger bg-opacity-100" in contendientes_content
    assert "player-partner-swatch bg-danger bg-opacity-50" in contendientes_content
    assert "player-partner-swatch bg-danger bg-opacity-25" in contendientes_content
    assert "player-partner-swatch bg-success bg-opacity-100" in contendientes_content
    assert "player-partner-swatch bg-success bg-opacity-50" in contendientes_content
    assert "player-partner-swatch bg-success bg-opacity-25" in contendientes_content
    assert "--progress-stroke: rgba(var(--bs-danger-rgb), 1);" in contendientes_content
    assert "--progress-stroke: rgba(var(--bs-success-rgb), 1);" in contendientes_content
    assert 'aria-label="Derrotas ante Loss More A: 75%"' in content
    assert 'aria-label="Victorias ante Win Recent A: 100%"' in content
    assert 'aria-label="Derrotas ante Loss Boundary: 60%"' not in content
    assert 'aria-label="Derrotas ante Loss Above: 67%"' not in content
    assert 'aria-label="Victorias ante Win Boundary: 60%"' not in content
    assert 'aria-label="Victorias ante Win Above: 67%"' not in content


def test_player_detail_partner_tiebreak_prefers_win_rate_before_recent_date(client):
    player = Player.objects.create(name="Tie Main", gender=Player.GENDER_MALE)
    partner_high_rate = Player.objects.create(name="Partner High", gender=Player.GENDER_MALE)
    partner_recent = Player.objects.create(name="Partner Recent", gender=Player.GENDER_MALE)
    rival_1 = Player.objects.create(name="Tie Rival 1", gender=Player.GENDER_MALE)
    rival_2 = Player.objects.create(name="Tie Rival 2", gender=Player.GENDER_MALE)

    create_match(player, partner_high_rate, rival_1, rival_2, winning_team=1, played_on=date(2026, 2, 1))
    create_match(player, partner_high_rate, rival_1, rival_2, winning_team=1, played_on=date(2026, 2, 2))
    create_match(player, partner_high_rate, rival_1, rival_2, winning_team=2, played_on=date(2026, 2, 3))

    create_match(player, partner_recent, rival_1, rival_2, winning_team=1, played_on=date(2026, 2, 4))
    create_match(player, partner_recent, rival_1, rival_2, winning_team=2, played_on=date(2026, 2, 5))
    create_match(player, partner_recent, rival_1, rival_2, winning_team=2, played_on=date(2026, 2, 6))

    response = client.get(reverse("player_detail", args=[player.id]))
    insights = response.context["player_insights"]

    assert response.status_code == 200
    assert insights["top_partners"][0]["player"].id == partner_high_rate.id
    assert insights["top_partners"][0]["matches_together"] == 3
    assert insights["top_partners"][0]["win_rate_percent"] == 67


def test_player_detail_shows_only_available_partner_rows_when_fewer_than_three(client):
    player = Player.objects.create(name="Few Partners", gender=Player.GENDER_MALE)
    partner_a = Player.objects.create(name="Few Partner A", gender=Player.GENDER_MALE)
    partner_b = Player.objects.create(name="Few Partner B", gender=Player.GENDER_MALE)
    rival_1 = Player.objects.create(name="Few Rival 1", gender=Player.GENDER_MALE)
    rival_2 = Player.objects.create(name="Few Rival 2", gender=Player.GENDER_MALE)

    create_match(player, partner_a, rival_1, rival_2, winning_team=1, played_on=date(2026, 3, 1))
    create_match(player, partner_b, rival_1, rival_2, winning_team=2, played_on=date(2026, 3, 2))

    response = client.get(reverse("player_detail", args=[player.id]))
    content = response.content.decode("utf-8")
    css = Path("paddle/frontend/static/frontend/css/styles.css").read_text()
    insights = response.context["player_insights"]

    assert response.status_code == 200
    assert len(insights["top_partners"]) == 2
    assert [row["display_percent"] for row in insights["partner_distribution"]] == [50, 50]
    assert [row["width_percent"] for row in insights["partner_distribution"]] == ["50", "50"]
    assert len(insights["partner_distribution"]) == 2
    assert [row["label"] for row in insights["partner_efficiency_cards"]] == [
        "Few Partner A",
        "Few Partner B",
        "Sin datos",
    ]
    assert [row["win_rate_percent"] for row in insights["partner_efficiency_cards"]] == [100, 0, 0]
    assert [row["record_label"] for row in insights["partner_efficiency_cards"]] == [
        "1🏆/1🏓",
        "0🏆/1🏓",
        "0🏆/0🏓",
    ]
    assert [row["is_placeholder"] for row in insights["partner_efficiency_cards"]] == [
        False,
        False,
        True,
    ]
    assert [row["is_inactive"] for row in insights["partner_efficiency_cards"]] == [
        False,
        False,
        True,
    ]
    assert [row["display_value"] for row in insights["partner_efficiency_cards"]] == [
        "",
        "",
        "--%",
    ]
    assert [row["label"] for row in insights["rival_distribution"]] == ["Few Rival 1 / Few Rival 2"]
    assert [row["display_percent"] for row in insights["rival_distribution"]] == [100]
    assert [row["width_percent"] for row in insights["rival_distribution"]] == ["100"]
    assert [row["label"] for row in insights["rival_efficiency_cards"]] == [
        "Few Rival 1 / Few Rival 2"
    ]
    assert [row["record_label"] for row in insights["rival_efficiency_cards"]] == ["1🏆/2🏓"]
    assert [row["win_rate_percent"] for row in insights["rival_efficiency_cards"]] == [50]
    assert "progress-stacked player-partner-progress" in content
    assert 'aria-label="Few Partner A: 50% de partidos"' in content
    assert 'aria-label="Few Partner B: 50% de partidos"' in content
    assert 'aria-label="Few Rival 1 / Few Rival 2: 100% de partidos ante rivales"' in content
    assert 'aria-label="Efectividad con Few Partner A: 100%"' in content
    assert 'aria-label="Efectividad con Few Partner B: 0%"' in content
    assert 'aria-label="Efectividad sin datos: sin porcentaje"' in content
    assert 'aria-label="Efectividad ante Few Rival 1 / Few Rival 2: 50%"' in content
    assert "1🏆/1🏓" in content
    assert "0🏆/1🏓" in content
    assert "0🏆/0🏓" in content
    assert "1🏆/2🏓" in content
    assert "--%" in content
    assert '<div class="player-partner-record text-muted" aria-hidden="true"></div>' not in content
    assert "player-partner-card-empty" in content
    assert "player-efficiency-card-disabled" in content
    assert "player-partner-card-empty.player-efficiency-card-disabled" in css
    assert ".player-partner-card-empty.player-efficiency-card-disabled {\n  border-color: var(--bs-border-color);\n  background-color: var(--bs-secondary-bg);" in css
    assert '<a href="" class="card h-100 player-trend-card player-partner-card' not in content
    assert '<a class="card h-100 player-trend-card player-partner-card player-partner-card-empty' not in content
    assert [row["label"] for row in insights["nemesis_cards"]] == [
        "Sin datos",
        "Sin datos",
        "Sin datos",
    ]
    assert [row["label"] for row in insights["victim_cards"]] == [
        "Sin datos",
        "Sin datos",
        "Sin datos",
    ]
    assert all(row["is_placeholder"] for row in insights["nemesis_cards"])
    assert all(row["is_placeholder"] for row in insights["victim_cards"])
    assert content.count('class="card h-100 player-trend-card player-partner-card') == 10
    assert "Otros" not in content
    assert f'href="/players/{partner_a.id}/"' in content
    assert f'href="/players/{partner_b.id}/"' in content


def test_player_detail_groups_remaining_partners_as_otros_in_distribution(client):
    player = Player.objects.create(name="Many Partners", gender=Player.GENDER_MALE)
    partners = [
        Player.objects.create(name="Distribution Partner A", gender=Player.GENDER_MALE),
        Player.objects.create(name="Distribution Partner B", gender=Player.GENDER_MALE),
        Player.objects.create(name="Distribution Partner C", gender=Player.GENDER_MALE),
        Player.objects.create(name="Distribution Partner D", gender=Player.GENDER_MALE),
    ]
    rival_1 = Player.objects.create(name="Distribution Rival 1", gender=Player.GENDER_MALE)
    rival_2 = Player.objects.create(name="Distribution Rival 2", gender=Player.GENDER_MALE)

    match_counts = [4, 3, 2, 1]
    played_on = date(2026, 4, 1)
    for partner, match_count in zip(partners, match_counts):
        for _ in range(match_count):
            create_match(player, partner, rival_1, rival_2, winning_team=1, played_on=played_on)
            played_on += timedelta(days=1)

    response = client.get(reverse("player_detail", args=[player.id]))
    content = response.content.decode("utf-8")
    partner_content = content.split('<h4 class="mb-2">Pareja habitual</h4>', 1)[1].split(
        '<h4 class="mb-2">Parejas rivales frecuentes</h4>',
        1,
    )[0]
    insights = response.context["player_insights"]

    assert response.status_code == 200
    assert [row["label"] for row in insights["partner_distribution"]] == [
        "Distribution Partner A",
        "Distribution Partner B",
        "Distribution Partner C",
        "Otros",
    ]
    assert [row["matches"] for row in insights["partner_distribution"]] == [4, 3, 2, 1]
    assert [row["display_percent"] for row in insights["partner_distribution"]] == [40, 30, 20, 10]
    assert [row["width_percent"] for row in insights["partner_distribution"]] == ["40", "30", "20", "10"]
    assert [row["color_class"] for row in insights["partner_distribution"]] == ["bg-primary", "bg-success", "bg-warning", ""]
    assert [row["is_empty_segment"] for row in insights["partner_distribution"]] == [False, False, False, True]
    assert insights["partner_distribution"][3]["player"] is None
    assert [row["label"] for row in insights["partner_efficiency_cards"]] == [
        "Distribution Partner A",
        "Distribution Partner B",
        "Distribution Partner C",
    ]
    assert [row["color_class"] for row in insights["partner_efficiency_cards"]] == [
        "bg-primary",
        "bg-success",
        "bg-warning",
    ]
    assert "progress-stacked player-partner-progress" in content
    assert 'aria-label="Otros: 10% de partidos"' in content
    assert '<div class="progress-bar bg-secondary">' not in content
    assert "player-partner-swatch bg-secondary" not in content
    assert "player-partner-swatch-empty" not in partner_content
    assert 'class="text-muted">10%</span>' not in content
    assert f'href="/players/{partners[0].id}/"' in content
    assert f'href="/players/{partners[1].id}/"' in content
    assert f'href="/players/{partners[2].id}/"' in content
    assert f'href="/players/{partners[3].id}/"' not in content
    assert ">Otros<" not in content
    assert "Efectividad con Distribution Partner A" in content
    assert "Efectividad con Distribution Partner B" in content
    assert "Efectividad con Distribution Partner C" in content
    assert "Efectividad con Distribution Partner D" not in content


def test_player_detail_groups_remaining_rivals_as_otros_in_distribution(client):
    player = Player.objects.create(name="Many Rivals", gender=Player.GENDER_MALE)
    partner = Player.objects.create(name="Rival Distribution Partner", gender=Player.GENDER_MALE)
    rivals = [
        Player.objects.create(name="Distribution Rival A", gender=Player.GENDER_MALE),
        Player.objects.create(name="Distribution Rival B", gender=Player.GENDER_MALE),
        Player.objects.create(name="Distribution Rival C", gender=Player.GENDER_MALE),
        Player.objects.create(name="Distribution Rival D", gender=Player.GENDER_MALE),
        Player.objects.create(name="Distribution Rival E", gender=Player.GENDER_MALE),
        Player.objects.create(name="Distribution Rival F", gender=Player.GENDER_MALE),
        Player.objects.create(name="Distribution Rival G", gender=Player.GENDER_MALE),
        Player.objects.create(name="Distribution Rival H", gender=Player.GENDER_MALE),
    ]

    rival_pairs = [
        (rivals[0], rivals[1], 4),
        (rivals[2], rivals[3], 3),
        (rivals[4], rivals[5], 2),
        (rivals[6], rivals[7], 1),
    ]
    played_on = date(2026, 6, 1)
    for rival_1, rival_2, match_count in rival_pairs:
        for _ in range(match_count):
            create_match(player, partner, rival_1, rival_2, winning_team=1, played_on=played_on)
            played_on += timedelta(days=1)

    response = client.get(reverse("player_detail", args=[player.id]))
    content = response.content.decode("utf-8")
    insights = response.context["player_insights"]

    assert response.status_code == 200
    assert [row["label"] for row in insights["rival_distribution"]] == [
        "Distribution Rival A / Distribution Rival B",
        "Distribution Rival C / Distribution Rival D",
        "Distribution Rival E / Distribution Rival F",
        "Otros",
    ]
    assert [row["matches"] for row in insights["rival_distribution"]] == [4, 3, 2, 1]
    assert [row["display_percent"] for row in insights["rival_distribution"]] == [40, 30, 20, 10]
    assert [row["width_percent"] for row in insights["rival_distribution"]] == [
        "40",
        "30",
        "20",
        "10",
    ]
    assert [row["color_class"] for row in insights["rival_distribution"]] == [
        "bg-primary",
        "bg-success",
        "bg-warning",
        "",
    ]
    assert [row["is_empty_segment"] for row in insights["rival_distribution"]] == [
        False,
        False,
        False,
        True,
    ]
    assert [row["label"] for row in insights["rival_efficiency_cards"]] == [
        "Distribution Rival A / Distribution Rival B",
        "Distribution Rival C / Distribution Rival D",
        "Distribution Rival E / Distribution Rival F",
    ]
    assert [row["record_label"] for row in insights["rival_efficiency_cards"]] == [
        "4🏆/4🏓",
        "3🏆/3🏓",
        "2🏆/2🏓",
    ]
    assert "Frecuencia de partidos" in content
    assert "Eficacia ante rivales" in content
    assert 'aria-label="Otros: 10% de partidos ante rivales"' in content
    assert "player-rival-legend" not in content
    assert ".player-rival-player-row {\n  display: block;" in Path(
        "paddle/frontend/static/frontend/css/styles.css"
    ).read_text()
    assert "player-rival-card" in content
    assert f'href="/players/{rivals[0].id}/"' in content
    assert f'href="/players/{rivals[1].id}/"' in content
    assert f'href="/players/{rivals[6].id}/"' not in content
    assert content.count('class="card h-100 player-trend-card player-partner-card player-rival-card"') == 3


def test_player_detail_partner_card_names_use_single_line_ellipsis(client):
    player = Player.objects.create(name="Long Name Main", gender=Player.GENDER_MALE)
    long_partner = Player.objects.create(
        name="Very Long Partner Name That Should Not Wrap In The Card",
        gender=Player.GENDER_MALE,
    )
    rival_1 = Player.objects.create(name="Long Name Rival 1", gender=Player.GENDER_MALE)
    rival_2 = Player.objects.create(name="Long Name Rival 2", gender=Player.GENDER_MALE)

    create_match(
        player,
        long_partner,
        rival_1,
        rival_2,
        winning_team=1,
        played_on=date(2026, 5, 1),
    )

    response = client.get(reverse("player_detail", args=[player.id]))
    content = response.content.decode("utf-8")
    css = Path("paddle/frontend/static/frontend/css/styles.css").read_text()

    assert response.status_code == 200
    assert long_partner.name in content
    assert "player-partner-card-title" in content
    assert ".player-partner-card-title .player-partner-name" in css
    assert "font-family: 'Montserrat', sans-serif;" in css
    assert "font-size: 0.95rem;" in css
    assert "text-overflow: ellipsis;" in css
    assert "white-space: nowrap;" in css
    assert ".player-partner-metric-label {\n  margin-bottom: 0.125rem;" in css
    assert ".player-partner-cards {\n  margin-top: 0;\n}" in css
