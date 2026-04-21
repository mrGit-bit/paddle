# Compact Release Summary Governance

## Tracking

- Task ID: `compact-release-summary-governance`
- Status: `implemented`
- Release tag: `v1.9.2`

## Summary

- Reduce repetitive release changelog sections into compact grouped summaries.
- Make release consolidation review shipped specs, changelog notes, and backlog
  wording so final release history stays readable.

## Scope

- In:
  - Rewrite `CHANGELOG.md` sections `1.9.1` and `1.9.0` to the approved
    grouped wording.
  - Update governance and release docs for compact grouped release summaries.
  - Add deterministic release-orchestrator review support for verbose
    same-category changelog sections.
  - Add focused tests for the new review behavior.
- Out:
  - Changing the public release command interface.
  - Auto-generating semantic release prose without human review.
  - Product behavior or database changes.

## Files Allowed to Change

- `CHANGELOG.md`
- `BACKLOG.md`
- `AGENTS.md`
- `RELEASE.md`
- `docs/PROJECT_INSTRUCTIONS.md`
- `scripts/release_orchestrator.py`
- `paddle/frontend/tests/test_release_orchestrator.py`
- `specs/048-compact-release-summary-governance.md`

## Files Forbidden to Change

- Product application code.
- Database migrations.
- Existing consolidated release specs.

## Implementation Plan

- [x] Rewrite `1.9.1` and `1.9.0` release notes to the approved grouped
  summaries and add an `Unreleased` governance entry.
- [x] Update governance docs so release consolidation includes completed
  backlog wording in final grouped changelog summaries.
- [x] Add release-orchestrator changelog review helpers and print the review
  during consolidation.
- [x] Add focused unit tests and run validation commands.

## Acceptance

- [x] The two target changelog sections use the approved grouped wording.
- [x] Governance docs describe compact grouped release summaries without
  duplicating excessive detail.
- [x] Release automation reports category counts and flags verbose repeated
  categories during consolidation.
- [x] Existing release command arguments remain unchanged.

## Validation

- `python scripts/validate_governance.py`
- `pytest paddle/frontend/tests/test_release_orchestrator.py -q`
- `markdownlint CHANGELOG.md BACKLOG.md AGENTS.md RELEASE.md docs/PROJECT_INSTRUCTIONS.md specs/048-compact-release-summary-governance.md`
- Review the changed governance wording for duplication and ownership drift.
