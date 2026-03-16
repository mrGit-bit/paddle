# Spec 021: Require Audit Skip Rationale in Governance

## Functional Goal

Update repository governance so when Codex does not suggest a spec-focused pre-audit or a scoped post-implementation audit, the response must briefly state why the audit was not needed for that specific scope or implementation result.

## Scope

### In

- Update `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md` so audit governance covers both cases:
  - when an audit is suggested, explain why it is needed
  - when an audit is not suggested, explain why it is not needed
- Update `README.md` if its workflow summary mentions audit-gating behavior and would otherwise become inconsistent.
- Update `CHANGELOG.md` under `## [Unreleased]` for the governance/workflow change.
- Keep the wording aligned with the existing optional-audit model rather than making audits mandatory.

### Out

- Product code, templates, JavaScript, tests, or runtime app behavior.
- Changing audit report format, skill behavior, or finding taxonomy.
- Making either audit mandatory by default.
- Broad governance rewrites unrelated to audit rationale expectations.

## UI/UX Requirements

- Not applicable to product UI.

## Backend/Documentation Requirements

- `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md` must remain aligned on version/date if either changes.
- Governance must stay clear that audits remain optional and should only be suggested when needed.
- Governance must require a concise explanation in both directions:
  - why an audit is being suggested
  - why an audit is not being suggested
- The wording should allow short, scope-specific rationale rather than forcing a long template every time.
- If `README.md` mentions the workflow, it must not contradict the updated governance language.

## Data Rules

- `docs/PROJECT_INSTRUCTIONS.md` must remain under 8000 characters after edits.
- Existing SDD approval gates and release-consolidation rules must remain unchanged.

## Reuse Rules

- Reuse the existing governance wording around optional audits and explicit reasons.
- Prefer minimal wording changes over restructuring entire sections.
- Reuse the existing audit-gate workflow language already established by Spec 019.

## Acceptance Criteria

1. Governance docs state that when Codex suggests a pre-audit or post-implementation audit, it must explain why that audit is needed.
2. Governance docs state that when Codex does not suggest a pre-audit or post-implementation audit, it must briefly explain why the audit is not needed.
3. Governance docs still make clear that audits are optional and only used when needed.
4. `README.md`, `AGENTS.md`, and `docs/PROJECT_INSTRUCTIONS.md` do not contradict each other on audit rationale behavior if `README.md` mentions that flow.
5. `CHANGELOG.md` includes an `Unreleased` entry matching the governance update.

## Manual Functional Checks

1. Read the updated governance docs and confirm they still say audits are optional rather than mandatory.
2. Confirm the docs now require a reason both when suggesting an audit and when not suggesting one.
3. Confirm the new wording still preserves the mandatory spec approval and plan approval gates.
4. If `README.md` is updated, confirm its workflow summary matches the governance docs.

## Files Allowed to Change

- `specs/021-governance-require-audit-skip-rationale.md`
- `plans/*.md`
- `AGENTS.md`
- `docs/PROJECT_INSTRUCTIONS.md`
- `README.md`
- `CHANGELOG.md`

## Files Forbidden to Change

- `paddle/**`
- `mobile/**`
- `.github/workflows/**`
- tests
- audit skill files
