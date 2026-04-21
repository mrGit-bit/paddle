# Player Detail Section Cards

## Tracking

- Task ID: `player-detail-section-cards`
- Status: `implemented`
- Release tag: `v1.9.2`

## Summary

- Group player detail insight sections into the same shadowed card treatment
  used by match-history cards.
- Preserve existing player insight content, calculations, links, and chart
  behavior.

## Scope

- In:
  - Wrap `Rankings`, `Últimos partidos`, `Pareja habitual`, and
    `Parejas rivales frecuentes` in `card shadow` containers.
  - Keep the existing inner insight cards, progress bars, chart hook, and empty
    states unchanged.
  - Add focused template-rendering coverage and an Unreleased changelog entry.
- Out:
  - Backend calculations, JavaScript behavior, match-history card markup,
    database, API, or broad styling changes.

## Files Allowed to Change

- `CHANGELOG.md`
- `paddle/frontend/templates/frontend/player_detail.html`
- `paddle/frontend/tests/test_players_pages.py`
- `specs/053-player-detail-section-cards.md`

## Files Forbidden to Change

- Django model and migration files.
- Deprecated DRF/API files.
- Unrelated frontend templates, static assets, governance files, or release
  records.

## Implementation Plan

- [x] Wrap the four requested player detail sections with full-width
  `card shadow` containers.
- [x] Preserve all existing nested markup and data hooks inside those sections.
- [x] Add a rendering assertion for the four section-card wrappers.
- [x] Update `CHANGELOG.md` under `Unreleased`.

## Acceptance

- [x] The four requested section headings render inside shadowed cards.
- [x] The existing match-history cards still render through `_match_card.html`.
- [x] Existing ranking, recent-form, partner, and rival content remains visible.
- [x] No backend, JavaScript, API, or database behavior changes are introduced.

## Validation

- [x] `pytest paddle/frontend/tests/test_players_pages.py -q`
- [x] `markdownlint --disable MD013 -- CHANGELOG.md specs/053-player-detail-section-cards.md`
- [ ] Manual check: player detail page shows each requested insight section inside
  a shadowed card.
- [ ] Manual check: `Partidos jugados` match cards retain their existing layout.
