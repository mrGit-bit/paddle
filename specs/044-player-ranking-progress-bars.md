# Player Ranking Progress Bars

Use for active SDD work only.

## Tracking

- Task ID: `player-ranking-progress-bars`
- Status: `implemented`
- Release tag: `unreleased`

`approved` stays in place until the scoped work is finished and the
development cycle for this spec is being closed. Only then move the spec to
`implemented`.

## Summary

- Replace the player detail `Posicion en los rankings` table with stacked
  Bootstrap progress rows.
- Keep backend ranking data as the source of truth and expose only
  display-ready fields to the template.

## Scope

- In:
  - Player detail ranking-position backend display context.
  - Player detail ranking-position template rendering.
  - Minimal local CSS for mobile-readable progress rows.
  - Focused player detail tests.
  - Changelog entry.
- Out:
  - Ranking calculation rules, scope definitions, models, migrations, and
    JavaScript.
  - Other player detail sections.

## Files Allowed to Change

- `paddle/frontend/view_modules/players.py`
- `paddle/frontend/templates/frontend/player_detail.html`
- `paddle/frontend/static/frontend/css/styles.css`
- `paddle/frontend/tests/test_players_pages.py`
- `CHANGELOG.md`
- `specs/044-player-ranking-progress-bars.md`

## Files Forbidden to Change

- Models, migrations, ranking services, JavaScript files, and unrelated
  templates.

## Implementation Plan

- [x] Add backend-prepared ranking progress display fields.
- [x] Replace the ranking table with compact Bootstrap progress rows.
- [x] Add focused styles only if Bootstrap utilities are insufficient.
- [x] Update focused tests and changelog.

## Acceptance

- [x] `Posicion en los rankings` renders stacked rows instead of a table.
- [x] Rows render `Todos`, the player's gender scope, and `Mixtos`.
- [x] Ranked rows show scope and `#X de Y` as labels inside one
  progress-bar-height row.
- [x] Progress uses linear inverse rank fill, preserving existing tied
  `display_position`.
- [x] Missing scoped ranking data renders a muted `Sin datos` fallback without
  click-through.
- [x] No JavaScript, ranking-rule, model, or migration changes are added.

## Validation

- [x] `pytest paddle/frontend/tests/test_players_pages.py -q`
- [x] `pytest paddle/frontend/tests/test_players_pages.py`
  `paddle/frontend/tests/test_ranking.py -q`
- [ ] `markdownlint CHANGELOG.md specs/044-player-ranking-progress-bars.md`
  reports only non-blocking pre-existing `MD013` line-length issues in
  `CHANGELOG.md`.
- [ ] Manual check zero-match, gender-scoped, mixed fallback, mobile readability,
  and row click-through behavior.
