# Spec 018: Solve Accepted Repository Initial Audit Findings

## Tracking

- Task ID: `solve-accepted-initial-audit-findings`
- Plan: `plans/2026-03-15_solve-accepted-initial-audit-findings.md`
- Release tag: `v1.5.0`

## Functional Goal

Resolve all findings marked `accepted` in `.codex/audits/2026-03-10_repository-initial_audit.md` using the recommended minimal fix for each item, while preserving the current user-visible flows for login, registration, profile updates, player stats, and the authenticated match list.

## Scope

### In

- Enforce unique email usage at the app/form layer so case-insensitive email login is unambiguous.
- Add focused login tests for username login, email login, invalid credentials, and duplicate-email rejection paths.
- Remove the inactive PATCH-based profile edit path and keep only the current POST-based profile update flow.
- Keep `frontend.views` as a thin facade that exports only callables still needed by active URLs, templates, or tests after the legacy profile helper is removed.
- Eliminate repeated player stat count work in the profile-related request path by computing wins, matches, and win rate once before rendering.
- Remove the duplicate registration queryset work in `register_view()` by building the selectable player queryset once from the source helper data.
- Add query-count regression coverage for registration GET, the authenticated matches page, and the profile/player-stats path where the accepted audit requires visibility.
- Update the existing audit file so accepted findings move to `solved` only after implementation and verification.
- Update `CHANGELOG.md` under `## [Unreleased]` to match the actual behavior and test changes.

### Out

- Unaccepted or discarded audit items.
- Broad auth rewrites, password reset redesign, or changes to login UX text beyond what the existing flow already returns.
- Database-level email uniqueness migrations unless implementation proves the minimal app/form fix cannot satisfy the accepted audit requirement.
- Refactors unrelated to the accepted findings.
- Template redesigns or JavaScript changes outside the legacy inactive profile-edit code path removal.

## UI/UX Requirements

- Registration, login, profile update, and match pages must keep their current navigation flow and Spanish UI text.
- Duplicate email attempts during registration or profile update must surface as form validation errors in the existing server-rendered flow.
- The profile page must continue to use the current POST submission path only.

## Backend Requirements

- Email lookup for login must remain case-insensitive, but it must no longer depend on ambiguous duplicate email rows.
- Registration and profile update forms must reject emails already used by another account, case-insensitively.
- The legacy PATCH profile helper and any facade export that exists only to support that inactive path must be removed.
- The request path that builds profile stats must reuse locally computed stats rather than re-triggering repeated `matches.count()` and win queries.
- `register_view()` must avoid re-querying the same non-registered player set after calling `fetch_available_players()`.
- The matches page must keep the current two-list behavior unless query-count validation shows a smaller safe optimization is needed for the accepted minimal fix.

## Data Rules

- Email uniqueness enforcement must be case-insensitive at the application/form level.
- Existing user records must remain untouched unless a user explicitly updates their profile through the supported POST flow.
- No audit finding may be marked `solved` until the repository state is re-checked after the code and tests are updated.

## Reuse Rules

- Reuse existing forms and view-module boundaries rather than introducing new auth flows.
- Reuse shared helpers in `frontend.view_modules.common` when adding query-count visibility or player-stat helpers.
- Prefer focused helper extraction over model-wide refactors if a request-local computation satisfies the accepted performance fix.
- Reuse existing test modules unless a new focused test file is clearly the smallest option.

## Acceptance Criteria

1. Registration rejects a new account whose email matches an existing user email case-insensitively, and profile updates reject changing to another user’s email the same way.
2. Login still succeeds with either username or email case-insensitively, and invalid credentials still render the current error response.
3. The inactive PATCH profile edit path is removed from application code and the compatibility facade no longer exports legacy-only helpers that are unused by active flows.
4. The profile-related request path no longer recomputes wins, matches, and win rate through repeated model property count queries when rendering the current user page.
5. `register_view()` no longer performs the duplicate non-registered-player query identified in the audit.
6. Focused tests cover the accepted auth cases and add query-count visibility for the registration GET path, authenticated matches page, and profile/player-stats path called out by the audit.
7. `.codex/audits/2026-03-10_repository-initial_audit.md` is updated so all previously accepted findings are marked `solved` after verification.
8. `CHANGELOG.md` includes an `Unreleased` entry matching the implemented auth, cleanup, and performance/test changes.

## Manual Functional Checks

1. Open the registration page, submit a new user with a unique email, and confirm the account is created and logged in normally.
2. Try registering a second user with an email already used by another account, including a case-only variation, and confirm the page shows a validation error in Spanish without creating the account.
3. Log in once with username and once with email using different casing, and confirm both succeed.
4. Open the user profile page, change only the username, and confirm the update succeeds without requiring email confirmation.
5. Open the user profile page, try changing the email to one already used by another account, and confirm the update is rejected without changing stored data.
6. Open the authenticated matches page as a linked player and confirm both match lists still render and paginate correctly after the backend cleanup.

## Files Allowed to Change

- `specs/018-solve-accepted-initial-audit-findings.md`
- `plans/*.md`
- `.codex/audits/2026-03-10_repository-initial_audit.md`
- `CHANGELOG.md`
- `paddle/frontend/forms.py`
- `paddle/frontend/views.py`
- `paddle/frontend/view_modules/auth_profile.py`
- `paddle/frontend/view_modules/common.py`
- `paddle/frontend/view_modules/matches.py`
- `paddle/frontend/static/frontend/js/editUserProfile.js`
- `paddle/frontend/tests/test_auth.py`
- `paddle/frontend/tests/test_views.py`
- `paddle/frontend/tests/test_views_coverage_extra.py`
- `paddle/frontend/tests/test_player_stats.py`
- `paddle/games/models.py`

## Files Forbidden to Change

- `.github/workflows/**`
- deployment or release automation files
- mobile wrapper code
- unrelated templates
- unrelated apps or API/DRF surfaces
