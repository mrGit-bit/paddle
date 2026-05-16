---
name: audit
description: Audit Django views for project governance, security, reuse, and maintainability issues.
---

# Audit

Use this skill when the user wants a structured audit of Django views or a
related repository review centered on view behavior.

Route template presentation, CSS cascade, same-page UI-coherence, and
responsive layout reviews to `template-presentation-audit`. If the user asks
for view behavior and presentation together, keep separate reports unless they
explicitly request a combined review.

## Audit Modes

Always produce separate reports for these three audit passes:

1. View Audit Report
2. Architecture Review Report
3. Performance Audit Report

If the user asks for only one pass, still keep the same section structure and
mark the other reports as `Not assessed`.

## Review Workflow

1. Verify branch and scope through `AGENTS.md` and task-relevant SDD context.
2. Start with the target Django views.
3. Expand only to related forms, templates, URLs, tests, JavaScript, models,
   app boundaries, or settings that materially affect the audited behavior.
4. Read `references/audit-checklist.md` only when you need the checklist.
5. Export or update the audit under `.codex/audits/` using
   `references/audit-review-template.md`.
6. Use predictable names: `YYYY-MM-DD_<target>_audit.md`, converting path
   separators and spaces to `-`.

## Best Practices

Use this skill as part of the normal development loop, not only for cleanup.

- Run an audit before implementing a spec when the target area already exists in
  the repository.
- Suggest a pre-spec audit especially for existing view flows such as auth,
  ranking, match list, player detail, or other code paths likely to contain
  accumulated permissions, reuse, architecture, or ORM issues.
- Use the first audit as the baseline decision file in `.codex/audits/`.
- Review the exported Markdown and mark findings `accepted`, `discarded`, or
  keep them `pending`.
- Add a short explanation immediately for discarded findings.
- Before continuing past a review/audit checkpoint, ask the user whether each
  surfaced finding should be addressed or discarded, then update the same audit
  file accordingly.
- When the user asks Codex to solve accepted issues, update the same audit file
  instead of creating a disconnected second review artifact.
- Prefer one audit file per module, view flow, or feature slice so decision
  history stays readable.

## What To Check

Check view behavior, architecture, and ORM performance. Use
`references/audit-checklist.md` for the full checklist instead of loading it by
default.

## Review Rules

- Prefer minimal, governance-compliant recommendations.
- Avoid speculative refactors and unrelated cleanup.
- Reuse existing helpers, forms, and patterns when recommending fixes.
- Keep deprecated API and DRF avoidance aligned with repository governance.
- Distinguish clearly between confirmed issues, possible risks, and suggestions.
- Do not overstate certainty for architecture or ORM performance concerns
  inferred from static review alone.

## Markdown Export Rules

When exporting a reviewable audit:

- Use the structure from `references/audit-review-template.md`.
- Write the report under `.codex/audits/` by default unless the user explicitly
  asks for a different repository-local location.
- Preserve intentionally generated long lines in exported audit files instead of
  reflowing them only to satisfy markdownlint line-length preferences.
- Give every finding a stable finding ID within the report.
- Include a `Status:` field for every finding.
- Include a `Discard explanation:` field for every finding so the user can fill
  it in when discarding.
- Preserve existing finding IDs and user-written explanations when updating an
  existing review file.
- Reuse the existing audit file for the same target when the filename still
  fits the current scope.
- If a prior discarded finding is suppressed because its explanation still
  applies, do not re-add it as a new active finding.
- If a prior accepted finding has been fixed and verified after an explicit user
  solve request, update its status to `solved`.

## Markdown Review Handling

When validating or cleaning up exported audit Markdown:

- Fix structural markdown problems such as malformed headings, list spacing, or
  missing required sections.
- Do not wrap or reflow generated evidence, recommendation, or status lines only
  to satisfy line-length linting.
- Prefer preserving generated audit content exactly as produced unless a
  structural correction is required.

## Working Style

- Track findings as `pending`, `accepted`, `discarded`, or `solved`.
- Start new findings as `pending` unless the user says otherwise.
- Mark accepted or discarded only after explicit user choice.
- Mark solved only after an explicit solve request, implementation, and
  verification.
- Surface only medium or high severity active findings; suppress low-severity
  suggestions instead of exporting them.
- Prefer direct evidence over broad generalizations.
- Keep findings actionable and tied to the current repository patterns.
- If no findings exist in a report section, state that explicitly instead of
  forcing weak findings.
