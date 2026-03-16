# Release 1.4.1 Consolidated Plan

## Release

- Release tag: `1.4.1`
- Release date: `2026-03-14`
- Consolidation status: post-release back-merge complete

## Source Provenance

- `plans/2026-03-12_release-workflow-git-identity-and-version-check.md`
- `plans/2026-03-14_governance-ignore-markdown-line-length.md`
- `plans/2026-03-14_governance-readme-consultation-and-maintenance.md`
- `plans/2026-03-14_readme-changelog-alignment-and-codex-guidance.md`

## Objectives Summary

- Fix annotated tag creation in the release workflow by setting a deterministic
  Git identity and validating version alignment before release creation.
- Refresh `README.md` and tighten governance around Markdown line length and
  README consultation/maintenance.

## Execution Summary

### Release Workflow Reliability

- Added Git identity configuration before `git tag -a`.
- Added runtime-version versus latest released changelog-version validation.

### Repository Guidance

- Rewrote `README.md` into an up-to-date repository guide.
- Clarified Markdown line-length handling as non-blocking in governance.
- Added governance rules to consult and maintain `README.md` when relevant.

## Validation Summary

- Release workflow changes were checked with workflow-focused validation.
- README and governance updates were checked through markdownlint/manual
  Markdown review and document-alignment verification.

## Manual Functional Checks Summary

1. Confirm the release workflow would no longer fail because of missing Git
   identity during annotated tag creation.
2. Confirm a runtime/changelog version mismatch would block release creation
   before tag creation.
3. Read `README.md` and verify it reflects the current documented repository
   state.
4. Confirm governance treats Markdown line-length findings as non-blocking.
5. Confirm governance requires consulting and maintaining `README.md` when
   repository context depends on it.

## Execution Log Summary

- 2026-03-12 to 2026-03-14 — Release-workflow reliability and repository
  guidance updates were planned and completed across the source plan files
  listed above.
