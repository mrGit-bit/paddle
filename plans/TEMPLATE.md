# Title

Use this template for active SDD work only. Active plans use
`plans/YYYY-MM-DD_short-description.md`. After a successful tagged release and
back-merge from `main` to `develop`, consolidate the completed deployment into
`plans/release-X.Y.Z-consolidated.md`.

## Tracking

- Task ID: `short-task-id`
- Spec: `specs/###-short-title.md`
- Release tag: `unreleased`

## Summary

- Current state and why this task is needed.
- Intended outcomes.

## Key Changes

- Group the intended implementation by subsystem or behavior.
- Keep this task-specific; do not restate global governance.

## Files Allowed to Change

- List explicitly.

## Files Forbidden to Change

- List explicitly.

## Proposed Changes

- Summarize the intended changes at a high level.
- Mention files only when needed to avoid ambiguity.

## Plan Steps (Execution Order)

- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Acceptance Criteria (Testable)

- [ ] AC1
- [ ] AC2
- [ ] AC3

## Risks and Constraints

- Key risks and mitigations.
- Relevant allowed/forbidden-file constraints.

## Validation

- Commands to run, for example `pytest <targeted-scope>`.
- 3-6 manual functional checks.
