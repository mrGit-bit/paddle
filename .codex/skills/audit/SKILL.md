---
name: audit
description: Audit Django views for project governance, security, reuse, and maintainability issues.
---

# Audit

Use this skill when the user wants a structured audit of Django views or a
related repository review centered on view behavior.

If the user asks specifically for one template's presentation, same-page UI
coherence, CSS reuse, cascade behavior, computed-style mismatches, or responsive
layout risks, use `template-presentation-audit` instead. If the user asks for
both view behavior and template presentation, keep separate reports unless they
explicitly request a combined review.

Read these files first before reviewing code:

- `AGENTS.md`
- `.codex/skills/sdd-workflow/SKILL.md`

Then inspect only the files needed for the requested scope. Start with the
target Django views and expand to related forms, templates, URLs, tests,
JavaScript, models, app boundaries, or settings only when they materially
affect the audited behavior.

Write audit results as Markdown by default under `.codex/audits/` using
`references/audit-review-template.md` as the output shape.

Use predictable file names:

- `YYYY-MM-DD_<target>_audit.md`
- Convert path separators and spaces to `-`
- Keep names short and stable enough for later updates

Good examples:

- `2026-03-10_auth-profile_audit.md`
- `2026-03-10_match-list_audit.md`
- `2026-03-10_ranking_audit.md`

## Audit Modes

Always produce separate reports for these three audit passes:

1. View Audit Report
2. Architecture Review Report
3. Performance Audit Report

If the user asks for only one pass, still keep the same section structure and
mark the other reports as `Not assessed`.

## Review Workflow

When exporting an audit for review, track each finding with one of these
statuses:

- `pending`
- `accepted`
- `discarded`
- `solved`

Use these rules:

- Start new findings as `pending` unless the user says otherwise.
- Mark a finding `accepted` only when the user explicitly accepts it.
- Mark a finding `discarded` only when the user explicitly discards it.
- Only surface findings that are medium or high severity as active findings in
  the audit report; suppress low-severity suggestions instead of exporting
  them.
- A discarded finding may include a user-written explanation for why the
  current state is acceptable.
- On later audits, read prior discarded explanations before repeating the same
  finding.
- Suppress a discarded finding only when the stored explanation clearly still
  applies to the current repository state.
- Re-surface the finding if repository context changed or the discard
  explanation no longer fits.
- Mark a finding `solved` automatically only after:
  - the user explicitly asks Codex CLI to solve accepted issues
  - the related repository change has been implemented
  - the repository state has been re-checked and the finding is resolved

If the user asks to solve all accepted issues, update only accepted findings to
`solved` after verification. Do not mark discarded findings as solved.

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

### View Audit Report

Check at least these issues:

- business logic in templates
- overly large or mixed-responsibility views
- missing ownership or access control
- missing login protection where appropriate
- avoidable duplicated query logic
- weak reuse of existing helpers or forms
- unnecessary DRF or deprecated API use or references
- missing or weak automated test coverage
- scope drift versus approved spec when detectable
- Spanish UI text rule violations in templates

### Architecture Review Report

Review relevant apps, models, views, templates, JavaScript, and settings when
they affect the audited flow. Look for cross-file architecture issues such as:

- business logic detected in templates
- repeated queryset logic across multiple views
- JavaScript duplication across templates or pages
- settings or app-boundary choices that weaken maintainability
- view, form, and template responsibilities leaking into each other

Example architecture findings:

- `Business logic detected in template: ranking_table.html`
- `Repeated queryset logic in 3 views`
- `JS duplication in two templates`
- `Potential N+1 query in match list`

### Performance Audit Report

Focus on static-analysis-friendly Django ORM inefficiencies unless the user
explicitly asks for runtime profiling. Check for:

- possible N+1 queries
- missing `select_related`
- missing `prefetch_related` when obviously needed
- missing indexes when reasonably inferable from repeated filter, join, or
  ordering patterns
- large queryset evaluation
- premature queryset materialization, such as avoidable `list()` or repeated
  iteration
- repeated count, exists, or aggregation work that could be consolidated

## Review Rules

- Prefer minimal, governance-compliant recommendations.
- Avoid speculative refactors and unrelated cleanup.
- Reuse existing helpers, forms, and patterns when recommending fixes.
- Keep deprecated API and DRF avoidance aligned with repository governance.
- Distinguish clearly between confirmed issues, possible risks, and suggestions.
- Do not overstate certainty for architecture or ORM performance concerns
  inferred from static review alone.

## Required Output Format

Use exactly these top-level sections:

### `Summary`

Give a short scope summary and whether the audit covered a specific module,
feature flow, or broader repository slice.

### `View Audit Report`

For each item:

- `Type:` Confirmed issue, Possible risk, or Suggestion
- `Severity:` high, medium, or low
- `Evidence:` file path plus a short explanation
- `Recommended minimal fix:`
- `Tests to add or update:`

### `Architecture Review Report`

For each item:

- `Type:` Confirmed issue, Possible risk, or Suggestion
- `Severity:` high, medium, or low
- `Evidence:` file path plus a short explanation
- `Recommended minimal fix:`
- `Tests to add or update:`

### `Performance Audit Report`

For each item:

- `Type:` Confirmed issue, Possible risk, or Suggestion
- `Severity:` high, medium, or low
- `Evidence:` file path plus a short explanation
- `Recommended minimal fix:`
- `Tests to add or update:`

### `Open Questions`

Only include this section if a necessary conclusion depends on missing
repository context. If not needed, write `None.`

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
- Reuse the existing audit file for the same target when the filename still fits
  the current scope.
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

- Read `references/audit-checklist.md` when you need a compact checklist during
  the audit.
- Read `references/audit-review-template.md` when you need to export or update a
  reviewable Markdown audit file.
- Prefer direct evidence over broad generalizations.
- Keep findings actionable and tied to the current repository patterns.
- If no findings exist in a report section, state that explicitly instead of
  forcing weak findings.
