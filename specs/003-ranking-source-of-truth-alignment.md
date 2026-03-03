# Spec 003: Ranking Source-of-Truth Alignment

## Functional Goal

Define and enforce a single, coherent ranking source of truth so ranking values and ordering behavior are consistent across persisted fields and rendered ranking pages.

## Scope

### In

- Audit current ranking pathways used by:
  - persisted `Player.ranking_position`
  - ranking page computation in `frontend/services/ranking.py`
  - any model-side ranking recalculation helpers
- Decide and document canonical ranking policy (ordering keys, tie behavior, scope behavior).
- Refactor code so only one canonical ranking policy is used for each supported context.
- Remove or adapt duplicate/conflicting ranking logic.
- Add or update tests that prove consistency between the canonical policy and rendered pages.

### Out

- No template redesign.
- No URL changes.
- No API reintroduction.
- No unrelated refactor of match workflows.

## UI/UX Requirements

- Ranking pages keep existing user-visible behavior unless explicitly approved.
- Tie style remains competition style where currently expected.
- Scope tabs and player pages keep existing navigation flow.

## Backend Requirements

- Ranking logic must have one authoritative implementation path per supported context.
- Conflicting duplicate ranking functions must be removed or converted into thin delegates to the source of truth.
- Behavior differences between persisted ranking and scope-specific ranking must be explicitly documented if both are intentionally retained.

## Data Rules

- Ordering keys and tie-breakers must be explicitly defined.
- Null/zero-match handling must be explicit and tested.
- If persisted `ranking_position` is kept, update triggers must be deterministic and test-covered.

## Reuse Rules

- Reuse `frontend/services/ranking.py` where possible instead of introducing new ranking engines.
- Do not duplicate sort/tie logic across model/service/view layers.

## Acceptance Criteria

- [x] AC1: A documented canonical ranking policy exists in code comments or supporting docs.
- [x] AC2: Duplicate/conflicting ranking implementations are removed or aligned.
- [x] AC3: Ranking page outputs remain stable for existing scenarios.
- [x] AC4: Tests cover tie cases, zero-match players, and scope-specific behavior.
- [x] AC5: Changelog clearly describes ranking coherence refactor.

## Manual Functional Checks

1. Validate ranking order and tie display in `all`, `male`, `female`, and `mixed` scopes.
2. Verify players with zero scoped matches appear in unranked sections as expected.
3. Create/delete match and verify ranking updates remain coherent.
4. Open player detail pages and confirm displayed rank references remain consistent with ranking pages.
5. Confirm no regression in pagination and neighbor/snippet behavior around tied positions.

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

## Notes

This spec starts the second coherence refactor track after frontend view modularization closure.

## Status

- Approved by user.
- Implemented and verified.
- Closed on 2026-03-03.
