# Use Unreleased Release Tag Until Release Plan

## Tracking

- Task ID: `use-unreleased-release-tag-until-release`
- Spec: `specs/031-use-unreleased-release-tag-until-release.md`
- Release tag: `unreleased`

## Summary

- Loose specs/plans currently guess the next release tag too early.
- The actual shipped version is only known when `/prompts:release <version>` is
  invoked.

## Scope

- In:
  - switch governance/docs to `Release tag: unreleased` for loose files
  - stamp the actual version during release consolidation
  - add regression tests
  - normalize current loose files
- Out:
  - product code
  - unrelated release-flow changes

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

## Plan

- [ ] Update governance and release docs for the `unreleased` rule.
- [ ] Update the orchestrator to treat `unreleased` as the pre-release state.
- [ ] Add targeted tests for retagging and source selection.
- [ ] Normalize the current loose files and validate.

## Acceptance

- [ ] Loose non-release specs/plans default to `unreleased`.
- [ ] The release command assigns the actual shipped `vX.Y.Z` during release.
- [ ] Current loose files no longer use guessed future versions.

## Validation

- `pytest paddle/frontend/tests/test_release_orchestrator.py -q`
- `markdownlint-cli2 --config /tmp/markdownlint-no-md013.json AGENTS.md docs/PROJECT_INSTRUCTIONS.md README.md RELEASE.md CHANGELOG.md .codex/commands/release.md specs/*.md plans/*.md`
- Manual checks:
  - governance/release docs describe `unreleased` consistently
  - loose active files now use `Release tag: unreleased`
