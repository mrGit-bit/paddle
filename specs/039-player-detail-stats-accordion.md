# Player Detail Stats Accordion

Use for active SDD work only.

## Tracking

- Task ID: `player-detail-stats-accordion`
- Status: `implemented`
- Release tag: `unreleased`

## Summary

- Start the player-detail `Medallas` card collapsed by default.
- Convert all `Estadísticas` cards into collapsed Bootstrap panels where
  opening one statistics card closes the previously opened statistics card.
- Keep `Medallas` independent from the `Estadísticas` collapse group.
- Keep header summaries compact and ellipsis-safe so summary pills do not
  overlap card names.

## Scope

- In:
  - Player-detail template collapse markup.
  - Backend-owned compact summary data for statistics card headers.
  - Focused player-detail tests for default collapse state, accordion grouping,
    and header summaries.
- Out:
  - Ranking, medal, match, and insight algorithm changes.
  - Schema, route, API, and public medallero page changes.

## Files Allowed to Change

- `specs/039-player-detail-stats-accordion.md`
- `paddle/frontend/view_modules/players.py`
- `paddle/frontend/templates/frontend/player_detail.html`
- `paddle/frontend/static/frontend/css/styles.css`
- `paddle/frontend/tests/test_players_pages.py`

## Files Forbidden to Change

- Database migrations.
- DRF/API code.
- Unrelated templates, styles, and release records.

## Execution Notes

- Reuse Bootstrap collapse behavior and existing player detail presentation
  classes before adding new styling.
- Keep summary selection in Python; templates only render prepared values.
- Keep collapsed header summaries to one row using pills or badges.
- Ranking summary pills show only `position/%`, such as `1/75%`.
- Partner, rival, and contender summaries are intentionally capped to avoid
  crowded headers.

## Acceptance

- [x] `Medallas` renders collapsed by default and toggles independently from
      `Estadísticas`.
- [x] `Rankings`, `Últimos partidos`, `Pareja habitual`, `Parejas rivales`,
      and `Contendientes` render collapsed by default.
- [x] Opening a statistics card collapses any other open statistics card.
- [x] Statistics card headers render one-row summaries with color-coded badges
      or pills.
- [x] Header pills avoid overlapping card names and truncate long labels.
- [x] Existing expanded card content remains available and unchanged in
      behavior.

## Validation

- `pytest paddle/frontend/tests/test_players_pages.py` passed.
- `pytest paddle/frontend/tests/test_medals.py` passed.
- `markdownlint specs/039-player-detail-stats-accordion.md` passed; `MD013` is
  non-blocking.
