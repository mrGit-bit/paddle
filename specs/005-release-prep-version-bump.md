# Spec 005: Release Prep Workflow Version Bump

## Functional Goal

Ensure `.github/workflows/release-prep-no-ai.yml` always includes the `paddle/config/__init__.py` version bump in the generated release branch commit and PR when executed via `workflow_dispatch`.

## Scope

### In

- Fix release-prep workflow commit staging so version updates in `paddle/config/__init__.py` are committed.
- Preserve existing changelog update behavior.
- Keep release branch creation, push, and PR creation flow unchanged.

### Out

- No changes to release semantics, version calculation rules, or branch naming.
- No changes to application runtime version-loading behavior.
- No modifications to unrelated workflows.

## UI/UX Requirements

- Not applicable (CI workflow-only change).

## Backend Requirements

- Workflow must stage and commit both `CHANGELOG.md` and `paddle/config/__init__.py` when they change.
- Workflow must fail fast if neither file is changed/staged.

## Data Rules

- Input `version` string from `workflow_dispatch` remains source of truth.
- `paddle/config/__init__.py` must contain one authoritative `__version__` assignment matching the provided input value.

## Reuse Rules

- Reuse existing inline Python step that updates `paddle/config/__init__.py`.
- Only adjust staging/commit logic needed to include version file changes.

## Acceptance Criteria

- AC1: Running workflow with `version=X.Y.Z` updates `paddle/config/__init__.py` to `__version__ = "X.Y.Z"` in the release branch.
- AC2: The release commit includes both `CHANGELOG.md` and `paddle/config/__init__.py` when both files changed.
- AC3: PR created by workflow contains the version bump diff in `paddle/config/__init__.py`.
- AC4: Existing workflow steps for branch creation and PR creation remain functional.

## Manual Functional Checks

1. Trigger `Release Prep (no-AI)` with a new version and confirm workflow job succeeds.
2. Open the created PR and verify `paddle/config/__init__.py` shows the new `__version__` value.
3. Verify `CHANGELOG.md` contains a new `## [X.Y.Z] - YYYY-MM-DD` section and `## [Unreleased]` remains present.
4. Confirm commit message remains `version(release): prepare release vX.Y.Z`.
5. Re-run with a different version and verify old release branch is replaced and new PR contains updated version/changelog.

## Files Allowed to Change

- `.github/workflows/release-prep-no-ai.yml`
- `CHANGELOG.md`

## Files Forbidden to Change

- `paddle/config/__init__.py`
- `paddle/frontend/**`
- `paddle/games/**`
- `paddle/users/**`
- `mobile/**`
- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`
