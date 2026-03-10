# Governance Markdown Authoritative Output

## Context

- Repository governance already defines mandatory Markdown structure checks in
  `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md`.
- The audit skill now treats generated audit text as authoritative output and
  preserves long generated lines instead of reflowing them for markdownlint
  width preferences.
- Governance documents should reflect the same rule so repository-wide Markdown
  handling stays consistent.

## Spec Reference

- Exact spec file:
  - `specs/011-governance-markdown-authoritative-output.md`

## Objectives

- Add an explicit governance rule that generated text is authoritative output.
- Clarify that markdown review should fix structural Markdown issues without
  rewriting or wrapping long generated audit lines purely for line-length
  compliance.
- Keep `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` synchronized.

## Scope

### In

- Update `docs/PROJECT_INSTRUCTIONS.md`.
- Update `AGENTS.md`.
- Keep version/date metadata synchronized.
- Validate changed Markdown files.

### Out

- Product code changes.
- Skill changes.
- Unrelated documentation updates.
- Test or workflow changes.

## Risks

- Risk: The new wording could be read as weakening Markdown quality rules.
  - Mitigation: keep the rule explicitly limited to generated text and preserve
    structural Markdown requirements.
- Risk: `docs/PROJECT_INSTRUCTIONS.md` could drift above its size limit.
  - Mitigation: edit in place with concise wording and re-check file size.

## Files Allowed to Change

- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`

## Files Forbidden to Change

- Product code files
- `.codex/skills/**`
- `.github/workflows/**`
- unrelated repository docs

## Proposed Changes (Step-by-Step by File)

- `docs/PROJECT_INSTRUCTIONS.md`
  - Change: add concise governance wording in the Markdown rules/validation area
    stating that generated text is authoritative output and that markdown review
    should correct structure rather than wrap long generated audit lines for
    line-length compliance.
  - Why: this file is the higher-precedence repository governance source.
  - Notes: keep the file under the 8000-character limit.

- `AGENTS.md`
  - Change: add matching wording in the Markdownlint rules section.
  - Why: keep Codex-specific repository instructions aligned with project
    governance.
  - Notes: mirror the project-doc wording closely without unnecessary churn.

## Plan Steps (Execution Order)

- [ ] Step 1: Update `docs/PROJECT_INSTRUCTIONS.md` with the new authoritative
  generated-text Markdown rule.
- [ ] Step 2: Update `AGENTS.md` with matching wording.
- [ ] Step 3: Synchronize version/date metadata across both files.
- [ ] Step 4: Validate Markdown structure and confirm
  `docs/PROJECT_INSTRUCTIONS.md` remains under its size limit.

## Acceptance Criteria (Testable)

- [ ] AC1: `docs/PROJECT_INSTRUCTIONS.md` states that generated text is
  authoritative output.
- [ ] AC2: `docs/PROJECT_INSTRUCTIONS.md` states that Markdown review should fix
  structure, not wrap long generated audit lines for width.
- [ ] AC3: `AGENTS.md` contains the same policy in consistent wording.
- [ ] AC4: Existing `MD022` and `MD032` requirements remain present.
- [ ] AC5: `Instruction Set Version` and `Last Updated` stay synchronized
  between the two files.
- [ ] AC6: `docs/PROJECT_INSTRUCTIONS.md` remains under 8000 characters.

## Validation Commands

- `wc -c docs/PROJECT_INSTRUCTIONS.md AGENTS.md`
- `markdownlint docs/PROJECT_INSTRUCTIONS.md AGENTS.md`

## Manual Functional Checks

1. Read both files and verify the new rule appears in both.
2. Confirm the rule preserves structural Markdown enforcement.
3. Confirm the rule does not require wrapping long generated audit lines for
   width.
4. Confirm the version/date metadata matches.

## Execution Log

- 2026-03-10 00:00 — Spec created.
- 2026-03-10 00:00 — Spec approved.
- 2026-03-10 00:00 — Plan created.

## Post-Mortem / Improvements

- What worked well:
  - The audit-skill rule provided a clear repository governance policy to mirror.
- What caused friction:
  - Governance updates require full spec/plan gating even for concise doc-only
    changes.
