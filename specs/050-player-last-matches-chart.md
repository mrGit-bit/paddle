# Player Last Matches Chart

## Tracking

- Task ID: `player-last-matches-chart`
- Status: `implemented`
- Release tag: `v1.9.2`

## Summary

- Add a player detail `Últimos partidos` section below `Rankings`.
- Show a simple cumulative result-balance line chart for the displayed
  player's last ten matches.

## Scope

- In:
  - Prepare last-ten cumulative win/loss balance data in the player detail
    backend.
  - Render a fixed `0` to `10` x-axis and a symmetric y-axis around `0`.
  - Show only available matches when the player has fewer than ten matches.
  - Use Bootstrap and small vanilla JavaScript for SVG rendering.
  - Add focused player detail tests and an Unreleased changelog entry.
- Out:
  - Ranking, match-history, partner, rival, API, or database changes.
  - Frontend business logic for choosing matches or calculating wins.
  - Broad template or styling refactors.

## Files Allowed to Change

- `CHANGELOG.md`
- `paddle/frontend/templates/frontend/player_detail.html`
- `paddle/frontend/tests/test_players_pages.py`
- `paddle/frontend/view_modules/players.py`
- `specs/050-player-last-matches-chart.md`

## Files Forbidden to Change

- Django model and migration files.
- Deprecated DRF/API files.
- Unrelated frontend templates, static assets, or governance files.

## Implementation Plan

- [x] Add a backend recent-form chart helper fed by existing player match
  results.
- [x] Render the new `Últimos partidos` section with backend JSON data and a
  Bootstrap-based chart frame.
- [x] Add minimal vanilla JavaScript that maps prepared points into an inline
  SVG curve chart.
- [x] Add tests for zero, partial, and more-than-ten match histories.
- [x] Update `CHANGELOG.md` under `Unreleased`.

## Acceptance

- [x] The section title is exactly `Últimos partidos`.
- [x] The chart uses the displayed player's latest ten matches ordered oldest
  to newest within that window.
- [x] The x-axis always spans `0` to `10`.
- [x] The y-axis uses the same positive and negative maximum around `0`.
- [x] The curve starts at `0`, increments by `1` for wins, and decrements by
  `1` for losses.
- [x] The chart path renders as a smooth curve while keeping point markers for
  exact match positions.
- [x] The chart fills positive balance area with Bootstrap success green and
  negative balance area with Bootstrap danger-subtle styling.
- [x] The chart keeps the filled areas visible without drawing the balance
  curve stroke over them.
- [x] The chart header row shows `Últimos 10` and a full balance formula like
  `Balance = 4🏆 - 2🌴 = +2` together.
- [x] The chart does not render point marker dots.
- [x] Zero-match players show stable empty axes and `Sin partidos`.
- [x] Player detail tests cover the prepared data and rendered section.

## Validation

- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `markdownlint --disable MD013 -- CHANGELOG.md specs/050-player-last-matches-chart.md`
- Manual check: player with no matches.
- Manual check: player with fewer than ten matches.
- Manual check: player with more than ten matches.
