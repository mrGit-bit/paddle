# Release 1.4.0 Consolidated Plan

## Release

- Release tag: `1.4.0`
- Release date: `2026-03-12`
- Consolidation status: post-release back-merge complete

## Source Provenance

- `plans/2026-03-09_release-workflow-version-source-and-doc-alignment.md`
- `plans/2026-03-10_user-profile-email-confirmation-account-deletion.md`
- `plans/2026-03-10_django-view-audit-skill.md`
- `plans/2026-03-10_governance-markdown-authoritative-output.md`

## Objectives Summary

- Align release workflow version resolution with the runtime version source and
  document the CI-driven release flow.
- Rework account management around standard form submissions, confirmed email,
  and dedicated account deletion.
- Add the repository-local `audit` skill and align governance so generated
  audit-style Markdown remains authoritative output.

## Execution Summary

### Release Workflow and Documentation

- Updated `.github/workflows/release.yml` to use
  `paddle/config/__init__.py` as the release version source.
- Kept changelog-sourced release notes and clarified release automation in
  `RELEASE.md`.
- Added the `.codex/skills/audit/` documentation bundle, checklist/reference
  files, and repository-local audit export workflow.
- Updated governance Markdown handling so generated audit content is preserved
  unless structural Markdown fixes are required.

### Account Management

- Replaced the prior JavaScript/AJAX profile-editing behavior with
  server-rendered form handling.
- Added confirmed-email validation to registration and profile editing.
- Added the dedicated account-deletion flow with `Player` unlinking.

## Validation Summary

- Release workflow changes were validated with workflow-focused checks and
  changelog/release-doc review.
- Account-management behavior was validated through targeted Django test scope
  covering profile updates, email confirmation, access restrictions, and
  account deletion behavior.
- Audit-skill and generated-Markdown-governance changes were validated through
  Markdown review, file-structure checks, and governance alignment checks.

## Manual Functional Checks Summary

1. Edit a profile and confirm standard form submission updates `username` and
   `email`.
2. Attempt registration or profile update with mismatched emails and confirm
   validation blocks the change.
3. Delete an account linked to a `Player` and confirm the user is removed while
   the player record persists.
4. Trigger the repository-local `audit` skill and confirm it is available with
   the expected repository-local audit workflow.
5. Confirm governance preserves generated audit-style Markdown lines unless a
   structural Markdown fix is required.
6. Review `RELEASE.md` and confirm the CI release flow guidance is accurate.
7. Verify release version resolution comes from `paddle/config/__init__.py`.

## Execution Log Summary

- 2026-03-09 to 2026-03-10 — Release-workflow alignment and account-management
  rework, audit-skill creation, and generated-Markdown governance updates were
  planned and completed across the source plan files listed above.
