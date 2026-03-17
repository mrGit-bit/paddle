# Governance Audit Report Export

## Functional Goal

Update the `governance-markdown-auditor` skill so it exports governance review
results as a reviewable Markdown report shaped similarly to the existing audit
review template, then generate the first governance audit report for the current
repository using that new output convention.

## Scope

### In

- Rewrite the `governance-markdown-auditor` skill instructions so its default
  output is a reviewable report artifact instead of only inline sections.
- Reuse the structure style of
  `.codex/skills/audit/references/audit-review-template.md` as the model for a
  governance-specific report format.
- Define governance-specific report sections that preserve the skill's current
  required content:
  - summary
  - findings
  - ownership map
  - coordination gaps
  - rewrite plan
  - open questions
- Define stable governance finding IDs and review statuses for exported reports.
- Create the initial governance audit report for the repository using the
  current audit results already identified.
- Update `CHANGELOG.md` under `## [Unreleased]` for the new skill/reporting
  behavior.

### Out

- Product application behavior changes.
- Changes to the existing `audit` skill behavior or its report template.
- New slash commands.
- Broad governance rewrites to `AGENTS.md`, `docs/PROJECT_INSTRUCTIONS.md`, or
  `README.md` beyond what is needed to describe the new skill/report artifact.

## UI / UX Requirements

- Not applicable to product UI.
- The exported governance audit must be easy for agents and humans to review.
- The report format must support later updates with accepted, discarded, or
  solved findings.

## Backend / Documentation Requirements

- The skill must remain concise and avoid restating repository governance
  unnecessarily.
- The skill must clearly distinguish between repository facts and
  recommendations.
- The governance audit report format must support stable finding IDs.
- The initial governance audit report must reflect the actual repository state,
  not hypothetical issues.

## Data / Config Rules

- No secrets or environment changes.
- Markdown changes must follow repository markdown rules.

## Reuse Rules

- Reuse `.codex/skills/audit/references/audit-review-template.md` as the shape
  reference, but adapt section names and fields to governance review needs
  instead of copying view/architecture/performance labels verbatim.
- Reuse the current governance findings already produced for the repository as
  the basis of the initial exported report.
- Prefer one governance audit report file under `.codex/audits/` for this
  initial baseline.

## Acceptance Criteria

1. The `governance-markdown-auditor` skill instructs Codex to export a
   governance audit report artifact by default.
2. The report format includes stable finding IDs, review statuses, and the
   governance-specific sections needed for findings, ownership map,
   coordination gaps, rewrite plan, and open questions.
3. A new initial governance audit report exists under `.codex/audits/` and
   captures the current repo findings.
4. `CHANGELOG.md` records the new governance-audit report-export behavior.
5. Changed Markdown files pass markdownlint with `MD013` disabled.

## Manual Functional Checks

1. Read the updated skill and confirm it tells Codex to export a governance
   audit report artifact by default.
2. Open the generated governance audit report and confirm it includes stable
   finding IDs plus review statuses.
3. Confirm the report includes the sections for findings, ownership map,
   coordination gaps, rewrite plan, and open questions.
4. Confirm the generated findings match the current repository state already
   observed in the governance review.
5. Read `CHANGELOG.md` and confirm the `Unreleased` entry mentions the new
   governance-audit report-export behavior.

## Allowed Files

- `specs/024-governance-audit-report-export.md`
- `plans/*.md`
- `CHANGELOG.md`
- `.codex/skills/governance-markdown-auditor/**`
- `.codex/audits/**`

## Forbidden Files

- Product application files under `paddle/**`
- Release scripts and workflows
- `.codex/skills/audit/**`
