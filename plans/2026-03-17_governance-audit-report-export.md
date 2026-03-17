# Governance Audit Report Export Plan

## Context

- The approved spec is
  `specs/024-governance-audit-report-export.md`.
- The repository already contains the `governance-markdown-auditor` skill, but
  it currently describes inline output sections rather than a reviewable export
  artifact.
- The repository already has an audit-review template under
  `.codex/skills/audit/references/audit-review-template.md` that can be reused
  as the structural model for governance audit exports.
- The initial governance findings for the current repository have already been
  identified and can be reused as the first exported governance audit report.

## Spec Reference

- `specs/024-governance-audit-report-export.md`

## Objectives

- Update the governance skill so exported reviewable audit reports are the
  default output mode.
- Define a governance-specific report format with stable finding IDs and review
  statuses.
- Generate the first repository governance audit report under `.codex/audits/`.
- Record the behavior change in `CHANGELOG.md`.

## Scope

### In

- `governance-markdown-auditor` skill updates
- governance audit reference/report-format additions if needed
- initial governance audit report export under `.codex/audits/`
- `CHANGELOG.md` update

### Out

- product code changes
- changes to the existing `audit` skill or its template
- governance rewrites to the main repo docs beyond the audit report artifact
- new slash commands or automation

## Risks

- Risk: the new governance report format could drift too far from the existing
  audit template and lose reviewability.
  Mitigation: keep the same reviewable finding pattern with status, type,
  severity, evidence, and discard explanation fields.
- Risk: the exported governance report could overstate certainty or mix facts
  with recommendations.
  Mitigation: keep evidence lines concrete and separate recommendations from
  observed repository state.
- Risk: the skill could become verbose if the report format is over-specified.
  Mitigation: keep the skill concise and move stable format detail into a small
  reference file only if needed.

## Files Allowed to Change

- `specs/024-governance-audit-report-export.md`
- `plans/2026-03-17_governance-audit-report-export.md`
- `CHANGELOG.md`
- `.codex/skills/governance-markdown-auditor/**`
- `.codex/audits/**`

## Files Forbidden to Change

- product application files under `paddle/**`
- release scripts and workflows
- `.codex/skills/audit/**`

## Proposed Changes (Step-by-Step by File)

- `.codex/skills/governance-markdown-auditor/SKILL.md`
  - Change: rewrite the output/export instructions so the default deliverable is
    a reviewable governance audit report written under `.codex/audits/`.
  - Why: the current skill defines inline sections only, while the approved spec
    requires a reusable report artifact.
- `.codex/skills/governance-markdown-auditor/references/*`
  - Change: add or update a compact governance report-format reference if it is
    needed to keep the main skill concise.
  - Why: the governance report should stay consistent without bloating the skill
    body.
- `.codex/audits/<date>_repository-governance_audit.md`
  - Change: create the first exported governance audit report using the current
    repository findings.
  - Why: the approved scope requires an initial baseline artifact.
- `CHANGELOG.md`
  - Change: add an `Unreleased` entry describing governance-audit report export
    support.
  - Why: repository guidance and skill behavior changed.

## Plan Steps (Execution Order)

- [ ] Update the governance skill to default to exported audit-report output.
- [ ] Add any compact governance report-format reference needed by the skill.
- [ ] Write the initial repository governance audit report under `.codex/audits/`.
- [ ] Update `CHANGELOG.md` under `## [Unreleased]`.
- [ ] Run markdownlint on the changed Markdown files and review the diff.

## Acceptance Criteria (Testable)

- [ ] The skill instructs Codex to export governance audit reports by default.
- [ ] The report format uses stable finding IDs and review statuses.
- [ ] The exported report includes findings, ownership map, coordination gaps,
      rewrite plan, and open questions.
- [ ] The initial governance audit report reflects the repository findings
      already identified.
- [ ] `CHANGELOG.md` contains an accurate `Unreleased` entry for the new
      reporting behavior.

## Validation Commands

- `markdownlint --disable MD013 -- .codex/skills/governance-markdown-auditor/SKILL.md .codex/skills/governance-markdown-auditor/references/*.md .codex/audits/*.md CHANGELOG.md specs/024-governance-audit-report-export.md plans/2026-03-17_governance-audit-report-export.md`

## Manual Functional Checks

1. Read the updated skill and confirm report export under `.codex/audits/` is
   the default output path.
2. Open the generated governance audit report and confirm each finding has a
   stable ID and status.
3. Confirm the report includes the ownership map, coordination gaps, rewrite
   plan, and open-questions sections.
4. Confirm the generated report findings match the current repository evidence.
5. Read `CHANGELOG.md` and confirm it records the report-export behavior.

## Execution Log

- 2026-03-17 00:00 UTC — Spec drafted for review.
- 2026-03-17 00:00 UTC — Spec approved by the user.
- 2026-03-17 00:00 UTC — Plan drafted for review.

## Post-Mortem / Improvements

- Keep governance audits reviewable and update-friendly, not just conversational.
- Prefer one baseline governance audit artifact that can be updated over time
  instead of disconnected one-off writeups.
