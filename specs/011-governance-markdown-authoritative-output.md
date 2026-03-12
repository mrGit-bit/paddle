# Spec 011: Governance Rule for Generated Markdown Output

## Functional Goal

Update repository governance documents so they explicitly state that generated
text is authoritative output and, when markdownlint review is needed, it should
correct structural Markdown issues without rewriting or wrapping long generated
audit lines just to satisfy maximum line-length preferences.

## Scope

### In

- Update `docs/PROJECT_INSTRUCTIONS.md`.
- Update `AGENTS.md`.
- Add an explicit governance rule that generated text remains authoritative.
- Add an explicit Markdown validation rule for generated audit-style Markdown:
  - preserve generated long lines
  - fix structure, spacing, headings, list formatting, and similar Markdown
    correctness issues
  - do not reflow long generated evidence, recommendation, or status lines only
    for line-length linting
- Keep the wording concise, enforceable, and consistent across both governance
  files.
- Keep version/date synchronized if `docs/PROJECT_INSTRUCTIONS.md` changes.

### Out

- Product code changes.
- Skill file changes.
- Changes to unrelated repository documentation.
- Changes to test code or workflows.

## UI/UX Requirements

- Not applicable to product UI.

## Backend/Automation Requirements

- The new rule must apply to repository Markdown handling guidance.
- The rule must be compatible with existing mandatory `MD022` and `MD032`
  requirements.
- The rule must not weaken structural Markdown quality requirements.

## Data Rules

- Generated text is authoritative output.
- Structural Markdown corrections are allowed.
- Pure line-wrapping rewrites of generated audit content are not required.

## Reuse Rules

- Reuse existing governance sections instead of adding unnecessary new sections.
- Keep the new rule aligned with the existing audit-skill behavior.

## Acceptance Criteria

1. `docs/PROJECT_INSTRUCTIONS.md` states that generated text is authoritative
   output.
2. `docs/PROJECT_INSTRUCTIONS.md` states that markdownlint review should correct
   structure, not rewrite long generated audit lines to fit line-length limits.
3. `AGENTS.md` contains the same policy in consistent wording.
4. Existing Markdown structure requirements such as `MD022` and `MD032` remain
   intact.
5. `Instruction Set Version` and `Last Updated` remain synchronized between
   `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md`.

## Manual Functional Checks

1. Read both governance docs and verify the new rule appears in both files.
2. Confirm the wording still requires structural Markdown fixes where needed.
3. Confirm the wording does not require wrapping generated audit lines just for
   width.
4. Confirm both docs keep the same version/date metadata.

## Files Allowed to Change

- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`
- this spec file
- the corresponding plan file

## Files Forbidden to Change

- Product code files
- `.codex/skills/**`
- `.github/workflows/**`
- unrelated repository docs
