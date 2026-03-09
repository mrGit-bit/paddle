# Release Workflow Notes Extraction Portability Plan

## Context

- `.github/workflows/release.yml` fails in GitHub Actions during release notes extraction with an `awk` syntax error.
- The failure blocks release creation even when tag handling is idempotent.
- Discovery files:
  - `.github/workflows/release.yml`
  - `CHANGELOG.md`
  - `specs/006-release-notes-extraction-portability.md`

## Spec Reference

- `specs/006-release-notes-extraction-portability.md`

## Objectives

- Eliminate the release workflow parser failure in notes extraction.
- Preserve existing tag/release idempotency behavior.
- Keep fallback notes behavior when no changelog section body is found.

## Scope

### In

- Update changelog section extraction logic in `.github/workflows/release.yml` to a portable implementation.
- Validate workflow syntax after change.
- Add changelog entry under `## [Unreleased]` documenting the fix.

### Out

- No changes to workflow triggers or permissions.
- No changes to release title/tag format.
- No changes to other workflow files or application code.

## Risks

- Risk: New extraction logic could capture incorrect boundaries.
  - Mitigation: Match section start as `## [<version>]` and stop at next `## [`.
- Risk: Shell quoting/newline handling could break `gh release create --notes`.
  - Mitigation: Keep multiline assignment simple and preserve existing fallback behavior.

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
  - Change: Replace failing `awk` release-notes extraction snippet with a portable, shell-safe section parser.
  - Why: Prevent workflow failure on GitHub Actions runner and keep intended release notes behavior.
  - Notes: Keep existing release existence check and fallback notes text.

- `CHANGELOG.md`
  - Change: Add unreleased entry describing release workflow extraction portability fix.
  - Why: Keep changelog discipline aligned with behavior changes.
  - Notes: Entry must match actual implementation.

## Plan Steps (Execution Order)

- [ ] Step 1: Patch release notes extraction logic in `.github/workflows/release.yml`.
- [ ] Step 2: Add matching `## [Unreleased]` changelog entry.
- [ ] Step 3: Validate workflow YAML and verify diff scope.

## Acceptance Criteria (Testable)

- [ ] AC1: `.github/workflows/release.yml` no longer uses the failing expression that caused `awk` syntax error.
- [ ] AC2: Release notes extraction returns section body for `## [X.Y.Z] - YYYY-MM-DD` headings until next `## [`.
- [ ] AC3: Empty extraction still falls back to default notes message.
- [ ] AC4: Tag/release idempotent checks remain unchanged in behavior.

## Validation Commands

- `python -c "import yaml, pathlib; yaml.safe_load(pathlib.Path('.github/workflows/release.yml').read_text(encoding='utf-8')); print('workflow yaml ok')"`
- `git diff -- .github/workflows/release.yml CHANGELOG.md`

## Manual Functional Checks

1. Push to `main` with a new changelog release header and verify workflow completes without parser errors.
2. Confirm created GitHub Release notes match the corresponding changelog section body.
3. Re-run workflow for same version and verify tag/release creation steps safely skip.
4. Validate fallback notes message by testing a release heading with no body content.

## Execution Log

- 2026-03-09 00:00 — Spec created.
- 2026-03-09 00:00 — Spec approved.
- 2026-03-09 00:00 — Plan created.

## Post-Mortem / Improvements

- What worked well:
  - Root cause was isolated directly from workflow logs and script snippet.
- What caused friction:
  - Parser portability differences were not covered by pre-merge validation.
- Suggested updates to:
  - `/docs/PROJECT_INSTRUCTIONS.md`: none.
  - `/AGENTS.md`: none.
  - `/plans/TEMPLATE.md`: none.
