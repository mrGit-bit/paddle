# Player Detail Medallas Accordion

Use for active SDD work only.

## Tracking

- Task ID: `player-detail-medallas-accordion`
- Status: `implemented`
- Release tag: `unreleased`

## Summary

- Add a player-detail `Medallas` category before existing statistics and
  matches sections.
- Show the selected player's medal card expanded by default and collapsible on
  click.

## Scope

- In:
  - Backend-owned player medal context built from existing medal rules.
  - Player detail template rendering for medal cards and empty state.
  - Focused player-detail tests for section order, collapse behavior, and
    empty state.
- Out:
  - Medal rule changes.
  - Schema, route, API, and ranking algorithm changes.
  - Public `Medallero` page redesign.

## Files Allowed to Change

- `specs/038-player-detail-medallas-accordion.md`
- `paddle/frontend/services/medals.py`
- `paddle/frontend/view_modules/players.py`
- `paddle/frontend/templates/frontend/player_detail.html`
- `paddle/frontend/tests/test_players_pages.py`

## Files Forbidden to Change

- Database migrations.
- DRF/API code.
- Unrelated templates, styles, and release records.

## Execution Notes

- [x] Add tests one behavior at a time and confirm each fails before
      implementation.
- [x] Reuse existing `medallero` presentation classes and Bootstrap collapse
      attributes.
- [x] Keep templates rendering-only; medal calculation stays in Python.

## Acceptance

- [x] `Medallas` appears before `Estadísticas`, which remains before
      `Partidos jugados`.
- [x] A player with medals sees a selected-player medal card expanded by
      default and collapsible on click.
- [x] A player without medals sees the empty medal state.
- [x] Existing public `Medallero` behavior remains unchanged.

## Validation

- `pytest paddle/frontend/tests/test_players_pages.py`
- `pytest paddle/frontend/tests/test_medals.py`
- `markdownlint specs/038-player-detail-medallas-accordion.md`; `MD013` is
  non-blocking.
