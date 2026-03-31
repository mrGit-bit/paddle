# Show Top 3 Player Partners

## Tracking

- Task ID: `show-top-3-player-partners`
- Plan: `plans/2026-03-29_show-top-3-player-partners.md`
- Release tag: `unreleased`

## Goal

- Show the top 3 habitual partners on the player detail page instead of a
  single partner row.
- Keep the existing partner ordering rules so the most-played partners appear
  first.

## Scope

- In:
  - expose the top 3 partner rows from player insights
  - render up to 3 clickable partner rows in `Pareja habitual`
  - preserve the current empty state when there are no partners
  - update focused player-detail tests
  - update the unreleased changelog entry
- Out:
  - changing partner ranking tie-break rules
  - changing rival or trend insights
  - changing layout or styling beyond what is required for the extra rows

## Files

- Allowed:
  - `paddle/frontend/view_modules/players.py`
  - `paddle/frontend/templates/frontend/player_detail.html`
  - `paddle/frontend/tests/test_players_pages.py`
  - `CHANGELOG.md`
- Forbidden:
  - `paddle/frontend/services/**`
  - `paddle/games/**`
  - `paddle/americano/**`
  - `.github/workflows/**`

## Acceptance

- [ ] `Pareja habitual` renders up to 3 partner rows ordered by matches
      together, then the existing tie-breakers.
- [ ] The table keeps clickable links for each rendered partner row.
- [ ] The page still shows `Sin datos` when the player has no partner rows.

## Checks

- Render a player detail page with 3+ partners and confirm the table shows the
  top 3 in order.
- Render a player detail page with fewer than 3 partners and confirm only real
  rows are shown.
