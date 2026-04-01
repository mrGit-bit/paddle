# Release 1.7.0 Consolidated Plan

## Release

- Tag: `1.7.0`
- Date: `2026-03-31`

## Sources

- `plans/2026-03-27_clear-remaining-loose-specs-and-plans.md`
- `plans/2026-03-27_reduce-markdown-verbosity-across-governance-and-history.md`
- `plans/2026-03-27_use-unreleased-release-tag-until-release.md`
- `plans/2026-03-29_enforce-match-expiry-window.md`
- `plans/2026-03-29_add-ranking-page-local-sorting.md`
- `plans/2026-03-29_show-top-3-player-partners.md`

## Execution Summary

- Updated governance and release history to keep loose active-work files on
  `unreleased` until the shipped release is known and to reduce low-value
  Markdown verbosity.
- Consolidated the remaining loose historical files from prior shipped work
  into release-level records.
- Implemented the shipped product changes for match expiry enforcement,
  ranking-page local sorting, and top 3 habitual partners.

## Validation Summary

- Product changes were covered by focused Django/pytest scopes for rankings,
  player pages, and release-orchestrator behavior.
- Governance and release-history updates were checked through scoped Markdown
  review and release-flow execution.
