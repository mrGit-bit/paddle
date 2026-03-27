# Harden Release SSH Key Permissions

## Tracking

- Task ID: `harden-release-ssh-key-permissions`
- Plan: `plans/2026-03-26_harden-release-ssh-key-permissions.md`
- Release tag: `v1.6.1`

## Functional Goal

Make `/prompts:release <version>` resilient to the observed shared-key failure
mode where the repo-local SSH private key files exist but have permissions that
OpenSSH refuses to use.

## Scope

### In

- Update release preflight so it validates the repository-local private key
  modes required by OpenSSH.
- Decide and implement the orchestrator behavior for unsafe private-key modes:
  either repair them automatically to the expected owner-only mode or fail with
  a precise prerequisite error before deployment starts.
- Apply the same handling to both staging and production private keys.
- Add focused regression tests for the SSH-key permission path.
- Update `RELEASE.md` and `CHANGELOG.md` so operators know the expected key
  permissions and the automation behavior.

### Out

- Rotating, replacing, or re-encrypting SSH keys.
- Changing remote deployment hosts or SSH config structure.
- GitHub workflow changes unrelated to SSH deployment.
- Product application code changes.

## UI / UX Requirements

- Release output must stay concise and centered on the script report.
- If the repo-local SSH keys have unsafe permissions, the release flow must not
  fail deep inside the deploy step with a generic SSH error when the
  orchestrator could detect or correct that state earlier.
- If the automation repairs a key mode, it should do so silently unless a later
  failure still occurs.
- If the automation refuses to repair the mode, the report must name the exact
  file and the required permission state.

## Backend / Automation Requirements

- Treat `.codex/private/release_ssh/staging-oracle-key.pem` and
  `.codex/private/release_ssh/production-oracle-key.pem` as OpenSSH private
  keys that must not be group- or world-accessible.
- Keep the existing repository-local SSH config usage:
  `ssh -F .codex/private/release_ssh/config`.
- Do not mutate SSH config or key contents.
- Keep failure handling strict for real SSH connection or deployment-command
  failures after permission handling is complete.

## Reuse Rules

- Reuse `ReleasePaths` and the existing preflight/deploy structure in
  `scripts/release_orchestrator.py`.
- Extend the existing release-orchestrator test module instead of creating a
  second test file.
- Keep the release command entrypoint unchanged.

## Acceptance Criteria

1. The orchestrator no longer reaches `ssh` with repo-local private keys in the
   observed unsafe `0666` state.
2. Both staging and production private keys are covered by the same permission
   handling path.
3. A normal `pytest paddle/frontend/tests/test_release_orchestrator.py -q` run
   covers the new SSH-key permission behavior.
4. `RELEASE.md` states the expected repo-local private-key permissions and how
   the automation handles unsafe modes.
5. Genuine SSH authentication or connectivity failures still surface as release
   failures after permission handling is satisfied.

## Manual Functional Checks

1. Set one repo-local release private key to mode `0666`, run the release
   command, and confirm the orchestrator handles the mode before `ssh` runs.
2. Repeat with the other repo-local release private key.
3. Run the targeted release-orchestrator tests and confirm they pass.
4. Confirm a real bad key or unreachable host still fails the release after the
   permission preflight succeeds.

## Allowed Files

- `specs/028-harden-release-ssh-key-permissions.md`
- `plans/2026-03-26_harden-release-ssh-key-permissions.md`
- `scripts/release_orchestrator.py`
- `paddle/frontend/tests/test_release_orchestrator.py`
- `RELEASE.md`
- `CHANGELOG.md`

## Forbidden Files

- `.github/workflows/*`
- `.codex/private/release_ssh/*` key material or SSH config contents
- Product app code unrelated to release automation
