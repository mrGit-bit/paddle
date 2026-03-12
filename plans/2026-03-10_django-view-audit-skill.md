# Audit Skill

## Context

- The repository currently has no local `.codex/skills/` directory, so the new skill must establish the requested directory structure from scratch.
- Repository governance requires skill work to follow spec approval before planning and implementation.
- The approved spec is [specs/010-django-view-audit-skill.md](/workspaces/paddle/specs/010-django-view-audit-skill.md).
- The requested skill is instructions-only, with no scripts, no product code changes, and no unrelated documentation churn.
- The skill must remain aligned with:
  - `docs/PROJECT_INSTRUCTIONS.md`
  - `AGENTS.md`
  - the system `skill-creator` guidance already available in the environment

## Spec Reference

- Exact spec file:
  - `specs/010-django-view-audit-skill.md`

## Objectives

- Create a reusable repository-local Codex skill named `audit`.
- Ensure the skill instructs Codex to perform three bounded audit passes:
  - Django view audit
  - repo-architecture review
  - Django ORM performance audit
- Keep the skill concise, governance-compliant, and explicitly structured around minimal-fix recommendations with three separate reports.
- Add a Markdown review workflow so findings can be tracked as `pending`, `accepted`, `discarded`, or `solved`.
- Export audit results by default into `.codex/audits/`.
- Allow future audits to consult user-written discard explanations to avoid repeating justified discarded findings.
- Allow Codex CLI to mark accepted findings as `solved` automatically only after the user requests implementation of accepted issues and the fixes are completed and verified.
- Preserve intentionally generated long lines in audit exports instead of reflowing them just to satisfy markdownlint line-length preferences.

## Scope

### In

- Create:
  - `.codex/skills/audit/SKILL.md`
  - `.codex/skills/audit/references/audit-checklist.md`
- Add valid YAML front matter in `SKILL.md`.
- Add operational instructions for governance-first reading, audit targets, issue categories, output format, and reporting boundaries.
- Add a compact supporting checklist with the required sections, including performance/ORM efficiency.
- Add a Markdown review/export workflow for tracked findings and user decisions.
- Add the default repository-local export location under `.codex/audits/`.
- Preserve generated audit content lines unless a markdown fix is needed for structure rather than width.
- Validate markdown formatting on the new files.

### Out

- Product code changes.
- Skill scripts or automation helpers.
- Changes to existing app code, templates, tests, settings, or URLs.
- Changes to unrelated governance files.
- Additional skill metadata files such as `agents/openai.yaml`.

## Risks

- Risk: The skill becomes too broad and drifts into architecture redesign guidance instead of focused audit behavior.
  - Mitigation: keep recommendations explicitly minimal, evidence-based, and scoped to confirmed findings or clearly labeled risks.
- Risk: The skill duplicates repository governance text and becomes harder to maintain.
  - Mitigation: instruct the skill to read governance files first instead of embedding large policy blocks.
- Risk: The performance section overstates certainty from static analysis.
  - Mitigation: require clear distinction between confirmed issues, possible risks, and suggestions.
- Risk: Decision-memory rules could suppress valid findings too aggressively.
  - Mitigation: only suppress discarded findings when the stored explanation clearly matches the current repository state, and re-surface them if context materially changes.
- Risk: `solved` state could be marked prematurely.
  - Mitigation: require explicit user request plus verified repository changes before Codex marks an accepted finding as solved.
- Risk: markdownlint cleanup can distort generated audit readability.
  - Mitigation: preserve long generated lines in audit exports and fix only structural markdown issues.

## Files Allowed to Change

- `.codex/skills/audit/SKILL.md`
- `.codex/skills/audit/references/audit-checklist.md`
- an additional Markdown reference/template file under `.codex/skills/audit/` if needed for the review workflow
- Markdown audit output files under `.codex/audits/`
- `CHANGELOG.md` only if required by the approved implementation scope

## Files Forbidden to Change

- Product code files
- Existing Django apps, templates, tests, forms, URLs, settings, or models
- Unrelated docs or governance files
- Any additional skill scripts or metadata files

## Proposed Changes (Step-by-Step by File)

- `.codex/skills/audit/SKILL.md`
  - Change: update the skill definition so it also describes the Markdown review/export workflow, default export path under `.codex/audits/`, per-finding decision states, discard explanations, solved-state transitions after accepted fixes are implemented, and the rule to preserve generated long lines in audit exports.
  - Why: this is the required entry point Codex uses to understand and trigger the skill.
  - Notes: include three separate report sections, explicit decision-state handling, a stable default audit output path, clear rules for when discarded findings may be suppressed or accepted findings may be marked solved, and long-line preservation for generated audits.

- `.codex/skills/audit/references/audit-checklist.md`
  - Change: create a compact checklist covering access control, view responsibility, query duplication/efficiency, ORM performance, helper/form reuse, template boundaries, tests, and governance compliance.
  - Why: gives the skill a small supporting reference without bloating the main skill instructions.
  - Notes: keep it concise and practical rather than explanatory.

- `.codex/skills/audit/` review workflow Markdown file if needed
  - Change: add a compact Markdown template or reference for exported audit reports with per-finding status fields and space for user discard explanations.
  - Why: the user wants a Markdown artifact they can review and update between audits.
  - Notes: keep it manual-edit-friendly and repository-local.

- `.codex/audits/`
  - Change: use this directory as the default location for exported audit Markdown files.
  - Why: the user wants every audit result exported automatically to a stable repository path.
  - Notes: keep naming predictable enough for later update/review cycles.

## Plan Steps (Execution Order)

- [ ] Step 1: Create the `.codex/skills/audit/` directory structure and add `SKILL.md` with the required front matter.
- [ ] Step 2: Update the skill instructions for governance-first audit flow, repo-architecture review, ORM performance review, and the Markdown review-state workflow with three separate report sections.
- [ ] Step 3: Add the compact supporting checklist in `references/audit-checklist.md`.
- [ ] Step 4: Add the minimal Markdown review/export template or reference needed for status tracking and discard explanations.
- [ ] Step 5: Add or use the default `.codex/audits/` export location and document the expected audit file behavior.
- [ ] Step 6: Update markdown review behavior so generated audit lines are preserved unless a structural markdown fix is required.
- [ ] Step 7: Validate markdown structure and confirm the created files match the approved scope exactly.

## Acceptance Criteria (Testable)

- [ ] AC1: The exact requested directory structure exists under `.codex/skills/audit/`.
- [ ] AC2: `SKILL.md` has valid YAML front matter with the required `name: audit` and the required `description`.
- [ ] AC3: `SKILL.md` instructs Codex to read `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` first.
- [ ] AC4: `SKILL.md` instructs Codex to inspect views plus related forms, templates, URLs, tests, and relevant apps/models/JS/settings when needed.
- [ ] AC5: `SKILL.md` includes the required issue checks for governance, reuse, access control, scope drift, Spanish UI text rules, architecture findings, and ORM performance findings.
- [ ] AC6: `SKILL.md` defines the output sections `Summary`, `View Audit Report`, `Architecture Review Report`, `Performance Audit Report`, `Tests to add or update`, and `Open questions`.
- [ ] AC7: `SKILL.md` instructs Codex to distinguish confirmed issues, possible risks, and suggestions.
- [ ] AC8: The skill defines a Markdown review/export format with per-finding states `pending`, `accepted`, `discarded`, and `solved`.
- [ ] AC9: The skill defines a user-editable place for discard explanations and instructs Codex to consult them in later audits before repeating discarded findings.
- [ ] AC10: The skill allows Codex to mark accepted findings as `solved` automatically only after explicit user implementation request and verified repository changes.
- [ ] AC11: The skill exports audit Markdown files by default under `.codex/audits/`.
- [ ] AC12: The skill preserves intentionally generated long lines in audit exports instead of reflowing them for markdownlint line-length cleanup.
- [ ] AC13: `references/audit-checklist.md` contains the required concise checklist sections, including performance / ORM efficiency.

## Validation Commands

- `find .codex/skills/audit -maxdepth 3 -type f | sort`
- `markdownlint .codex/skills/audit/SKILL.md .codex/skills/audit/references/audit-checklist.md`

## Manual Functional Checks

1. Reference the skill as `$audit` and verify Codex can locate the skill bundle.
2. Ask for a view audit and verify the response starts from repository governance files and returns a dedicated `View Audit Report`.
3. Ask for an architecture review and verify the output includes a dedicated `Architecture Review Report`.
4. Ask for a performance audit and verify the output includes a dedicated `Performance Audit Report` with likely ORM issues such as N+1 risks or missing `select_related`.
5. Export an audit report to Markdown and verify each finding can be marked `pending`, `accepted`, `discarded`, or `solved`.
6. Add a discard explanation to one discarded finding and verify a later audit can use that explanation to suppress repetition when it still clearly applies.
7. Request that Codex solve all accepted issues and verify resolved accepted findings can be marked `solved` only after the fixes are completed and verified.
8. Run the skill normally and verify it writes the audit report under `.codex/audits/` without requiring an extra export request.
9. Generate an audit with long evidence lines and verify markdown cleanup preserves those lines instead of wrapping them.
10. Verify the skill recommendations stay minimal and avoid unrelated cleanup.

## Execution Log

- 2026-03-10 00:00 — Spec created.
- 2026-03-10 00:00 — Spec revised for architecture review.
- 2026-03-10 00:00 — Spec revised for performance audit.
- 2026-03-10 00:00 — Spec revised for Markdown review workflow and discard memory.
- 2026-03-10 00:00 — Spec revised for automatic solved-state transitions after accepted fixes.
- 2026-03-10 00:00 — Spec revised for preserving generated long lines in audit exports.
- 2026-03-10 00:00 — Spec approved.
- 2026-03-10 00:00 — Plan created.

## Post-Mortem / Improvements

- What worked well:
  - The skill scope was clarified before implementation, which kept the planned file set small and explicit.
- What caused friction:
  - The audit scope expanded from view-only to architecture and performance review, so the skill instructions must stay disciplined to avoid becoming a redesign guide.
- Suggested updates to:
  - `/plans/TEMPLATE.md`
    - Consider adding a reminder for skill work that repository-local skills are documentation bundles and should avoid extra files unless explicitly requested.
