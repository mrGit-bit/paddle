# Player Trend Progress Wheels

Use for active SDD work only.

## Tracking

- Task ID: `player-trend-progress-wheels`
- Status: `implemented`
- Release tag: `unreleased`

`approved` stays in place until the scoped work is finished and the
development cycle for that spec is being closed. Only then move the spec to
`implemented`.

## Summary

- Replace the player detail `Tendencias` table with a new `Eficacia` section
  using three responsive
  Bootstrap stat cards.
- Show circular efficiency indicators for `Últimos 5`, `Últimos 10`, and
  `Total` using the existing backend-calculated win-rate percentages.
- Keep all three wheels visible while muting duplicate result windows to a
  neutral grey track-only wheel.
- Show only the wheel in each card; wins, losses, and match counts remain part
  of the backend comparison data but are not displayed in the cards.

## Scope

- In:
  - Player detail trend rendering.
  - Reusable circular progress template partial.
  - Bootstrap-compatible CSS for the wheel/card presentation.
  - Focused player detail rendering tests.
  - Changelog entry.
- Out:
  - JavaScript, Chart.js, or external libraries.
  - New efficiency calculations or frontend business logic.
  - Match queryset, pagination, partner, rival, ranking, model, or migration
    changes.

## Files Allowed to Change

- `paddle/frontend/view_modules/players.py`
- `paddle/frontend/templates/frontend/player_detail.html`
- `paddle/frontend/templates/frontend/_circular_progress.html`
- `paddle/frontend/static/frontend/css/styles.css`
- `paddle/frontend/tests/test_players_pages.py`
- `CHANGELOG.md`
- `specs/040-player-trend-progress-wheels.md`

## Files Forbidden to Change

- Models, migrations, ranking services, JavaScript files, and unrelated
  templates.

## Implementation Plan

- [x] Add a display-only duplicate-progress flag to trend rows.
- [x] Add a reusable circular progress template partial.
- [x] Replace the `Tendencias` table with three responsive wheel-only stat
  cards.
- [x] Add Bootstrap-compatible wheel/card CSS.
- [x] Update focused rendering tests and changelog.

## Acceptance

- [x] Player detail always renders three trend wheels.
- [x] Duplicate trend result windows stay visible but show only the neutral
  grey track.
- [x] Distinct trend result windows show a Bootstrap success green progress
  stroke.
- [x] Existing win-rate calculation behavior remains unchanged.
- [x] No JavaScript or external charting dependency is added.

## Validation

- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `markdownlint CHANGELOG.md specs/040-player-trend-progress-wheels.md`
- Manually check zero-match, partial-history, and long-history player detail
  pages.
- Manually check mobile and desktop trend card layout.
