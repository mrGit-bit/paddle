# Player Partner Efficiency Cards

Use for active SDD work only.

## Tracking

- Task ID: `player-partner-efficiency-cards`
- Status: `implemented`
- Release tag: `unreleased`

`approved` stays in place until the scoped work is finished and the
development cycle for this spec is being closed. Only then move the spec to
`implemented`.

## Summary

- Replace the player detail `Pareja habitual` legend with three partner
  efficiency cards below the existing stacked progress bar.
- Keep partner ranking, card values, colors, and empty slot data prepared by
  backend context.
- Clarify that the stacked bar shows play frequency and the wheels show partner
  efficiency.

## Scope

- In:
  - Player detail habitual-partner rendering.
  - Backend display context for partner efficiency cards.
  - Minimal circular progress partial extension for optional color and aria
    values.
  - Focused CSS, tests, and changelog entry.
- Out:
  - Stacked progress bar behavior changes.
  - Ranking logic, match query, model, migration, or JavaScript changes.
  - Reworking unrelated player detail sections.

## Files Allowed to Change

- `paddle/frontend/view_modules/players.py`
- `paddle/frontend/templates/frontend/player_detail.html`
- `paddle/frontend/templates/frontend/_circular_progress.html`
- `paddle/frontend/static/frontend/css/styles.css`
- `paddle/frontend/tests/test_players_pages.py`
- `CHANGELOG.md`
- `specs/045-player-partner-efficiency-cards.md`

## Files Forbidden to Change

- Models, migrations, ranking services, JavaScript files, and unrelated
  templates.

## Implementation Plan

- [x] Add backend-prepared partner efficiency card rows.
- [x] Replace the partner legend with a three-card row.
- [x] Extend circular progress styling without changing existing efficiency
  wheel defaults.
- [x] Add metric labels and full-card links for real partner cards.
- [x] Update focused tests and changelog.

## Acceptance

- [x] `Pareja habitual` keeps the existing stacked progress bar.
- [x] The old legend below the bar is replaced by three card slots.
- [x] Real partner cards show the existing swatch/name pattern, link to player
  detail pages, and show matching-color efficiency wheels.
- [x] The bar is labeled `Frecuencia de juego` and cards are labeled `Eficacia
  por pareja`.
- [x] Real partner cards are fully clickable, including the wheel.
- [x] Partner labels use the section title typography, stay on one line, and
  truncate with ellipsis.
- [x] `Otros` remains only in the stacked bar and never renders as a card.
- [x] Fewer than three partners render `Sin datos` placeholder cards.
- [x] Players with no partner data still show `Sin datos`.
- [x] No frontend business logic or JavaScript is added.

## Validation

- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `markdownlint CHANGELOG.md specs/045-player-partner-efficiency-cards.md`
- Manual check: zero-partner, two-partner, three-partner, and four-plus-partner
  player detail pages.
- Manual check: mobile and desktop readability.
