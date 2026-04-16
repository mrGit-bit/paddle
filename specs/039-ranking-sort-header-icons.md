# Ranking Sort Header Icons

## Tracking

- Task ID: `ranking-sort-header-icons`
- Status: `implemented`
- Release tag: `v1.9.1`

## Summary

- Ranking table sort icons currently inherit Bootstrap link blue.
- On small screens, table header truncation can show ellipsis dots beside the
  sort arrows.
- Sort icons should render white and remain clean on narrow viewports.

## Scope

- In:
  - Ranking table sort header styling.
  - Hall of Fame ranking sort header markup.
  - Changelog entry for the UI fix.
- Out:
  - Pagination ellipsis behavior.
  - Ranking sort logic.
  - Backend ranking computation.

## Files Allowed to Change

- `CHANGELOG.md`
- `paddle/frontend/static/frontend/css/styles.css`
- `paddle/frontend/templates/frontend/hall_of_fame.html`
- `specs/039-ranking-sort-header-icons.md`

## Files Forbidden to Change

- Backend models, views, services, migrations, and JavaScript sorting logic.

## Implementation Plan

- [x] Add a targeted class to ranking sort header cells.
- [x] Add CSS rules that keep sort buttons and icons white in all button states.
- [x] Disable ellipsis only for ranking sort header cells.
- [x] Document the visible UI change in the changelog.

## Acceptance

- [x] Ranking sort icons render white instead of blue.
- [x] Small screens do not show ellipsis dots beside ranking sort arrows.
- [x] Pagination ellipsis dots are unchanged.

## Validation

- `pytest paddle/frontend/tests/test_views.py::TestFrontendViews::test_hall_of_fame_view_renders_ranking_sort_controls -q`
- `pytest paddle/frontend/tests/test_views.py paddle/frontend/tests/test_ranking.py -q`
- `markdownlint CHANGELOG.md specs/039-ranking-sort-header-icons.md`
- Manual checks on desktop and narrow mobile ranking pages.
