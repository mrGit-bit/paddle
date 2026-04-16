# Player Partner Progress Bar

Use for active SDD work only.

## Tracking

- Task ID: `player-partner-progress-bar`
- Status: `implemented`
- Release tag: `v1.9.1`

`approved` stays in place until the scoped work is finished and the
development cycle for this spec is being closed. Only then move the spec to
`implemented`.

## Summary

- Replace the player detail `Pareja habitual` table with a Bootstrap stacked
  progress bar.
- Show the top three partners plus a grouped `Otros` remainder as a compact
  partner distribution.
- Keep partner ranking and percentage preparation in backend context; templates
  only render prepared rows.

## Scope

- In:
  - Player detail habitual-partner rendering.
  - Backend display context for partner distribution.
  - Focused CSS for the stacked bar and legend.
  - Focused player detail tests.
  - Changelog entry.
- Out:
  - Ranking logic changes.
  - Match query, pagination, rival, model, migration, or JavaScript changes.
  - Reworking unrelated player detail layout.

## Files Allowed to Change

- `paddle/frontend/view_modules/players.py`
- `paddle/frontend/templates/frontend/player_detail.html`
- `paddle/frontend/static/frontend/css/styles.css`
- `paddle/frontend/tests/test_players_pages.py`
- `CHANGELOG.md`
- `specs/042-player-partner-progress-bar.md`

## Files Forbidden to Change

- Models, migrations, ranking services, JavaScript files, and unrelated
  templates.

## Implementation Plan

- [x] Add backend-prepared partner distribution rows.
- [x] Replace the partner table with a stacked Bootstrap progress bar.
- [x] Add compact legend and focused CSS.
- [x] Update tests and changelog.

## Acceptance

- [x] `Pareja habitual` renders a single stacked progress bar when partner data
  exists.
- [x] The bar shows up to three partners plus empty-track `Otros` for remaining
  partners.
- [x] Segment percentages are based on total matches represented by partner
  rows.
- [x] Partner legend labels link to player detail pages, while `Otros` stays
  out of the legend.
- [x] Players with no partner data still show `Sin datos`.
- [x] No JavaScript or frontend ranking logic is added.

## Validation

- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `markdownlint CHANGELOG.md specs/042-player-partner-progress-bar.md`
- Manually check zero-match, two-partner, three-partner, and four-plus-partner
  player detail pages.
- Manually check mobile and desktop readability.
