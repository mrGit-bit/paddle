# Release 1.4.1 Consolidated Spec

## Release

- Release tag: `1.4.1`
- Release date: `2026-03-14`
- Consolidation status: post-release back-merge complete

## Source Provenance

- `specs/012-release-workflow-git-identity.md`
- `specs/013-readme-changelog-alignment-and-codex-guidance.md`
- `specs/014-governance-ignore-markdown-line-length.md`
- `specs/015-governance-check-readme-when-necessary.md`

## Functional Goal

Preserve the approved SDD scope for the `1.4.1` deployment in one release-level
spec after release completion, covering the release-workflow Git identity fix,
the README refresh, and the governance updates shipped in that release.

## Release Scope Summary

### Release Workflow Reliability

- Configure a deterministic Git identity before annotated tag creation in the
  production release workflow.
- Validate that `paddle/config/__init__.py` matches the latest released version
  in `CHANGELOG.md` before release-note extraction or tag creation.

### Repository Guidance

- Refresh `README.md` so it reflects the current documented project state and
  gives high-signal repository guidance for Codex CLI work.
- Clarify that Markdown line-length findings are non-blocking and long lines
  should not be wrapped only for line-length linting.
- Clarify that contributors consult `README.md` when repository context is
  needed and keep it updated when README-covered guidance changes.

## Acceptance Criteria Summary

1. The release workflow can create annotated release tags without the prior Git
   identity failure.
2. The release workflow verifies runtime version and latest released changelog
   version alignment before release creation.
3. `README.md` reflects the current documented project state and repository
   guidance relevant to agents and contributors.
4. Governance documents treat `MD013` findings as non-blocking and preserve
   long authoritative lines.
5. Governance documents require consulting and maintaining `README.md` when it
   is the relevant repository-context source.

## Manual Functional Checks Summary

1. Review the release workflow behavior and confirm annotated tags no longer
   fail because of missing Git identity.
2. Confirm version mismatch between runtime config and the latest released
   changelog header would fail before tag creation.
3. Read `README.md` and verify it matches the current documented project state.
4. Read `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md` and confirm they keep
   Markdown line-length findings non-blocking.
5. Read the governance files and confirm they instruct contributors to consult
   and maintain `README.md` when relevant.

## Notes

- Unreleased work after `1.4.1`, including changelog backfill/governance
  clarification and later consolidation governance, remains separate.
