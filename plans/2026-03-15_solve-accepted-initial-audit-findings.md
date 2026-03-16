# Solve Accepted Initial Audit Findings

## Context

- The accepted findings in `.codex/audits/2026-03-10_repository-initial_audit.md` identify six concrete issues in the auth/profile flow, frontend view facade, and a small set of request-path ORM patterns.
- The approved scope is defined in `specs/018-solve-accepted-initial-audit-findings.md`.
- Discovery first covered:
  - `paddle/frontend/view_modules/auth_profile.py`
  - `paddle/frontend/forms.py`
  - `paddle/frontend/view_modules/common.py`
  - `paddle/frontend/view_modules/matches.py`
  - `paddle/frontend/views.py`
  - `paddle/frontend/static/frontend/js/editUserProfile.js`
  - `paddle/games/models.py`
  - `paddle/frontend/tests/test_auth.py`
  - `paddle/frontend/tests/test_views.py`
  - `paddle/frontend/tests/test_views_coverage_extra.py`

## Spec Reference

- Exact active spec:
  - `specs/018-solve-accepted-initial-audit-findings.md`

## Objectives

- Make email login safe by preventing case-insensitive duplicate email reuse through the supported forms.
- Remove the inactive PATCH profile-edit path and any facade export kept only for that legacy flow.
- Reduce repeated ORM work in the accepted request paths without changing page behavior.
- Add focused automated coverage for auth behavior and query-count visibility required by the accepted audit.
- Update the existing audit file so the accepted findings are marked `solved` only after verification.

## Scope

### In

- Registration/profile form validation for case-insensitive email uniqueness.
- Login regression tests for username, email, and invalid credential handling.
- Legacy profile PATCH helper and facade cleanup.
- Request-local player stat computation for the active user/profile path.
- Registration queryset cleanup.
- Query-count coverage for registration GET, authenticated matches GET, and player/profile stats.
- `CHANGELOG.md` update and audit status update.

### Out

- New auth flows, password reset redesign, or schema migrations unless unexpectedly required.
- Broader refactors of player ranking or match list architecture.
- Optimization work outside the accepted findings.

## Risks

- Existing duplicate email rows could make stricter form validation fail in profile-edit cases.
  - Mitigation: preserve unchanged current-user email while rejecting conflicts with other accounts only.
- Query-count assertions can be brittle if they are too tight.
  - Mitigation: use focused request setup and assert stable upper bounds only where the current implementation can support them.
- Removing legacy exports can break tests or imports that still depend on them.
  - Mitigation: search references first and update only the import/test surfaces still relying on the removed helper.

## Files Allowed to Change

- `specs/018-solve-accepted-initial-audit-findings.md`
- `plans/2026-03-15_solve-accepted-initial-audit-findings.md`
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

## Proposed Changes (Step-by-Step by File)

- `paddle/frontend/forms.py`
  - Change: add a shared case-insensitive email-conflict validator used by registration and profile-update forms; preserve the current user’s own email on profile edits.
  - Why: resolves the accepted duplicate-email ambiguity without introducing a migration-first solution.
  - Notes: keep existing Spanish validation style and current confirm-email behavior.

- `paddle/frontend/view_modules/auth_profile.py`
  - Change: remove `process_form_data`, build the registration player queryset without a second database lookup, and compute profile stats once per request before rendering.
  - Why: resolves the accepted legacy PATCH cleanup, duplicate registration queryset, and repeated player-stat queries.
  - Notes: keep login behavior and current POST profile flow intact.

- `paddle/frontend/view_modules/common.py`
  - Change: add or reuse a small helper for player stat calculation if needed by the profile path and query-count tests.
  - Why: centralizes the minimal reusable logic instead of duplicating query math.
  - Notes: avoid broad model refactors if a narrow helper is enough.

- `paddle/frontend/views.py`
  - Change: remove facade exports/imports for legacy-only helpers no longer used after the PATCH path cleanup.
  - Why: keeps the compatibility facade thin per the accepted architecture finding.
  - Notes: preserve active imports used by URLs, templates, and tests.

- `paddle/frontend/static/frontend/js/editUserProfile.js`
  - Change: remove the inactive legacy PATCH-based profile-edit script if it is no longer referenced by the supported flow.
  - Why: accepted architecture finding requires removing the inactive PATCH path.
  - Notes: confirm no active template depends on it before deletion.

- `paddle/games/models.py`
  - Change: make only the smallest supporting adjustment if request-local player stats still need a shared primitive here; otherwise leave unchanged.
  - Why: avoids speculative model refactors while still allowing the accepted performance fix if needed.
  - Notes: prefer no change unless implementation proves necessary.

- `paddle/frontend/tests/test_auth.py`
  - Change: extend focused login coverage for username login, email login, invalid credentials, and duplicate-email registration/profile rejection behavior as appropriate.
  - Why: addresses the accepted auth test gaps directly.
  - Notes: keep tests compact and readable.

- `paddle/frontend/tests/test_views.py`
  - Change: replace helper-only legacy tests with active-flow tests, add duplicate-email rejection assertions, and add query-count coverage for registration GET and authenticated matches/profile paths.
  - Why: aligns tests with the current POST profile flow and the accepted performance findings.
  - Notes: use the smallest relevant pytest scope and stable query ceilings.

- `paddle/frontend/tests/test_views_coverage_extra.py`
  - Change: remove or adapt tests that exist only for `process_form_data` or the legacy PATCH branch.
  - Why: prevents coverage tests from pinning dead code in place.
  - Notes: keep only tests relevant to active behavior.

- `paddle/frontend/tests/test_player_stats.py`
  - Change: update or add assertions if the shared player-stat helper changes behavior or formatting expectations.
  - Why: preserves regression coverage for stat presentation while enabling the accepted performance fix.
  - Notes: no behavioral output change is expected.

- `.codex/audits/2026-03-10_repository-initial_audit.md`
  - Change: mark each accepted finding as `solved` after implementation and verification.
  - Why: the audit skill requires updating the same audit artifact once accepted issues are resolved.
  - Notes: preserve finding IDs and all prior context.

- `CHANGELOG.md`
  - Change: add an `## [Unreleased]` entry describing the auth validation hardening, legacy cleanup, and focused performance/test coverage.
  - Why: required by governance for behavior and repository changes.
  - Notes: entry text must match the actual implemented behavior.

## Plan Steps (Execution Order)

- [x] Step 1: Search remaining references to the legacy PATCH helper/script and verify the smallest safe removal set.
- [x] Step 2: Implement case-insensitive email uniqueness checks in the supported forms and preserve current login behavior.
- [x] Step 3: Remove the inactive PATCH profile path and thin the `frontend.views` facade to active exports only.
- [x] Step 4: Apply the minimal performance fixes for registration queryset reuse and request-local player stat computation.
- [x] Step 5: Add/update focused auth, active-flow, and query-count tests for the accepted findings.
- [x] Step 6: Run the smallest relevant pytest scopes, adjust if failures reveal overlooked active dependencies, then update the audit file and changelog.

## Acceptance Criteria (Testable)

- [x] AC1: Registration and profile update reject case-insensitive duplicate emails while allowing the current user to keep their unchanged email.
- [x] AC2: Login still succeeds with username or email case-insensitively and still rejects invalid credentials with the current response.
- [x] AC3: No active code path or public facade export remains for the removed PATCH profile helper if it is not required by URLs, templates, or current tests.
- [x] AC4: Registration GET no longer performs the duplicate player queryset work identified in the audit.
- [x] AC5: Profile/user stats rendering no longer depends on repeated win/match count queries in the same request path.
- [x] AC6: Automated tests cover the accepted auth cases and provide query-count visibility for registration GET, authenticated matches GET, and the profile/player-stats path.
- [x] AC7: The audit file marks all previously accepted findings as `solved` after verification, and `CHANGELOG.md` is updated under `## [Unreleased]`.

## Validation Commands

- `pytest paddle/frontend/tests/test_auth.py paddle/frontend/tests/test_views.py paddle/frontend/tests/test_views_coverage_extra.py paddle/frontend/tests/test_player_stats.py`
- `pytest paddle/frontend/tests/test_views.py -k "register_view_get or match_view_get or user_view_get"`
- `python -m markdownlint-cli2 specs/018-solve-accepted-initial-audit-findings.md plans/2026-03-15_solve-accepted-initial-audit-findings.md .codex/audits/2026-03-10_repository-initial_audit.md CHANGELOG.md`

## Manual Functional Checks

1. Register with a new unique email and confirm the account is created and logged in.
2. Register with an existing email using different casing and confirm the form rejects it without creating an account.
3. Log in with username and then email using different casing and confirm both paths still succeed.
4. Edit the profile to change only the username and confirm the update succeeds without extra email confirmation.
5. Edit the profile to use another account’s email and confirm the update is rejected and the stored email stays unchanged.
6. Open the authenticated matches page and confirm both lists still render and paginate after the backend cleanup.

## Execution Log

- 2026-03-15 20:49 — Spec created.
- 2026-03-15 20:49 — Spec approved.
- 2026-03-15 20:49 — Plan created.
- 2026-03-15 20:50 — Plan approved.
- 2026-03-15 20:51 — Implementation started.
- 2026-03-15 20:58 — Targeted pytest scope executed successfully.
- 2026-03-15 21:00 — Audit statuses updated to solved and changelog entry added.

## Post-Mortem / Improvements

- What worked well
  - The accepted audit findings already provided a tight, minimal implementation target.
- What caused friction
  - Legacy coverage tests still reference dead-path helpers, so cleanup must be coordinated with test updates.
- Suggested updates to:
  - `/docs/PROJECT_INSTRUCTIONS.md`
  - `/AGENTS.md`
  - `/plans/TEMPLATE.md`
  - None currently identified.
