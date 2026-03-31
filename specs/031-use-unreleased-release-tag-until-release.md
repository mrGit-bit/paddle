# Use Unreleased Release Tag Until Release

## Tracking

- Task ID: `use-unreleased-release-tag-until-release`
- Plan: `plans/2026-03-27_use-unreleased-release-tag-until-release.md`
- Release tag: `unreleased`

## Goal

- Stop guessing the next shipped version in loose spec/plan tracking.
- Keep loose non-release files on `unreleased` until `/prompts:release
  <version>` assigns the actual shipped `vX.Y.Z`.

## Scope

- In:
  - update governance/docs for the `unreleased` workflow
  - update release automation to stamp loose files during release
  - add focused regression tests
  - normalize current loose files to `unreleased`
- Out:
  - product code changes
  - workflow changes unrelated to release-tag stamping

## Files

- Allowed:
  - `AGENTS.md`
  - `docs/PROJECT_INSTRUCTIONS.md`
  - `README.md`
  - `RELEASE.md`
  - `CHANGELOG.md`
  - `.codex/commands/release.md`
  - `scripts/release_orchestrator.py`
  - `paddle/frontend/tests/test_release_orchestrator.py`
  - `specs/*.md`
  - `plans/*.md`
- Forbidden:
  - `paddle/**`
  - `.github/workflows/**`
  - `.codex/private/**`

## Acceptance

- [ ] Governance says loose non-release specs/plans default to `unreleased`.
- [ ] `/prompts:release <version>` stamps matched loose files to the shipped
      `vX.Y.Z` during release consolidation.
- [ ] Current loose active files no longer guess `v1.6.2`.

## Checks

- Read governance/release docs and confirm they describe the `unreleased`
  workflow consistently.
- Run the release-orchestrator test scope and confirm the new tagging behavior
  is covered.
- Confirm the current loose spec/plan files use `Release tag: unreleased`.
