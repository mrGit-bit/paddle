# Spec 004: Repository Harmonization for Core Match-Participation Queries

## Functional Goal

Harmonize duplicated core query patterns across frontend modules by centralizing player match-participation queryset construction and reusing the same helper paths, without changing routes, templates, or user-visible behavior.

## Scope

### In

- Identify duplicated `Match` participation query logic used for:
  - player profile match history
  - user match list in `/matches/`
  - session “new matches” detection
- Introduce one shared helper for player participation queryset construction in frontend shared helpers.
- Refactor frontend modules to reuse that helper instead of inlining duplicated query expressions.
- Keep ordering and distinct behavior identical to current behavior.
- Add or update tests to prove no regressions in rendered pages and helper behavior.

### Out

- No ranking algorithm changes.
- No URL/path/name changes.
- No template file modifications.
- No model schema/migration changes.
- No changes to americano/mobile modules.

## UI/UX Requirements

- `/matches/`, `/players/`, and `/players/<id>/` render and behave exactly as before.
- Existing pagination and “new matches” badges/behavior remain unchanged.
- Existing Spanish UI copy remains unchanged.

## Backend Requirements

- Shared helper must be reusable by `matches.py`, `players.py`, and `common.py`.
- Query result semantics must remain equivalent (same participant coverage, distinct rows, ordering expectations).
- Refactor should reduce duplicated query blocks and keep module responsibilities clear.

## Data Rules

- Participation query must include all four match slots (`team1_player1`, `team1_player2`, `team2_player1`, `team2_player2`).
- Distinct behavior must prevent duplicate match rows.
- Existing ordering rules (`-date_played` where currently expected) must remain unchanged.

## Reuse Rules

- Reuse existing shared module `paddle/frontend/view_modules/common.py` for new helper placement.
- Do not duplicate participant filter logic across modules after refactor.
- Keep helper naming explicit and domain-focused.

## Acceptance Criteria

- [x] AC1: One shared helper exists for player match-participation queryset construction.
- [x] AC2: `matches.py`, `players.py`, and `common.py` no longer duplicate participant filter blocks.
- [x] AC3: Existing frontend tests for matches/player pages/stat helpers pass.
- [x] AC4: Targeted new/updated tests verify helper equivalence and no behavior regressions.
- [x] AC5: `CHANGELOG.md` includes an Unreleased entry describing the harmonization refactor.

## Manual Functional Checks

1. Open `/matches/` and verify full matches list and “Mis partidos” still show expected rows and ordering.
2. Open `/players/<id>/` and verify profile match history renders the same matches as before.
3. Log in as a player with unseen matches and verify new-match indicators still appear and clear correctly.
4. Create a new match and verify it appears correctly in both global and user-specific match lists.
5. Delete a match as authorized user and verify both lists and badges update coherently.

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

## Notes

This spec continues the harmonization track by removing duplicated core query logic while preserving behavior.

## Status

- Approved by user.
- Implemented and verified.
- Closed on 2026-03-03.
