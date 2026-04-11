# Release 1.8.0 Consolidated Spec

## Release

- Tag: `1.8.0`
- Date: `2026-04-01`

## Sources

- `specs/035-harden-release-remote-deploy-verification.md`
- `specs/036-pairs-ranking-page.md`

## Shipped Scope

- Hardened the tracked release flow so staging and production deploys verify
  the requested remote app version and the tracked SSH update aliases remain
  non-interactive.
- Added the public `Parejas` ranking page, stacked pair-name cells, and the
  related stacked rival-pair rendering on player detail pages.

## Notes

- `1.8.1` later adjusted the minimum-match threshold for the rate-based pairs
  tables as follow-up work after this shipped task first reached production.
