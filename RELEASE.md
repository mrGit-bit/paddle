# Release Process

This repository supports a command-first release flow through the repository
local Codex slash command `/release`.

## Command

- `/release 1.6.0`
- `/release v1.6.0`

The command delegates to `python scripts/release_orchestrator.py <version>` and
automates the GitHub workflow, branch-promotion, deployment, back-merge, and
post-release consolidation steps described below.

## Prerequisites

- Current branch is `develop`.
- `git status --short` is clean.
- Local `develop` is synchronized with `origin/develop`.
- `gh` is installed and authenticated.
- `ssh` is installed.
- Repo-local SSH config exists at `.codex/private/release_ssh/config`.
- Repo-local staging key exists at
  `.codex/private/release_ssh/staging-oracle-key.pem`.
- Repo-local production key exists at
  `.codex/private/release_ssh/production-oracle-key.pem`.

## Repo-local SSH Setup

1. Copy `.codex/templates/release_ssh_config.example` to
   `.codex/private/release_ssh/config`.
2. Copy the real staging key to
   `.codex/private/release_ssh/staging-oracle-key.pem`.
3. Copy the real production key to
   `.codex/private/release_ssh/production-oracle-key.pem`.
4. Keep those files untracked. The repository ignores the config and `.pem`
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
   SSH assets.
2. Dispatch `Release Prep (no-AI)` for `X.Y.Z` from `develop`.
3. Wait for the workflow run and locate PR
   `version(release): prepare release vX.Y.Z`.
4. Wait for required checks, squash-merge the release-prep PR, and delete
   `chore/release-vX.Y.Z`.
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
11. Consolidate loose release spec files into
    `specs/release-X.Y.Z-consolidated.md`.
12. Consolidate loose release plan files into
    `plans/release-X.Y.Z-consolidated.md`.
13. Print a human-readable release report.

If the user declines at the staging approval gate, the command stops after the
staging deploy and reports the paused release state.

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
