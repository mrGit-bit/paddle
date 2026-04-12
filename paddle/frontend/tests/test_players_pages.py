import re
from datetime import date, timedelta

import pytest
from django.urls import reverse

from games.models import Group, Match, Player


pytestmark = pytest.mark.django_db


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
    assert 'data-href="/?page=1#top"' in content
    assert 'data-href="/ranking/male/?page=1#top"' in content
    assert 'data-href="/ranking/mixed/' not in content


def test_player_detail_insights_defaults_with_zero_matches(client):
    player = Player.objects.create(name="Zero Insights", gender=Player.GENDER_MALE)

    response = client.get(reverse("player_detail", args=[player.id]))
    content = response.content.decode("utf-8")
    insights = response.context["player_insights"]

    assert response.status_code == 200
    assert "Posición" in content
    assert "Eficacia" in content
    assert "Tendencias" not in content
    assert "Sin datos" in content
    assert "Sin partidos" in content
    assert insights["top_partners"] == []
    assert insights["partner_distribution"] == []
    assert insights["top_rivals"] == []
    assert insights["trend_rows"] == [
        {
            "label": "Últimos 5",
            "wins": 0,
            "losses": 0,
            "matches": 0,
            "win_rate_percent": 0,
            "show_progress_stroke": True,
        },
        {
            "label": "Últimos 10",
            "wins": 0,
            "losses": 0,
            "matches": 0,
            "win_rate_percent": 0,
            "show_progress_stroke": False,
        },
        {
            "label": "Total",
            "wins": 0,
            "losses": 0,
            "matches": 0,
            "win_rate_percent": 0,
            "show_progress_stroke": False,
        },
    ]
    assert count_trend_wheels(content) == 3
    assert content.count("circular-progress-active") == 1
    assert 'aria-valuenow="0"' in content
    assert "player-trend-meta" not in content


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
            "label": "Últimos 5",
            "wins": 4,
            "losses": 1,
            "matches": 5,
            "win_rate_percent": 80,
            "show_progress_stroke": True,
        },
        {
            "label": "Últimos 10",
            "wins": 7,
            "losses": 3,
            "matches": 10,
            "win_rate_percent": 70,
            "show_progress_stroke": True,
        },
        {
            "label": "Total",
            "wins": 7,
            "losses": 5,
            "matches": 12,
            "win_rate_percent": 58,
            "show_progress_stroke": True,
        },
    ]
    content = response.content.decode("utf-8")
    assert count_trend_wheels(content) == 3
    assert content.count("circular-progress-active") == 3
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
    insights = response.context["player_insights"]

    assert response.status_code == 200
    assert [row["show_progress_stroke"] for row in insights["trend_rows"]] == [True, False, False]
    assert count_trend_wheels(content) == 3
    assert content.count("circular-progress-active") == 1
    assert content.count('aria-valuenow="40"') == 3


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
    assert count_trend_wheels(content) == 3
    assert content.count("circular-progress-active") == 2


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
    assert "Otros" not in content
    assert content.count("player-partner-legend-item") == 3
    assert '<span class="text-muted">50%</span>' not in content
    assert '<span class="text-muted">30%</span>' not in content
    assert '<span class="text-muted">20%</span>' not in content
    assert f'href="/players/{rival_1.id}/"' in content
    assert f'href="/players/{rival_2.id}/"' in content
    assert f'<div>\n              <a href="/players/{rival_1.id}/"' in content
    assert f'<div>\n              <a href="/players/{rival_2.id}/"' in content
    assert "/\n" not in content


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
    insights = response.context["player_insights"]

    assert response.status_code == 200
    assert len(insights["top_partners"]) == 2
    assert [row["display_percent"] for row in insights["partner_distribution"]] == [50, 50]
    assert [row["width_percent"] for row in insights["partner_distribution"]] == ["50", "50"]
    assert len(insights["partner_distribution"]) == 2
    assert "progress-stacked player-partner-progress" in content
    assert 'aria-label="Few Partner A: 50% de partidos"' in content
    assert 'aria-label="Few Partner B: 50% de partidos"' in content
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
    assert "progress-stacked player-partner-progress" in content
    assert 'aria-label="Otros: 10% de partidos"' in content
    assert '<div class="progress-bar bg-secondary">' not in content
    assert "player-partner-swatch bg-secondary" not in content
    assert "player-partner-swatch-empty" not in content
    assert 'class="text-muted">10%</span>' not in content
    assert f'href="/players/{partners[0].id}/"' in content
    assert f'href="/players/{partners[1].id}/"' in content
    assert f'href="/players/{partners[2].id}/"' in content
    assert f'href="/players/{partners[3].id}/"' not in content
    assert ">Otros<" not in content
