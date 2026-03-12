# Release Workflow Version Source and Documentation Alignment Plan

## Context

- Current `.github/workflows/release.yml` derives version from the latest released header in `CHANGELOG.md`.
- Repository governance and `RELEASE.md` state runtime version source of truth is `paddle/config/__init__.py`.
- Release documentation currently describes scripts and manual flows, but CI automation coverage and when scripts are needed can be clearer.
- Discovery files:
  - `.github/workflows/release.yml`
  - `RELEASE.md`
  - `CHANGELOG.md`
  - `paddle/config/__init__.py`
  - `specs/007-release-workflow-version-source-and-doc-alignment.md`

## Spec Reference

- `specs/007-release-workflow-version-source-and-doc-alignment.md`

## Objectives

- Align release workflow version derivation with runtime source of truth (`paddle/config/__init__.py`).
- Preserve current tag/release idempotency and changelog-notes behavior.
- Clarify in `RELEASE.md` which CI jobs automate release tasks and when scripts should be used.
- Record the behavior/documentation update in `CHANGELOG.md` under `## [Unreleased]`.

## Scope

### In

- Update version extraction step in `.github/workflows/release.yml` to parse `__version__` from `paddle/config/__init__.py`.
- Keep release-notes extraction from `CHANGELOG.md` section for resolved version.
- Update `RELEASE.md` to document CI release jobs and script usage guidance.
- Add corresponding `CHANGELOG.md` unreleased entry.

### Out

- No changes to release-prep workflows.
- No changes to deployment commands or infra scripts.
- No changes to runtime version file contents.
- No changes to mobile release steps.

## Risks

- Risk: Regex for `__version__` extraction may fail on formatting variations.
  - Mitigation: Use tolerant pattern for whitespace around assignment.
- Risk: Documentation edits may become inconsistent with current workflow behavior.
  - Mitigation: Reflect only behavior verified in `.github/workflows/release.yml`.
- Risk: Markdownlint rule violations in updated markdown files.
  - Mitigation: Keep heading/list spacing compliant (manual checklist if CLI unavailable).

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

## Proposed Changes (Step-by-Step by File)

- `.github/workflows/release.yml`
  - Change: Replace changelog-header-based version extraction with parsing `__version__` from `paddle/config/__init__.py`.
  - Why: Use runtime version source of truth for release tagging.
  - Notes: Preserve existing `tag=v$version`, idempotent guards, and changelog notes extraction/fallback.

- `RELEASE.md`
  - Change: Add/update sections describing CI jobs involved in release automation and explicit criteria for when scripts are needed.
  - Why: Reduce ambiguity between CI-based and script-based release operations.
  - Notes: Keep existing high-level flow, only clarify ownership of steps.

- `CHANGELOG.md`
  - Change: Add `## [Unreleased]` entries for workflow source-of-truth alignment and release documentation clarification.
  - Why: Maintain changelog discipline.
  - Notes: Entry text must map directly to actual changes.

## Plan Steps (Execution Order)

- [ ] Step 1: Patch `.github/workflows/release.yml` version extraction to use `paddle/config/__init__.py`.
- [ ] Step 2: Update `RELEASE.md` to include CI-job mapping and script usage guidance.
- [ ] Step 3: Add matching unreleased changelog entry.
- [ ] Step 4: Validate changed files and diff scope.

## Acceptance Criteria (Testable)

- [ ] AC1: Workflow derives `version` from `paddle/config/__init__.py` and computes `tag=vX.Y.Z`.
- [ ] AC2: Release notes still target `CHANGELOG.md` section for that version.
- [ ] AC3: Tag/release idempotent checks remain in place.
- [ ] AC4: `RELEASE.md` clearly states CI-automated steps and when local scripts are needed.
- [ ] AC5: `CHANGELOG.md` includes aligned unreleased entries.

## Validation Commands

- `grep -n "__version__" paddle/config/__init__.py`
- `git diff -- .github/workflows/release.yml RELEASE.md CHANGELOG.md`
- `markdownlint RELEASE.md CHANGELOG.md specs/007-release-workflow-version-source-and-doc-alignment.md plans/2026-03-09_release-workflow-version-source-and-doc-alignment.md`

## Manual Functional Checks

1. Verify push to `main` resolves release tag from `paddle/config/__init__.py` version and not from changelog ordering.
2. Confirm release notes in GitHub Release still reflect the matching changelog section for that version.
3. Re-run release workflow on same version and confirm idempotent skip behavior for existing tag/release.
4. Review updated `RELEASE.md` and ensure it clearly indicates when CI already handles tagging/back-merge.
5. Confirm `RELEASE.md` script guidance indicates scripts are fallback/manual tooling when CI automation is unavailable or intentionally bypassed.

## Execution Log

- 2026-03-09 00:00 — Spec created.
- 2026-03-09 00:00 — Spec approved.
- 2026-03-09 00:00 — Plan created.

## Post-Mortem / Improvements

- What worked well:
  - Scope separation between automation logic and documentation clarified quickly.
- What caused friction:
  - Need to keep SDD stop-gates strict even for small workflow/docs changes.
- Suggested updates to:
  - `/docs/PROJECT_INSTRUCTIONS.md`: none.
  - `/AGENTS.md`: none.
  - `/plans/TEMPLATE.md`: none.
