<!-- markdownlint-disable MD022 -->
<!-- markdownlint-disable MD032 -->

# Spec 001: Remove Deprecated DRF API Surface

## Functional Goal
Remove deprecated Django REST Framework API functionality from the repository so the product remains a web-template-first app without an active API runtime surface.

## Scope

### In
- Remove API URL exposure and DRF browsable API auth routes.
- Remove API app-level routing files that are no longer needed.
- Remove API viewsets/serializers that only serve deprecated API endpoints.
- Remove DRF-specific settings and dependencies that are no longer required by runtime.
- Remove API tests and update remaining tests to validate non-API behavior.
- Update docs/changelog to reflect API removal.

### Out
- No redesign of web template flows.
- No refactor of ranking behavior unrelated to API removal.
- No mobile app feature redesign.
- No database schema change unless strictly required by API code deletion.

## UI/UX Requirements
- Existing server-rendered pages remain available and unchanged in behavior.
- Any user-facing texts affected by removed API links/messages must remain in Spanish.
- No visible API entry points should appear in navigation or redirects.

## Backend Requirements
- `config.urls` must not include API endpoint includes.
- Runtime settings must not require `rest_framework` unless still required by non-deprecated code.
- API-only modules should be removed or replaced with minimal stubs only if import compatibility is required.
- Authentication/login redirects must point to web routes, not API endpoints.

## Data Rules
- Ranking and match business logic must continue to run through existing domain models/services.
- Removal of API layers must not change ranking ordering, tie behavior, or persisted match/player data.
- No data migration is expected for this removal.

## Reuse Rules
- Reuse existing web views/services/models as-is.
- Do not duplicate business logic while replacing API paths.
- Prefer deleting dead code over introducing adapters.

## Acceptance Criteria
- [ ] AC1: Requests to `/api/games/`, `/api/users/`, and `/api-auth/` no longer resolve to active endpoints.
- [ ] AC2: Web routes (`/`, ranking pages, player pages, auth pages) still respond correctly.
- [ ] AC3: Project runs without DRF configuration requirements when API is removed.
- [ ] AC4: API-only tests are removed/updated; non-API test suite remains green in targeted scope.
- [ ] AC5: Documentation and changelog clearly state that deprecated API functionality has been removed.

## Manual Functional Checks
1. Open `/` and confirm Hall of Fame loads correctly.
2. Navigate ranking scope tabs (`Todos`, `Masculino`, `Femenino`, `Mixto`) and confirm expected content.
3. Login/logout from web routes and confirm redirects never target `/api/...`.
4. Open `/api/games/` and `/api/users/` and verify they return not found.
5. Create and delete a match from the web UI and confirm ranking updates still render correctly.

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

## Notes
This spec is intentionally focused on decommissioning deprecated API functionality first, before broader coherence/simplicity work.
