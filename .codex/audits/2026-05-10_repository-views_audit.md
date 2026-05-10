# Audit Review Template

## Summary

- Scope: Repository-level Django view audit across `frontend` and `americano` view flows.
- Audited target: `paddle/frontend/view_modules/*.py`, `paddle/americano/views.py`, related Americano template and tests.
- Audit date: 2026-05-10
- Reviewer: Codex

## View Audit Report

### Finding VA-001

- Status: solved
- Type: Confirmed issue
- Severity: medium
- Evidence: `paddle/americano/views.py` validates and saves each match inside the same loop in `americano_assign_round`. Earlier matches are persisted with `m.save()` before later submitted matches can fail validation for duplicate players or players outside the tournament. For example, lines 365-436 mutate and save each match, while lines 374-395 can return early on a later row. The existing duplicate-across-matches test at `paddle/americano/tests/test_americano_views.py` lines 609-646 asserts only the error message, not that earlier match rows remain unchanged.
- Recommended minimal fix: Split `americano_assign_round` into a validation/parse pass and a persistence pass inside `transaction.atomic()`. Return validation errors before saving any `AmericanoMatch`; only recompute standings after the full batch is valid and saved.
- Tests to add or update: Add a regression test where match 1 has valid assignments and match 2 fails duplicate-across-round validation, then assert match 1 is still unassigned after the redirect.
- Verification: Solved in `paddle/americano/views.py` by validating the submitted round before persistence and saving inside `transaction.atomic()`. Covered by `test_assign_round_validation_error_does_not_partially_save_earlier_matches`; verified with `pytest paddle/americano/tests/test_americano_views.py -q`.
- Discard explanation:

## Architecture Review Report

### Finding AR-001

- Status: solved
- Type: Confirmed issue
- Severity: medium
- Evidence: Americano round assignment combines permission checks, POST parsing, validation, mutation, optional round creation, and standings recomputation in one view function (`paddle/americano/views.py` lines 327-446). The current structure directly produced VA-001 because validation cannot be reasoned about independently from persistence.
- Recommended minimal fix: Extract the round assignment workflow into a small service/helper that returns either parsed match updates plus requested action or a validation error. Keep the view responsible for permission, redirect, and messages/session error only.
- Tests to add or update: Keep the existing Americano view tests as integration coverage and add focused tests for the extracted helper/service covering duplicate players, invalid outsider IDs, partial saves, and `action=new_round`.
- Verification: Solved in `paddle/americano/views.py` by extracting parse/validation and persistence helpers for round assignment while keeping the view responsible for permissions, session error state, and redirects. Verified with `pytest paddle/americano/tests/test_americano_views.py -q`.
- Discard explanation:

## Performance Audit Report

### Finding PR-001

- Status: solved
- Type: Confirmed issue
- Severity: medium
- Evidence: `americano_detail` renders round matches without loading related match players or tournament players up front. The view uses `tournament.rounds.prefetch_related("matches")` at `paddle/americano/views.py` line 256, while the template repeatedly dereferences `match.team1_player1`, `match.team1_player2`, `match.team2_player1`, and `match.team2_player2` at `paddle/frontend/templates/frontend/americano/americano_detail.html` lines 132, 146, 178, and 192. The same template also calls `tournament.players.all|dictsort:"name"` four times per match at lines 130, 144, 176, and 190.
- Recommended minimal fix: In `americano_detail`, prefetch matches with a `Prefetch` queryset using `select_related` for the four player fields, and prefetch/sort tournament players once in Python for template reuse. Pass the sorted player list in context instead of calling `tournament.players.all|dictsort:"name"` repeatedly.
- Tests to add or update: Add an `assertNumQueries`-style test for `americano_detail` with multiple rounds/matches/players to cap query growth.
- Verification: Solved by using `Prefetch` with `select_related` for round matches and passing a single sorted `americano_players` list to the template. Covered by `test_americano_detail_query_count_is_bounded_with_round_matches_and_players`; verified with `pytest paddle/americano/tests/test_americano_views.py -q`.
- Discard explanation:

## Open Questions

- Should Americano write endpoints be scoped by the current user's group context before permission checks, or is creator/staff/participant access intentionally allowed across direct URLs regardless of current group context?
