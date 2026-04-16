# Player Partner Card Records

Use for active SDD work only.

## Tracking

- Task ID: `player-partner-card-records`
- Status: `implemented`
- Release tag: `unreleased`

`approved` stays in place until the scoped work is finished and the
development cycle for this spec is being closed. Only then move the spec to
`implemented`.

## Summary

- Add each partner efficiency card's win and match record below the partner
  name on player detail pages.
- Keep the record prepared by backend context and rendered as compact display
  text.

## Scope

- In:
  - Player detail habitual-partner efficiency card context.
  - Partner card template rendering.
  - Focused tests and changelog entry.
- Out:
  - Partner ranking, efficiency, distribution, match query, model, migration,
    or JavaScript changes.
  - Placeholder card behavior changes beyond the planned alignment record.

## Files Allowed to Change

- `paddle/frontend/view_modules/players.py`
- `paddle/frontend/templates/frontend/player_detail.html`
- `paddle/frontend/tests/test_players_pages.py`
- `CHANGELOG.md`
- `specs/047-player-partner-card-records.md`

## Files Forbidden to Change

- Models, migrations, ranking services, JavaScript assets, and unrelated
  templates.

## Implementation Plan

- [x] Add backend-prepared record text to real partner efficiency card rows.
- [x] Render the record below each real partner name.
- [x] Update focused tests and changelog.

## Acceptance

- [x] Real partner cards show a compact record line such as `4🏆/5🏓` below
  the partner name.
- [x] The wins count uses existing wins with that partner and the matches count
  uses existing matches with that partner.
- [x] Placeholder `Sin datos` cards show `0🏆/0🏓` to keep progress wheels
  aligned with real partner cards.
- [x] Existing partner ordering, links, efficiency wheels, stacked progress
  bar, and `Otros` behavior remain unchanged.
- [x] No frontend business logic or JavaScript is added.

## Validation

- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `markdownlint CHANGELOG.md specs/047-player-partner-card-records.md`
- Manual check: two-partner and three-partner player detail pages.
- Manual check: mobile and desktop partner card readability.
