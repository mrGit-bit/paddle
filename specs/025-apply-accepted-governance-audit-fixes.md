# Apply Accepted Governance Audit Fixes

## Tracking

- Task ID: `apply-accepted-governance-audit-fixes`
- Plan: `plans/2026-03-17_apply-accepted-governance-audit-fixes.md`
- Release tag: `v1.6.0`

## Functional Goal

Implement the accepted findings from
`.codex/audits/2026-03-17_repository-governance_audit.md` by clarifying
governance file ownership, reducing duplicated guidance, fixing the identified
coordination gaps, simplifying SDD template overhead, and aligning markdown
governance with actual `CHANGELOG.md` handling.

## Scope

### In

- Apply the accepted recommended role split from the governance audit ownership
  map.
- Apply the accepted recommended minimal fixes for findings `GF-001` through
  `GF-006`.
- Apply the accepted recommended minimal fixes for all listed coordination gaps.
- Follow the rewrite plan from the governance audit as the implementation
  sequence.
- Update the governance audit report statuses from `accepted` to `solved` only
  after the corresponding changes are implemented and re-checked.
- Update `CHANGELOG.md` under `## [Unreleased]` for the governance cleanup.

### Out

- Product application behavior changes.
- Changes to release automation scripts or GitHub workflows unless a reviewed
  documentation-only coordination point requires wording alignment.
- New governance files unless no existing file can own the responsibility
  cleanly.
- Reopening discarded or non-accepted governance findings.

## UI / UX Requirements

- Not applicable to product UI.
- Governance wording must become shorter, clearer, and easier for agents to
  consult.
- README must become a routing/orientation document rather than a release summary
  or duplicate governance checklist.

## Backend / Documentation Requirements

- `docs/PROJECT_INSTRUCTIONS.md` must become the compact authority file for
  non-negotiable repository constraints only.
- `AGENTS.md` must become the Codex execution-behavior and workflow-mechanics
  file without duplicating the compact repository-constraint content.
- `README.md` must focus on current-state repository orientation and pointers to
  the owner docs.
- `BACKLOG.md` coordination with `CHANGELOG.md` must be explicitly
  operationalized or explicitly scoped as manual. The accepted finding requires
  operationalization.
- `plans/TEMPLATE.md` must be simplified to a shorter, task-specific structure.
- Governance must define one canonical active-work discovery rule for relevant
  specs and plans.
- `CHANGELOG.md` markdownlint handling must align with stated markdown rules,
  either by removing undeclared exceptions or by documenting a single explicit
  exception centrally. The accepted fix is removal of the current undeclared
  directives if feasible within markdownlint compliance.

## Data / Config Rules

- No secrets or environment changes.
- Markdown changes must pass markdownlint with `MD013` disabled.
- `Instruction Set Version` and `Last Updated` must stay synchronized between
  `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md` if either changes.

## Reuse Rules

- Reuse the accepted governance audit findings as the sole decision basis for
  this cleanup.
- Prefer consolidation into existing files over creating new governance files.
- Reuse existing release and closure workflow docs when adding coordination
  checkpoints instead of creating parallel process documents.

## Acceptance Criteria

1. `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` have a clear, non-overlapping
   responsibility split.
2. `README.md` no longer contains changelog-style release summaries or a large
   duplicated governance checklist.
3. Governance explicitly operationalizes backlog/changelog reconciliation.
4. Governance defines one canonical active-work selector or lookup rule for
   current specs and plans.
5. `plans/TEMPLATE.md` is materially shorter and focused on task-specific
   decisions, tests, constraints, and risks.
6. `CHANGELOG.md` no longer relies on an undeclared markdownlint-disable carve-out
   that contradicts governance.
7. The accepted findings in the governance audit are updated to `solved` after
   verification.
8. `CHANGELOG.md` records the governance cleanup accurately.

## Manual Functional Checks

1. Read `docs/PROJECT_INSTRUCTIONS.md` and confirm it now contains only compact
   repository constraints and authority guidance.
2. Read `AGENTS.md` and confirm it now focuses on Codex execution behavior and
   workflow mechanics rather than repeating the compact repository constraints.
3. Read `README.md` and confirm it routes to owner docs without carrying release
   history summaries.
4. Read the updated governance/closure/release guidance and confirm backlog to
   changelog reconciliation is now an explicit operational checkpoint.
5. Read `plans/TEMPLATE.md` and confirm it is shorter and centered on task
   decisions, validation, and risks.
6. Run markdownlint on changed Markdown files and confirm there is no undeclared
   `CHANGELOG.md` carve-out left in place.

## Allowed Files

- `specs/025-apply-accepted-governance-audit-fixes.md`
- `plans/*.md`
- `.codex/audits/2026-03-17_repository-governance_audit.md`
- `AGENTS.md`
- `docs/PROJECT_INSTRUCTIONS.md`
- `README.md`
- `BACKLOG.md`
- `CHANGELOG.md`
- `RELEASE.md`
- `plans/TEMPLATE.md`

## Forbidden Files

- Product application files under `paddle/**`
- GitHub workflow files
- release automation scripts under `scripts/**`
- `.codex/skills/audit/**`
