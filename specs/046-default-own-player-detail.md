# Default Own Player Detail

Use for active SDD work only.

## Tracking

- Task ID: `default-own-player-detail`
- Status: `implemented`
- Release tag: `v1.9.1`

`approved` stays in place until the scoped work is finished and the
development cycle for this spec is being closed. Only then move the spec to
`implemented`.

## Summary

- When an authenticated user opens the public players page, default the page to
  their linked player detail instead of showing the empty selector-only state.
- Keep anonymous users on the current empty players page by default.
- Keep direct player detail URLs public and unchanged.

## Scope

- In:
  - Public players landing view default behavior.
  - Focused tests for authenticated and anonymous default behavior.
  - Changelog entry.
- Out:
  - Player detail layout changes.
  - Selector JavaScript changes unless required by the backend route behavior.
  - Registration, authentication, model, migration, or ranking logic changes.

## Files Allowed to Change

- `paddle/frontend/view_modules/players.py`
- `paddle/frontend/tests/test_players_pages.py`
- `CHANGELOG.md`
- `specs/046-default-own-player-detail.md`

## Files Forbidden to Change

- Models, migrations, ranking services, JavaScript assets, and unrelated
  templates.

## Implementation Plan

- [x] Resolve the authenticated user's linked `Player` in `players_view`.
- [x] Redirect or render the authenticated user's player detail as the default
  while preserving group scoping rules.
- [x] Preserve the current anonymous empty players page.
- [x] Add focused tests for both default paths.
- [x] Update the changelog.

## Acceptance

- [x] Authenticated users with a valid linked player opening `/players/` land on
  their player detail by default.
- [x] Anonymous users opening `/players/` still see the empty selector-only page.
- [x] Authenticated users without a linked player still see the empty
  selector-only page.
- [x] Direct `/players/<id>/` detail pages remain public and unchanged.
- [x] No model, migration, ranking, or JavaScript behavior changes are made.

## Validation

- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `markdownlint CHANGELOG.md specs/046-default-own-player-detail.md`
- Manual check: anonymous `/players/`.
- Manual check: authenticated `/players/` with a linked player.
- Manual check: authenticated `/players/` without a linked player.
