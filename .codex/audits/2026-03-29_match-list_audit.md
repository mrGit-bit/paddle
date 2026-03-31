# Match List Audit

## Summary

- Scope: Match create/delete flow after the 30-day add-and-lock window change.
- Audited target: `frontend.view_modules.matches`, related match templates, `games.Match`, and targeted tests.
- Audit date: 2026-03-29
- Reviewer: Codex

## View Audit Report

### Finding VA-001

- Status: discarded
- Type: Suggestion
- Severity: low
- Evidence: `paddle/frontend/tests/test_views.py` covers locked deletion for a participant, but the new rule also applies to staff users and that path is not directly asserted.
- Recommended minimal fix: Add one focused test that verifies a staff user also cannot delete a locked match older than 30 days.
- Tests to add or update: Extend `paddle/frontend/tests/test_views.py` with a staff locked-delete case.
- Discard explanation: Staff users are intentionally allowed to override the 30-day lock when operational intervention is needed, so this suggested test does not match the intended rule.

## Architecture Review Report

- No findings.

## Performance Audit Report

### Finding PR-001

- Status: discarded
- Type: Possible risk
- Severity: low
- Evidence: `paddle/frontend/view_modules/matches.py` filters and orders by `date_played`, and `paddle/games/admin.py` also filters on `date_played`, but `paddle/games/models.py` defines `Match.date_played` without an explicit index.
- Recommended minimal fix: If match volume is expected to grow, add `db_index=True` to `Match.date_played` in a focused schema change.
- Tests to add or update: No behavioral test required; validate with migration coverage and admin/list smoke checks.
- Discard explanation: Current match volume and observed responsiveness do not justify the extra schema/index maintenance cost at this time.

## Open Questions

- None.
