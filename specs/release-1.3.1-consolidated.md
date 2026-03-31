# Release 1.3.1 Consolidated Spec

## Release

- Tag: `1.3.1`
- Date: `2026-03-09`

## Sources

- `specs/001-004-refactoring-consolidated.md`
- `specs/005-release-prep-version-bump.md`
- `specs/006-release-notes-extraction-portability.md`
- `specs/008-branch-check-before-development.md`
- Legacy plan-only source: `plans/2026-03-01_player-insights-jugadores.md`

## Shipped Scope

- Player insights on player pages: trend, frequent partner, and top rival
  pairs.
- Refactoring tracks `001-004`: API removal, view modularization, ranking and
  queryset consolidation, and pytest DB-safety hardening.
- Release workflow fixes for prep staging and portable release-note extraction.
- Mandatory branch verification before implementation.

## Notes

- Includes a legacy plan-only player-insights track because no standalone spec
  exists for that shipped work.
