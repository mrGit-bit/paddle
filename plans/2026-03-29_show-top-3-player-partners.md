# Show Top 3 Player Partners Plan

## Tracking

- Task ID: `show-top-3-player-partners`
- Spec: `specs/034-show-top-3-player-partners.md`
- Release tag: `unreleased`

## Summary

- Player detail insights already compute and sort all partner rows.
- The page currently truncates that data to one `top_partner` row.

## Scope

- In:
  - return the top 3 sorted partner rows from player insights
  - update the player detail template to render those rows
  - adapt focused player-detail tests to the new payload and HTML
  - update the unreleased changelog entry
- Out:
  - tie-breaker changes
  - rival table changes
  - broader player-page refactors

## Files Allowed to Change

- `paddle/frontend/view_modules/players.py`
- `paddle/frontend/templates/frontend/player_detail.html`
- `paddle/frontend/tests/test_players_pages.py`
- `CHANGELOG.md`

## Files Forbidden to Change

- `paddle/frontend/services/**`
- `paddle/games/**`
- `paddle/americano/**`
- `.github/workflows/**`

## Plan

- [ ] Replace the single `top_partner` payload with a `top_partners[:3]`
      payload while preserving current sort behavior.
- [ ] Update the habitual-partner table to loop over the returned partner rows
      and keep the existing empty state.
- [ ] Update focused player-detail tests and changelog text.

## Acceptance

- [ ] The player detail view returns and renders up to 3 habitual partners.
- [ ] Partners remain ordered by matches together and current tie-breakers.
- [ ] The page still renders `Sin datos` when there are no partner rows.

## Validation

- `pytest paddle/frontend/tests/test_players_pages.py -q`
- Manual checks:
  - open a player with at least 3 partners and confirm the table shows the top
    3 rows in order
  - open a player with 1 or 2 partners and confirm no placeholder rows appear
  - open a player with no matches and confirm `Sin datos` still shows
