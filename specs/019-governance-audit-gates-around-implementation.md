# Spec 019: Add Governance Audit Gates Around Implementation

## Functional Goal

Update repository governance so the standard delivery workflow explicitly allows a spec-focused pre-audit after spec approval and before implementation planning when an audit is deemed necessary, followed by an optional scoped post-implementation audit when needed before closing the development cycle.

## Scope

### In

- Update governance documentation to recommend a spec-focused pre-audit after spec approval only when an audit is deemed necessary.
- Define that the pre-audit must stay within the approved spec scope.
- Define that accepted pre-audit findings should be solved before requesting implementation plan approval.
- Update governance documentation to recommend a scoped post-implementation audit only when needed after implementation is complete.
- Define that accepted post-implementation audit findings should be solved before stage/commit/push/closure.
- Update `README.md` if its workflow guidance should reflect the new audit gates.
- Update `CHANGELOG.md` under `## [Unreleased]` to reflect the governance/workflow change.

### Out

- Product code, tests, templates, or runtime behavior.
- Replacing the mandatory Spec -> Plan -> Implementation structure.
- Making either audit mandatory for every task.
- Changing audit report format, finding taxonomy, or audit skill content beyond what governance documentation needs to reference.

## UI/UX Requirements

- Not applicable to product UI.

## Backend/Documentation Requirements

- `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` must remain aligned on version/date if either changes.
- Governance wording must preserve the existing mandatory branch check and spec/plan approval gates.
- The updated workflow should read clearly as:
  1. request for a new spec,
  2. spec approval,
  3. spec-focused pre-audit when needed,
  4. solve accepted findings,
  5. implementation plan approval,
  6. implementation,
  7. scoped post-implementation audit when needed,
  8. solve accepted findings,
  9. close cycle,
  10. stage, commit, push.
- The documentation must distinguish between optional audit suggestions and mandatory approval gates so the workflow remains operationally clear.
- When suggesting either a pre-audit or a post-implementation audit, Codex must state why the audit is being suggested for that specific spec scope or implementation result.

## Data Rules

- `Instruction Set Version` and `Last Updated` must be updated in both governance files in the same change set if either file changes.
- `docs/PROJECT_INSTRUCTIONS.md` must remain under 8000 characters after edits.
- Existing release-consolidation governance must remain intact.

## Reuse Rules

- Reuse the existing SDD terminology and audit terminology already present in repository governance.
- Prefer minimal wording changes over rewriting whole sections.
- Reuse `README.md` only if it needs adjustment to avoid contradicting the governance docs.

## Acceptance Criteria

1. Governance docs state that after a spec is approved, a spec-focused pre-audit may be suggested before implementation planning only when an audit is deemed necessary, and the suggestion must include the reason.
2. Governance docs state that the pre-audit must stay within the approved spec scope and that accepted findings should be solved before plan approval when that audit path is used.
3. Governance docs state that after implementation, a scoped post-implementation audit may be suggested only when needed, and the suggestion must include the reason.
4. Governance docs state that accepted findings from an optional post-implementation audit should be solved before closing the development cycle when that audit path is used.
5. The documented workflow order clearly reflects spec approval -> pre-audit when needed -> solve findings -> plan approval -> implementation -> post-implementation audit when needed -> solve findings -> close/stage/commit/push.
6. `README.md`, `docs/PROJECT_INSTRUCTIONS.md`, and `AGENTS.md` do not contradict each other about the updated workflow.
7. `CHANGELOG.md` includes an `Unreleased` entry matching the governance/workflow update.

## Manual Functional Checks

1. Read the updated governance docs and confirm they still require spec approval before planning and plan approval before implementation.
2. Confirm the updated workflow says a spec-focused pre-audit is optional and should be suggested only when needed, with an explicit reason.
3. Confirm the updated workflow says accepted pre-audit findings should be solved before plan approval when that audit path is used.
4. Confirm the updated workflow says a scoped post-implementation audit is optional and should be suggested only when needed, with an explicit reason.
5. Confirm `README.md` does not conflict with the governance docs if it mentions the workflow.

## Files Allowed to Change

- `specs/019-governance-audit-gates-around-implementation.md`
- `plans/*.md`
- `plans/TEMPLATE.md`
- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`
- `README.md`
- `CHANGELOG.md`

## Files Forbidden to Change

- `paddle/**`
- `.github/workflows/**`
- release scripts
- tests
- audit skill files
