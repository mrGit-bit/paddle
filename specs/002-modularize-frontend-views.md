<!-- markdownlint-disable MD022 -->
<!-- markdownlint-disable MD032 -->

# Spec 002: Modularize Frontend Views Without Behavior Changes

## Functional Goal
Improve coherence and simplicity by splitting `paddle/frontend/views.py` into focused internal modules while preserving all current routes, outputs, and user-visible behavior.

## Scope

### In
- Create internal view modules grouped by responsibility (ranking, players, matches, auth/profile, shared helpers).
- Keep `paddle/frontend/views.py` as compatibility facade exporting the same callable names used by URLs/tests.
- Keep `paddle/frontend/urls.py` behavior unchanged.
- Add/update tests only as needed to validate no behavioral regression.
- Update changelog for architectural refactor.

### Out
- No URL path/name changes.
- No template behavior changes.
- No ranking/business-rule changes.
- No database model/schema changes.

## UI/UX Requirements
- All visible pages and messages remain exactly as before.
- Existing redirects and scope behavior remain unchanged.

## Backend Requirements
- Existing imports from `frontend.views` must continue to work.
- Module split must avoid circular imports and duplicated logic.
- Keep functions thinly organized by domain responsibility.

## Data Rules
- No ranking/sorting/tie behavior changes.
- No match/player/user persistence behavior changes.

## Reuse Rules
- Reuse existing function implementations; move code with minimal edits.
- Do not duplicate helper logic across modules.

## Acceptance Criteria
- [ ] AC1: `paddle/frontend/views.py` is reduced to a facade and exports existing public view/helper callables.
- [ ] AC2: `paddle/frontend/urls.py` continues resolving the same callables without route changes.
- [ ] AC3: Targeted frontend and americano tests pass unchanged.
- [ ] AC4: Changelog includes a clear note about internal frontend view modularization.

## Manual Functional Checks
1. Open `/`, `/ranking/male/`, `/ranking/female/`, `/ranking/mixed/` and confirm same rendering/behavior.
2. Open `/players/` and `/players/<id>/` and confirm insights, match list, and scope links work.
3. Create and delete a match in `/matches/` and confirm success/error flows are unchanged.
4. Login, logout, register, and update email in `/users/<id>/` and confirm behavior is unchanged.
5. Open `/about/` and confirm stats/version label render.

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

## Notes
This spec focuses on module boundaries and maintainability only (no functional deltas).
