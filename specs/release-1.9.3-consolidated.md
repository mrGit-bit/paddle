# Release 1.9.3 Consolidated Spec

Status: shipped
Release tag: v1.9.3

## Shipped Scope

- Added player detail `Contendientes` cards for individual head-to-head
  nemesis and victim ratios.
- Reused existing player-detail card, swatch, record-label, and circular
  progress presentation patterns.
- Prevented inactive efficiency selector cards from activating or changing the
  visible trend row.
- Aligned template presentation audit guidance with the repository audit
  lifecycle and focused audit routing.

## Source Specs

- `specs/054-player-detail-contendientes-cards.md`

## Validation

- Frontend release validation passed with coverage above the release gate.
- Americano release validation passed with coverage above the release gate.
- Staging and production deployed `1.9.3` and reported no pending migrations.
