# Refactoring Plan Consolidated (001-004)

## Overview

This consolidated plan merges refactoring tracks 001 through 004.

All four tracks are complete and preserved below.

## Track 001: Remove Deprecated DRF API Surface

### Objectives

- Remove deprecated API runtime exposure.
- Keep web functionality unaffected.
- Reduce dead API-only code and test surface.

### Plan Steps

- [x] Step 1: Remove API URL exposure and DRF settings dependencies.
- [x] Step 2: Remove API-only modules (viewsets/serializers/routes) and fix imports.
- [x] Step 3: Update tests for supported non-API behavior and run targeted scope.
- [x] Step 4: Update `README.md` and `CHANGELOG.md`.

### Validation

- Targeted tests executed and passed during implementation cycle.

### Execution Log

- 2026-03-03 21:09 UTC — Spec created.
- 2026-03-03 21:09 UTC — Plan created.
- 2026-03-03 21:09 UTC — Implementation started.
- 2026-03-03 21:13 UTC — Tests executed (`72 passed`).
- 2026-03-03 — Cycle closed.

## Track 002: Modularize Frontend Views

### Objectives

- Split `frontend/views.py` into domain modules.
- Preserve facade import compatibility and behavior.

### Plan Steps

- [x] Step 1: Create `frontend/view_modules/` and move code by domain.
- [x] Step 2: Convert `frontend/views.py` into compatibility facade.
- [x] Step 3: Run targeted frontend + americano regression scopes.
- [x] Step 4: Update changelog.

### Validation

- `pytest -q paddle/frontend/tests/test_auth.py paddle/frontend/tests/test_views.py paddle/frontend/tests/test_players_pages.py paddle/frontend/tests/test_ranking.py paddle/frontend/tests/test_player_stats.py`
- `pytest -q paddle/frontend/tests/test_about.py paddle/frontend/tests/test_about_version.py paddle/frontend/tests/test_views_coverage_extra.py paddle/americano/tests/test_americano_views.py`
- Result: `63 passed`, `43 passed`.

### Execution Log

- 2026-03-03 21:36 UTC — Spec created.
- 2026-03-03 21:36 UTC — Plan created.
- 2026-03-03 21:36 UTC — Spec approved.
- 2026-03-03 21:36 UTC — Plan approved.
- 2026-03-03 21:37 UTC — Implementation started.
- 2026-03-03 21:42 UTC — Tests executed (`63 passed`, `43 passed`).
- 2026-03-03 22:19 UTC — Manual checks confirmed; cycle closed.

## Track 003: Ranking Source-of-Truth Alignment

### Objectives

- Enforce one canonical ranking policy.
- Align persisted and rendered ranking behavior.

### Plan Steps

- [x] Step 1: Baseline current ranking behavior and identify canonical policy.
- [x] Step 2: Refactor ranking paths to canonical policy.
- [x] Step 3: Add tests for ties/scope/zero-match and persisted-rendered coherence.
- [x] Step 4: Run targeted ranking-related test scopes.
- [x] Step 5: Update changelog.

### Validation

- `pytest -q paddle/frontend/tests/test_ranking.py paddle/frontend/tests/test_players_pages.py paddle/frontend/tests/test_player_stats.py paddle/frontend/tests/test_views.py`
- `pytest -q paddle/games/tests`
- Result: `59 passed` baseline, then `61 passed` post-refactor.

### Execution Log

- 2026-03-03 22:24 UTC — Spec approved.
- 2026-03-03 22:24 UTC — Plan created.
- 2026-03-03 22:53 UTC — Baseline tests executed (`59 passed`).
- 2026-03-03 22:58 UTC — Canonical policy implementation aligned.
- 2026-03-03 22:59 UTC — Extended ranking tests added.
- 2026-03-03 23:00 UTC — Validation tests executed (`61 passed`).
- 2026-03-03 23:01 UTC — Changelog updated.
- 2026-03-03 23:07 UTC — Cycle closed.

## Track 004: Core Match-Participation Query Harmonization

### Objectives

- Centralize player match-participation query construction.
- Reuse shared helper across core frontend paths.

### Plan Steps

- [x] Step 1: Baseline tests for matches/player/helper flows.
- [x] Step 2: Add shared helper and refactor call sites.
- [x] Step 3: Add/update helper equivalence regression tests.
- [x] Step 4: Run targeted validation tests.
- [x] Step 5: Update changelog.

### Validation

- `pytest -q paddle/frontend/tests/test_views.py paddle/frontend/tests/test_players_pages.py paddle/frontend/tests/test_views_coverage_extra.py paddle/frontend/tests/test_auth.py`
- Result: `60 passed` baseline, then `61 passed` post-refactor.

### Execution Log

- 2026-03-03 23:10 UTC — Spec created.
- 2026-03-03 23:12 UTC — Spec approved.
- 2026-03-03 23:13 UTC — Plan created.
- 2026-03-03 23:14 UTC — Plan approved.
- 2026-03-03 23:16 UTC — Baseline tests executed (`60 passed`).
- 2026-03-03 23:19 UTC — Shared helper implemented and call sites refactored.
- 2026-03-03 23:21 UTC — Helper equivalence regression test added.
- 2026-03-03 23:22 UTC — Validation tests executed (`61 passed`).
- 2026-03-03 23:23 UTC — Changelog updated.
- 2026-03-03 23:24 UTC — Cycle closed.

## Combined Post-Mortem

### Worked Well

- Incremental refactor tracks stayed behavior-safe by using targeted tests and manual checks.
- Facade and shared-helper patterns reduced drift risk without changing user-visible behavior.

### Friction

- `markdownlint` CLI not available in environment required manual checks.
- Duplicate query-path detection relied on manual inspection.

### Suggested Future Improvements

- Add architecture guard tests for key shared helper reuse.
- Add structural checks to prevent reintroduction of duplicated query/filter logic.
