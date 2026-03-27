# Clear Remaining Loose Specs and Plans Plan

## Tracking

- Task ID: `clear-remaining-loose-specs-and-plans`
- Spec: `specs/029-clear-remaining-loose-specs-and-plans.md`
- Release tag: `v1.6.2`

## Summary

- Loose historical spec/plan files remained after release consolidation.
- Some files still pointed at draft `v1.6.0` even though the work shipped in
  `1.6.1`.

## Scope

- In:
  - map loose historical files to the shipped production release
  - update/create the matching consolidated files
  - rewrite the affected changelog slice
  - remove absorbed loose files
  - update governance docs for non-shipped release rollover
- Out:
  - product code
  - workflows
  - private files

## Files

- Allowed:
  - `specs/*.md`
  - `plans/*.md`
  - `README.md`
  - `AGENTS.md`
  - `docs/PROJECT_INSTRUCTIONS.md`
  - `RELEASE.md`
  - `CHANGELOG.md`
- Forbidden:
  - `paddle/**`
  - `.github/workflows/**`
  - `.codex/private/**`

## Plan

- [ ] Map loose historical files to shipped releases.
- [ ] Update the consolidated spec files.
- [ ] Update the consolidated plan files.
- [ ] Correct `CHANGELOG.md` and remove absorbed loose files.
- [ ] Update governance/release docs and validate Markdown.

## Acceptance

- [ ] No loose released spec files remain in scope.
- [ ] No loose released plan files remain in scope.
- [ ] `1.6.0` is removed as a shipped release.
- [ ] Governance documents the rollover rule.

## Validation

- `ls -1 specs`
- `ls -1 plans`
- `markdownlint-cli2 --config /tmp/markdownlint-no-md013.json README.md AGENTS.md docs/PROJECT_INSTRUCTIONS.md RELEASE.md CHANGELOG.md specs/*.md plans/*.md`
- Manual checks:
  - `release-1.6.1` contains the former `v1.6.0` sources.
  - `CHANGELOG.md` has no `1.6.0` release header.
  - Removed loose historical files are gone from `specs/` and `plans/`.
