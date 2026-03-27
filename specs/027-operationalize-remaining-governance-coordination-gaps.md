# Operationalize Remaining Governance Coordination Gaps

## Tracking

- Task ID: `operationalize-remaining-governance-coordination-gaps`
- Plan: `plans/2026-03-26_operationalize-remaining-governance-coordination-gaps.md`
- Release tag: `v1.6.0`

## Functional Goal

Resolve the remaining pending findings in
`.codex/audits/2026-03-17_repository-governance_audit.md` by making backlog
reconciliation ownership explicit, making active spec/plan pairing inspectable
without filename inference, and making release-consolidation selection depend
on explicit release provenance instead of sweeping all loose non-release SDD
artifacts.

## Scope

### In

- Choose and document one workflow owner for backlog reconciliation.
- Remove any release-flow promises that the live automation does not actually
  own after that owner decision.
- Add lightweight tracking metadata to loose non-release specs and plans so a
  spec-plan pair can be identified directly from the files.
- Backfill the current loose non-release spec and plan files with the new
  tracking metadata.
- Update the release orchestrator so consolidation only includes loose
  spec/plan files explicitly marked for the requested release tag.
- Add targeted tests for the new release-provenance parsing and consolidation
  selection behavior.
- Update the governance audit report so findings `GF-003`, `GF-005`, and
  `GF-007` move to `solved` only after the implementation is verified.
- Update governance docs and `CHANGELOG.md` to reflect the new operational
  rules.

### Out

- Product application behavior changes unrelated to governance or release
  automation.
- GitHub workflow rewrites.
- New long-form governance files unless no existing file has a clean ownership
  fit.
- Automatic interpretation of backlog scope from arbitrary prose in
  `BACKLOG.md`.

## UI / UX Requirements

- Governance wording stays concise and agent-readable.
- Release output remains focused on the script report.
- If no loose specs/plans are explicitly marked for the release tag, the
  release flow must not guess. It should leave loose files untouched and report
  that no release-tagged artifacts were selected.

## Backend / Automation Requirements

- Backlog reconciliation ownership must be explicit in governance and must not
  be promised by `RELEASE.md` unless the automation actually performs it.
- Loose non-release specs and plans must expose:
  - a stable task identifier
  - the matching plan/spec reference
  - a release provenance marker
- Release-consolidation selection in `scripts/release_orchestrator.py` must use
  explicit release provenance markers, not body-text heuristics and not “all
  loose files”.
- The orchestrator must preserve the existing safe behavior of skipping
  consolidation when no release-tagged files match the requested version.

## Reuse Rules

- Reuse the existing governance audit file as the status-tracking surface for
  these findings.
- Reuse current spec and plan files by adding tracking metadata rather than
  inventing a separate active-work index.
- Reuse `plans/TEMPLATE.md` for the plan-side tracking pattern.

## Acceptance Criteria

1. Governance clearly assigns backlog reconciliation to one owner and no longer
   implies that `/prompts:release` performs it if the script does not.
2. Loose non-release specs and plans expose enough metadata to identify the
   intended spec-plan pair without filename inference alone.
3. The release orchestrator consolidates only loose non-release specs/plans
   explicitly marked with the requested release tag.
4. The release orchestrator leaves loose files untouched when no files are
   marked for the requested release tag.
5. Focused regression tests cover release-provenance parsing and tagged
   consolidation selection.
6. Findings `GF-003`, `GF-005`, and `GF-007` in the governance audit are marked
   `solved` only after implementation and verification.

## Manual Functional Checks

1. Read `AGENTS.md`, `docs/PROJECT_INSTRUCTIONS.md`, `BACKLOG.md`, and
   `RELEASE.md` and confirm backlog reconciliation has one explicit owner.
2. Open a loose spec and its matching loose plan and confirm each exposes task
   tracking and cross-reference metadata.
3. Run the release-orchestrator tests and confirm consolidation selection uses
   explicit release tags.
4. Simulate a release where no loose files carry the requested release tag and
   confirm consolidation is skipped without deleting unrelated files.

## Allowed Files

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

## Forbidden Files

- `.github/workflows/*`
- Product app code unrelated to governance or release automation
- SSH private keys or repo-local SSH secrets
