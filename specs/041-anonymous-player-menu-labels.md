# Anonymous Player Menu Labels

## Tracking

- Task ID: `anonymous-player-menu-labels`
- Status: `implemented`
- Release tag: `v1.9.1`

## Summary

- Anonymous users browsing the public `Jugadores` flow currently see player
  options with club/group names in the `Selecciona jugador` dropdown.
- The dropdown should show only player names for anonymous users.

## Scope

- In:
  - Public players landing page selector labels.
  - Public player detail page selector labels.
  - Focused rendering tests for anonymous selector labels.
  - Changelog entry for the visible UI change.
- Out:
  - Registered-user scoped selectors.
  - Match-entry player selectors.
  - Ranking, match, player insight, model, migration, or grouping logic.

## Files Allowed to Change

- `paddle/frontend/view_modules/players.py`
- `paddle/frontend/tests/test_players_pages.py`
- `CHANGELOG.md`
- `specs/041-anonymous-player-menu-labels.md`

## Files Forbidden to Change

- Models, migrations, JavaScript files, ranking services, match-entry views,
  and unrelated templates.

## Implementation Plan

- [x] Stop requesting aggregate group labels for the public players selector.
- [x] Add or update focused tests so anonymous `Jugadores` dropdown options
  render player names without club/group names.
- [x] Document the visible UI change under `CHANGELOG.md` `Unreleased`.

## Acceptance

- [x] Anonymous `/players/` selector options show only player names.
- [x] Anonymous `/players/<id>/` selector options show only player names.
- [x] Public player lookup still works by selected player ID.
- [x] Existing registered-user group scoping behavior is unchanged.

## Validation

- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `markdownlint CHANGELOG.md specs/041-anonymous-player-menu-labels.md`
- Manual check anonymous `/players/` and `/players/<id>/` dropdown labels.
