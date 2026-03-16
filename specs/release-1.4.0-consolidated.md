# Release 1.4.0 Consolidated Spec

## Release

- Release tag: `1.4.0`
- Release date: `2026-03-12`
- Consolidation status: post-release back-merge complete

## Source Provenance

- `specs/007-release-workflow-version-source-and-doc-alignment.md`
- `specs/009-user-profile-edit-email-confirmation-account-deletion.md`
- `specs/010-django-view-audit-skill.md`
- `specs/011-governance-markdown-authoritative-output.md`

## Functional Goal

Preserve the approved SDD scope for the `1.4.0` deployment in one release-level
spec after release completion, covering the release workflow version-source
alignment, the account-management rework, the repository-local `audit` skill,
and the generated-Markdown governance rule shipped in that release.

## Release Scope Summary

### Account Management

- Allow authenticated users to edit `username` and `email` through standard
  Django form submissions.
- Require confirmed email entry in registration and profile editing using
  normalized comparison rules.
- Replace the JavaScript-driven profile-editing flow with a server-rendered
  form flow.
- Add a dedicated account-deletion confirmation path that unlinks any related
  `Player`, deletes the `User`, logs the user out, and redirects home with the
  released goodbye flow.

### Release Workflow and Documentation

- Make `.github/workflows/release.yml` derive the release version from
  `paddle/config/__init__.py`.
- Keep release notes sourced from the matching `CHANGELOG.md` section.
- Update `RELEASE.md` to describe the current CI release jobs and when the
  helper scripts are only fallback tools.
- Create the repository-local `.codex/skills/audit/` skill bundle so Codex can
  perform governance-aware Django view, architecture, and ORM performance
  audits with reviewable Markdown exports under `.codex/audits/`.
- Update governance so generated audit text remains authoritative output and
  Markdown review fixes structure without reflowing long generated lines only
  for line-length preferences.

## Acceptance Criteria Summary

1. Users can manage their own profile through standard Django form handling
   without the prior JavaScript/AJAX editing path.
2. Registration and profile editing enforce confirmed email rules using the
   approved normalization behavior.
3. Account deletion preserves linked `Player` history by unlinking before user
   deletion.
4. The release workflow reads `__version__` from `paddle/config/__init__.py`
   and still generates release notes from the matching changelog section.
5. The repository includes the `audit` skill with its required governance-first
   audit flow, review states, and repository-local audit export behavior.
6. Governance states that generated audit-style Markdown remains authoritative
   output and should not be reflowed only for line-length linting.
7. Release documentation reflects the CI-driven release flow and helper-script
   fallback usage.

## Manual Functional Checks Summary

1. Edit a user profile and confirm `username` and `email` updates go through the
   standard form flow.
2. Register or edit a profile with mismatched emails and confirm validation
   blocks submission.
3. Delete an account linked to a `Player` and confirm the user is removed while
   the player history remains intact.
4. Trigger the repository-local `audit` skill and confirm it is available with
   the expected repository-local references and audit-export workflow.
5. Read the governance docs and confirm generated audit-style Markdown remains
   authoritative output without forced line wrapping for width.
6. Review `RELEASE.md` and confirm it matches the release workflow behavior for
   `1.4.0`.
7. Verify release version resolution comes from `paddle/config/__init__.py`.

## Notes

- Unreleased governance/documentation work created after `1.4.0` is not part
  of this consolidated artifact.
