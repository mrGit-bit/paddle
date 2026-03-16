# Release 1.3.1 Consolidated Plan

## Release

- Release tag: `1.3.1`
- Release date: `2026-03-09`
- Consolidation status: post-release back-merge complete

## Source Provenance

- `plans/2026-03-01_player-insights-jugadores.md`
- `plans/2026-03-03_refactoring-001-004-consolidated.md`
- `plans/2026-03-05_release-prep-version-bump.md`
- `plans/2026-03-09_branch-check-before-development.md`
- `plans/2026-03-09_release-notes-extraction-portability.md`

## Objectives Summary

- Ship player insights on player detail pages.
- Preserve the completed `001-004` refactoring execution tracks.
- Fix release-prep workflow staging for runtime version bumps.
- Fix release-note extraction portability in the release workflow.
- Add mandatory branch-check governance before implementation.

## Execution Summary

### Player Insights

- Added a backend-computed player-insights section between ranking and played
  matches on player detail pages.
- Reused shared match-query helpers and targeted frontend tests.

### Refactoring Tracks 001-004

- Completed the grouped refactoring tracks already captured in the original
  consolidated plan, including API removal, view modularization, ranking-policy
  consolidation, and pytest database-safety hardening.

### Release Automation and Governance

- Updated release-prep staging so release commits capture both release files.
- Replaced the failing release-note extraction logic with a portable approach.
- Added mandatory pre-implementation branch verification in governance docs.

## Validation Summary

- Player-insight behavior was covered through targeted frontend test scope.
- Refactoring tracks `001-004` were already recorded as completed with passing
  targeted validation in the original consolidated plan.
- Workflow changes were validated through YAML and diff-focused checks.
- Governance updates were validated through Markdown review and alignment checks.

## Manual Functional Checks Summary

1. Open a player detail page and verify the released insights blocks render with
   the expected tables and ordering.
2. Confirm refactored routes still behave as expected without the removed API
   surface.
3. Verify the release-prep workflow would stage both `CHANGELOG.md` and the
   runtime version file.
4. Verify the release workflow can extract notes for a release section without
   the previous parser failure.
5. Confirm governance requires branch verification before implementation work.

## Execution Log Summary

- 2026-03-01 to 2026-03-09 — Player insights, refactoring tracks, release
  automation fixes, and branch-check governance were planned and completed
  across the source plan files listed above.

## Notes

- This consolidated plan preserves the legacy player-insights plan even though a
  separate spec file for that released work is not present in the repository.
