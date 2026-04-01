# Harden Release Remote Deploy Verification

## Tracking

- Task ID: `harden-release-remote-deploy-verification`
- Plan: `plans/2026-03-31_harden-release-remote-deploy-verification.md`
- Release tag: `unreleased`

## Goal

- Make the tracked release flow fail clearly when remote deployment does not
  leave staging or production on the requested release version.
- Remove the interactive-shell behavior from the tracked SSH config template so
  the orchestrator can continue after remote deploy commands complete.

## Scope

- In:
  - harden the orchestrator around remote deploy verification
  - update the tracked SSH config template to avoid hanging interactive shells
  - add focused tests for the new release checks
  - update release documentation and the unreleased changelog entry
- Out:
  - editing untracked server-local `deploy_update.sh`
  - changing the release promotion sequence
  - changing unrelated GitHub workflow behavior

## Files

- Allowed:
  - `scripts/release_orchestrator.py`
  - `paddle/frontend/tests/test_release_orchestrator.py`
  - `.codex/templates/release_ssh_config.example`
  - `RELEASE.md`
  - `CHANGELOG.md`
- Forbidden:
  - `.github/workflows/**`
  - `paddle/frontend/**` except
    `paddle/frontend/tests/test_release_orchestrator.py`
  - `.codex/private/**`

## Acceptance

- [ ] The orchestrator fails the release when a remote deploy command returns
      without the requested app version on the target host.
- [ ] The tracked SSH config template no longer leaves the operator in an
      interactive remote shell after `staging-update` or `prod-update`.
- [ ] Focused tests cover the new remote-version verification behavior.

## Checks

- Run the focused orchestrator pytest scope.
- Review the SSH config template and confirm the update aliases are
  non-interactive.
