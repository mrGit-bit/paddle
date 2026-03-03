# Refactoring Specification Consolidated (001-004)

## Overview

This consolidated specification merges refactoring tracks 001 through 004.

All four tracks are implementation-closed and preserved below as sections.

## Track 001: Remove Deprecated DRF API Surface

### Functional Goal

Remove deprecated Django REST Framework API functionality so the product remains a web-template-first app without an active API runtime surface.

### Scope

#### In

- Remove API URL exposure and DRF browsable API auth routes.
- Remove API app-level routing files no longer needed.
- Remove API viewsets/serializers only serving deprecated endpoints.
- Remove DRF-specific settings and dependencies no longer required by runtime.
- Remove/update API tests to validate non-API behavior.
- Update docs/changelog to reflect API removal.

#### Out

- No redesign of web template flows.
- No ranking refactor unrelated to API removal.
- No mobile app feature redesign.
- No database schema change unless strictly required by API code deletion.

### Acceptance Criteria

- [x] AC1: `/api/games/`, `/api/users/`, and `/api-auth/` are no longer active.
- [x] AC2: Web routes continue responding correctly.
- [x] AC3: Project runs without DRF runtime requirements for deprecated API surface.
- [x] AC4: API-only tests removed/updated; supported test scope remains green.
- [x] AC5: Documentation and changelog state deprecated API removal.

### Status

- Approved by user.
- Implemented and verified.
- Closed on 2026-03-03.

## Track 002: Modularize Frontend Views Without Behavior Changes

### Functional Goal

Improve coherence by splitting `paddle/frontend/views.py` into focused internal modules while preserving routes, outputs, and user-visible behavior.

### Scope

#### In

- Create internal modules grouped by responsibility.
- Keep `paddle/frontend/views.py` as compatibility facade exporting the same callables used by URLs/tests.
- Keep `paddle/frontend/urls.py` behavior unchanged.
- Add/update tests as needed to validate no behavioral regression.
- Update changelog for architectural refactor.

#### Out

- No URL path/name changes.
- No template behavior changes.
- No ranking/business-rule changes.
- No database model/schema changes.

### Acceptance Criteria

- [x] AC1: `paddle/frontend/views.py` reduced to facade with same exported public callables.
- [x] AC2: `paddle/frontend/urls.py` still resolves unchanged callables/routes.
- [x] AC3: Targeted frontend and americano tests pass.
- [x] AC4: Changelog includes frontend view modularization note.

### Status

- Approved by user.
- Implemented and verified.
- Closed on 2026-03-03.

## Track 003: Ranking Source-of-Truth Alignment

### Functional Goal

Define and enforce a coherent ranking source of truth so ranking values and ordering are consistent across persisted fields and rendered ranking pages.

### Scope

#### In

- Audit ranking pathways for persisted `Player.ranking_position`, frontend ranking computation, and model-side recalculation helpers.
- Decide and document canonical ranking policy (ordering/ties/scope behavior).
- Refactor to one canonical policy per supported context.
- Remove/adapt duplicate/conflicting ranking logic.
- Add/update tests proving consistency.

#### Out

- No template redesign.
- No URL changes.
- No API reintroduction.
- No unrelated refactor of match workflows.

### Acceptance Criteria

- [x] AC1: Canonical ranking policy documented in code comments/supporting docs.
- [x] AC2: Duplicate/conflicting ranking implementations removed or aligned.
- [x] AC3: Ranking page outputs stable for existing scenarios.
- [x] AC4: Tests cover ties, zero-match players, and scope behavior.
- [x] AC5: Changelog describes ranking coherence refactor.

### Status

- Approved by user.
- Implemented and verified.
- Closed on 2026-03-03.

## Track 004: Repository Harmonization for Core Match-Participation Queries

### Functional Goal

Harmonize duplicated core query patterns by centralizing player match-participation queryset construction and reusing shared helper paths without behavior changes.

### Scope

#### In

- Identify duplicated participation query logic in player profile history, user match list, and new-match detection.
- Introduce one shared helper for participation queryset construction.
- Refactor frontend modules to reuse helper.
- Keep ordering/distinct behavior unchanged.
- Add/update tests proving no regressions.

#### Out

- No ranking algorithm changes.
- No URL/path/name changes.
- No template modifications.
- No model schema/migration changes.
- No americano/mobile changes.

### Acceptance Criteria

- [x] AC1: Shared helper exists for participation queryset construction.
- [x] AC2: Scoped modules no longer duplicate participant filter blocks.
- [x] AC3: Existing frontend tests for matches/player pages/helpers pass.
- [x] AC4: Targeted tests verify helper equivalence and no regressions.
- [x] AC5: Changelog includes harmonization entry.

### Status

- Approved by user.
- Implemented and verified.
- Closed on 2026-03-03.

## Combined Manual Functional Checks

1. Verify `/`, ranking scopes, `/players/`, `/players/<id>/`, and `/matches/` behave unchanged.
2. Verify login/logout/register/profile flows remain functional and Spanish UI copy remains intact.
3. Verify API deprecated endpoints are unavailable (`/api/games/`, `/api/users/`, `/api-auth/`).
4. Verify ranking tie display and persisted/displayed rank coherence after create/delete match.
5. Verify new-match indicators and user-specific match lists remain coherent.

## Files Allowed to Change (Historical Union)

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
- `paddle/games/tests/**`
- `paddle/frontend/views.py`
- `paddle/frontend/urls.py`
- `paddle/frontend/services/ranking.py`
- `paddle/frontend/view_modules/**`
- `paddle/frontend/tests/test_views.py`
- `paddle/frontend/tests/test_players_pages.py`
- `paddle/frontend/tests/test_auth.py`
- `paddle/frontend/tests/test_player_stats.py`
- `paddle/frontend/tests/test_ranking.py`
- `paddle/frontend/tests/test_about.py`
- `paddle/frontend/tests/test_about_version.py`
- `paddle/frontend/tests/test_views_coverage_extra.py`
- `paddle/pytest.ini`
- `requirements.in`
- `requirements.txt`
- `README.md`
- `CHANGELOG.md`

## Files Forbidden to Change (Historical Union)

- `paddle/frontend/templates/**`
- `paddle/americano/**`
- `mobile/**`
- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`
