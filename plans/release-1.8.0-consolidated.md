# Release 1.8.0 Consolidated Plan

## Release

- Tag: `1.8.0`
- Date: `2026-04-01`

## Sources

- `plans/2026-03-31_harden-release-remote-deploy-verification.md`
- `plans/2026-04-01_pairs-ranking-page.md`

## Execution Summary

- Hardened the tracked release tooling around remote deploy verification and
  removed the interactive-shell behavior from the tracked SSH update aliases.
- Implemented the public pairs-ranking flow, its pair-table rendering, and the
  related player-page rival-pair presentation updates.

## Validation Summary

- Release-tooling work was covered by the focused release-orchestrator pytest
  scope plus SSH-template and release-doc review.
- Product work was covered by focused Django/pytest scopes for rankings, views,
  and player pages.
