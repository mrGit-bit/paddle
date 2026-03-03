<!-- markdownlint-disable MD032 -->
<!-- markdownlint-disable MD022 -->

# Modularize Frontend Views (No Behavior Change)

## Context
- `paddle/frontend/views.py` is currently a high-size mixed-responsibility file (~900+ lines).
- This increases cognitive load and makes targeted maintenance harder.
- A structural split is needed while preserving route contracts and behavior.

## Spec Reference
- `specs/002-modularize-frontend-views.md`

## Objectives
- Improve code coherence by grouping views/helpers by domain.
- Keep import compatibility via `frontend.views` facade.
- Preserve runtime behavior and test outcomes.

## Scope

### In
- Internal module split + facade export.
- Minimal import rewiring.
- Targeted regression tests.
- Changelog update.

### Out
- No route/template/business logic redesign.
- No ranking algorithm changes.

## Risks
- Risk: accidental behavioral change while moving code.
  - Mitigation: mostly copy-move code, avoid logic edits, run targeted tests.
- Risk: missing exported names used by tests or URLconf.
  - Mitigation: explicit export list in `frontend/views.py` and import checks.
- Risk: circular imports.
  - Mitigation: centralize shared helpers in one module and keep dependency direction unidirectional.

## Files Allowed to Change
- `paddle/frontend/views.py`
- `paddle/frontend/urls.py`
- `paddle/frontend/tests/test_views.py`
- `paddle/frontend/tests/test_players_pages.py`
- `paddle/frontend/tests/test_auth.py`
- `paddle/frontend/tests/test_player_stats.py`
- `paddle/frontend/tests/test_ranking.py`
- `paddle/frontend/tests/test_about.py`
- `paddle/frontend/tests/test_about_version.py`
- `paddle/frontend/tests/test_views_coverage_extra.py`
- `paddle/frontend/view_modules/**`
- `CHANGELOG.md`

## Files Forbidden to Change
- `paddle/frontend/templates/**`
- `paddle/frontend/services/ranking.py`
- `paddle/games/**`
- `paddle/users/**`
- `paddle/americano/**`
- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`

## Proposed Changes (Step-by-Step by File)
- `paddle/frontend/view_modules/common.py`
  - Change: move shared helpers/forms/common pagination/session helpers.
  - Why: remove cross-domain duplication and isolate utility concerns.
- `paddle/frontend/view_modules/ranking.py`
  - Change: move ranking-specific views/helpers.
  - Why: isolate ranking page orchestration.
- `paddle/frontend/view_modules/players.py`
  - Change: move player profile/list logic and insights helpers.
  - Why: isolate player-facing page logic.
- `paddle/frontend/view_modules/matches.py`
  - Change: move match-page orchestration and match display helpers.
  - Why: isolate match workflow logic.
- `paddle/frontend/view_modules/auth_profile.py`
  - Change: move register/login/logout/user/about flows and form parsing.
  - Why: isolate auth/profile concerns.
- `paddle/frontend/views.py`
  - Change: convert to facade that re-exports existing callables.
  - Why: preserve stable import path for URLconf/tests.
- `CHANGELOG.md`
  - Change: add Unreleased note for internal modularization.
  - Why: keep release notes aligned.

## Plan Steps (Execution Order)
- [x] Step 1: Create `frontend/view_modules/` package and move code into domain modules.
- [x] Step 2: Replace `frontend/views.py` with compatibility facade exporting unchanged names.
- [x] Step 3: Run targeted pytest scopes for frontend + americano regression checks.
- [x] Step 4: Update changelog under `[Unreleased]`.

## Acceptance Criteria (Testable)
- [x] AC1: All existing route handlers still resolve via `frontend.views`.
- [x] AC2: No user-visible behavior changes in core frontend flows.
- [x] AC3: Targeted tests pass.
- [x] AC4: Changelog updated.

## Validation Commands
- `pytest -q paddle/frontend/tests/test_auth.py paddle/frontend/tests/test_views.py paddle/frontend/tests/test_players_pages.py paddle/frontend/tests/test_ranking.py paddle/frontend/tests/test_player_stats.py`
- `pytest -q paddle/frontend/tests/test_about.py paddle/frontend/tests/test_about_version.py paddle/frontend/tests/test_views_coverage_extra.py paddle/americano/tests/test_americano_views.py`

## Manual Functional Checks
1. Verify ranking pages and scope redirects.
2. Verify players list/detail and insights.
3. Verify match create/delete flows.
4. Verify register/login/logout/user profile update.
5. Verify about page metrics and version label.

## Execution Log
- 2026-03-03 21:36 UTC — Spec created.
- 2026-03-03 21:36 UTC — Plan created.
- 2026-03-03 21:37 UTC — Implementation started.
- 2026-03-03 21:42 UTC — Tests executed (`63 passed`, `43 passed`).

## Post-Mortem / Improvements
- To be completed after implementation.
