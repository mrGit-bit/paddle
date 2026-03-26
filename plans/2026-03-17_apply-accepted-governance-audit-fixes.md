# Apply Accepted Governance Audit Fixes Plan

## Context

- The approved scope is defined in
  `specs/025-apply-accepted-governance-audit-fixes.md`.
- The accepted findings live in
  `.codex/audits/2026-03-17_repository-governance_audit.md`.
- The requested implementation should follow the governance audit rewrite plan:
  separate authority bands, remove README overlap, operationalize coordination
  gaps, simplify the SDD template, and resolve markdown-governance exceptions.
- `AGENTS.md`, `docs/PROJECT_INSTRUCTIONS.md`, `README.md`, `BACKLOG.md`,
  `CHANGELOG.md`, `RELEASE.md`, and `plans/TEMPLATE.md` are the main affected
  files.

## Spec Reference

- `specs/025-apply-accepted-governance-audit-fixes.md`

## Objectives

- Split ownership cleanly between `docs/PROJECT_INSTRUCTIONS.md` and
  `AGENTS.md`.
- Reduce README to current-state orientation and routing only.
- Add explicit operational checkpoints for backlog/changelog reconciliation and
  active spec/plan discovery.
- Simplify `plans/TEMPLATE.md` to a shorter task-focused structure.
- Align `CHANGELOG.md` markdown handling with declared governance rules.
- Update the accepted governance-audit findings to `solved` after verification.

## Scope

### In

- governance file rewrites in `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md`
- README cleanup and routing-focused rewrite
- backlog/changelog coordination wording updates
- active spec/plan lookup rule introduction
- `plans/TEMPLATE.md` simplification
- `CHANGELOG.md` cleanup and changelog entry update
- governance audit report status updates after implementation

### Out

- product code changes
- release automation script changes
- GitHub workflow changes
- new governance files unless unavoidable

## Risks

- Risk: the compact `docs/PROJECT_INSTRUCTIONS.md` could lose important required
  constraints while removing duplicated workflow detail.
  Mitigation: keep only non-negotiable repository constraints, authority, and
  the minimum SDD gate requirements.
- Risk: reducing README too far could remove useful repo orientation.
  Mitigation: preserve architecture, important paths, environment notes, and
  owner-doc pointers while removing release-summary and governance duplication.
- Risk: simplifying `plans/TEMPLATE.md` could conflict with current governance
  wording.
  Mitigation: update governance docs and template together in one change set.
- Risk: removing changelog markdownlint carve-outs may expose structural issues.
  Mitigation: fix the markdown structure in the same change set and validate
  with markdownlint.

## Files Allowed to Change

- `specs/025-apply-accepted-governance-audit-fixes.md`
- `plans/2026-03-17_apply-accepted-governance-audit-fixes.md`
- `.codex/audits/2026-03-17_repository-governance_audit.md`
- `AGENTS.md`
- `docs/PROJECT_INSTRUCTIONS.md`
- `README.md`
- `BACKLOG.md`
- `CHANGELOG.md`
- `RELEASE.md`
- `plans/TEMPLATE.md`

## Files Forbidden to Change

- product application files under `paddle/**`
- GitHub workflow files
- release automation scripts under `scripts/**`
- `.codex/skills/audit/**`

## Proposed Changes (Step-by-Step by File)

- `docs/PROJECT_INSTRUCTIONS.md`
  - Change: rewrite into a compact authority-and-constraints document with the
    minimum mandatory SDD gates, ownership rules, active-work lookup rule, and
    closure coordination requirements.
  - Why: the accepted audit requires it to become the compact authority file.
- `AGENTS.md`
  - Change: trim repeated repository constraints and focus on Codex execution
    behavior, workflow mechanics, approval gates, handoff rules, and the new
    coordination checkpoints.
  - Why: the accepted audit requires a non-overlapping split with project
    instructions.
- `README.md`
  - Change: remove release-history summary and reduce governance duplication,
    keeping only repo orientation, important paths, and routing guidance to the
    owner docs.
  - Why: README should be orientation and navigation only.
- `BACKLOG.md`
  - Change: clarify the operational checkpoint for moving completed items into
    `CHANGELOG.md`, aligned with closure/release governance.
  - Why: backlog/changelog coordination must stop being memory-based.
- `CHANGELOG.md`
  - Change: remove the current undeclared markdownlint-disable carve-out if
    structurally possible, and add an `Unreleased` entry for the governance
    cleanup.
  - Why: governance must match actual changelog handling.
- `RELEASE.md`
  - Change: add backlog-reconciliation wording only if release or closure
    guidance needs one explicit coordination checkpoint there.
  - Why: reuse existing operational docs instead of creating new process files.
- `plans/TEMPLATE.md`
  - Change: simplify to a shorter structure focused on summary, key changes,
    tests/validation, constraints, and risks.
  - Why: accepted finding `GF-004` requires materially lower SDD overhead.
- `.codex/audits/2026-03-17_repository-governance_audit.md`
  - Change: update accepted findings to `solved` after the fixes are
    implemented and verified.
  - Why: keep the governance audit as the living decision record.

## Plan Steps (Execution Order)

- [ ] Rewrite `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` to establish the
      new ownership split and active-work/closure coordination rules.
- [ ] Rewrite `README.md` to orientation-and-routing only.
- [ ] Update `BACKLOG.md`, `CHANGELOG.md`, and `RELEASE.md` as needed to
      operationalize backlog/changelog coordination and resolve changelog
      markdown-governance issues.
- [ ] Simplify `plans/TEMPLATE.md` and align the governance wording with it.
- [ ] Update the governance audit report statuses from `accepted` to `solved`
      after verifying each fix.
- [ ] Run markdownlint on the changed Markdown files and review the diff.

## Acceptance Criteria (Testable)

- [ ] `docs/PROJECT_INSTRUCTIONS.md` is compact and limited to non-negotiable
      repository constraints plus the minimum SDD gates.
- [ ] `AGENTS.md` focuses on Codex execution behavior and workflow mechanics
      without materially duplicating the compact project-instructions content.
- [ ] `README.md` no longer contains release-history summary material and now
      routes users to owner docs.
- [ ] Governance explicitly states how backlog/changelog reconciliation happens.
- [ ] Governance explicitly states how the active spec/plan for a task is
      identified.
- [ ] `plans/TEMPLATE.md` is materially shorter and task-focused.
- [ ] `CHANGELOG.md` is structurally valid without the undeclared carve-out, or
      any exception retained is explicitly documented in governance.
- [ ] The accepted findings in the governance audit are updated to `solved`.

## Validation Commands

- `markdownlint --disable MD013 -- AGENTS.md docs/PROJECT_INSTRUCTIONS.md README.md BACKLOG.md CHANGELOG.md RELEASE.md plans/TEMPLATE.md .codex/audits/2026-03-17_repository-governance_audit.md specs/025-apply-accepted-governance-audit-fixes.md plans/2026-03-17_apply-accepted-governance-audit-fixes.md`

## Manual Functional Checks

1. Read `docs/PROJECT_INSTRUCTIONS.md` and confirm it contains compact
   repository constraints, authority, and the minimum SDD gates only.
2. Read `AGENTS.md` and confirm it now centers on Codex execution behavior,
   approval gates, and delivery flow rather than duplicating repository
   constraints.
3. Read `README.md` and confirm it no longer includes release-history summary
   content and instead routes to `CHANGELOG.md`, `AGENTS.md`, and
   `docs/PROJECT_INSTRUCTIONS.md`.
4. Read the updated backlog/closure/release guidance and confirm backlog to
   changelog reconciliation is now an explicit operational checkpoint.
5. Read `plans/TEMPLATE.md` and confirm it is shorter and focused on task
   decisions, constraints, validation, and risks.
6. Open the governance audit report and confirm accepted findings are marked
   `solved` only after the corresponding repo changes exist.

## Execution Log

- 2026-03-17 00:00 UTC — Spec drafted for review.
- 2026-03-17 00:00 UTC — Spec approved by the user.
- 2026-03-17 00:00 UTC — Plan drafted for review.

## Post-Mortem / Improvements

- Keep governance split by document role, not by trying to mirror the same
  instructions in shorter and longer forms.
- Keep SDD artifacts decision-rich and shorter so they help execution instead of
  becoming ceremony.
