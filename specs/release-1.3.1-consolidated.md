# Release 1.3.1 Consolidated Spec

## Release

- Release tag: `1.3.1`
- Release date: `2026-03-09`
- Consolidation status: post-release back-merge complete

## Source Provenance

- `specs/001-004-refactoring-consolidated.md`
- `specs/005-release-prep-version-bump.md`
- `specs/006-release-notes-extraction-portability.md`
- `specs/008-branch-check-before-development.md`
- Legacy plan-only track carried into this release:
  - `plans/2026-03-01_player-insights-jugadores.md`

## Functional Goal

Preserve the approved SDD scope for the `1.3.1` deployment in one release-level
spec after release completion, covering player insights, refactoring tracks
001-004, release-prep workflow staging, release-note extraction portability,
and the mandatory branch-check governance rule.

## Release Scope Summary

### Product and Refactoring Tracks

- Add player insights on player detail pages with trend, frequent partner, and
  top rival pairs.
- Preserve the completed refactoring tracks grouped in the original
  `001-004` consolidated spec:
  - remove deprecated DRF/API runtime surface
  - modularize frontend views while preserving the external route surface
  - centralize ranking policy and shared queryset helpers
  - harden pytest database safety and related developer workflow protections

### Release Automation and Governance Tracks

- Ensure release-prep commits include both `CHANGELOG.md` and
  `paddle/config/__init__.py`.
- Ensure release-note extraction in `.github/workflows/release.yml` is portable
  in GitHub Actions.
- Require a mandatory branch check before implementation when work does not
  start from `develop`.

## Acceptance Criteria Summary

1. Player detail pages expose the released insights blocks and related tests
   cover the expected edge cases.
2. Refactoring tracks `001-004` remain preserved as completed implementation
   tracks with their approved behavior and documentation outcomes.
3. Release-prep workflow staging includes both release files when changed.
4. Release-note extraction no longer fails with the `awk` parser issue and
   keeps its idempotent behavior.
5. Governance explicitly requires checking the active branch before
   implementation and asking the user when it is not `develop`.

## Manual Functional Checks Summary

1. Open a player detail page and verify trend, frequent partner, and rival-pair
   insights render correctly.
2. Confirm deprecated API routes are no longer part of the active application
   surface and the web routes still behave correctly.
3. Verify the release-prep workflow change records both `CHANGELOG.md` and the
   runtime version file in the release commit.
4. Verify the release workflow can extract release notes for `1.3.1` without
   the previous parser failure.
5. Confirm governance docs require a branch check before implementation work.

## Notes

- This consolidated spec intentionally preserves the legacy plan-only player
  insights track because no separate spec file for that released work exists in
  the repository.
- Unreleased or later release work is not part of this consolidated artifact.
