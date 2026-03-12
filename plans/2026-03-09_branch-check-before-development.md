# Mandatory Branch Check Before Development Work Plan

## Context

- User requested a governance rule requiring branch verification before starting development tasks.
- Current instructions do not consistently enforce a pre-implementation active-branch check with explicit user confirmation when branch is not `develop`.
- Discovery files:
  - `AGENTS.md`
  - `docs/PROJECT_INSTRUCTIONS.md`
  - `specs/008-branch-check-before-development.md`

## Spec Reference

- `specs/008-branch-check-before-development.md`

## Objectives

- Add explicit, mandatory branch-check instructions to both governance documents.
- Ensure wording clearly requires:
  - checking current branch before development work,
  - warning when branch is not `develop`,
  - asking user explicitly which branch to apply changes on.

## Scope

### In

- Update `AGENTS.md` with mandatory branch-check rule.
- Update `docs/PROJECT_INSTRUCTIONS.md` with the same rule.
- Keep wording aligned across both files.

### Out

- No product code edits.
- No CI/workflow changes.
- No branch renaming or strategy changes.

## Risks

- Risk: Rule text could conflict with existing authority hierarchy or SDD flow.
  - Mitigation: Add as operational pre-check before implementation without altering hierarchy.
- Risk: Inconsistent wording between files could cause ambiguity.
  - Mitigation: Use the same core rule text in both files.

## Files Allowed to Change

- `AGENTS.md`
- `docs/PROJECT_INSTRUCTIONS.md`

## Files Forbidden to Change

- `.github/workflows/**`
- `paddle/**`
- `mobile/**`
- `CHANGELOG.md`

## Proposed Changes (Step-by-Step by File)

- `AGENTS.md`
  - Change: Add mandatory pre-development branch-check rule under workflow/governance instructions.
  - Why: Enforce consistent branch safety behavior in Codex execution.
  - Notes: Include explicit warning + branch confirmation requirement when not on `develop`.

- `docs/PROJECT_INSTRUCTIONS.md`
  - Change: Add matching mandatory branch-check rule in governance/workflow section.
  - Why: Keep project-level and Codex-level instructions aligned.
  - Notes: Preserve existing authority/SDD sections and only add targeted rule text.

## Plan Steps (Execution Order)

- [ ] Step 1: Insert branch-check rule in `AGENTS.md`.
- [ ] Step 2: Insert aligned branch-check rule in `docs/PROJECT_INSTRUCTIONS.md`.
- [ ] Step 3: Validate markdown spacing/compliance and diff scope.

## Acceptance Criteria (Testable)

- [ ] AC1: `AGENTS.md` explicitly requires branch check before development work.
- [ ] AC2: `docs/PROJECT_INSTRUCTIONS.md` explicitly requires branch check before development work.
- [ ] AC3: Both files explicitly require warning + explicit user branch choice when current branch is not `develop`.

## Validation Commands

- `git diff -- AGENTS.md docs/PROJECT_INSTRUCTIONS.md`
- `markdownlint AGENTS.md docs/PROJECT_INSTRUCTIONS.md specs/008-branch-check-before-development.md plans/2026-03-09_branch-check-before-development.md`

## Manual Functional Checks

1. Read updated `AGENTS.md` and confirm the rule mandates branch verification before development.
2. Read updated `docs/PROJECT_INSTRUCTIONS.md` and confirm identical operational behavior.
3. Confirm both files explicitly state warning + explicit user branch question when branch is not `develop`.
4. Confirm no unrelated instruction content changed.

## Execution Log

- 2026-03-09 00:00 — Spec created.
- 2026-03-09 00:00 — Spec approved.
- 2026-03-09 00:00 — Plan created.

## Post-Mortem / Improvements

- What worked well:
  - Requirement was precise and directly translatable into governance text.
- What caused friction:
  - SDD stop gates require extra cycle even for small markdown governance updates.
- Suggested updates to:
  - `/docs/PROJECT_INSTRUCTIONS.md`: none beyond requested change.
  - `/AGENTS.md`: none beyond requested change.
  - `/plans/TEMPLATE.md`: none.
