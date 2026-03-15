# Title

Use this template for active SDD work only. Active plans use
`plans/YYYY-MM-DD_short-description.md`. After a successful tagged release and
back-merge from `main` to `develop`, consolidate the completed deployment into
`plans/release-X.Y.Z-consolidated.md`.

## Context

- Current state and why this task is needed.
- Files/components that will be read first (discovery list).

## Spec Reference

- Link the exact active spec file:
  - `specs/###-short-title.md`

## Objectives

- Intended outcomes (measurable).

## Scope

### In

- Explicitly included items.

### Out

- Explicit exclusions.

## Risks

- Key risks and mitigations.

## Files Allowed to Change

- List explicitly.

## Files Forbidden to Change

- List explicitly.

## Proposed Changes (Step-by-Step by File)

For each file, describe the intended change at a high level. Do not include
product code in Plan Mode.

Example structure:

- `path/to/file.py`
  - Change:
  - Why:
  - Notes:

## Plan Steps (Execution Order)

- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Acceptance Criteria (Testable)

- [ ] AC1
- [ ] AC2
- [ ] AC3

## Validation Commands

- `pytest <targeted-scope>`
- Add other commands only if required.

## Manual Functional Checks

1. Check 1
2. Check 2
3. Check 3

## Execution Log

- YYYY-MM-DD HH:MM — Spec created.
- YYYY-MM-DD HH:MM — Spec approved.
- YYYY-MM-DD HH:MM — Plan created.
- YYYY-MM-DD HH:MM — Plan approved.
- YYYY-MM-DD HH:MM — Implementation started.
- YYYY-MM-DD HH:MM — Tests executed.
- YYYY-MM-DD HH:MM — Implementation approved.
- YYYY-MM-DD HH:MM — Governance changed (if needed).

## Post-Mortem / Improvements

- What worked well
- What caused friction
- Suggested updates to:
  - `/docs/PROJECT_INSTRUCTIONS.md`
  - `/AGENTS.md`
  - `/plans/TEMPLATE.md`
