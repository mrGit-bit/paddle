# Governance Audit Gates Around Implementation

## Tracking

- Task ID: `governance-audit-gates-around-implementation`
- Spec: `specs/019-governance-audit-gates-around-implementation.md`
- Release tag: `v1.5.0`

## Context

- Current governance enforces the mandatory Spec -> Plan -> Implementation flow, but it does not yet describe when Codex should suggest a spec-focused pre-audit or a scoped post-implementation audit.
- The approved scope is defined in `specs/019-governance-audit-gates-around-implementation.md`.
- Discovery first covered:
  - `docs/PROJECT_INSTRUCTIONS.md`
  - `AGENTS.md`
  - `README.md`
  - `CHANGELOG.md`
  - `plans/TEMPLATE.md`

## Spec Reference

- Exact active spec:
  - `specs/019-governance-audit-gates-around-implementation.md`

## Objectives

- Document that audits are optional and should only be suggested when needed.
- Require Codex to state the reason whenever suggesting either a pre-audit or post-implementation audit.
- Keep the mandatory approval gates unchanged and aligned across governance docs.
- Keep `docs/PROJECT_INSTRUCTIONS.md` under 8000 characters after the update.

## Scope

### In

- Governance wording updates in `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md`.
- `README.md` alignment if workflow guidance there would otherwise drift.
- `CHANGELOG.md` update for the workflow/governance change.
- `plans/TEMPLATE.md` only if it needs a minimal wording update to avoid workflow mismatch.

### Out

- Product code, tests, templates, or runtime behavior.
- Making audits mandatory.
- Changing the audit report structure or skill behavior itself.

## Risks

- The two governance files could drift if the workflow wording changes in only one place.
  - Mitigation: update `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` in the same change set and keep version/date synchronized.
- `docs/PROJECT_INSTRUCTIONS.md` has a hard size limit.
  - Mitigation: use compact wording and re-check the file size after edits.
- README workflow text could become inconsistent with governance if not reviewed.
  - Mitigation: update README only where necessary to avoid contradiction.

## Files Allowed to Change

- `specs/019-governance-audit-gates-around-implementation.md`
- `plans/2026-03-15_governance-audit-gates-around-implementation.md`
- `plans/TEMPLATE.md`
- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`
- `README.md`
- `CHANGELOG.md`

## Files Forbidden to Change

- `paddle/**`
- `.github/workflows/**`
- release scripts
- tests
- audit skill files

## Proposed Changes (Step-by-Step by File)

- `docs/PROJECT_INSTRUCTIONS.md`
  - Change: add compact workflow wording that audits are optional, suggested only when needed, and must include the reason when suggested.
  - Why: this is the primary governance source after the explicit task brief.
  - Notes: preserve mandatory branch/spec/plan approval rules and keep the file under 8000 characters.

- `AGENTS.md`
  - Change: mirror the workflow wording from `docs/PROJECT_INSTRUCTIONS.md` with the same version/date metadata.
  - Why: these files must stay aligned.
  - Notes: keep the stronger detail level while avoiding contradiction.

- `README.md`
  - Change: update the Codex CLI workflow guidance only if needed so it reflects optional audit suggestions and stated reasons.
  - Why: README currently summarizes repository workflow for safe navigation.
  - Notes: avoid duplicating the full governance text.

- `plans/TEMPLATE.md`
  - Change: update only if the template needs a short note so planning remains compatible with the optional audit recommendation.
  - Why: prevents future friction if the template implies a workflow that governance no longer recommends.
  - Notes: skip if no template change is needed.

- `CHANGELOG.md`
  - Change: add an `## [Unreleased]` entry describing the governance workflow update around optional audit suggestions.
  - Why: required by repository changelog discipline.
  - Notes: entry text must match the final implemented governance wording.

## Plan Steps (Execution Order)

- [x] Step 1: Update `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` with aligned wording for optional pre-audit and post-implementation audit suggestions, including the requirement to state the reason.
- [x] Step 2: Adjust `README.md` and `plans/TEMPLATE.md` only where needed to keep the workflow summary consistent.
- [x] Step 3: Update `CHANGELOG.md` and synchronize governance version/date metadata.
- [x] Step 4: Validate markdown structure manually or with markdownlint if available, and verify `docs/PROJECT_INSTRUCTIONS.md` remains under 8000 characters.

## Acceptance Criteria (Testable)

- [x] AC1: Governance docs state that a spec-focused pre-audit may be suggested only when needed, and the suggestion must include the reason.
- [x] AC2: Governance docs state that a scoped post-implementation audit may be suggested only when needed, and the suggestion must include the reason.
- [x] AC3: Governance docs preserve the mandatory spec approval before planning and plan approval before implementation.
- [x] AC4: `README.md`, `AGENTS.md`, and `docs/PROJECT_INSTRUCTIONS.md` do not contradict each other about the updated workflow.
- [x] AC5: `Instruction Set Version` and `Last Updated` are synchronized in `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md`.
- [x] AC6: `CHANGELOG.md` contains an `Unreleased` entry matching the governance update.

## Validation Commands

- `python -m markdownlint_cli2 docs/PROJECT_INSTRUCTIONS.md AGENTS.md README.md plans/TEMPLATE.md CHANGELOG.md specs/019-governance-audit-gates-around-implementation.md plans/2026-03-15_governance-audit-gates-around-implementation.md`
- `wc -c docs/PROJECT_INSTRUCTIONS.md`

## Manual Functional Checks

1. Read `docs/PROJECT_INSTRUCTIONS.md` and confirm audits are optional and only suggested when needed, with a stated reason.
2. Read `AGENTS.md` and confirm it matches the same workflow intent and metadata.
3. Read `README.md` and confirm its workflow summary does not contradict the governance docs.
4. Confirm the mandatory spec and plan approval gates remain intact.
5. Confirm `docs/PROJECT_INSTRUCTIONS.md` remains under 8000 characters.

## Execution Log

- 2026-03-15 21:32 — Spec created.
- 2026-03-15 21:32 — Spec approved.
- 2026-03-15 21:32 — Plan created.
- 2026-03-15 21:33 — Plan approved.
- 2026-03-15 21:34 — Governance docs updated and version/date synchronized.
- 2026-03-15 21:35 — Markdown manually reviewed and `docs/PROJECT_INSTRUCTIONS.md` size verified under 8000 characters.

## Post-Mortem / Improvements

- What worked well
  - The requested workflow change is narrow and maps cleanly to existing governance sections.
- What caused friction
  - Governance updates must stay concise because `docs/PROJECT_INSTRUCTIONS.md` has a strict size limit.
- Suggested updates to:
  - `/docs/PROJECT_INSTRUCTIONS.md`
  - `/AGENTS.md`
  - `/plans/TEMPLATE.md`
  - None currently identified.
