# Release 1.9.2 Consolidated Spec

## Release

- Tag: `1.9.2`
- Date: `2026-04-21`

## Sources

- `specs/048-compact-release-summary-governance.md`
- `specs/049-player-detail-ranking-efficiency-colors.md`
- `specs/050-player-last-matches-chart.md`
- `specs/051-rivales-frecuentes-visual-refresh.md`
- `specs/052-recent-form-balance-labels.md`
- `specs/053-player-detail-section-cards.md`

## Shipped Scope

- Reduce repetitive release changelog sections into compact grouped summaries.
- Make release consolidation review shipped specs, changelog notes, and backlog
  wording so final release history stays readable.
- Rework the player detail ranking and efficiency sections under a single
  `Rankings` heading with partner-style subsection labels.
- Keep the current ranking progress bars and efficiency selector behavior.
- Use the same blue, green, and yellow color palette as `Pareja habitual`.
- Add a player detail `Últimos partidos` section below `Rankings`.
- Show a simple cumulative result-balance line chart for the displayed
  player's last ten matches.
- Replace the player detail frequent rival-pairs table with a visual layout
  aligned with `Rankings`, `Eficacia`, and `Pareja habitual`.
- Keep rival frequency and efficiency calculations in the backend.
- Replace the explicit `Últimos partidos` balance formula with a qualitative
  Spanish balance label.
- Keep the chart data and balance calculation in the backend.
- Group player detail insight sections into the same shadowed card treatment
  used by match-history cards.
- Preserve existing player insight content, calculations, links, and chart
  behavior.

## Validation Summary

- `python scripts/validate_governance.py`
- `pytest paddle/frontend/tests/test_release_orchestrator.py -q`
- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `markdownlint --disable MD013 -- CHANGELOG.md`
- `markdownlint --disable MD013 -- specs/048-compact-release-summary-governance.md specs/049-player-detail-ranking-efficiency-colors.md specs/050-player-last-matches-chart.md specs/051-rivales-frecuentes-visual-refresh.md specs/052-recent-form-balance-labels.md specs/053-player-detail-section-cards.md`
- Release validation: `pytest paddle/frontend/tests/ --cov=frontend.views
  --cov-report=term-missing --cov-fail-under=90`
- Release validation: `pytest paddle/americano/tests/test_americano_views.py
  --cov=americano.views --cov-report=term-missing --cov-fail-under=90`
- Manual staging checks covered player detail insight cards, wheel alignment,
  partner/rival name fit, recent-form chart labels, empty states, and match-card
  continuity.
