# Player Efficiency Scope Wheels

Use for active SDD work only.

## Tracking

- Task ID: `player-efficiency-scope-wheels`
- Status: `implemented`
- Release tag: `unreleased`

`approved` stays in place until the scoped work is finished and the
development cycle for that spec is being closed. Only then move the spec to
`implemented`.

## Summary

- Extend the public player detail `Eficacia` section with selector wheels for
  `Todos`, the displayed player's gender category, and `Mixtos`.
- Update the trend wheels to show `Ultimos 5`, `Ultimos 10`, and `Ultimos 20`
  for the selected scope.
- Keep selected cards readable with selected-tab borders and an inverted `Ver`
  action instead of full-card background color.

## Scope

- In:
  - Player detail efficiency backend data.
  - Player detail template, local CSS, and lightweight vanilla JS.
  - Focused player detail tests.
  - Changelog entry.
- Out:
  - Ranking logic changes.
  - Other player insight blocks.
  - Models and migrations.

## Files Allowed to Change

- `paddle/frontend/view_modules/players.py`
- `paddle/frontend/templates/frontend/player_detail.html`
- `paddle/frontend/static/frontend/css/styles.css`
- `paddle/frontend/tests/test_players_pages.py`
- `CHANGELOG.md`
- `specs/043-player-efficiency-scope-wheels.md`

## Files Forbidden to Change

- Models, migrations, ranking services, and unrelated templates.

## Implementation Plan

- [x] Build all, gender, and mixed efficiency scope data in the player insights
  helper.
- [x] Replace the single trend row with selector and scoped trend rows.
- [x] Add minimal JS and local styles for active scope switching with explicit
  selector-card affordance.
- [x] Update focused tests and changelog.

## Acceptance

- [x] The first efficiency row renders three selector wheels and defaults to
  `Todos`.
- [x] The second row renders `Ultimos 5`, `Ultimos 10`, and `Ultimos 20` for
  the selected scope.
- [x] The selected selector card uses a readable selected-tab border and
  inverted `Ver` action.
- [x] The visible trend row uses a subtle selected-scope treatment without full
  green card backgrounds.
- [x] Unknown player gender keeps the three-card layout with `Categoria` and
  stable empty values.
- [x] Duplicate trend-window muting continues per scope.

## Validation

- [x] `pytest paddle/frontend/tests/test_players_pages.py -q`
- [x] `pytest paddle/frontend/tests/test_players_pages.py`
  `paddle/frontend/tests/test_ranking.py -q`
- [x] `markdownlint specs/043-player-efficiency-scope-wheels.md`
- [ ] `markdownlint CHANGELOG.md specs/043-player-efficiency-scope-wheels.md`
- [ ] Manually check zero-match, sparse-history, gender-scoped, mixed-scoped, and
  mobile player detail pages.
