# Spec 012: Release Workflow Git Identity for Tag Creation

## Functional Goal

Ensure the production release workflow can create and push the annotated release
tag without failing on Git committer identity configuration in GitHub Actions.

## Scope

### In

- Update the release workflow that runs on `main` pushes.
- Configure a deterministic Git identity before annotated tag creation.
- Extract the candidate release version from `paddle/config/__init__.py`.
- Compare that version against the latest released version header in
  `CHANGELOG.md` before extracting release notes or creating the release tag.
- Preserve the current release flow:
  - extract released version from `paddle/config/__init__.py`
  - verify it matches the latest released section in `CHANGELOG.md`
  - create and push the release tag if missing
  - create the GitHub Release
  - open the back-merge PR from `main` to `develop`
- Keep the configuration aligned with the existing release-prep workflow bot
  identity unless there is a strong reason to differ.

### Out

- Changes to release version extraction logic.
- Changes to release notes generation logic.
- Changes to application code, templates, or tests unrelated to the workflow.
- Changes to deployment scripts or server configuration.

## UI/UX Requirements

- Not applicable to product UI.

## Backend/Automation Requirements

- The workflow must set `git config user.name` and `git config user.email`
  before running `git tag -a`.
- The chosen identity must be valid in a GitHub Actions runner context.
- The workflow must remain idempotent when the tag already exists.
- The workflow must fail fast if the version in `paddle/config/__init__.py` does
  not match the latest released version header in `CHANGELOG.md`.
- Release notes extraction must use the verified version after the consistency
  check passes.

## Data Rules

- The release tag format remains `v<version>`.
- The primary version source is `paddle/config/__init__.py`.
- `CHANGELOG.md` remains the release-notes source and must contain a matching
  latest released version header.
- The fix must not alter the release notes body content beyond selecting the
  section using the verified version.

## Reuse Rules

- Reuse the same GitHub Actions bot identity already used in
  `.github/workflows/release-prep-no-ai.yml` unless a repository-specific reason
  requires different values.
- Keep the workflow changes minimal and localized.

## Acceptance Criteria

1. The release workflow configures a valid Git identity before annotated tag
   creation.
2. The `Create tag if missing` step can run `git tag -a "$tag" -m "Release
   $tag"` without the "Committer identity unknown" failure.
3. The workflow reads the release version from `paddle/config/__init__.py` and
   verifies that the latest released version in `CHANGELOG.md` matches it.
4. The workflow fails with a clear error if those versions differ.
5. Existing behavior for already-existing tags is preserved.
6. GitHub Release creation and back-merge PR creation behavior remain unchanged.

## Manual Functional Checks

1. Trigger the release workflow in a branch or test context and verify the tag
   creation step no longer fails on missing Git identity.
2. Confirm the workflow reads the version from `paddle/config/__init__.py` and
   pushes the expected annotated tag name, for example `v1.4.0`.
3. Temporarily test a mismatch scenario and confirm the workflow stops before
   tag creation or release creation with a clear version-mismatch error.
4. Confirm the workflow still skips tag creation cleanly when the tag already
   exists.
5. Confirm the GitHub Release is created from the changelog section matching the
   verified version.
6. Confirm the back-merge PR from `main` to `develop` is still opened or
   skipped only when already open.

## Files Allowed to Change

- `.github/workflows/release.yml`
- `paddle/config/__init__.py`
- `CHANGELOG.md`
- this spec file
- the corresponding plan file

## Files Forbidden to Change

- Application code under `paddle/**`
- deployment scripts
- unrelated GitHub workflows
- unrelated documentation
