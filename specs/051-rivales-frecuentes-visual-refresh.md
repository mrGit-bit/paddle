# Rivales Frecuentes Visual Refresh

## Tracking

- Task ID: `rivales-frecuentes-visual-refresh`
- Status: `implemented`
- Release tag: `unreleased`

## Summary

- Replace the player detail frequent rival-pairs table with a visual layout
  aligned with `Rankings`, `Eficacia`, and `Pareja habitual`.
- Keep rival frequency and efficiency calculations in the backend.

## Scope

- In:
  - Prepare rival pair distribution and efficiency card data in the player
    detail backend.
  - Render a stacked rival-frequency bar with top three rival pairs and
    `Otros`.
  - Render up to three rival pair efficiency cards using the existing circular
    progress wheel pattern.
  - Preserve player-detail links for both names in each rival pair.
  - Remove the player detail `Volver al ranking` button.
  - Add focused player detail tests and an Unreleased changelog entry.
- Out:
  - Ranking, partner, match-history, API, database, or JavaScript behavior
    changes.
  - New rival-stat scopes or expanded data sources.
  - Broad template or styling refactors.

## Files Allowed to Change

- `CHANGELOG.md`
- `paddle/frontend/static/frontend/css/styles.css`
- `paddle/frontend/templates/frontend/player_detail.html`
- `paddle/frontend/tests/test_players_pages.py`
- `paddle/frontend/view_modules/players.py`
- `specs/051-rivales-frecuentes-visual-refresh.md`

## Files Forbidden to Change

- Django model and migration files.
- Deprecated DRF/API files.
- Unrelated frontend templates, static assets, governance files, or release
  records.

## Implementation Plan

- [x] Add backend rival distribution and efficiency-card helpers.
- [x] Replace the rival table with stacked-bar, legend, and wheel-card markup.
- [x] Add only narrow CSS hooks needed for rival-pair names or legend layout.
- [x] Update tests for top-three, `Otros`, fewer-than-three, and empty states.
- [x] Update `CHANGELOG.md` under `Unreleased`.

## Acceptance

- [x] The section title is `Parejas rivales frecuentes`.
- [x] The frequency subsection label is `Frecuencia de partidos`.
- [x] The stacked bar shows the top three rival pairs followed by `Otros` when
  remaining rival pairs exist.
- [x] Each stacked-bar segment displays its backend-prepared percentage when
  wide enough.
- [x] No separate legend renders under the stacked bar.
- [x] The efficiency subsection label is `Eficacia ante rivales`.
- [x] Up to three rival pair cards render with matching colors, win/match
  records, efficiency percentages, and circular progress wheels.
- [x] Rival card player names render as two linked lines.
- [x] Fewer than three rival pairs render only available cards.
- [x] No rival data renders the existing muted `Sin datos` empty state.
- [x] Both players in each rival pair link to their player detail pages.
- [x] The `Volver al ranking` button no longer renders on player detail.

## Validation

- [x] `pytest paddle/frontend/tests/test_players_pages.py -q`
- [x] `markdownlint --disable MD013 -- CHANGELOG.md specs/051-rivales-frecuentes-visual-refresh.md`
- Manual check: player with no rival data.
- Manual check: player with fewer than three rival pairs.
- Manual check: player with more than three rival pairs and `Otros`.
- Manual check: both rival names navigate correctly.
