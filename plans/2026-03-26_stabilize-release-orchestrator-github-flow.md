# Stabilize Release Orchestrator GitHub Flow Plan

## Tracking

- Task ID: `stabilize-release-orchestrator-github-flow`
- Spec: `specs/026-stabilize-release-orchestrator-github-flow.md`
- Release tag: `v1.6.0`

## Spec Reference

- `specs/026-stabilize-release-orchestrator-github-flow.md`

## Summary

- The current release orchestrator fails under the observed Codespaces GitHub
  CLI conditions even after the user completes `gh auth login`.
- The failure path is a combination of invalid env-token overrides,
  over-constrained workflow-dispatch matching, and PR-check waiting that does
  not tolerate repos with no required checks on the release-prep PR.
- The current regression coverage is not active under the repository’s default
  pytest configuration, and the current consolidation selector can miss shipped
  loose spec/plan files when they do not mention the release number in body
  text.

## Key Changes

- Add a narrow `gh` command wrapper that retries auth-sensitive calls without
  `GH_TOKEN` and `GITHUB_TOKEN` when the initial failure indicates invalid
  token overrides.
- Loosen workflow-run selection so it keys off dispatch timing and release
  identifiers instead of a fragile branch assumption.
- Treat “no checks reported” as a non-blocking condition for PRs that do not
  have required checks configured.
- Point the repo’s default pytest settings at `config.test_settings`.
- Replace version-text consolidation matching with an explicit release-aware
  selection rule for loose spec/plan files.
- Extend targeted tests and refresh release documentation/changelog text.

## Files Allowed to Change

- `specs/026-stabilize-release-orchestrator-github-flow.md`
- `plans/2026-03-26_stabilize-release-orchestrator-github-flow.md`
- `scripts/release_orchestrator.py`
- `paddle/frontend/tests/test_release_orchestrator.py`
- `paddle/pytest.ini`
- `RELEASE.md`
- `CHANGELOG.md`

## Files Forbidden to Change

- `.github/workflows/*`
- SSH private keys or repo-local SSH config
- Unrelated product files

## Proposed Changes

- Refactor GitHub CLI subprocess execution in the orchestrator so auth fallback
  is explicit, centralized, and limited to `gh` commands.
- Update workflow-run matching helpers to stop depending on the live
  `headBranch` value from `gh run list`.
- Update PR-check waiting to continue when GitHub reports no checks for the PR.
- Update default pytest configuration so focused tests run without manual
  settings overrides.
- Update consolidation-source selection to rely on deterministic release
  provenance rules instead of Markdown body text.
- Add regression tests for each failure mode found during the live release run.
- Document the fallback behavior and add an `Unreleased` changelog note.

## Plan Steps (Execution Order)

- [ ] Update the spec and plan for this release-automation fix.
- [ ] Patch the orchestrator GitHub CLI helpers and release gating logic.
- [ ] Patch default pytest settings and consolidation-source selection.
- [ ] Extend the targeted release orchestrator tests.
- [ ] Update `RELEASE.md` and `CHANGELOG.md`.
- [ ] Run targeted tests and markdown lint for changed Markdown files.

## Acceptance Criteria (Testable)

- [ ] The orchestrator retries auth-sensitive `gh` commands without env-token
      overrides when the failure is specifically an invalid `GH_TOKEN` or
      `GITHUB_TOKEN`.
- [ ] The workflow-run lookup succeeds against the currently observed
      `gh run list` shape for release-prep dispatches.
- [ ] The release-prep PR path does not fail when `gh pr checks` reports no
      checks.
- [ ] A normal `pytest paddle/frontend/tests/test_release_orchestrator.py -q`
      run uses `config.test_settings`.
- [ ] Consolidation selection can include shipped loose spec/plan files without
      relying on raw release-number mentions in the file body.
- [ ] The targeted Python tests pass.
- [ ] Changed Markdown files remain markdownlint-clean except `MD013`.

## Risks and Constraints

- Falling back too broadly could hide legitimate auth failures.
  Mitigation: only retry on the explicit invalid-token error text.
- Relaxing workflow matching too far could select the wrong run.
  Mitigation: keep creation-time, workflow-dispatch, and release-identifier
  filtering, and fail on ambiguous multiple matches.
- Treating no-check PRs as success must not hide real failing required checks.
  Mitigation: only bypass when GitHub explicitly reports no checks.
- Broadening consolidation selection could sweep unrelated loose files into the
  release artifacts.
  Mitigation: base selection on explicit allowed filename patterns and
  repository release provenance instead of free-form text matching.

## Validation

- `pytest paddle/frontend/tests/test_release_orchestrator.py -q`
- `pytest paddle/frontend/tests/test_release_orchestrator.py -q`
- `python -m markdownlint-cli2 specs/026-stabilize-release-orchestrator-github-flow.md plans/2026-03-26_stabilize-release-orchestrator-github-flow.md RELEASE.md CHANGELOG.md`

- Manual functional checks:
- Run the release command with invalid env-token overrides and a valid stored
  `gh` login.
- Dispatch a release-prep run for `v1.6.0` and confirm the run is found.
- Confirm the release-prep PR does not block on “no checks reported”.
- Confirm a real missing `gh` login still aborts the release.
