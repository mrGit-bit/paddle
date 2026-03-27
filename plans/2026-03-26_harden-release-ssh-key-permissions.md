# Harden Release SSH Key Permissions Plan

## Tracking

- Task ID: `harden-release-ssh-key-permissions`
- Spec: `specs/028-harden-release-ssh-key-permissions.md`
- Release tag: `v1.6.1`

## Spec Reference

- `specs/028-harden-release-ssh-key-permissions.md`

## Summary

- The `v1.6.1` release run reached staging deployment and then failed because
  the repo-local shared SSH private key had mode `0666`, which OpenSSH rejects.
- Current preflight only checks that the SSH files exist, so the failure
  appears late and with low-quality operator feedback.

## Key Changes

- Add private-key permission handling to release preflight for both staging and
  production keys.
- Keep deployment execution unchanged once the key modes satisfy OpenSSH.
- Extend targeted orchestrator tests for the new behavior.
- Update release documentation and changelog text to make the expected
  repository-local key modes explicit.

## Files Allowed to Change

- `specs/028-harden-release-ssh-key-permissions.md`
- `plans/2026-03-26_harden-release-ssh-key-permissions.md`
- `scripts/release_orchestrator.py`
- `paddle/frontend/tests/test_release_orchestrator.py`
- `RELEASE.md`
- `CHANGELOG.md`

## Files Forbidden to Change

- `.github/workflows/*`
- `.codex/private/release_ssh/*`
- Unrelated product or governance files

## Proposed Changes

- Add a helper that inspects the mode bits of the repo-local release private
  keys and normalizes or rejects unsafe permissions before deployment.
- Route release preflight through that helper so the release report reflects the
  SSH prerequisite accurately.
- Add focused tests for both the safe path and the unsafe-permission path.
- Document the expected key permissions in `RELEASE.md` and add an `Unreleased`
  changelog note.

## Plan Steps (Execution Order)

- [ ] Approve the active-work spec and plan for this SSH permission fix.
- [ ] Patch the release orchestrator preflight/deploy path.
- [ ] Extend the targeted release-orchestrator tests.
- [ ] Update `RELEASE.md` and `CHANGELOG.md`.
- [ ] Run targeted tests and markdown lint for changed Markdown files.

## Acceptance Criteria (Testable)

- [ ] The orchestrator handles unsafe repo-local SSH private-key modes before
      running `ssh`.
- [ ] Both release private keys use the same permission-handling path.
- [ ] `pytest paddle/frontend/tests/test_release_orchestrator.py -q` passes.
- [ ] Changed Markdown files remain markdownlint-clean except `MD013`.

## Risks and Constraints

- Auto-repairing key modes changes local file metadata.
  Mitigation: limit the change to owner-only permission bits on the known
  repo-local key paths.
- Rejecting unsafe modes instead of repairing them would keep the failure user
  visible.
  Mitigation: if that route is chosen, surface an exact prerequisite message
  before any deployment step starts.
- The shared-key workflow depends on current OpenSSH behavior.
  Mitigation: implement against the current observed CLI failure mode rather
  than a guessed policy.

## Validation

- `pytest paddle/frontend/tests/test_release_orchestrator.py -q`
- `markdownlint-cli2 specs/028-harden-release-ssh-key-permissions.md`
  `plans/2026-03-26_harden-release-ssh-key-permissions.md RELEASE.md`
  `CHANGELOG.md`

- Manual functional checks:
- Re-run the release with a repo-local key intentionally set to `0666` and
  confirm the orchestrator handles that state before deploy.
- Confirm a release with already-correct key modes still follows the normal
  path.
