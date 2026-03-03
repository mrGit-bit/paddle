<!-- markdownlint-disable MD032 -->
<!-- markdownlint-disable MD022 -->

# Remove Deprecated DRF API Surface

## Context
- Governance declares DRF endpoints deprecated, but API routes and DRF settings are still active at runtime.
- This creates architectural incoherence and unnecessary maintenance/test burden.
- Discovery list:
  - `paddle/config/urls.py`
  - `paddle/config/settings/base.py`
  - `paddle/games/urls.py`
  - `paddle/users/urls.py`
  - `paddle/games/views.py`
  - `paddle/users/views.py`
  - `paddle/games/serializers.py`
  - `paddle/users/serializers.py`
  - `paddle/games/tests/*`
  - `paddle/users/tests/*`
  - `requirements.in`
  - `requirements.txt`
  - `README.md`
  - `CHANGELOG.md`

## Spec Reference
- `specs/001-remove-deprecated-api.md`

## Objectives
- Remove deprecated API runtime exposure.
- Ensure web functionality is unaffected.
- Reduce dead code and test surface tied to API-only behavior.

## Scope

### In
- URL/settings cleanup for API removal.
- API module cleanup (views/serializers/urls where obsolete).
- API test cleanup/update.
- Docs/changelog updates.

### Out
- No broader refactor of frontend pages.
- No ranking algorithm redesign.
- No mobile changes.

## Risks
- Risk: Removing DRF too early could break imports or auth flows.
  - Mitigation: Remove routes first, run targeted tests, then remove dependencies.
- Risk: Web login redirects currently point to API URLs.
  - Mitigation: Explicitly update redirect settings and auth flow tests.
- Risk: Hidden coupling in tests to API serializers/viewsets.
  - Mitigation: Replace/remove tests in same PR and validate non-API paths.

## Files Allowed to Change
- `paddle/config/urls.py`
- `paddle/config/settings/base.py`
- `paddle/games/urls.py`
- `paddle/games/views.py`
- `paddle/games/serializers.py`
- `paddle/users/urls.py`
- `paddle/users/views.py`
- `paddle/users/serializers.py`
- `paddle/users/tests/test_api_auth.py`
- `paddle/users/tests/test_api_permissions.py`
- `paddle/users/tests/test_serializers.py`
- `paddle/users/tests/test_registration.py`
- `paddle/games/tests/test_matches.py`
- `paddle/games/tests/test_permissions.py`
- `paddle/games/tests/test_players.py`
- `paddle/games/tests/test_stats.py`
- `paddle/frontend/tests/test_views.py`
- `paddle/pytest.ini`
- `requirements.in`
- `requirements.txt`
- `README.md`
- `CHANGELOG.md`

## Files Forbidden to Change
- `paddle/frontend/services/ranking.py`
- `paddle/frontend/templates/**`
- `paddle/americano/**`
- `mobile/**`
- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`

## Proposed Changes (Step-by-Step by File)
- `paddle/config/urls.py`
  - Change: Remove `api/games`, `api/users`, and `api-auth` URL includes.
  - Why: Remove deprecated API public surface.
  - Notes: Keep admin/frontend/americano routes intact.
- `paddle/config/settings/base.py`
  - Change: Remove DRF app/settings and replace API login redirects with web-safe redirect.
  - Why: Runtime should not depend on DRF after API removal.
  - Notes: Keep core Django/auth settings stable.
- `paddle/games/urls.py`, `paddle/users/urls.py`
  - Change: Remove obsolete API routing declarations if no longer referenced.
  - Why: Avoid dead URL modules.
  - Notes: If retained for compatibility, leave inert and documented.
- `paddle/games/views.py`, `paddle/users/views.py`, `paddle/*/serializers.py`
  - Change: Remove DRF viewsets/serializers only used by deprecated endpoints.
  - Why: Reduce maintenance and ambiguity.
  - Notes: Preserve model/business logic in non-API layers.
- `paddle/games/tests/*`, `paddle/users/tests/*`
  - Change: Remove or replace API-only tests; preserve/extend web behavior tests.
  - Why: Align tests with supported product surface.
  - Notes: Keep smallest relevant pytest scope.
- `requirements.in`, `requirements.txt`
  - Change: Remove DRF dependency if unused after cleanup.
  - Why: Simpler dependency graph.
  - Notes: Ensure lock file consistency.
- `README.md`, `CHANGELOG.md`
  - Change: Update architecture/docs and unreleased notes.
  - Why: Accurate project behavior and release documentation.
  - Notes: Changelog text must match implemented behavior.

## Plan Steps (Execution Order)
- [x] Step 1: Remove API URL exposure and DRF settings dependencies.
- [x] Step 2: Remove API-only modules (viewsets/serializers/routes) and fix imports.
- [x] Step 3: Update tests to reflect supported non-API behavior and run targeted pytest scope.
- [x] Step 4: Update `README.md` and `CHANGELOG.md` under `[Unreleased]`.

## Acceptance Criteria (Testable)
- [ ] AC1: `/api/games/`, `/api/users/`, `/api-auth/` are no longer active.
- [ ] AC2: Core web pages and auth flow work without API redirects.
- [ ] AC3: No runtime dependency on DRF remains unless justified by non-API code.
- [ ] AC4: Targeted tests for supported behavior pass.
- [ ] AC5: Changelog and README state API removal.

## Validation Commands
- `pytest -q paddle/frontend/tests/test_auth.py paddle/frontend/tests/test_views.py paddle/frontend/tests/test_players_pages.py`
- `pytest -q paddle/games/tests paddle/users/tests`

## Manual Functional Checks
1. Access `/` and verify ranking page renders.
2. Login on `/login/` and verify post-login redirection goes to a web route.
3. Visit `/api/games/`, `/api/users/`, and `/api-auth/` and verify they are unavailable.
4. Create/delete a match via web UI and verify player stats/ranking views still update.
5. Verify admin route `/admin/` remains accessible for admin users.

## Execution Log
- 2026-03-03 21:09 UTC — Spec created.
- 2026-03-03 21:09 UTC — Plan created.
- 2026-03-03 21:09 UTC — Implementation started.
- 2026-03-03 21:13 UTC — Tests executed (`72 passed`).

## Post-Mortem / Improvements
- To be completed after implementation.
