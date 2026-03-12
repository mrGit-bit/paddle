# Spec 010: Codex Skill `audit`

## Functional Goal

Create a first repository-local Codex skill at `.codex/skills/audit/` that helps Codex audit Django views and adjacent repository architecture for project-specific governance, security, reuse, maintainability, performance, and test-coverage issues, including Django ORM inefficiency review, and export the audit into a decision-friendly Markdown report format under `.codex/audits/` that can track accepted and discarded findings.

## Scope

### In

- Create a directory-based Codex skill bundle at `.codex/skills/audit/`.
- Add a required `SKILL.md` with valid YAML front matter and clear markdown instructions.
- Add a compact supporting reference file at `.codex/skills/audit/references/audit-checklist.md`.
- Add a Markdown report template and decision-memory structure so audit findings can be accepted or discarded by the user.
- Make the skill export audit results by default into `.codex/audits/`.
- Make the skill keep audit exports repository-local and Markdown-based.
- Make the skill instructions require governance-first review of:
  - `docs/PROJECT_INSTRUCTIONS.md`
  - `AGENTS.md`
- Make the skill instruct Codex to inspect related views, forms, templates, URLs, and tests as needed.
- Add a repo-architecture review pass that inspects relevant apps, models, views, templates, JavaScript, and settings when they materially affect the audited view behavior.
- Add a performance-audit pass focused on Django ORM inefficiencies in the audited flow.
- Make the skill check for:
  - business logic in templates
  - overly large or mixed-responsibility views
  - missing ownership/access control
  - missing login protection where appropriate
  - avoidable duplicated query logic
  - weak reuse of existing helpers/forms
  - unnecessary DRF/API use or references
  - missing or weak automated test coverage
  - scope drift versus approved spec/plan when detectable
  - Spanish UI text rule violations in templates
- Make the performance-audit pass detect at least:
  - possible N+1 queries
  - missing `select_related`
  - missing indexes when reasonably inferable from common filter/order patterns
  - large queryset evaluation or premature queryset materialization
- Make the skill produce architecture findings when detected, including examples such as:
  - `Business logic detected in template: ranking_table.html`
  - `Repeated queryset logic in 3 views`
  - `JS duplication in two templates`
  - `Potential N+1 query in match list`
- Make the skill require separate output sections for:
  - Summary
  - View Audit Report
  - Architecture Review Report
  - Performance Audit Report
  - Tests to add or update
  - Open questions, only if strictly necessary
- Make each report include:
  - findings
  - severity for each finding: high / medium / low
  - evidence: file paths and short explanation
  - recommended minimal fix
- Make the skill support export into a Markdown review file where each finding can be marked at least as:
  - accepted
  - discarded
  - pending
  - solved
- Make the review file leave room for a user-written discard explanation for discarded findings.
- Make the default export location predictable enough that later audit runs can reopen and update prior review files in `.codex/audits/`.
- Make the skill instruct Codex to use prior discard explanations in future audits to avoid repeating the same finding when the explanation justifies the current state.
- Make the skill allow Codex CLI to mark accepted findings as `solved` automatically after the user explicitly requests that Codex solve all accepted reported issues and the implementation is completed.
- Make the skill instruct Codex to mark a finding as `solved` only after the corresponding change has been applied and verified as resolved in the current repository state.
- Make the skill preserve intentionally generated long lines in audit output instead of reflowing them only to satisfy markdownlint line-length preferences.
- Make markdownlint handling for audit exports prefer preserving generated audit content structure over wrapping long evidence or recommendation lines.
- Make the skill require conservative behavior for suppressed findings:
  - only suppress when a prior discard explanation clearly applies
  - surface the issue again if repository context has materially changed or the prior explanation no longer fits
- Make the skill distinguish clearly between confirmed issues, possible risks, and suggestions.

### Out

- Product code changes.
- Changes to existing Django views, templates, URLs, forms, or tests.
- Changes to unrelated repository files.
- Skill installer metadata such as `agents/openai.yaml`.
- Automatic persistence outside the repository.

## UI/UX Requirements

- Not applicable to product UI.
- When the skill refers to user-facing product copy rules, it must preserve the project requirement that UI text is in Spanish.

## Backend Requirements

- The skill must remain instructions-only and operate as repository documentation for Codex.
- The architecture-review pass must stay audit-focused.
- The performance-audit pass must stay static-analysis-oriented unless the task explicitly asks for runtime profiling.
- The review workflow must stay Markdown-based and repository-local.
- Default audit exports must live under `.codex/audits/`.
- Automatic `solved` transitions must remain tied to explicit user intent and verified repository changes.

## Data Rules

- Documentation inside the skill must be in English.
- References to product UI text must use Spanish only when describing the project rule.
- The skill must remain explicit, reusable, concise, and governance-aligned.
- Decision tracking must remain easy to edit manually by the user.
- Generated audit readability must not depend on forced line wrapping.

## Reuse Rules

- Reuse repository governance language and existing project constraints rather than inventing new policy.
- Keep the checklist compact and move detailed operational guidance into `SKILL.md`.
- Avoid duplicating large blocks of governance text; reference the relevant governance files directly.
- Keep the review-file workflow minimal and avoid adding scripts unless explicitly requested later.
- Keep the audit export path stable and repository-local unless the user explicitly asks for another location.
- Preserve generated audit lines unless a markdown fix is required for structure rather than width.

## Acceptance Criteria

1. `.codex/skills/audit/SKILL.md` exists with valid YAML front matter containing:
   - `name: audit`
   - `description: Audit Django views for project governance, security, reuse, and maintainability issues.`
2. `SKILL.md` instructs Codex to read `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` first.
3. `SKILL.md` instructs Codex to inspect views, related forms, templates, URLs, and tests as needed.
4. `SKILL.md` instructs Codex to include a repo-architecture review over relevant apps, models, views, templates, JavaScript, and settings when applicable.
5. `SKILL.md` instructs Codex to perform a performance audit for Django ORM inefficiencies.
6. `SKILL.md` includes the full required audit issue list from the task brief.
7. `SKILL.md` defines the required audit output structure from the task brief with separate sections for `View Audit Report`, `Architecture Review Report`, and `Performance Audit Report`.
8. `SKILL.md` instructs Codex to prefer minimal, governance-compliant recommendations and avoid speculative refactors or unrelated cleanup.
9. `SKILL.md` clearly separates confirmed issues, possible risks, and suggestions.
10. The skill defines a Markdown export format for audit review with per-finding status fields for `accepted`, `discarded`, `pending`, and `solved`.
11. The skill defines a place for a user-written discard explanation and instructs Codex to consult it in later audits before repeating a discarded finding.
12. The skill instructs Codex CLI to mark accepted findings as `solved` automatically only after the user requests implementation of accepted issues and the corresponding fixes are completed and verified.
13. The skill exports reviewable audit Markdown files by default under `.codex/audits/`.
14. The skill preserves intentionally generated long lines in audit exports instead of reflowing them for markdownlint line-length cleanup.
15. `.codex/skills/audit/references/audit-checklist.md` exists and includes concise sections for:
   - Access control
   - View responsibility
   - Query efficiency / duplication
   - Performance / ORM efficiency
   - Reuse of forms/helpers
   - Template boundary enforcement
   - Tests
   - Governance compliance

## Manual Functional Checks

1. Trigger the skill by name and verify Codex recognizes `.codex/skills/audit/SKILL.md`.
2. Ask Codex to audit a Django view module and verify it reads governance files before reporting findings.
3. Ask Codex to perform a repo-architecture review and verify it can report architecture findings across apps, models, views, templates, JavaScript, and settings when relevant.
4. Ask Codex to run the performance-audit pass and verify it can report likely ORM issues such as N+1 risks, missing `select_related`, missing indexes, or large queryset evaluation.
5. Verify the skill output uses the required sections and includes severity plus evidence for each finding.
6. Verify the skill distinguishes confirmed issues from possible risks and suggestions.
7. Export an audit to Markdown and verify findings can be marked `accepted`, `discarded`, or `pending`.
8. Add a discard explanation for one finding, rerun the audit, and verify Codex does not repeat that finding when the explanation still clearly applies.
9. Request that Codex solve all accepted issues, complete the fixes, and verify the corresponding accepted findings are marked `solved`.
10. Run the skill normally and verify it exports the audit result into `.codex/audits/` without needing an extra export instruction.
11. Generate an audit with long evidence lines and verify markdown cleanup preserves those lines instead of wrapping them.
12. Verify the skill does not propose unrelated refactors when a smaller compliant fix exists.

## Test Expectations

- No automated product tests are required for this instructions-only skill.
- Validation should focus on:
  - correct file placement
  - markdown structure
  - required front matter
  - alignment with repository governance
  - usable Markdown decision workflow for future audits

## Files Allowed to Change

- `.codex/skills/audit/SKILL.md`
- `.codex/skills/audit/references/audit-checklist.md`
- a Markdown template or reference file under `.codex/skills/audit/` if needed for the review export workflow
- Markdown audit files under `.codex/audits/`
- `CHANGELOG.md` if governance requires documenting this repository behavior change
- this spec file
- the corresponding plan file

## Files Forbidden to Change

- Product code files
- Existing Django app logic, templates, URLs, forms, or tests
- Unrelated documentation or governance files
- Any skill scripts or auxiliary files beyond the requested structure
