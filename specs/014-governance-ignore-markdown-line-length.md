# Spec 014: Governance Ignore Markdown Line Length

## Functional Goal

Update the repository governance documents so long Markdown lines are not
treated as violations and authors do not wrap long lines into multiple lines
only to satisfy line-length linting.

## Scope

### In

- Update Markdown-governance language in `docs/PROJECT_INSTRUCTIONS.md`.
- Update matching Markdown-governance language in `AGENTS.md`.
- Keep version/date metadata synchronized across both governance files in the
  same change set.
- Preserve the existing mandatory Markdown structure rules for `MD022` and
  `MD032`.

### Out

- Changes to product code, tests, workflows, or runtime behavior.
- Changes to spec/plan workflow beyond the specific Markdown line-length rule.
- Changes to other documentation files unless needed for this task’s required
  spec and plan.

## UI/UX Requirements

- Not applicable to product UI.

## Backend/Documentation Requirements

- Governance must explicitly state that long lines are acceptable.
- Governance must explicitly state that long lines should remain single-line
  when that preserves authoritative generated text or readability.
- Governance must continue requiring markdownlint validation where available,
  while not treating line length as a blocking violation.
- The wording in `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` must stay
  aligned.

## Data Rules

- `docs/PROJECT_INSTRUCTIONS.md` overrides `AGENTS.md`, so both files must say
  the same thing for Markdown line-length handling.
- `Instruction Set Version` and `Last Updated` must match across the two files
  after the change.

## Reuse Rules

- Reuse the existing Markdown-rules sections in both governance files instead
  of creating new policy sections.
- Keep edits minimal and localized to the Markdown-governance wording and
  synchronized metadata.

## Acceptance Criteria

1. `docs/PROJECT_INSTRUCTIONS.md` states that long Markdown lines are not
   treated as violations.
2. `AGENTS.md` states the same Markdown line-length policy.
3. Both governance files explicitly instruct authors not to wrap long lines
   into multiple lines solely for line-length linting.
4. `Instruction Set Version` and `Last Updated` remain synchronized between the
   two governance files.
5. The change does not alter the mandatory `MD022` and `MD032` requirements.

## Manual Functional Checks

1. Read the Markdown-rules sections in both governance files and confirm they
   allow long lines without treating them as blocking violations.
2. Confirm both files instruct authors to leave long authoritative lines on one
   line instead of manually wrapping them for line-length reasons.
3. Confirm the version/date metadata is identical in both governance files
   after the update.
4. Confirm the rules still require `MD022` and `MD032` compliance.

## Files Allowed to Change

- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`
- this spec file
- the corresponding plan file

## Files Forbidden to Change

- `CHANGELOG.md`
- application code under `paddle/**`
- GitHub workflows
- test files
- unrelated documentation
