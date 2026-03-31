# Enforce Match Expiry Window

## Tracking

- Task ID: `enforce-match-expiry-window`
- Plan: `plans/2026-03-29_enforce-match-expiry-window.md`
- Release tag: `unreleased`

## Goal

- Limit match creation to a recent time window.
- Treat older match results as automatically approved and no longer deletable.

## Scope

- In:
  - enforce a 30-day add window based on `date_played`
  - enforce a 30-day delete window based on `date_played`
  - hide or disable delete affordances for locked matches in the match UI
  - add targeted tests for the new match-window rules
  - update the unreleased changelog entry
- Out:
  - a new manual approval workflow or approval UI
  - editing existing matches
  - changing ranking calculation rules

## Files

- Allowed:
  - `paddle/games/models.py`
  - `paddle/frontend/view_modules/matches.py`
  - `paddle/frontend/templates/frontend/_match_card.html`
  - `paddle/frontend/templates/frontend/match.html`
  - `paddle/frontend/tests/test_views.py`
  - `paddle/frontend/tests/test_views_coverage_extra.py`
  - `paddle/games/migrations/*.py`
  - `CHANGELOG.md`
- Forbidden:
  - `paddle/frontend/services/**`
  - `paddle/frontend/view_modules/players.py`
  - `paddle/americano/**`
  - `.github/workflows/**`

## Acceptance

- [ ] Match creation rejects `date_played` values more than 30 days before the current day.
- [ ] Match deletion rejects attempts for matches older than 30 days even for participants and staff.
- [ ] The match UI no longer shows a delete button for locked user matches and communicates the lock state.
- [ ] Tests cover add-window and delete-window behavior at both allowed and blocked boundaries.

## Checks

- Run the targeted match-view test scope covering create/delete restrictions.
- Confirm the match form date input uses the same 30-day window shown by backend validation.
- Confirm an older match still renders in history but cannot be deleted.
