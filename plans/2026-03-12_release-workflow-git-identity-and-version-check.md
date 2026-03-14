# Release Workflow Git Identity and Version Check Plan

## Context

- `.github/workflows/release.yml` fails during annotated tag creation because
  GitHub Actions has no configured Git committer identity for `git tag -a`.
- The release workflow currently derives the release version directly from
  `CHANGELOG.md`, but the approved scope now requires `paddle/config/__init__.py`
  to be the primary version source and `CHANGELOG.md` to be validated against it
  before release notes extraction.
- Discovery files:
  - `.github/workflows/release.yml`
  - `.github/workflows/release-prep-no-ai.yml`
  - `paddle/config/__init__.py`
  - `CHANGELOG.md`
  - `specs/012-release-workflow-git-identity.md`

## Spec Reference

- `specs/012-release-workflow-git-identity.md`

## Objectives

- Prevent release workflow failure caused by missing Git identity during tag
  creation.
- Make `paddle/config/__init__.py` the release version source in the workflow.
- Fail fast if the latest released `CHANGELOG.md` version does not match the app
  version before any tag or GitHub Release action.
- Preserve existing tag/release/back-merge behavior outside that validation.

## Scope

### In

- Update `.github/workflows/release.yml` to configure Git identity before
  `git tag -a`.
- Update `.github/workflows/release.yml` to read the version from
  `paddle/config/__init__.py`.
- Add a release-version consistency check against the latest released header in
  `CHANGELOG.md`.
- Keep changelog release notes extraction keyed off the verified version.
- Add an unreleased changelog entry describing the workflow fix.

### Out

- No changes to workflow trigger conditions or permissions.
- No changes to release-prep workflows.
- No application behavior changes under `paddle/**` other than reading the
  existing version file from the workflow.
- No deployment or server-side script changes.

## Risks

- Risk: Version parsing from `paddle/config/__init__.py` could be too loose and
  capture the wrong value.
  - Mitigation: Match only the explicit `__version__ = "X.Y.Z"` assignment.
- Risk: The changelog comparison could choose the wrong section if unreleased
  formatting changes.
  - Mitigation: Continue matching the first released header of the form
    `## [X.Y.Z] - YYYY-MM-DD`, not `## [Unreleased]`.
- Risk: Workflow edits could accidentally change idempotent behavior for
  existing tags or releases.
  - Mitigation: Keep those guards intact and limit changes to the version
    extraction and Git identity setup.

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

## Proposed Changes (Step-by-Step by File)

- `.github/workflows/release.yml`
  - Change: Add explicit GitHub Actions bot `user.name` and `user.email`
    configuration before annotated tag creation.
  - Why: `git tag -a` requires a valid Git identity on the runner.
  - Notes: Reuse the same identity already used by
    `.github/workflows/release-prep-no-ai.yml`.

- `.github/workflows/release.yml`
  - Change: Replace version discovery so it reads `__version__` from
    `paddle/config/__init__.py`, then compare it with the latest released
    `CHANGELOG.md` version before creating the tag or extracting notes.
  - Why: Make the application version the source of truth while ensuring release
    notes stay synchronized with the changelog.
  - Notes: Fail clearly on mismatch and preserve the existing outputs `version`
    and `tag`.

- `CHANGELOG.md`
  - Change: Add a concise unreleased entry describing the release workflow fix.
  - Why: Keep changelog discipline aligned with the shipped behavior change.
  - Notes: Entry should mention both Git identity setup and version consistency
    validation only if both are implemented.

## Plan Steps (Execution Order)

- [ ] Step 1: Patch `.github/workflows/release.yml` to configure Git identity
  and implement version extraction plus changelog consistency validation.
- [ ] Step 2: Add the matching `## [Unreleased]` changelog entry.
- [ ] Step 3: Run targeted validation for workflow syntax and inspect the final
  diff for scope compliance.

## Acceptance Criteria (Testable)

- [ ] AC1: The workflow configures `git config user.name` and `git config
  user.email` before `git tag -a`.
- [ ] AC2: The workflow reads the release version from
  `paddle/config/__init__.py`.
- [ ] AC3: The workflow compares that version to the latest released version
  header in `CHANGELOG.md` and fails clearly on mismatch.
- [ ] AC4: Release notes extraction uses the verified version after the
  consistency check passes.
- [ ] AC5: Existing skip behavior for already-existing tags remains intact.

## Validation Commands

- `ruby -e 'require "yaml"; YAML.load_file(".github/workflows/release.yml")'`
- `git diff -- .github/workflows/release.yml CHANGELOG.md`

## Manual Functional Checks

1. Run the release workflow with matching versions in
   `paddle/config/__init__.py` and `CHANGELOG.md` and verify the tag step no
   longer fails on missing Git identity.
2. Confirm the created tag matches the version from
   `paddle/config/__init__.py`, for example `v1.4.0`.
3. Test a deliberate version mismatch and verify the workflow stops before tag
   creation with a clear mismatch error.
4. Confirm the GitHub Release notes still come from the changelog section that
   matches the verified version.
5. Re-run for an already existing tag and verify tag creation is skipped
   cleanly.

## Execution Log

- 2026-03-12 00:00 — Spec created.
- 2026-03-12 00:00 — Spec updated with version-source requirement.
- 2026-03-12 00:00 — Spec approved.
- 2026-03-12 00:00 — Plan created.

## Post-Mortem / Improvements

- What worked well:
  - The workflow failure message directly exposed the missing Git identity root
    cause.
- What caused friction:
  - The original workflow relied on changelog-only version discovery, which made
    source-of-truth expectations ambiguous.
- Suggested updates to:
  - `/docs/PROJECT_INSTRUCTIONS.md`: none.
  - `/AGENTS.md`: none.
  - `/plans/TEMPLATE.md`: none.
