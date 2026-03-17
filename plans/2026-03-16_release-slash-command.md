# Release Slash Command Automation Plan

## Context

- The repository already has release workflows, release docs, and a manual
  local SSH workflow, but it does not have a repo-local slash command that can
  execute the full release cycle.
- Discovery list:
  - `RELEASE.md`
  - `.github/workflows/release-prep-no-ai.yml`
  - `.github/workflows/ci.yml`
  - `.github/workflows/release.yml`
  - `scripts/backmerge_main_to_develop.sh`

## Spec Reference

- `specs/022-release-slash-command.md`

## Objectives

- Add a repo-local `/release` command that automates the documented GitHub and
  SSH release flow for `X.Y.Z` and `vX.Y.Z`.
- Move SSH setup from a Windows-only local path to a documented repo-local
  config and ignored key layout.
- Produce deterministic release reports and post-release consolidation output.

## Scope

### In

- Slash command entrypoint
- Release orchestration script
- Repo-local SSH template and ignore rules
- Release docs and changelog updates
- Targeted tests for parsing, reporting, SSH validation, and consolidation

### Out

- Product behavior changes unrelated to release automation
- Tracking any real credential material in git
- Replacing existing release workflows with new CI architecture

## Risks

- GitHub CLI polling can be brittle if matching logic is vague.
  Mitigation: use exact titles, exact base/head branches, and explicit required
  check waiting through `gh pr checks --watch`.
- Release consolidation can capture the wrong artifacts.
  Mitigation: limit candidates to loose active spec/plan files and exclude
  consolidated release files plus `plans/TEMPLATE.md`.
- SSH setup can fail silently if the command falls back to user SSH config.
  Mitigation: always pass `ssh -F <repo-local-config>`.

## Files Allowed to Change

- `specs/022-release-slash-command.md`
- `plans/2026-03-16_release-slash-command.md`
- `.codex/commands/release.md`
- `.codex/templates/release_ssh_config.example`
- `.codex/private/release_ssh/.gitignore`
- `scripts/release_orchestrator.py`
- `scripts/backmerge_main_to_develop.sh`
- `paddle/frontend/tests/test_release_orchestrator.py`
- `RELEASE.md`
- `README.md`
- `CHANGELOG.md`
- `.gitignore`

## Files Forbidden to Change

- Real SSH keys
- Real SSH config
- Unrelated product files
- Deprecated DRF/API files

## Proposed Changes (Step-by-Step by File)

- `.codex/commands/release.md`
  - Change: Add the repository-local slash command entrypoint.
  - Why: Give Codex a stable `/release` command contract.
  - Notes: Keep it thin and delegate to the script.
- `scripts/release_orchestrator.py`
  - Change: Add the full release orchestration flow, reporting, approval gate,
    SSH handling, and consolidation helpers.
  - Why: Centralize the release automation in one deterministic script.
  - Notes: Keep helper functions unit-testable.
- `.codex/templates/release_ssh_config.example`
  - Change: Add a tracked SSH config example for `staging-update` and
    `prod-update`.
  - Why: Replace the Windows-only local config dependency.
  - Notes: Use repo-local key placeholders.
- `.codex/private/release_ssh/.gitignore`
  - Change: Keep the real SSH config and `.pem` files untracked.
  - Why: Enforce secret safety in the repo.
  - Notes: Leave the directory in place for local setup.
- `paddle/frontend/tests/test_release_orchestrator.py`
  - Change: Add focused tests for version parsing, SSH validation, reporting,
    and consolidation helpers.
  - Why: Cover the new automation logic without needing live GitHub or SSH.
  - Notes: Import the script with `importlib.util`.
- `RELEASE.md`
  - Change: Rewrite the release guide around the new `/release` flow and
    repo-local SSH setup.
  - Why: Keep release docs aligned with the implementation.
  - Notes: Keep references to the existing workflows and fallback scripts.
- `CHANGELOG.md`
  - Change: Add an `Unreleased` entry for the release automation command and
    repo-local SSH setup.
  - Why: Repository guidance and workflow behavior changed.
  - Notes: Use Keep a Changelog categories.

## Plan Steps (Execution Order)

- [ ] Create the approved spec and plan files in the repo.
- [ ] Add the repo-local `/release` command and orchestration script.
- [ ] Add repo-local SSH template and ignore rules.
- [ ] Add targeted tests for the new script helpers.
- [ ] Update release docs and changelog.
- [ ] Run the smallest relevant validation scope and review the diff.

## Acceptance Criteria (Testable)

- [ ] `/release` accepts `X.Y.Z` and `vX.Y.Z`.
- [ ] The script enforces clean synced `develop` before starting.
- [ ] The script uses existing workflows and waits for required PR checks.
- [ ] The script uses repo-local SSH config and fails clearly when assets are
      missing.
- [ ] The script pauses for explicit staging approval before production.
- [ ] The script can generate consolidated spec and plan markdown for a release.
- [ ] `RELEASE.md` documents the new command and setup accurately.

## Validation Commands

- `pytest paddle/frontend/tests/test_release_orchestrator.py -q`
- `python -m markdownlint-cli2 specs/022-release-slash-command.md plans/2026-03-16_release-slash-command.md RELEASE.md CHANGELOG.md README.md`

## Manual Functional Checks

1. Run `/release 1.6.0` and confirm the release-prep workflow dispatch starts.
2. Run `/release v1.6.0` and confirm the normalized release branch and PR title
   still use `v1.6.0`.
3. Run `/release 1.6.0` with missing repo-local SSH assets and confirm the
   command stops before deploy steps.
4. Decline the staging approval prompt and confirm the command reports a paused
   release after staging.
5. Complete a full release and confirm the report includes prep, promotion,
   deploy, back-merge, and consolidation.

## Execution Log

- 2026-03-16 00:00 UTC — Spec drafted inline for user review.
- 2026-03-16 00:00 UTC — Spec approved inline by the user.
- 2026-03-16 00:00 UTC — Plan drafted inline for user review.
- 2026-03-16 00:00 UTC — Plan approved inline by the user.
- 2026-03-16 00:00 UTC — Implementation started.

## Post-Mortem / Improvements

- Keep the slash command thin and test the script helpers directly.
- If GitHub polling proves too brittle in practice, add a dedicated helper
  around `gh` JSON responses rather than spreading matching logic.
