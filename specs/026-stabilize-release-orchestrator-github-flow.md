# Stabilize Release Orchestrator GitHub Flow

## Tracking

- Task ID: `stabilize-release-orchestrator-github-flow`
- Plan: `plans/2026-03-26_stabilize-release-orchestrator-github-flow.md`
- Release tag: `v1.6.0`

## Functional Goal

Make the release orchestrator resilient to the GitHub CLI conditions observed in
Codespaces so `/prompts:release <version>` can continue past GitHub
authentication, workflow discovery, and release-prep PR gating when the release
prerequisites are otherwise satisfied.

## Scope

### In

- Update the release orchestrator GitHub CLI invocation path so it can fall
  back to a valid stored `gh` login when `GH_TOKEN` or `GITHUB_TOKEN` are set
  but invalid.
- Relax release workflow run matching so `workflow_dispatch` runs are matched
  using stable release identifiers instead of assuming the reported
  `headBranch` is `develop`.
- Handle release-prep PRs that have no reported required checks without
  blocking the release.
- Point the default pytest configuration at the isolated test settings module
  so the release-orchestrator test suite runs under normal repository pytest
  invocation.
- Make post-release spec/plan consolidation select the intended shipped loose
  files without depending on raw version text inside the file body.
- Add focused automated tests for the new GitHub auth and PR-check behavior.
- Update release documentation and changelog entries to reflect the stabilized
  behavior.

### Out

- Replacing the existing GitHub Actions workflows.
- Changing deployment SSH behavior.
- Changing product code unrelated to release automation.
- Automatically repairing invalid Codespaces secrets.

## UI / UX Requirements

- Release output remains concise and centered on the script report.
- If env-token auth is invalid but stored `gh` auth works, the command should
  continue without asking the user to diagnose GitHub CLI internals first.
- If a PR has no required checks, the automation should treat that condition as
  non-blocking and continue instead of surfacing a misleading failure.
- Genuine GitHub auth failures must still stop the release with actionable
  output.

## Backend / Automation Requirements

- Centralize GitHub CLI execution behind helpers that can retry without
  `GH_TOKEN` and `GITHUB_TOKEN` when the initial auth-related failure matches
  the invalid-token condition.
- Keep non-`gh` commands unchanged.
- Match release workflow runs by creation time, dispatch event, and release
  identifiers without requiring the live `gh run list` response to report
  `headBranch=develop`.
- Default repository pytest runs must use `config.test_settings`.
- Consolidation selection must use deterministic release metadata or explicit
  release provenance rules instead of scanning for version text in arbitrary
  Markdown bodies.
- Preserve strict failure handling for real workflow, merge, deployment, and
  back-merge errors.

## Reuse Rules

- Keep the release command entrypoint thin and continue delegating all logic to
  `scripts/release_orchestrator.py`.
- Extend the existing test module instead of adding a second release test file.
- Reuse existing report rendering and release flow structure.

## Acceptance Criteria

1. When `GH_TOKEN` or `GITHUB_TOKEN` are invalid but a stored `gh` login is
   valid, the orchestrator can pass GitHub preflight and continue using the
   stored login.
2. `wait_for_workflow_run(...)` can identify the intended release-prep
   `workflow_dispatch` run even when `gh run list` reports `headBranch` as
   `main` or omits the requested target branch signal.
3. The release-prep PR step does not fail when GitHub reports no required
   checks for that PR.
4. Real GitHub auth failures still raise a release error instead of silently
   continuing.
5. A normal `pytest paddle/frontend/tests/test_release_orchestrator.py -q` run
   uses isolated test settings without needing a manual `--ds` override.
6. Post-release consolidation can include shipped loose spec/plan files even
   when their bodies do not mention the release number verbatim.
7. Automated tests cover the new auth fallback, workflow-run matching, no-check
   PR handling, and consolidation-selection behavior.
8. `RELEASE.md` explains the GitHub CLI behavior accurately for Codespaces.

## Manual Functional Checks

1. In a Codespace with invalid `GH_TOKEN`/`GITHUB_TOKEN` env values but a valid
   stored `gh` login, run the release command and confirm GitHub preflight
   succeeds.
2. Dispatch a release-prep run and confirm the orchestrator finds the matching
   workflow run instead of timing out on the branch match.
3. Run the release flow where the release-prep PR has no required checks and
   confirm the automation proceeds to the merge step.
4. Remove both env-token auth and stored `gh` auth and confirm the release
   still aborts with a clear GitHub auth failure.

## Allowed Files

- `specs/026-stabilize-release-orchestrator-github-flow.md`
- `plans/2026-03-26_stabilize-release-orchestrator-github-flow.md`
- `scripts/release_orchestrator.py`
- `paddle/frontend/tests/test_release_orchestrator.py`
- `paddle/pytest.ini`
- `RELEASE.md`
- `CHANGELOG.md`

## Forbidden Files

- GitHub workflow files unless a later approved scope explicitly expands there
- Deployment SSH keys or SSH config
- Product app code unrelated to release automation
