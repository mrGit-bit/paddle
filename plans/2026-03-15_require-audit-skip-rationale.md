# Require Audit Skip Rationale in Governance

## Context

- The approved scope is defined in `specs/021-governance-require-audit-skip-rationale.md`.
- Current governance requires Codex to explain why an audit is needed when suggesting one, but it does not yet require explaining why an audit is not needed when no audit is suggested.
- The active workflow summary also appears in `README.md`, so that file must be checked for consistency.
- `CHANGELOG.md` must be updated under `## [Unreleased]`.

## Spec Reference

- `specs/021-governance-require-audit-skip-rationale.md`

## Objectives

- Require a brief rationale both when suggesting an audit and when not suggesting one.
- Keep audits optional and only used when needed.
- Keep `AGENTS.md`, `docs/PROJECT_INSTRUCTIONS.md`, and `README.md` aligned.
- Update `CHANGELOG.md` to reflect the governance/workflow change.

## Scope

### In

- Update the audit-gating language in `AGENTS.md`.
- Update the matching audit-gating language in `docs/PROJECT_INSTRUCTIONS.md`.
- Update `README.md` if needed so its workflow summary stays consistent.
- Update `CHANGELOG.md`.

### Out

- Product code, templates, JavaScript, tests, or runtime behavior.
- Changes to the audit skill, audit report format, or finding taxonomy.
- Making audits mandatory.
- Broader governance changes outside the audit-rationale requirement.

## Risks

- Governance wording can accidentally imply audits are now mandatory.
  - Mitigation: preserve the current “optional and only when needed” language while adding the skip-rationale requirement.
- The repo has mirrored governance in two authoritative files plus a workflow summary in `README.md`.
  - Mitigation: update all relevant references in one change set and keep wording materially aligned.
- `docs/PROJECT_INSTRUCTIONS.md` has a size limit.
  - Mitigation: make targeted wording changes only and avoid unnecessary expansion.

## Files Allowed to Change

- `specs/021-governance-require-audit-skip-rationale.md`
- `plans/2026-03-15_require-audit-skip-rationale.md`
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

## Proposed Changes (Step-by-Step by File)

- `AGENTS.md`
  - Change: extend the pre-audit and post-implementation audit rules so Codex must also briefly state why an audit is not needed when it does not suggest one.
  - Why: this is the primary operational governance file for the repo workflow.
  - Notes: preserve the existing approval gates and optional-audit model.

- `docs/PROJECT_INSTRUCTIONS.md`
  - Change: mirror the same audit-skip rationale requirement now added to `AGENTS.md`.
  - Why: the project instructions must stay aligned with `AGENTS.md`.
  - Notes: keep version/date aligned with `AGENTS.md` if either file changes.

- `README.md`
  - Change: adjust the workflow summary bullets if needed so they mention a brief rationale whether an audit is suggested or skipped.
  - Why: the repo summary should not contradict the authoritative governance docs.
  - Notes: keep the wording short and practical.

- `CHANGELOG.md`
  - Change: add one `## [Unreleased]` entry describing the governance update.
  - Why: changelog discipline is mandatory for governance/workflow changes.
  - Notes: keep the entry limited to the new audit-rationale expectation.

## Plan Steps (Execution Order)

- [ ] Step 1: Update `AGENTS.md` audit-gating language to require brief rationale when audits are skipped as well as when they are suggested.
- [ ] Step 2: Mirror the same audit-rationale rule in `docs/PROJECT_INSTRUCTIONS.md`, keeping version/date aligned if edited.
- [ ] Step 3: Update `README.md` only if needed to keep its workflow summary consistent.
- [ ] Step 4: Update `CHANGELOG.md` under `## [Unreleased]`.
- [ ] Step 5: Run markdownlint on changed Markdown files and verify only non-blocking `MD013` findings, if any, remain.

## Acceptance Criteria (Testable)

- [ ] AC1: `AGENTS.md` states that Codex must briefly explain why an audit is not needed when it does not suggest a pre-audit or post-implementation audit.
- [ ] AC2: `docs/PROJECT_INSTRUCTIONS.md` contains the same audit-skip rationale requirement as `AGENTS.md`.
- [ ] AC3: The updated wording still makes clear that audits are optional and only suggested when needed.
- [ ] AC4: `README.md` does not contradict the updated governance if it references the audit workflow.
- [ ] AC5: `CHANGELOG.md` contains an accurate `Unreleased` entry for the governance change.

## Validation Commands

- `markdownlint AGENTS.md docs/PROJECT_INSTRUCTIONS.md README.md specs/021-governance-require-audit-skip-rationale.md plans/2026-03-15_require-audit-skip-rationale.md CHANGELOG.md`

## Manual Functional Checks

1. Read `AGENTS.md` and confirm it now requires a brief reason both when suggesting and when skipping audits.
2. Read `docs/PROJECT_INSTRUCTIONS.md` and confirm the same rule appears there with aligned meaning.
3. Confirm the updated wording still says audits are optional and only used when needed.
4. Read `README.md` and confirm its workflow summary does not contradict the updated audit rationale rule.

## Execution Log

- 2026-03-15 22:17 — Spec created.
- 2026-03-15 22:17 — Spec approved.
- 2026-03-15 22:17 — Plan created.

## Post-Mortem / Improvements

- Expected to be none for this targeted governance clarification.
