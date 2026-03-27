# Release Process

This repository supports a command-first release flow through a user-level
Codex custom prompt invoked as `/prompts:release` when it is installed in the
current Codespace.

## Command

- Command: `/prompts:release`
- Version argument examples:
  - `/prompts:release 1.6.0`
  - `/prompts:release v1.6.0`

Current Codex CLI behavior in this repository:

- The working custom-prompt discovery path is
  `~/.codex/prompts/release.md`.
- The checked-in file `.codex/commands/release.md` is a repository copy of the
  prompt content, but current Codex CLI builds in this environment do not
  auto-discover it as a repo-local slash command.
- If the user-level prompt is not installed, run the orchestrator directly:
  `python scripts/release_orchestrator.py <version>`.

Whether invoked through the user-level `/prompts:release` custom prompt or the
direct Python entrypoint, the same orchestrator automates the GitHub workflow,
branch promotion, deployment, back-merge, and post-release consolidation steps
described below.

## Custom Prompt Setup

1. Create the user prompt directory if it does not exist:
   `mkdir -p ~/.codex/prompts`
2. Copy the checked-in prompt content to the user-level discovery path:
   `cp .codex/commands/release.md ~/.codex/prompts/release.md`
3. Start a fresh Codex session in the repository.
4. Run the command `/prompts:release` with one version argument, for example
   `1.6.0` or `v1.6.0`.

If Codex still does not recognize `/prompts:release`, use the direct script
fallback: `python scripts/release_orchestrator.py 1.6.0`.

## Prerequisites

- Current branch is `develop`.
- `git status --short` is clean.
- Local `develop` is synchronized with `origin/develop`.
- Every loose non-release spec/plan intended for the release is marked with
  `Release tag: \`vX.Y.Z\`` matching the requested version.
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

The command always uses `ssh -F .codex/private/release_ssh/config` and never
depends on a Windows user profile SSH config.

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
4. Wait for required checks when they exist, squash-merge the release-prep PR,
   and delete `chore/release-vX.Y.Z`.
5. Create PR `develop -> staging`, wait for required checks from
   `.github/workflows/ci.yml`, and merge it.
6. Deploy staging with `ssh -F .codex/private/release_ssh/config
   staging-update`.
7. Print 3-6 manual functional checks for staging and wait for explicit user
   approval.
8. If approved, create PR `staging -> main`, wait for CI, and merge it.
9. Deploy production with `ssh -F .codex/private/release_ssh/config
   prod-update`.
10. Back-merge `origin/main` into local `develop`.
11. Consolidate only the loose spec files explicitly marked with
    `Release tag: vX.Y.Z` into `specs/release-X.Y.Z-consolidated.md`.
12. Consolidate only the loose plan files explicitly marked with
    `Release tag: vX.Y.Z` into `plans/release-X.Y.Z-consolidated.md`.
13. Print a human-readable release report.

If the user declines at the staging approval gate, the command stops after the
staging deploy and reports the paused release state.

`BACKLOG.md` reconciliation is not owned by this command. It remains part of
development-cycle closure unless a future release workflow explicitly
implements it.

## Manual Functional Checks for Staging

The command prints a release-specific staging checklist, but the baseline checks
should cover:

1. Iniciar sesion y cerrar sesion sin errores.
2. Abrir rankings y confirmar que la paginacion funciona.
3. Abrir la lista de partidos y confirmar que la paginacion funciona.
4. Crear un partido y confirmar que ranking y estadisticas se actualizan.
5. Abrir Americano y confirmar que la vista carga correctamente.
6. Validar los cambios especificos de la version liberada.

## Fallback Scripts

- `scripts/backmerge_main_to_develop.sh <version>`: manual fallback for the
  local back-merge if the automated flow stops after production.
- `scripts/tag_release.sh <version> "<summary>"`: manual fallback only when
  `.github/workflows/release.yml` is intentionally bypassed or needs recovery.
