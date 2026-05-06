# Release Process

This repository uses a command-first release flow through
`python scripts/release_orchestrator.py <version>`.

## Command

- Primary command: `python scripts/release_orchestrator.py`
- Argument: `x.y.z` or `vx.y.z`
- Resume after staging checks:
  `python scripts/release_orchestrator.py <version> --resume-from staging-approval --staging-approved`
- Record a paused stop after staging checks:
  `python scripts/release_orchestrator.py <version> --resume-from staging-approval --staging-declined`
- Examples:
  - `python scripts/release_orchestrator.py 1.6.0`
  - `python scripts/release_orchestrator.py v1.6.0`

Current Codex CLI behavior in this repository:

- The direct script is the primary supported entrypoint and should be used for
  normal release work.
- The working custom-prompt discovery path is
  `~/.codex/prompts/release.md`.
- Bare `/release` is not a supported registration target in the current
  `codex-cli 0.117.0` environment. Custom prompts are invoked through the
  `/prompts:` namespace, so the optional wrapper command is
  `/prompts:release`.
- The checked-in file `.codex/commands/release.md` is a repository copy of the
  prompt content, but current Codex CLI builds in this environment do not
  auto-discover it as a repo-local slash command.

Both entrypoints call the same orchestrator.

## Custom Prompt Setup

This setup is optional. Use it only if you want the slash-command wrapper in
addition to the direct script.

1. Create the user prompt directory if it does not exist:
   `mkdir -p ~/.codex/prompts`
2. Copy the checked-in prompt content to the user-level discovery path:
   `cp .codex/commands/release.md ~/.codex/prompts/release.md`
3. Start a fresh Codex session in the repository.
4. Run `/prompts:release <version>`, for example `1.6.0` or `v1.6.0`.

If Codex does not recognize `/prompts:release`, use the primary command
instead: `python scripts/release_orchestrator.py 1.6.0`.

## Prerequisites

- Current branch is `develop`.
- `git status --short` is clean.
- Local `develop` is synchronized with `origin/develop`.
- Loose spec files being shipped in the release are already marked with
  `Status: \`implemented\`` or `Status: \`shipped\``.
- Loose spec files being shipped in the release are already marked with
  `Release tag: \`vX.Y.Z\`` matching the requested version.
- Unrelated in-progress loose spec files remain on
  `Status: \`approved\`` with `Release tag: \`unreleased\`` and are not
  touched by consolidation.
- `gh` is installed and authenticated.
- `ssh` is installed.
- Repo-local SSH config exists at `.codex/private/release_ssh/config`.
- Repo-local staging key exists at
  `.codex/private/release_ssh/staging-oracle-key.pem`.
- Repo-local production key exists at
  `.codex/private/release_ssh/production-oracle-key.pem`.
- Repo-local private keys must be owner-only files. `0600` is the expected
  mode, and the orchestrator repairs unsafe group/world-readable modes to
  `0600` before deployment when it can.
- If the release changes Django models, the deploy steps for staging and
  production must run the corresponding migrations before final verification.

## GitHub CLI Authentication in Codespaces

Creating a GitHub token is not sufficient by itself. The token must be
available to `gh` inside the active Codespace where the release command runs.

Preferred setup:

1. Store the token as a GitHub Codespaces secret named `GH_TOKEN`.
2. Restart the Codespace so the secret is available in the terminal session.
3. Verify the session before running the release command:
   - `gh auth status`
   - `gh repo view`
   - `gh workflow list`
4. If git HTTPS operations also need the same GitHub CLI session, run
   `gh auth setup-git`.

Current orchestrator behavior:

- If `GH_TOKEN` or `GITHUB_TOKEN` are present but invalid, the orchestrator
  retries `gh` commands without those env-token overrides and uses the stored
  `gh` login if it is valid.
- This fallback only applies inside the orchestrator. Plain shell `gh`
  commands in the same Codespace will still fail until the bad env vars are
  corrected or removed.

Do not commit tokens or paste secret values into tracked repository files.

## Repo-local SSH Setup

1. Copy `.codex/templates/release_ssh_config.example` to
   `.codex/private/release_ssh/config`.
2. Copy the real staging key to
   `.codex/private/release_ssh/staging-oracle-key.pem`.
3. Copy the real production key to
   `.codex/private/release_ssh/production-oracle-key.pem`.
4. Set owner-only permissions on both key files:
   `chmod 600 .codex/private/release_ssh/staging-oracle-key.pem .codex/private/release_ssh/production-oracle-key.pem`
5. Keep those files untracked. The repository ignores the config and `.pem`
   files automatically.

The command always uses `ssh -F .codex/private/release_ssh/config`.
Keep `staging-update` and `prod-update` non-interactive so the SSH command
returns to the orchestrator after `./deploy_update.sh` finishes.
Keep the checked-in [deploy_update.sh](/workspaces/paddle/deploy_update.sh)
aligned with the host copy so release automation has one reviewable source of
truth for the remote deploy steps.

## GitHub Actions Used

- `.github/workflows/release-prep-no-ai.yml`: manual dispatch workflow used to
  prepare `CHANGELOG.md` and `paddle/config/__init__.py`, create
  `chore/release-vX.Y.Z`, and open the release-prep PR.
- `.github/workflows/ci.yml`: required PR checks for `develop`, `staging`, and
  `main` promotions.
- `.github/workflows/release.yml`: runs on `main` after production promotion,
  creates or confirms the release tag and GitHub Release, and may open the
  `main -> develop` back-merge PR.

## Automated Flow

1. Validate branch, clean git state, sync state, GitHub auth, and repo-local
   SSH assets, and normalize unsafe private-key modes before deployment.
2. Dispatch `Release Prep (no-AI)` for `X.Y.Z` from `develop`.
3. Wait for the workflow run and locate PR
   `version(release): prepare release vX.Y.Z`.
4. Wait for required checks when they exist, otherwise fall back to visible PR
   checks, squash-merge the release-prep PR, and delete
   `chore/release-vX.Y.Z`.
5. Pull the merged release-prep changes onto local `develop`, then run the
   local CI-equivalent pytest and coverage commands for `frontend` and
   `americano`. If either command fails, stop the release before opening the
   promotion PR.
6. Create PR `develop -> staging`, wait for required or visible PR checks
   from `.github/workflows/ci.yml`, and merge it.
7. Deploy staging with `ssh -F .codex/private/release_ssh/config
   staging-update`, then have the orchestrator run `python manage.py migrate
   --settings=config.settings.prod` on the staging host and fail if any
   migrations remain pending; only then verify the remote host reports
   `paddle/config/__init__.py` at `X.Y.Z`.
8. Print 3-6 manual functional checks for staging and wait for explicit user
   approval.
9. If approved, create PR `staging -> main`, wait for required or visible CI,
   and merge it.
10. Deploy production with `ssh -F .codex/private/release_ssh/config
   prod-update`, then have the orchestrator run `python manage.py migrate
   --settings=config.settings.prod` on the production host and fail if any
   migrations remain pending; only then verify the remote host reports
   `paddle/config/__init__.py` at `X.Y.Z`.
11. Back-merge `origin/main` into local `develop` with an unsigned merge
    commit so local GPG configuration cannot block the release.
12. Consolidate only the loose spec files explicitly marked with
    `Release tag: vX.Y.Z` and a closure-complete `Status`
    (`implemented` or `shipped`) into `specs/release-X.Y.Z-consolidated.md`.
13. Review `CHANGELOG.md` for `## [X.Y.Z]` using the shipped specs, existing
    changelog notes, and any available completed backlog wording, then keep
    the section as compact grouped category summaries.
14. Print a human-readable release report.

If the user declines at the staging gate, the command stops after staging and
reports the paused state.

If the command reaches staging in a non-interactive session, it now prints the
manual checks and exits with resume guidance instead of crashing on `input()`.
After the checks are complete, resume with:

- `python scripts/release_orchestrator.py <version> --resume-from staging-approval --staging-approved`

If staging is not approved, record the pause cleanly with:

- `python scripts/release_orchestrator.py <version> --resume-from staging-approval --staging-declined`

If a remote deploy command returns but the host still reports the wrong app
version, the orchestrator aborts instead of continuing to the next release
step.

Backlog reconciliation is owned by development-cycle closure. Release
consolidation only uses completed backlog wording as release-summary source
material when that wording is still available.

If a planned version never reaches production, do not keep a synthetic release
record for it. Fold its unshipped specs and changelog notes into the next
production release that actually ships that work.

Loose active specs should default to `Status: approved` plus
`Release tag: unreleased` during development. Once the scoped development
cycle is closed, move the loose spec to `Status: implemented`. Before running
the release flow, mark only the actually shipped loose files with the
requested `vX.Y.Z`. During release consolidation, the command selects only
loose specs whose `Release tag` matches and whose `Status` is already
closure-complete (`implemented` or `shipped`). Also review the release
changelog section and compress repetitive same-category bullets into grouped
outcome summaries so release history stays easy to scan.

## Manual Functional Checks

The command now prints two different release-specific checklists:

- `Develop manual checks`: logic-oriented checks printed before the local
  CI-equivalent pytest+coverage gate. These focus on business rules, data
  integrity, scope isolation, permissions, and release-specific logic.
- `Staging manual checks`: UI-oriented checks printed after staging deploy.
  These focus on visible flows, pagination, rendered states, and release-
  specific UI verification.

Baseline staging checks:

1. Sign in and sign out without visible UI errors.
2. Open rankings and confirm pagination and rendering behave correctly.
3. Open the match list and confirm cards, actions, and states display
   correctly.
4. Create a match and confirm the interface reflects the change correctly.
5. Open Americano and confirm the view loads and renders correctly.
6. Validate the release-specific UI changes. If the release has no UI/UX
   changes, state `No UI/UX changes in this release.`

## Fallback Scripts

- `scripts/backmerge_main_to_develop.sh <version>`: manual fallback for the
  local back-merge if the automated flow stops after production.
- `scripts/tag_release.sh <version> "<summary>"`: manual fallback only when
  `.github/workflows/release.yml` is intentionally bypassed or needs recovery.
