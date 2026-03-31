# Add Ranking Page Local Sorting Plan

## Tracking

- Task ID: `add-ranking-page-local-sorting`
- Spec: `specs/033-add-ranking-page-local-sorting.md`
- Release tag: `unreleased`

## Summary

- Ranking pages currently render only canonical server order.
- Users need local reordering by position, wins, matches, and win rate without
  changing backend ranking or pagination.

## Scope

- In:
  - add sortable ranking headers and row metadata
  - add client-side table sorting for the visible page only
  - preserve canonical ranking as the reset/default state
  - apply the position-visibility rule for canonical vs non-canonical sorts
  - add focused render coverage
- Out:
  - backend ranking changes
  - persistent sort state
  - user snippet or unranked table sorting

## Files Allowed to Change

- `paddle/frontend/templates/frontend/hall_of_fame.html`
- `paddle/frontend/static/frontend/js/rowLink.js`
- `paddle/frontend/static/frontend/js/rankingTableSort.js`
- `paddle/frontend/view_modules/ranking.py`
- `paddle/frontend/tests/test_views.py`
- `paddle/frontend/tests/test_ranking.py`
- `CHANGELOG.md`

## Files Forbidden to Change

- `paddle/frontend/services/ranking.py`
- `paddle/games/**`
- `paddle/americano/**`
- `.github/workflows/**`

## Plan

- [ ] Pass any minimal ranking-table defaults needed by the template.
- [ ] Add sortable headers and per-row metadata to the shared ranking table.
- [ ] Implement client-side current-page sorting with canonical reset behavior.
- [ ] Add focused ranking render tests and update the changelog.

## Acceptance

- [ ] Users can locally sort by position, wins, matches, and win rate.
- [ ] Position cells keep compact tie display in canonical modes and show every
      position in non-canonical modes.
- [ ] Pagination changes reset the table to canonical order automatically.

## Validation

- `pytest paddle/frontend/tests/test_views.py -q`
- `pytest paddle/frontend/tests/test_ranking.py -q`
- Manual checks:
  - load a ranking page and confirm it starts in canonical order
  - sort by matches and confirm only the current page reorders
  - sort by win rate and confirm only the current page reorders
  - click wins ascending or position ascending and confirm compact position
    display is restored
  - move to another page and confirm canonical order is restored
