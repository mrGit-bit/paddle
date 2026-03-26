# Governance Review Strategy and Plan-Input Workflow Plan

## Tracking

- Task ID: `governance-review-and-plan-input`
- Spec: `specs/023-governance-review-and-plan-input.md`
- Release tag: `v1.6.0`

## Context

- The approved spec is
  `specs/023-governance-review-and-plan-input.md`.
- Current governance requires Spec -> Plan -> Implementation approval gates,
  but it does not yet clearly define how `/review` should be used in the
  workflow, how it complements the `audit` skill, or how `/plan` can assist
  spec definition.
- `AGENTS.md`, `docs/PROJECT_INSTRUCTIONS.md`, and `README.md` already describe
  the SDD workflow and must remain aligned after this update.

## Spec Reference

- `specs/023-governance-review-and-plan-input.md`

## Objectives

- Add a clearly placed `/review` strategy to the governance workflow.
- Define how `/review` and the `audit` skill complement each other.
- Allow `/plan` to be used as input for spec definition without bypassing the
  approved-spec gate.
- Clarify that Plan Mode may modify Markdown files when requested.
- Keep all governance documents aligned and update the changelog.

## Scope

### In

- `AGENTS.md` workflow updates
- `docs/PROJECT_INSTRUCTIONS.md` workflow updates
- `README.md` workflow-alignment updates if needed
- `CHANGELOG.md` update for governance/workflow changes

### Out

- Product code changes
- Release automation changes
- Skill implementation changes
- New slash commands or tooling

## Risks

- Risk: `/review` language could accidentally imply a mandatory extra gate for
  every task and create workflow friction.
  Mitigation: define it as a strategy/checkpoint with explicit placement and
  clear rules for when accepted findings must be corrected.
- Risk: allowing `/plan` as spec input could be read as bypassing spec
  approval.
  Mitigation: repeat that implementation still requires an approved spec file
  and an approved plan file.
- Risk: workflow wording could drift across governance files.
  Mitigation: update `AGENTS.md`, `docs/PROJECT_INSTRUCTIONS.md`, and `README.md`
  together in one change set.

## Files Allowed to Change

- `specs/023-governance-review-and-plan-input.md`
- `plans/2026-03-17_governance-review-and-plan-input.md`
- `AGENTS.md`
- `docs/PROJECT_INSTRUCTIONS.md`
- `README.md`
- `CHANGELOG.md`

## Files Forbidden to Change

- Product application files under `paddle/**`
- Release scripts and workflows
- Skill implementation files under `.codex/skills/**`

## Proposed Changes (Step-by-Step by File)

- `AGENTS.md`
  - Change: Rewrite the SDD workflow to add the `/review` strategy, define its
    relationship to `audit`, and clarify `/plan` usage for spec input and
    Markdown-only edits.
  - Why: This is the primary governance source for repository workflow.
- `docs/PROJECT_INSTRUCTIONS.md`
  - Change: Mirror the same workflow rules in the shorter governance subset.
  - Why: Project Instructions override `AGENTS.md` and must stay aligned.
- `README.md`
  - Change: Update the Codex CLI workflow summary if needed to reflect the new
    `/review` and `/plan` guidance.
  - Why: README is a maintained repo-context source and must not contradict
    governance.
- `CHANGELOG.md`
  - Change: Add an `Unreleased` entry describing the workflow/governance update.
  - Why: Repository guidance changes require changelog coverage under project
    rules.

## Plan Steps (Execution Order)

- [ ] Update `AGENTS.md` with the revised full workflow wording.
- [ ] Update `docs/PROJECT_INSTRUCTIONS.md` to mirror the governance changes.
- [ ] Update `README.md` so repository guidance stays aligned.
- [ ] Update `CHANGELOG.md` under `## [Unreleased]`.
- [ ] Run markdownlint on changed Markdown files and review the diff.

## Acceptance Criteria (Testable)

- [ ] `AGENTS.md` defines where `/review` fits in the workflow and when
      accepted findings must be corrected.
- [ ] `AGENTS.md` explains how `/review` and the `audit` skill complement each
      other.
- [ ] Governance wording allows `/plan` to be used as input for spec
      definition without bypassing the approved-spec requirement.
- [ ] Plan Mode wording explicitly allows requested Markdown-file updates.
- [ ] `docs/PROJECT_INSTRUCTIONS.md` and `README.md` do not contradict the new
      workflow wording.
- [ ] `CHANGELOG.md` records the governance update.

## Validation Commands

- `markdownlint --disable MD013 -- AGENTS.md docs/PROJECT_INSTRUCTIONS.md README.md CHANGELOG.md specs/023-governance-review-and-plan-input.md plans/2026-03-17_governance-review-and-plan-input.md`

## Manual Functional Checks

1. Read `AGENTS.md` and confirm the updated process includes a clear `/review`
   strategy and correction follow-through.
2. Confirm the updated process explains when to use `/review` versus `audit`
   and how they can be combined.
3. Confirm the updated process allows `/plan` to be used as input for spec
   definition without allowing implementation before spec approval.
4. Confirm the Plan Mode wording explicitly allows requested Markdown edits.
5. Read `docs/PROJECT_INSTRUCTIONS.md` and `README.md` and confirm they remain
   consistent with `AGENTS.md`.

## Execution Log

- 2026-03-17 00:00 UTC — Spec drafted for review.
- 2026-03-17 00:00 UTC — Spec approved by the user.
- 2026-03-17 00:00 UTC — Plan drafted for review.

## Post-Mortem / Improvements

- Keep `/review` positioned as a pragmatic quality checkpoint rather than an
  always-on bureaucratic gate.
- Keep `/plan` useful for structuring ambiguous work, but preserve the explicit
  approved-spec and approved-plan implementation gates.
