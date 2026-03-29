# Add Ranking Page Local Sorting

## Tracking

- Task ID: `add-ranking-page-local-sorting`
- Plan: `plans/2026-03-29_add-ranking-page-local-sorting.md`
- Release tag: `unreleased`

## Goal

- Let users locally reorder the currently visible ranking page by position,
  wins, matches, or win rate.
- Preserve canonical server-side ranking order as the default on each page
  load and page change.

## Scope

- In:
  - add local sorting controls to the shared ranking table
  - sort only the currently visible page in the browser
  - restore canonical order on every fresh page load
  - show position for every visible player in non-canonical sort modes
  - add focused render tests for the new controls and row metadata
  - update the unreleased changelog entry
- Out:
  - changing backend ranking policy
  - changing pagination boundaries or query params
  - sorting the user snippet or unranked table

## Files

- Allowed:
  - `paddle/frontend/templates/frontend/hall_of_fame.html`
  - `paddle/frontend/static/frontend/js/rowLink.js`
  - `paddle/frontend/static/frontend/js/rankingTableSort.js`
  - `paddle/frontend/view_modules/ranking.py`
  - `paddle/frontend/tests/test_views.py`
  - `paddle/frontend/tests/test_ranking.py`
  - `CHANGELOG.md`
- Forbidden:
  - `paddle/frontend/services/ranking.py`
  - `paddle/games/**`
  - `paddle/americano/**`
  - `.github/workflows/**`

## Acceptance

- [ ] The ranking table exposes local sort controls for position, wins, matches,
      and win rate.
- [ ] Sorting only reorders the players already visible on the current page.
- [ ] Fresh page loads and page changes start in canonical position order.
- [ ] The position column shows one row per tie group only in canonical display
      modes and shows every player position in other sort modes.

## Checks

- Render the ranking page and confirm the new sort controls and row metadata
  are present.
- Verify manually that sorting changes only the visible page and resets after a
  page change.
