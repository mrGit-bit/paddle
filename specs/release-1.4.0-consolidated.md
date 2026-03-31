# Release 1.4.0 Consolidated Spec

## Release

- Tag: `1.4.0`
- Date: `2026-03-12`

## Sources

- `specs/007-release-workflow-version-source-and-doc-alignment.md`
- `specs/009-user-profile-edit-email-confirmation-account-deletion.md`
- `specs/010-django-view-audit-skill.md`
- `specs/011-governance-markdown-authoritative-output.md`

## Shipped Scope

- Account management moved to standard Django forms with confirmed-email
  handling and dedicated account deletion.
- Release workflow version resolution moved to
  `paddle/config/__init__.py`, with `RELEASE.md` aligned to the CI flow.
- Added the repo-local `audit` skill and governance for preserving generated
  audit output.
