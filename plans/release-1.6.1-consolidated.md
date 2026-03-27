# Release 1.6.1 Consolidated Plan

## Release

- Tag: `1.6.1`
- Date: `2026-03-27`

## Sources

- `plans/2026-03-16_release-slash-command.md`
- `plans/2026-03-17_governance-review-and-plan-input.md`
- `plans/2026-03-17_governance-audit-report-export.md`
- `plans/2026-03-17_apply-accepted-governance-audit-fixes.md`
- `plans/2026-03-26_stabilize-release-orchestrator-github-flow.md`
- `plans/2026-03-26_operationalize-remaining-governance-coordination-gaps.md`
- `plans/2026-03-26_harden-release-ssh-key-permissions.md`

## Execution Summary

- Added the release command/orchestrator, repo-local SSH setup, and release
  docs.
- Added governance review strategy, audit export, and explicit tracking
  metadata.
- Hardened the release orchestrator for GitHub auth fallback, workflow
  matching, required-check handling, release provenance, and SSH key
  permissions.

## Validation Summary

- Release-orchestrator behavior was covered by targeted pytest scope.
- Governance/history changes were checked through scoped Markdown review.
