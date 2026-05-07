# Release Orchestrator Check Fallback

Use for active SDD work only.

## Tracking

- Task ID: `release-orchestrator-check-fallback`
- Status: `implemented`
- Release tag: `unreleased`

## Summary

- Keep release automation moving when GitHub reports no required checks but
  visible PR checks are present.
- Avoid release back-merge failures caused by local GPG signing configuration.

## Scope

- In:
  - Fallback from required PR checks to visible PR checks.
  - Tests for required-check use, visible-check fallback, and no-check
    timeout behavior.
  - Back-merge script adjustment to create unsigned merge commits.
  - Release-prep changelog generation that preserves Markdown heading/list
    spacing.
  - Release-process documentation for the fallback behavior.
- Out:
  - GitHub branch-protection changes.
  - Remote deploy script changes.
  - Release workflow YAML changes.

## Acceptance

- [x] Required checks still pass through the strict required-check path.
- [x] If required checks are not configured, visible PR checks can satisfy the
      gate.
- [x] The orchestrator still aborts when neither required nor visible checks
      appear before timeout.
- [x] Back-merge does not depend on GPG signing keys in the local environment.
- [x] Release-prep changelog generation creates a blank line between the new
      version header and its first bullet.

## Validation

- `python scripts/validate_governance.py`
- `markdownlint` on changed Markdown files; `MD013` is non-blocking.
- `pytest paddle/frontend/tests/test_release_orchestrator.py`
- `pytest paddle/frontend/tests/test_release_pr_body_script.py`
