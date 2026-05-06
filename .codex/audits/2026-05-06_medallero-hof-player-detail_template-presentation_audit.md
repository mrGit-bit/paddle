# Template Presentation Audit Report

## Summary

- Scope: Cross-template presentation coherence for Medallero collapsed and
  expanded cards, Hall of Fame ranking tables, and player-detail metric cards.
- Audited target: `paddle/frontend/templates/frontend/medallero.html`,
  `paddle/frontend/templates/frontend/hall_of_fame.html`, and
  `paddle/frontend/templates/frontend/player_detail.html`.
- Audit date: 2026-05-06
- Reviewer: Codex
- Verification: Source cascade tracing across the target templates, included
  partials, `base.html`, and `paddle/frontend/static/frontend/css/styles.css`.
  Browser computed-style verification was not run.

## Presentation Findings

### Finding TPA-001

- Status: pending
- Type: Possible risk
- Severity: medium
- Location: `paddle/frontend/templates/frontend/medallero.html` lines 43-49;
  `paddle/frontend/templates/frontend/player_detail.html` lines 63-94;
  `paddle/frontend/static/frontend/css/styles.css` lines 387-395 and 878-886.
- Evidence: Player detail renders the compact three-column trend cards inside
  rows carrying `player-trend-cards`, so the tiny-phone media rule reduces
  Bootstrap gutters at widths below 360 px. Medallero expanded medal cards reuse
  `player-trend-card` and the same `col-4` grid shape, but the row only has
  `row g-2 mb-2`. Its card body receives the tiny-phone padding reduction from
  `.player-trend-card .card-body`, while the row gutter remains at `g-2`.
  Medallero also keeps a fixed 3 rem large medal icon. That creates a responsive
  mismatch versus equivalent player-detail card grids and increases the chance
  of cramped or clipped medal cards on very narrow screens.
- Root cause: Markup variant. Medallero reuses the shared card class but not the
  shared responsive grid container class that accompanies that component in
  player detail.
- Recommended minimal fix: Add `player-trend-cards` to the Medallero expanded
  medal grid rows, or add an equally narrow `.medallero-medal-grid .row` media
  rule beside the Medallero CSS. Prefer the shared class if the intended gutter
  behavior should match player-detail trend cards.
- Tests or manual checks: Add a rendered-template assertion that Medallero medal
  rows include the chosen responsive grid class, then manually check a narrow
  mobile viewport around 320-360 px with a full three-medal row.
- Discard explanation:

## Residual Risk

- Browser computed-style verification was not run, so layout risk is based on
  source cascade tracing rather than measured rendered dimensions.
- Hall of Fame table and player-detail card interactions were reviewed for
  same-page class coherence, but no screenshots were captured for visual
  comparison across breakpoints.

## Open Questions

- None.
