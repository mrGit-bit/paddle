# Release 1.4.0 Consolidated Plan

## Release

- Tag: `1.4.0`
- Date: `2026-03-12`

## Sources

- `plans/2026-03-09_release-workflow-version-source-and-doc-alignment.md`
- `plans/2026-03-10_user-profile-email-confirmation-account-deletion.md`
- `plans/2026-03-10_django-view-audit-skill.md`
- `plans/2026-03-10_governance-markdown-authoritative-output.md`
- Absorbed later: `plans/2026-02-28_repository_governance_docs.md`

## Execution Summary

- Moved release version sourcing to `paddle/config/__init__.py` and aligned
  release docs.
- Reworked account management around standard forms, confirmed email, and safe
  account deletion.
- Added the repo-local `audit` skill and governance for preserving generated
  audit output.

## Validation Summary

- Account-management behavior was covered by targeted Django tests.
- Release and governance changes were checked through scoped review and
  Markdown validation.
