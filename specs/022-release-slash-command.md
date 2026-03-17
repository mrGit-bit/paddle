# Release Slash Command Automation

## Functional Goal

Create a repository-local Codex slash command `/release` that accepts a single
version parameter in either `X.Y.Z` or `vX.Y.Z` form and automates the
documented release flow currently described in `RELEASE.md`, including GitHub
workflow dispatch, PR creation and merge, staging and production deployment
handoff through repo-local SSH configuration, post-release consolidation, and a
final human-readable report.

## Scope

### In

- Add a repository-local Codex slash command with canonical name `/release`.
- Accept version input as `X.Y.Z` or `vX.Y.Z`.
- Enforce release preflight checks on `develop`, clean git state, and
  synchronization with `origin/develop`.
- Trigger `.github/workflows/release-prep-no-ai.yml`.
- Auto-merge the release prep PR with squash merge and delete the release
  branch.
- Create and merge `develop -> staging` after required CI checks pass.
- Deploy staging through repo-local SSH config and `staging-update`.
- Pause for explicit user approval after printing staging manual checks.
- Create and merge `staging -> main` after required CI checks pass.
- Deploy production through repo-local SSH config and `prod-update`.
- Back-merge `origin/main` into local `develop`.
- Perform post-release spec and plan consolidation for the released deployment.
- Produce a human-readable release report.
- Update repository docs to explain the command and repo-local SSH setup.

### Out

- Tracking real SSH private keys or real SSH config files in git.
- Replacing the existing GitHub workflows with a different release system.
- Automating the manual staging checks themselves.
- Product behavior changes unrelated to release automation.

## UI / UX Requirements

- The command is invoked as `/release 1.6.0` or `/release v1.6.0`.
- User-facing output stays concise and action-oriented.
- The staging gate is interactive and requires explicit approval before the
  production promotion starts.
- Failures identify the blocking step and the remediation needed.

## Backend / Automation Requirements

- Use a repo-local slash command entrypoint that delegates to one checked-in
  orchestration script.
- Reuse existing workflows:
  - `.github/workflows/release-prep-no-ai.yml`
  - `.github/workflows/ci.yml`
  - `.github/workflows/release.yml`
- Reuse `scripts/backmerge_main_to_develop.sh` where practical.
- Validate required tools and credentials before any remote deploy step:
  - `gh`
  - `ssh`
  - authenticated GitHub CLI session
  - repo-local SSH config
  - repo-local `.pem` files
- Stop immediately on workflow, check, merge, SSH, or back-merge failures while
  preserving a final report of completed and failed steps.

## Data / Config Rules

- Store a tracked SSH config example in the repo.
- Store the real SSH config and `.pem` files only under a repo-local ignored
  private path.
- Use explicit repo-local SSH config with `ssh -F <repo-local-config>`.
- Never print secret material in command output.

## Reuse Rules

- Keep execution logic in the orchestration script, not in `RELEASE.md`.
- Reuse existing workflows and release scripts instead of duplicating them.
- Keep the slash command entrypoint thin.

## Acceptance Criteria

1. `/release X.Y.Z` dispatches `release-prep-no-ai.yml` with the expected
   inputs from clean synced `develop`.
2. The automation finds, checks, squash-merges, and deletes the release prep
   branch `chore/release-vX.Y.Z`.
3. The automation creates and merges `develop -> staging` only after CI passes.
4. Staging deployment uses repo-local SSH configuration instead of a user-level
   Windows SSH config.
5. The command prints release-specific staging checks and pauses for approval.
6. After approval, the automation creates and merges `staging -> main`,
   deploys production, and back-merges `origin/main` into local `develop`.
7. The release run writes consolidated spec and plan artifacts for the released
   deployment.
8. Real SSH keys and real SSH config remain untracked.
9. `RELEASE.md` documents the new command-based flow and repo-local SSH setup.

## Manual Functional Checks

1. Run `/release 1.6.0` and confirm the command normalizes the version and
   dispatches the release prep workflow.
2. Run `/release v1.6.0` and confirm it behaves identically to `1.6.0`.
3. Run the command with a dirty worktree and confirm it aborts before any
   workflow or SSH action.
4. Run the command with missing repo-local SSH assets and confirm it fails with
   setup guidance without exposing secrets.
5. Decline the staging approval prompt and confirm production steps do not run.
6. Complete a happy-path release and confirm the final report covers prep, PR
   merges, deploys, back-merge, and consolidation.

## Allowed Files

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

## Forbidden Files

- Real SSH key files
- Real SSH config files
- Product app code unrelated to release automation
- Deprecated DRF/API files
