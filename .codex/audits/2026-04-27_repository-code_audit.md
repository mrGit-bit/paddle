# Repository Code Audit

## Summary

- Scope: broad static audit of repository code, centered on Django view
  behavior and expanded to related models, forms, services, URLs, and tests
  where they affect security, maintainability, or performance.
- Audited target: `paddle/frontend`, `paddle/americano`, `paddle/games`, and
  related tests.
- Audit date: 2026-04-27.
- Reviewer: Codex using `$audit`.

## View Audit Report

### Finding VA-001

- Status: solved
- Type: Confirmed issue
- Severity: high
- Evidence: `paddle/americano/views.py:309` exposes `americano_new_round` as a login-protected view but not a POST-only view, and `paddle/americano/urls.py:9` routes it as a normal endpoint. The view creates a database round at `paddle/americano/views.py:319-320`, while the existing test at `paddle/americano/tests/test_americano_views.py:319-322` confirms a GET request creates a round.
- Recommended minimal fix: Add `@require_POST` to `americano_new_round`, update the UI/form that triggers new-round creation to submit POST with CSRF, and keep the same permission check inside the view.
- Tests to add or update: Update the current GET-based test to assert GET is rejected or redirected without creating a round, and add/adjust a POST test that creates exactly one round for an authorized editor.
- Discard explanation: Addressed by making `americano_new_round` POST-only,
  replacing the empty-state link with a CSRF-protected form, and updating
  regression tests for GET rejection and POST creation.

## Architecture Review Report

### Finding AR-001

- Status: solved
- Type: Possible risk
- Severity: medium
- Evidence: `paddle/games/models.py:315-333` reverts old match side effects before validating and saving the new match state. If a model save/update path fails after `old.revert_match_effects()` but before `self.apply_match_effects()`, player-match links and persisted ranking positions can be left inconsistent. The same block is not wrapped in `transaction.atomic()`.
- Recommended minimal fix: Wrap `Match.save()` side-effect changes in a transaction and validate the new state before mutating old player relationships. Keep ranking updates scoped to the affected group.
- Tests to add or update: Add a model test that simulates an invalid match update after an existing match has effects applied, then asserts original player-match links and ranking positions remain unchanged.
- Discard explanation: Addressed by validating the new match state before
  reverting old effects and wrapping save side effects in `transaction.atomic()`.

## Performance Audit Report

### Finding PR-001

- Status: solved
- Type: Possible risk
- Severity: medium
- Evidence: `paddle/frontend/services/ranking.py:217-259` computes rankings by loading matching rows and scoped player populations into Python lists on each request. `paddle/frontend/view_modules/ranking.py:38-45` invokes this for every ranking page, and `paddle/frontend/view_modules/players.py:791-799` recomputes rankings for multiple scopes on each player-detail request.
- Recommended minimal fix: Introduce request-scoped or short-lived per-group/per-scope ranking reuse so one page render does not repeatedly scan the same matches and players. Keep the canonical ranking policy centralized in `frontend.services.ranking`.
- Tests to add or update: Add query-count or service-call regression coverage for player detail so rendering one profile does not recompute unchanged ranking scopes more than necessary.
- Discard explanation: Addressed by adding `compute_rankings_for_scopes()` and
  using it from player detail to batch scope-card ranking computation.

### Finding PR-002

- Status: solved
- Type: Confirmed issue
- Severity: medium
- Evidence: `paddle/frontend/view_modules/common.py:190-192` builds `new_match_ids` by iterating full `Match` objects from `build_player_participation_queryset()`. This helper is called from ranking pages (`paddle/frontend/view_modules/ranking.py:45`, `paddle/frontend/view_modules/ranking.py:105`), players pages (`paddle/frontend/view_modules/players.py:755`, `paddle/frontend/view_modules/players.py:813`), and the match page (`paddle/frontend/view_modules/matches.py:223`), even though it only needs IDs.
- Recommended minimal fix: Change `get_new_match_ids()` to query `values_list("id", flat=True)` and filter out seen IDs at the database level when practical. Preserve the existing session semantics.
- Tests to add or update: Add a helper-level test that verifies `get_new_match_ids()` returns the same IDs with seen-match filtering, and add query-count coverage for a page that displays `new_matches_number`.
- Discard explanation: Addressed by changing `get_new_match_ids()` to filter
  seen IDs and read only `values_list("id", flat=True)`.

## Open Questions

- None.
