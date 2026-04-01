# Harden Release Remote Deploy Verification Plan

## Tracking

- Task ID: `harden-release-remote-deploy-verification`
- Spec: `specs/035-harden-release-remote-deploy-verification.md`
- Release tag: `unreleased`

## Summary

- The current release flow trusts the remote deploy command exit status but
  does not verify that the target host now serves the requested version.
- The tracked SSH update aliases end with `exec bash`, which leaves the
  orchestrator stuck in an interactive shell after deployment.

## Scope

- In:
  - add a post-deploy remote version check for staging and production
  - make the tracked SSH update aliases non-interactive
  - add focused release-orchestrator tests
  - update release docs and changelog text
- Out:
  - tracked automation for repairing server-local deploy scripts
  - broader release refactors
  - production promotion changes unrelated to deploy verification

## Files Allowed to Change

- `scripts/release_orchestrator.py`
- `paddle/frontend/tests/test_release_orchestrator.py`
- `.codex/templates/release_ssh_config.example`
- `RELEASE.md`
- `CHANGELOG.md`

## Files Forbidden to Change

- `.github/workflows/**`
- `.codex/private/**`
- `paddle/frontend/**` except `paddle/frontend/tests/test_release_orchestrator.py`

## Plan

- [ ] Add a helper that reads `paddle/config/__init__.py` on the remote host
      after each deploy and raises a release error if the version is not the
      requested `X.Y.Z`.
- [ ] Reuse that helper for both staging and production deploy steps so the
      release pauses or aborts with a concrete mismatch message instead of
      silently continuing.
- [ ] Remove `exec bash` from the tracked SSH config template update aliases.
- [ ] Extend focused orchestrator tests and update release documentation and
      changelog wording.

## Acceptance

- [ ] Staging and production deploy steps verify the requested remote app
      version before the release continues.
- [ ] The tracked SSH template update aliases terminate after the remote deploy
      command instead of opening an interactive shell.
- [ ] The focused orchestrator test scope passes.

## Validation

- `pytest paddle/frontend/tests/test_release_orchestrator.py -q`
- Manual checks:
  - inspect `.codex/templates/release_ssh_config.example` and confirm the
    update aliases no longer end in `exec bash`
  - run the focused orchestrator tests and confirm the remote version
    verification paths pass
