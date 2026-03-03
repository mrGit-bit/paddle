# Ranking Source-of-Truth Alignment

## Context

- Ranking behavior currently spans multiple layers (model-level persisted position and frontend scoped ranking computation).
- Without a clearly enforced single policy, coherence risk remains high (future drift in ordering/ties/scope handling).
- This plan aligns ranking logic under an explicit canonical policy and removes duplicate/conflicting implementations.

## Spec Reference

- `specs/003-ranking-source-of-truth-alignment.md`

## Objectives

- Define and enforce one canonical ranking policy per supported context.
- Remove duplicate ranking implementations or convert them to thin delegates.
- Preserve current user-visible ranking behavior unless explicitly changed.

## Scope

### In

- Ranking code-path audit and policy codification.
- Refactor of ranking-related modules/models as needed for coherence.
- Targeted tests for ranking tie/order/scope consistency.
- Changelog update.

### Out

- No template/UI redesign.
- No route changes.
- No unrelated match/auth refactors.

## Risks

- Risk: subtle ranking behavior change in ties or ordering keys.
  - Mitigation: lock current expected behavior via tests before and after refactor.
- Risk: persisted `ranking_position` semantics diverge from scoped rankings.
  - Mitigation: explicitly document intended distinction and enforce deterministic update rules.
- Risk: hidden dependencies on legacy ranking fields.
  - Mitigation: run targeted frontend/game test scopes touching ranking, players, and match updates.

## Files Allowed to Change

- `paddle/frontend/services/ranking.py`
- `paddle/games/models.py`
- `paddle/frontend/view_modules/ranking.py`
- `paddle/frontend/view_modules/players.py`
- `paddle/frontend/tests/test_ranking.py`
- `paddle/frontend/tests/test_players_pages.py`
- `paddle/frontend/tests/test_player_stats.py`
- `paddle/frontend/tests/test_views.py`
- `paddle/games/tests/**`
- `CHANGELOG.md`

## Files Forbidden to Change

- `paddle/frontend/templates/**`
- `paddle/americano/**`
- `mobile/**`
- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`

## Proposed Changes (Step-by-Step by File)

- `paddle/frontend/services/ranking.py`
  - Change: codify canonical ordering and tie policy with explicit comments and helper boundaries.
  - Why: make ranking behavior explicit and reusable.
- `paddle/games/models.py`
  - Change: align persisted `ranking_position` computation to canonical policy or delegate to shared ranking engine where feasible.
  - Why: eliminate policy drift between persisted and rendered ranking semantics.
- `paddle/frontend/view_modules/ranking.py`
  - Change: consume canonical ranking outputs only.
  - Why: prevent local sorting/policy forks.
- `paddle/frontend/view_modules/players.py`
  - Change: ensure scoped rank/page lookups rely on canonical ranking path.
  - Why: keep player detail consistency with ranking pages.
- `paddle/frontend/tests/test_ranking.py`
  - Change: extend/adjust tie-order and scope consistency assertions.
  - Why: enforce canonical behavior.
- `paddle/frontend/tests/test_players_pages.py` and `paddle/frontend/tests/test_player_stats.py`
  - Change: ensure player-facing rank references remain coherent with ranking pages.
  - Why: catch user-visible inconsistencies.
- `paddle/games/tests/**`
  - Change: validate persisted ranking update behavior where applicable after match changes.
  - Why: ensure model-level coherence.
- `CHANGELOG.md`
  - Change: add Unreleased entry describing ranking coherence refactor.
  - Why: keep release documentation accurate.

## Plan Steps (Execution Order)

- [x] Step 1: Baseline current ranking behavior with targeted tests and identify canonical policy from existing expected behavior.
- [x] Step 2: Refactor ranking code paths to a single canonical policy and remove/align duplicates.
- [x] Step 3: Update/add tests for ties, scope, zero-match handling, and persisted vs rendered coherence.
- [x] Step 4: Run targeted ranking-related pytest scopes and verify no regressions.
- [x] Step 5: Update changelog under `[Unreleased]`.

## Acceptance Criteria (Testable)

- [x] AC1: Canonical ranking policy is explicit and test-backed.
- [x] AC2: No conflicting ranking implementations remain.
- [x] AC3: Ranking UI behavior remains coherent across scopes and player pages.
- [x] AC4: Persisted ranking behavior is deterministic and aligned/documented.
- [x] AC5: Targeted tests pass.

## Validation Commands

- `pytest -q paddle/frontend/tests/test_ranking.py paddle/frontend/tests/test_players_pages.py paddle/frontend/tests/test_player_stats.py paddle/frontend/tests/test_views.py`
- `pytest -q paddle/games/tests`

## Manual Functional Checks

1. Verify ranking ordering/ties across all ranking scopes.
2. Verify zero-match players appear in unranked list per scope.
3. Create/delete match and verify ranking updates remain coherent.
4. Verify player detail rank references align with ranking pages.
5. Verify pagination/snippet behavior for tied players.

## Execution Log

- 2026-03-03 22:24 UTC — Spec approved by user.
- 2026-03-03 22:24 UTC — Plan created.
- 2026-03-03 22:53 UTC — Baseline ranking/player test scope executed (`59 passed`).
- 2026-03-03 22:58 UTC — Canonical ranking policy implemented and model ranking recalculation aligned.
- 2026-03-03 22:59 UTC — Extended ranking coherence tests added (frontend + games).
- 2026-03-03 23:00 UTC — Targeted validation executed (`61 passed`).
- 2026-03-03 23:01 UTC — Changelog updated under `[Unreleased]`.
- 2026-03-03 23:07 UTC — User confirmed closure; cycle closed.

## Post-Mortem / Improvements

- Worked well:
  - Shared canonical helpers eliminated sort/tie drift cleanly.
  - Targeted regression coverage validated persisted/rendered coherence.
- Friction:
  - `markdownlint` CLI is unavailable in this environment, requiring manual Markdown checks.
- Suggested follow-up:
  - Add optional architecture guard ensuring `update_player_rankings` keeps using canonical helpers.
