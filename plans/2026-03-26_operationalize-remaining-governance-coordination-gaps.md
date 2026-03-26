# Operationalize Remaining Governance Coordination Gaps Plan

## Tracking

- Task ID: `operationalize-remaining-governance-coordination-gaps`
- Spec: `specs/027-operationalize-remaining-governance-coordination-gaps.md`
- Release tag: `v1.6.0`

## Spec Reference

- `specs/027-operationalize-remaining-governance-coordination-gaps.md`

## Summary

- The repository governance audit still has three pending findings:
  backlog-reconciliation ownership, active spec/plan lookup ambiguity, and
  unsafe release-consolidation provenance.
- The live repository now needs an explicit operational rule set instead of
  more prose about what “should” happen.

## Key Changes

- Assign backlog reconciliation to development-cycle closure and remove any
  release-flow wording that incorrectly promises it.
- Add compact tracking metadata to loose specs and plans:
  - task identifier
  - matching spec/plan reference
  - release tag
- Backfill the current loose non-release SDD files with that metadata.
- Change release consolidation to select only loose spec/plan files whose
  release tag matches the requested version.
- Update the governance audit statuses after the changes are verified.

## Files Allowed to Change

- `specs/027-operationalize-remaining-governance-coordination-gaps.md`
- `plans/2026-03-26_operationalize-remaining-governance-coordination-gaps.md`
- `.codex/audits/2026-03-17_repository-governance_audit.md`
- `AGENTS.md`
- `docs/PROJECT_INSTRUCTIONS.md`
- `README.md`
- `BACKLOG.md`
- `RELEASE.md`
- `CHANGELOG.md`
- `plans/TEMPLATE.md`
- `specs/[0-9][0-9][0-9]-*.md`
- `plans/20*.md`
- `scripts/release_orchestrator.py`
- `paddle/frontend/tests/test_release_orchestrator.py`

## Files Forbidden to Change

- `.github/workflows/*`
- Product files outside the governance/release-automation scope
- Secret-bearing SSH files

## Proposed Changes

- Update governance wording so backlog reconciliation is mandatory at
  development-cycle closure and is not claimed as part of `/prompts:release`.
- Introduce a compact `Tracking` section in loose specs and plans and backfill
  the current non-release files.
- Update `plans/TEMPLATE.md` to preserve the tracking pattern for future work.
- Parse release-tag metadata in `scripts/release_orchestrator.py` and select
  only matching loose files for consolidation.
- Extend the targeted release-orchestrator tests and update the audit file to
  mark the three accepted findings as solved.

## Plan Steps (Execution Order)

- [ ] Create and approve the active spec and plan for these governance fixes.
- [ ] Patch governance docs to assign backlog-reconciliation ownership and align
      release documentation.
- [ ] Add and backfill spec/plan tracking metadata across the current loose
      non-release artifacts.
- [ ] Patch release-consolidation selection and add focused regression tests.
- [ ] Update the governance audit statuses and `CHANGELOG.md`.
- [ ] Run targeted validation for the changed automation and Markdown files.

## Acceptance Criteria (Testable)

- [ ] Governance no longer claims that release automation owns backlog
      reconciliation unless the automation actually performs it.
- [ ] Current loose non-release specs and plans expose explicit task and pairing
      metadata.
- [ ] Consolidation selection uses only explicit release tags.
- [ ] The release-orchestrator test suite passes.
- [ ] Findings `GF-003`, `GF-005`, and `GF-007` are updated to `solved` after
      verification.

## Risks and Constraints

- Backfilling many spec/plan files can create noisy Markdown changes.
  Mitigation: keep the new tracking block compact and mechanically consistent.
- Release-tag metadata can drift if it is not part of the normal artifact
  workflow.
  Mitigation: add the pattern to templates and governance wording, and keep the
  release script strict about explicit tags.
- Removing release-flow promises may change operator expectations.
  Mitigation: update `RELEASE.md` and the governance docs in the same change
  set.

## Validation

- `pytest paddle/frontend/tests/test_release_orchestrator.py -q`
- `python -m markdownlint-cli2 AGENTS.md docs/PROJECT_INSTRUCTIONS.md README.md BACKLOG.md RELEASE.md CHANGELOG.md plans/TEMPLATE.md specs/027-operationalize-remaining-governance-coordination-gaps.md plans/2026-03-26_operationalize-remaining-governance-coordination-gaps.md`

- Manual functional checks:
- Confirm backlog-reconciliation ownership is consistent across governance and
  release docs.
- Confirm a loose spec and loose plan show the same task identifier and
  cross-reference each other.
- Confirm release consolidation ignores loose files marked `unreleased`.
- Confirm the audit report marks only the fixed findings as `solved`.
