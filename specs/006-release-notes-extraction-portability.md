# Spec 006: Release Notes Extraction Portability Fix

## Functional Goal

Ensure `.github/workflows/release.yml` can extract release notes for a semantic version section from `CHANGELOG.md` without `awk` parser errors in GitHub Actions.

## Scope

### In

- Replace or adjust the release-notes extraction logic in `.github/workflows/release.yml` to be portable and shell-safe in the Ubuntu runner environment.
- Preserve existing behavior for:
  - tag reuse when tag already exists,
  - release creation only when release does not exist,
  - fallback notes message when no changelog section is found.

### Out

- No changes to release trigger conditions (`push` to `main`).
- No changes to tag naming (`vX.Y.Z`) or release title format.
- No changes to other workflows.
- No application/runtime code changes.

## UI/UX Requirements

- Not applicable (CI workflow change only).

## Backend/Automation Requirements

- Notes extraction must correctly capture lines after `## [X.Y.Z]` until the next `## [` heading.
- Pattern matching must support current changelog heading format `## [X.Y.Z] - YYYY-MM-DD`.
- Workflow step must continue to set a fallback notes message when extraction returns empty output.

## Data Rules

- `version` comes from the parsed first released entry in `CHANGELOG.md`.
- `tag` remains `v${version}`.
- Notes content is plain text passed to `gh release create --notes`.

## Reuse Rules

- Reuse existing release step structure in `.github/workflows/release.yml`.
- Limit modifications to the failing extraction logic and any minimal guard logic directly required for correctness.

## Acceptance Criteria

- AC1: Workflow no longer fails with `awk` syntax error in release note extraction.
- AC2: For a changelog section like `## [1.3.1] - 2026-03-09`, extraction returns the section body until the next `## [` heading.
- AC3: If no section body is found, fallback notes message is used and release creation still proceeds.
- AC4: Existing tag/release idempotency behavior remains unchanged.

## Manual Functional Checks

1. Run the release workflow on a commit in `main` where `CHANGELOG.md` contains `## [X.Y.Z] - YYYY-MM-DD` and confirm workflow success.
2. Verify created GitHub Release `vX.Y.Z` includes notes from the corresponding changelog section body.
3. Re-run workflow for same tag and confirm job reports tag/release already exists and skips creation safely.
4. Temporarily test with a release heading that has no body lines and confirm fallback notes message is used.

## Files Allowed to Change

- `.github/workflows/release.yml`
- `CHANGELOG.md`

## Files Forbidden to Change

- `.github/workflows/release-prep-no-ai.yml`
- `.github/workflows/release-prep-codex.yml`
- `paddle/**`
- `mobile/**`
- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`
