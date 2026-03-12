# Repository Initial Audit

## Summary

- Scope: Initial repository baseline audit
- Audited target: Django frontend view modules, related model/query patterns, and audit workflow hotspots
- Audit date: 2026-03-10
- Reviewer: Codex CLI

## View Audit Report

### Finding VA-001

- Status: discarded
- Type: Confirmed issue
- Severity: high
- Evidence: Email login in [auth_profile.py](/workspaces/paddle/paddle/frontend/view_modules/auth_profile.py#L157) resolves the first user by `email__iexact`, while registration and profile updates save non-unique emails in [forms.py](/workspaces/paddle/paddle/frontend/forms.py#L210) and [forms.py](/workspaces/paddle/paddle/frontend/forms.py#L291).
- Recommended minimal fix: Either remove email-based login or enforce unique email at the app/form level before keeping email login.
- Tests to add or update: Add focused login coverage for username login, email login, and duplicate-email behavior.
- Discard explanation: no unique email requirement, several users can keep same email

### Finding VA-002

- Status: accepted
- Type: Possible risk
- Severity: medium
- Evidence: Repository-wide view coverage appears strongest around `frontend/tests/test_views.py`, but the email-login branch in [auth_profile.py](/workspaces/paddle/paddle/frontend/view_modules/auth_profile.py#L152) does not have focused tests visible in the current audit surface.
- Recommended minimal fix: Add direct tests for login-by-email and invalid credential behavior.
- Tests to add or update: Add login tests in [test_views.py](/workspaces/paddle/paddle/frontend/tests/test_views.py) or [test_auth.py](/workspaces/paddle/paddle/frontend/tests/test_auth.py).
- Discard explanation:

## Architecture Review Report

### Finding AR-001

- Status: accepted
- Type: Confirmed issue
- Severity: medium
- Evidence: The old AJAX profile-edit path still exists in [editUserProfile.js](/workspaces/paddle/paddle/frontend/static/frontend/js/editUserProfile.js#L58), while the current profile page is server-rendered. The legacy helper also remains in [auth_profile.py](/workspaces/paddle/paddle/frontend/view_modules/auth_profile.py#L21) and is re-exported from [views.py](/workspaces/paddle/paddle/frontend/views.py#L8).
- Recommended minimal fix: Remove the inactive PATCH profile-edit path and keep only the current POST-based profile flow.
- Tests to add or update: Replace helper-only tests with tests on the active POST profile flow.
- Discard explanation:

### Finding AR-002

- Status: accepted
- Type: Possible risk
- Severity: low
- Evidence: The compatibility facade in [views.py](/workspaces/paddle/paddle/frontend/views.py#L8) still exports legacy-only helpers such as `process_form_data`, which increases drift between public exports and the active application flow.
- Recommended minimal fix: Keep the facade thin and export only callables still required by URLs, templates, or tests.
- Tests to add or update: Add a small regression check only if facade cleanup affects import stability relied on elsewhere.
- Discard explanation:

## Performance Audit Report

### Finding PR-001

- Status: accepted
- Type: Confirmed issue
- Severity: medium
- Evidence: Player stats properties in [models.py](/workspaces/paddle/paddle/games/models.py#L131) issue repeated count queries. `win_rate` recomputes `matches_played` and `wins`, which can multiply ORM work in profile and ranking-adjacent views.
- Recommended minimal fix: Compute wins and matches once per request path and derive win rate locally, or annotate/cache those values before rendering.
- Tests to add or update: Add query-count regression coverage for profile and player-detail views that display player stats.
- Discard explanation:

### Finding PR-002

- Status: accepted
- Type: Confirmed issue
- Severity: medium
- Evidence: [register_view()](/workspaces/paddle/paddle/frontend/view_modules/auth_profile.py#L69) calls `fetch_available_players()`, which already queries/materializes players, and then re-queries `Player` by extracted IDs. This duplicates queryset work on the same dataset.
- Recommended minimal fix: Build the registration queryset once, or expose a queryset-ready helper instead of values-plus-requery behavior.
- Tests to add or update: Add a query-count test for registration GET if this path remains performance-sensitive.
- Discard explanation:

### Finding PR-003

- Status: accepted
- Type: Possible risk
- Severity: medium
- Evidence: [match_view()](/workspaces/paddle/paddle/frontend/view_modules/matches.py#L169) paginates `Match.objects.all()` and then paginates a second participation queryset for the current user. This may be acceptable, but it is a likely hotspot for future query-count growth as match volume increases.
- Recommended minimal fix: Add query-count visibility first, then optimize only if the two-list page becomes materially expensive.
- Tests to add or update: Add a query-count benchmark or focused regression test for the authenticated matches page.
- Discard explanation:

## Open Questions

- None.
