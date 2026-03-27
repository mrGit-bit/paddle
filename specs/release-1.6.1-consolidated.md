# Release 1.6.1 Consolidated Spec

## Release

- Tag: `1.6.1`
- Date: `2026-03-27`

## Sources

- `specs/022-release-slash-command.md`
- `specs/023-governance-review-and-plan-input.md`
- `specs/024-governance-audit-report-export.md`
- `specs/025-apply-accepted-governance-audit-fixes.md`
- `specs/026-stabilize-release-orchestrator-github-flow.md`
- `specs/027-operationalize-remaining-governance-coordination-gaps.md`
- `specs/028-harden-release-ssh-key-permissions.md`

## Shipped Scope

- Added `/prompts:release`, repo-local SSH release setup, and command-first
  release guidance.
- Added governance review/audit workflow clarifications, audit export support,
  and explicit task/release tracking metadata.
- Hardened the release orchestrator for GitHub auth fallback, workflow
  matching, required-check handling, release provenance, and shared SSH key
  permissions.

## Notes

- Source files originally drafted for non-shipped `v1.6.0` are recorded here
  because the work first shipped in `1.6.1`.
