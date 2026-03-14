# Spec 007: Release Workflow Version Source and Documentation Alignment

## Functional Goal

Align `.github/workflows/release.yml` to derive release version/tag from `paddle/config/__init__.py` (runtime source of truth), and update `RELEASE.md` to document current CI automation and when helper scripts are needed.

## Scope

### In

- Update `.github/workflows/release.yml` to read `__version__` from `paddle/config/__init__.py` instead of extracting the latest version from `CHANGELOG.md`.
- Keep release notes generation from `CHANGELOG.md` using the resolved version.
- Update `RELEASE.md` to:
  - explicitly describe CI jobs currently automating tag/release/back-merge behavior,
  - the other CI jobs used for release automation: `ci.yml` and `release-prep-no-ai.yml`
  - clarify when to use local scripts (`scripts/tag_release.sh`, `scripts/backmerge_main_to_develop.sh`) and when they are unnecessary due to CI.
- Add matching changelog entry under `## [Unreleased]`.

### Out

- No changes to release-prep workflow logic (`release-prep-*` workflows).
- No changes to application runtime version-loading behavior in `paddle/config/__init__.py`.
- No changes to deployment scripts or server deploy steps.
- No changes to mobile release pipeline.

## UI/UX Requirements

- Not applicable (CI + documentation update).

## Backend/Automation Requirements

- `release.yml` must fail fast with a clear error if `__version__` cannot be extracted.
- Tag remains `v${version}` and existing idempotent behavior for tag/release creation is preserved.
- Release notes extraction continues to target `CHANGELOG.md` section `## [${version}]`.

## Data Rules

- Source of truth for release version: `paddle/config/__init__.py` `__version__ = "X.Y.Z"`.
- `CHANGELOG.md` remains release notes source; section must match the runtime version.

## Reuse Rules

- Reuse existing workflow step structure and guard patterns.
- Keep documentation edits constrained to `RELEASE.md` sections related to release automation/scripts.

## Acceptance Criteria

- AC1: `release.yml` derives `version` from `paddle/config/__init__.py` and sets `tag=vX.Y.Z`.
- AC2: Workflow still creates release notes from matching `CHANGELOG.md` version section.
- AC3: Workflow still skips tag/release creation when they already exist.
- AC4: `RELEASE.md` explicitly documents CI jobs involved in release automation.
- AC5: `RELEASE.md` clearly states when scripts are needed vs not needed.

## Manual Functional Checks

1. Merge/push to `main` with `paddle/config/__init__.py` version `X.Y.Z` and matching changelog section; confirm workflow derives tag `vX.Y.Z`.
2. Verify GitHub Release notes are taken from `CHANGELOG.md` section `## [X.Y.Z]`.
3. Re-run workflow and confirm existing tag/release are skipped.
4. Review `RELEASE.md` and confirm there is a clear decision path for CI-automated flow vs script-based/manual flow.

## Files Allowed to Change

- `.github/workflows/release.yml`
- `RELEASE.md`
- `CHANGELOG.md`

## Files Forbidden to Change

- `.github/workflows/release-prep-no-ai.yml`
- `.github/workflows/release-prep-codex.yml`
- `paddle/config/__init__.py`
- `paddle/**` (except read-only inspection)
- `mobile/**`
- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`
