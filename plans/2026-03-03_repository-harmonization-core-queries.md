# Repository Harmonization for Core Match-Participation Queries

## Context

- Frontend modules currently duplicate player-participation `Match` query logic across multiple files.
- The duplication appears in player profile history, user matches list, and new-match detection helpers.
- Centralizing this query path improves maintainability and reduces drift risk without changing behavior.

## Spec Reference

- `specs/004-repository-harmonization-core-queries.md`

## Objectives

- Define one shared helper for player match-participation queryset construction.
- Replace duplicated participant filter blocks with helper reuse.
- Preserve existing behavior, ordering, and distinct semantics.
- Validate no regressions through targeted frontend tests.

## Scope

### In

- Add shared helper in frontend shared module.
- Refactor `matches.py`, `players.py`, and `common.py` to use shared helper.
- Add/update targeted tests for helper equivalence and behavior continuity.
- Update `CHANGELOG.md` under `## [Unreleased]`.

### Out

- No template modifications.
- No ranking policy changes.
- No model/migration changes.
- No route or URL-name changes.
- No americano/mobile changes.

## Risks

- Risk: subtle queryset ordering changes.
  - Mitigation: keep existing call-site ordering semantics (`order_by("-date_played")`) and add tests.
- Risk: duplicate rows if `distinct()` handling changes.
  - Mitigation: preserve current `distinct()` behavior in shared helper and verify with tests.
- Risk: regression in new-match session indicators.
  - Mitigation: run existing tests covering `get_new_match_ids` and add targeted assertions if needed.

## Files Allowed to Change

- `paddle/frontend/view_modules/common.py`
- `paddle/frontend/view_modules/matches.py`
- `paddle/frontend/view_modules/players.py`
- `paddle/frontend/tests/test_views.py`
- `paddle/frontend/tests/test_players_pages.py`
- `paddle/frontend/tests/test_views_coverage_extra.py`
- `paddle/frontend/tests/test_auth.py`
- `CHANGELOG.md`

## Files Forbidden to Change

- `paddle/frontend/templates/**`
- `paddle/frontend/services/ranking.py`
- `paddle/games/models.py`
- `paddle/americano/**`
- `mobile/**`
- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`

## Proposed Changes (Step-by-Step by File)

- `paddle/frontend/view_modules/common.py`
  - Change: introduce shared helper to build player participation match queryset.
  - Why: remove duplicated participant filter logic and standardize semantics.
  - Notes: helper should return a queryset suitable for call-site ordering.
- `paddle/frontend/view_modules/players.py`
  - Change: replace inline participation query in `build_player_matches_queryset` with shared helper usage.
  - Why: align player profile flow to canonical query path.
- `paddle/frontend/view_modules/matches.py`
  - Change: replace inline user-match participation queryset construction with shared helper usage.
  - Why: remove duplicate query block and harmonize behavior.
- `paddle/frontend/view_modules/common.py` (`get_new_match_ids`)
  - Change: reuse the same shared helper for participant match retrieval.
  - Why: keep new-match detection consistent with other match retrieval paths.
- `paddle/frontend/tests/test_views.py`, `paddle/frontend/tests/test_players_pages.py`, `paddle/frontend/tests/test_views_coverage_extra.py`
  - Change: add/adjust tests to assert helper reuse behavior equivalence where needed.
  - Why: lock existing behavior and prevent regressions.
- `CHANGELOG.md`
  - Change: add Unreleased entry describing harmonization of core participation queries.
  - Why: keep changelog aligned with implemented behavior-neutral refactor.

## Plan Steps (Execution Order)

- [x] Step 1: Baseline current behavior by running targeted frontend test scope for matches/player/helper flows.
- [x] Step 2: Add shared participation queryset helper in `common.py` and refactor call sites in `players.py`, `matches.py`, and `get_new_match_ids`.
- [x] Step 3: Add/update tests to confirm equivalence of participant retrieval semantics and no regression in views/helpers.
- [x] Step 4: Run targeted pytest validation scope and ensure all tests pass.
- [x] Step 5: Update `CHANGELOG.md` under `[Unreleased]`.

## Acceptance Criteria (Testable)

- [x] AC1: Shared helper exists and is used by all intended frontend call sites.
- [x] AC2: No duplicated participant query blocks remain in the scoped frontend modules.
- [x] AC3: Targeted frontend tests for matches/players/helpers pass.
- [x] AC4: New-match detection behavior remains unchanged.
- [x] AC5: Changelog is updated with harmonization entry.

## Validation Commands

- `pytest -q paddle/frontend/tests/test_views.py paddle/frontend/tests/test_players_pages.py paddle/frontend/tests/test_views_coverage_extra.py paddle/frontend/tests/test_auth.py`

## Manual Functional Checks

1. Open `/matches/` and verify global matches table and “Mis partidos” list still match expected participant coverage.
2. Open `/players/<id>/` and verify profile match history rows are unchanged.
3. Log in as a linked player and confirm new-match indicator appears and clears as before.
4. Create a match and verify it appears in both global and user-specific views.
5. Delete a match and verify both lists update without duplicate or missing rows.

## Execution Log

- 2026-03-03 23:10 UTC — Spec created.
- 2026-03-03 23:12 UTC — Spec approved.
- 2026-03-03 23:13 UTC — Plan created.
- 2026-03-03 23:14 UTC — Plan approved.
- 2026-03-03 23:16 UTC — Baseline tests executed (`60 passed`).
- 2026-03-03 23:19 UTC — Shared participation queryset helper implemented and call sites refactored.
- 2026-03-03 23:21 UTC — Targeted helper equivalence regression test added.
- 2026-03-03 23:22 UTC — Validation tests executed (`61 passed`).
- 2026-03-03 23:23 UTC — Changelog updated under `[Unreleased]`.
- 2026-03-03 23:24 UTC — User requested closure; cycle closed.

## Post-Mortem / Improvements

- Worked well:
  - Narrow-scope harmonization removed duplication without user-visible changes.
  - Existing tests plus one focused helper test gave clear regression coverage.
- Friction:
  - Query duplication detection relied on manual inspection/grep instead of a structural lint rule.
- Suggested follow-up:
  - Add architecture guard tests for helper reuse in core match-participation retrieval paths.
