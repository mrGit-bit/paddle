# Governance Audit Report

## Summary

- Scope: Governance changes for the single-spec SDD migration and the related
  release-workflow documentation and tooling contract.
- Audited target: Repository governance markdown and release-workflow
  coordination.
- Audit date: `2026-04-01`
- Reviewer: Codex

## Governance Findings

### Finding GF-001

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: coordination
- Evidence: [.codex/commands/release.md](/workspaces/paddle/.codex/commands/release.md#L20)
  still says loose unreleased specs are stamped to the shipped version during
  consolidation, while [RELEASE.md](/workspaces/paddle/RELEASE.md#L54) and
  [RELEASE.md](/workspaces/paddle/RELEASE.md#L176) require shipped specs to be
  pre-tagged before the release command runs.
- Why it matters: The optional slash-command wrapper now gives different
  release-tagging instructions than the documented release flow, which makes
  the release gate ambiguous and drift-prone.
- Recommended minimal fix: Align `.codex/commands/release.md` with the
  pre-tagged release flow and remove the obsolete “stamp during consolidation”
  wording.
- Discard explanation:

### Finding GF-002

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: coordination
- Evidence: [.codex/skills/audit/SKILL.md](/workspaces/paddle/.codex/skills/audit/SKILL.md#L116)
  and [.codex/skills/audit/references/audit-checklist.md](/workspaces/paddle/.codex/skills/audit/references/audit-checklist.md#L48)
  still instruct reviewers to evaluate scope drift against an approved “spec or
  plan,” but the active governance in
  [docs/PROJECT_INSTRUCTIONS.md](/workspaces/paddle/docs/PROJECT_INSTRUCTIONS.md#L55)
  and [AGENTS.md](/workspaces/paddle/AGENTS.md#L54) now defines a single-spec
  workflow.
- Why it matters: The repository’s own audit gate now evaluates work against an
  artifact model that governance just removed, so future audit runs will keep
  reintroducing obsolete plan-based language.
- Recommended minimal fix: Update the `audit` skill and its checklist to refer
  only to the approved spec artifact for governance-compliance checks.
- Discard explanation:

## Ownership Map

- File: `docs/PROJECT_INSTRUCTIONS.md`
  - Current role: Compact authority source for minimum SDD gates.
  - Recommended role: Keep as the sole compact source for the active single-spec
    workflow.
- File: `AGENTS.md`
  - Current role: Long-form execution and handoff behavior.
  - Recommended role: Keep execution detail here, but require skill and command
    docs to mirror the same artifact model.
- File: `RELEASE.md`
  - Current role: Primary release-flow source of truth.
  - Recommended role: Keep release-tagging and consolidation rules here and
    make wrappers defer to it exactly.
- File: `.codex/commands/release.md`
  - Current role: Optional wrapper contract for the release command.
  - Recommended role: Mirror `RELEASE.md` without adding independent workflow
    rules.
- File: `.codex/skills/audit/`
  - Current role: Review gate guidance reused during implementation work.
  - Recommended role: Stay aligned with the current SDD artifact model so audit
    checkpoints do not reintroduce retired process language.

## Coordination Gaps

- Gap: The optional release wrapper still describes release-tag stamping as a
  consolidation step.
  - Evidence: `.codex/commands/release.md` conflicts with `RELEASE.md` and the
    release orchestrator’s pre-tagged source selection.
  - Recommended minimal fix: Remove the stamping language and say the wrapper
    expects already-tagged loose specs.
- Gap: The generic audit gate still depends on “spec or plan” wording.
  - Evidence: `audit` skill guidance and checklist still reference plans after
    governance removed them.
  - Recommended minimal fix: Update the audit skill text in the same
    single-spec governance sweep.

## Rewrite Plan

- Step: Align release-wrapper wording with the current release flow.
  - Goal: Eliminate conflicting release-tag instructions.
  - Files primarily affected: `.codex/commands/release.md`
- Step: Align the generic audit skill with the single-spec workflow.
  - Goal: Keep review gates consistent with current governance.
  - Files primarily affected: `.codex/skills/audit/SKILL.md`,
    `.codex/skills/audit/references/audit-checklist.md`

## Open Questions

- None.
