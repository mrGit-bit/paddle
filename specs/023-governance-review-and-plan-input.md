# Governance Review Strategy and Plan-Input Workflow

## Tracking

- Task ID: `governance-review-and-plan-input`
- Plan: `plans/2026-03-17_governance-review-and-plan-input.md`
- Release tag: `v1.6.0`

## Functional Goal

Update repository governance so the documented SDD process explicitly includes
an appropriate `/review` strategy with automated correction follow-through,
defines how `/review` can complement the `audit` skill, and allows `/plan` to
be used as an input for spec definition while still preserving the spec-plan-
implementation approval gates. Clarify that Plan Mode may modify Markdown files
when requested.

## Scope

### In

- Rewrite the governance workflow in `AGENTS.md` and
  `docs/PROJECT_INSTRUCTIONS.md` to include a defined `/review` step or
  decision point in the overall process.
- Define when `/review` should be considered relative to spec approval, audit,
  implementation, and closure.
- Define how `/review` and the `audit` skill complement each other without
  duplicating purpose.
- Clarify that `/plan` may be used to help define a spec and may serve as an
  input into spec drafting/refinement.
- Clarify that Plan Mode may modify Markdown files when requested, including
  governance/spec/plan/template Markdown updates.
- Update `README.md` if its workflow guidance needs to stay aligned.
- Update `CHANGELOG.md` for the governance/workflow change.

### Out

- Product code changes unrelated to governance documentation.
- Changes to release automation, application behavior, or test infrastructure.
- New slash commands or new Codex skills.
- Changes to the `audit` skill implementation itself.

## UI / UX Requirements

- Not applicable to product UI.
- Workflow wording must stay concise, explicit, and easy to execute.
- The `/review` strategy must clearly state when review findings should be
  corrected before progressing.

## Backend / Documentation Requirements

- `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md` must remain version/date
  aligned.
- Governance must preserve the mandatory branch check and explicit spec/plan
  approval gates.
- Governance must distinguish the purpose of:
  - spec drafting,
  - planning,
  - `/review`,
  - `audit`,
  - implementation.
- Governance must state when `/review` is optional, recommended, or required.
- Governance must state that accepted `/review` findings are corrected before
  the development cycle advances past the relevant gate.
- Governance must clarify that `/plan` can be used before spec approval for
  structuring or refining a spec request, without bypassing the requirement for
  an approved spec file before implementation.
- Governance must clarify that Plan Mode can modify Markdown files when
  requested.
- `README.md` must not contradict the updated workflow if it references SDD
  execution.

## Data / Config Rules

- No repository secrets or environment configuration changes.
- `Instruction Set Version` and `Last Updated` must stay synchronized between
  `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md`.

## Reuse Rules

- Reuse the existing SDD structure instead of replacing it with a different
  process.
- Reuse the existing `audit` skill as a complementary governance checkpoint;
  do not redefine it as a substitute for `/review`.
- Prefer minimal wording changes that make the workflow unambiguous.

## Acceptance Criteria

1. Governance documents describe where `/review` fits into the full workflow.
2. Governance documents explain how `/review` and `audit` complement each
   other and when accepted findings must be corrected.
3. Governance documents allow `/plan` to be used as input for spec definition
   without bypassing the approved-spec requirement.
4. Governance documents explicitly allow Plan Mode to modify Markdown files
   when requested.
5. `README.md` remains aligned with the updated workflow guidance if it
   references that workflow.
6. `CHANGELOG.md` records the governance/workflow update.

## Manual Functional Checks

1. Read `AGENTS.md` and confirm the workflow now includes a defined `/review`
   strategy and follow-through on accepted review findings.
2. Read `AGENTS.md` and confirm the `audit` skill is described as complementary
   to `/review`, not a replacement for it.
3. Read the planning section and confirm `/plan` may be used as input for spec
   definition while still requiring spec approval before implementation.
4. Read the Plan Mode wording and confirm Markdown-only edits are allowed when
   requested.
5. Read `docs/PROJECT_INSTRUCTIONS.md` and `README.md` and confirm they do not
   contradict the updated workflow.

## Allowed Files

- `specs/023-governance-review-and-plan-input.md`
- `plans/2026-03-17_governance-review-and-plan-input.md`
- `AGENTS.md`
- `docs/PROJECT_INSTRUCTIONS.md`
- `README.md`
- `CHANGELOG.md`

## Forbidden Files

- Product application files under `paddle/**`
- Release scripts and workflows
- Skill implementation files under `.codex/skills/**`
