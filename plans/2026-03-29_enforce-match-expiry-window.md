# Enforce Match Expiry Window Plan

## Tracking

- Task ID: `enforce-match-expiry-window`
- Spec: `specs/032-enforce-match-expiry-window.md`
- Release tag: `unreleased`

## Summary

- The backlog requires old results to become implicitly approved after about a
  month and stop being deletable.
- The same one-month window should also cap how far back users can add a match.

## Scope

- In:
  - define a shared 30-day match window helper
  - enforce the window in match creation and deletion
  - expose lock/add-window state to the templates
  - add focused regression tests
  - record the behavior under `Unreleased`
- Out:
  - manual approval states
  - match editing flows
  - unrelated ranking or profile changes

## Files Allowed to Change

- `paddle/games/models.py`
- `paddle/frontend/view_modules/matches.py`
- `paddle/frontend/templates/frontend/_match_card.html`
- `paddle/frontend/templates/frontend/match.html`
- `paddle/frontend/tests/test_views.py`
- `paddle/frontend/tests/test_views_coverage_extra.py`
- `paddle/games/migrations/*.py`
- `CHANGELOG.md`

## Files Forbidden to Change

- `paddle/frontend/services/**`
- `paddle/frontend/view_modules/players.py`
- `paddle/americano/**`
- `.github/workflows/**`

## Plan

- [ ] Add a canonical 30-day window helper on the match domain model.
- [ ] Use that helper in `match_view` to reject stale additions and locked deletions.
- [ ] Pass add-window bounds and per-match lock state into the templates.
- [ ] Update match templates so the form and cards reflect the restriction.
- [ ] Add regression tests for allowed/blocked boundaries and update the changelog.

## Acceptance

- [ ] Users can only submit matches whose `date_played` falls within the last 30 days inclusive.
- [ ] Matches older than 30 days are treated as approved/locked and cannot be deleted.
- [ ] UI affordances stay consistent with backend enforcement.
- [ ] Targeted tests pass for creation and deletion window scenarios.

## Validation

- `pytest paddle/frontend/tests/test_views.py -q`
- `pytest paddle/frontend/tests/test_views_coverage_extra.py -q`
- Manual checks:
  - open `/matches/` and confirm the date picker does not allow dates older than 30 days
  - submit a match dated 30 days ago and confirm success
  - submit a match dated 31 days ago and confirm the rejection message
  - view a user match older than 30 days and confirm the delete button is hidden or replaced by lock text
  - try a direct POST delete for an older match and confirm the backend rejects it
