# Repository Governance Audit

## Summary

- Scope: Repository-wide governance markdown review.
- Audited target: `AGENTS.md`, `docs/PROJECT_INSTRUCTIONS.md`, `README.md`, `CHANGELOG.md`, `BACKLOG.md`, `RELEASE.md`, `specs/`, `plans/`, `plans/TEMPLATE.md`, `.codex/commands/release.md`, and `scripts/release_orchestrator.py`.
- Audit date: 2026-03-17
- Reviewer: Codex via `governance-markdown-auditor`

## Governance Findings

### Finding GF-001

- Status: solved
- Type: Confirmed issue
- Severity: critical
- Category: boundary
- Evidence: `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` both define authority, tool roles, branch checks, the full SDD flow, post-release consolidation, changelog rules, and markdown rules. The duplication is structural rather than incidental.
- Why it matters: The two highest-priority governance files do not have a clean responsibility split, so every change requires mirrored edits and drift remains likely.
- Recommended minimal fix: Redefine `docs/PROJECT_INSTRUCTIONS.md` as the compact authority file for non-negotiable constraints only, and trim `AGENTS.md` to Codex execution behavior, workflow mechanics, and handoff rules without restating the same repository rules verbatim.
- Discard explanation:

### Finding GF-002

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: duplication
- Evidence: `README.md` contains a `Recent Changes` section summarizing unreleased and released work even though it points to `CHANGELOG.md` for release history. It also restates a large share of governance already owned by `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md`.
- Why it matters: README is acting as repo orientation, release summary, and governance quick-reference at the same time, which increases maintenance burden and creates overlap with clearer sources of truth.
- Recommended minimal fix: Remove the release-summary material from `README.md`, keep it focused on current-state repo orientation, and reduce the Codex workflow guidance to short routing pointers.
- Discard explanation:

### Finding GF-003

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: coordination
- Evidence: `BACKLOG.md` says completed tasks are removed from backlog and added to `CHANGELOG.md`, but the reviewed release and workflow surface only operationalizes changelog handling. No corresponding hook, checklist, or automation path coordinates `BACKLOG.md`.
- Why it matters: The repository declares backlog-to-changelog coordination as a rule, but the rule currently depends on memory and manual discipline.
- Recommended minimal fix: add an explicit backlog-reconciliation checkpoint to the closure or release workflow.
- Discard explanation:

### Finding GF-004

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: artifact-value
- Evidence: `plans/TEMPLATE.md` requires file-by-file proposed changes, acceptance criteria, validation commands, execution log, and post-mortem sections for every plan, while current specs and plans restate much of the same governance structure again.
- Why it matters: The SDD artifacts are readable but verbose, and the current structure encourages ceremonial repetition of governance rather than task-specific decisions.
- Recommended minimal fix: Shrink the plan template to task-specific deltas only: summary, key changes, tests, constraints, and risks. Keep longer sections only when the task genuinely needs them.
- Discard explanation:

### Finding GF-005

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: operationalization
- Evidence: Governance requires an approved spec and plan before implementation, and README tells agents to read the relevant spec and plan, but the repository has multiple unreleased loose specs and plans with no canonical active-work selector or index.
- Why it matters: The rule is strong, but active artifact discovery is weak, so compliance still depends on agent memory and local inference.
- Recommended minimal fix: Add one canonical active-work selector, such as a small index file or a deterministic lookup rule, and make README point to that instead of generically referencing a relevant spec and plan.
- Discard explanation:

### Finding GF-006

- Status: solved
- Type: Confirmed issue
- Severity: minor
- Category: operationalization
- Evidence: `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md` say not to add markdownlint-disable directives and require `MD022` compliance, but `CHANGELOG.md` currently begins with markdownlint-disable directives including `MD022`.
- Why it matters: The markdown governance has an undeclared carve-out, which weakens the meaning of “mandatory” markdown rules.
- Recommended minimal fix: remove the markdownlint-disable lines in `CHANGELOG.md` and review the markdown rules correcting them if necessary.
- Discard explanation:

## Ownership Map

- File: `docs/PROJECT_INSTRUCTIONS.md`
  - Current role: Compact authority file plus duplicated workflow and delivery governance.
  - Recommended role: Compact authority file for non-negotiable repo constraints only.
- File: `AGENTS.md`
  - Current role: Full Codex execution and repository governance document, overlapping heavily with project instructions.
  - Recommended role: Codex execution behavior, workflow mechanics, and delivery rules.
- File: `README.md`
  - Current role: Repo orientation, release summary, and governance quick-reference.
  - Recommended role: Current-state repo orientation and navigation only.
- File: `CHANGELOG.md`
  - Current role: Release history and unreleased change tracking.
  - Recommended role: Keep as release history and unreleased change tracking.
- File: `BACKLOG.md`
  - Current role: Pending work inventory with implied changelog coordination.
  - Recommended role: Pending work inventory with explicit operational coordination.
- File: `RELEASE.md`
  - Current role: Human-readable release workflow documentation.
  - Recommended role: Keep both as human-readable and agents release workflow documentation.
- File: `.codex/commands/release.md`
  - Current role: Slash-command invocation contract for release automation.
  - Recommended role: Keep as the command contract only.
- File: `plans/TEMPLATE.md`
  - Current role: Mandatory detailed plan structure for all SDD work.
  - Recommended role: Minimal plan scaffold focused on task-specific decisions and validation.
- File: `specs/` and `plans/`
  - Current role: Required SDD artifacts with uneven operational discoverability.
  - Recommended role: Task-specific decision records with a canonical active-work discovery rule.

## Coordination Gaps

- Gap: `BACKLOG.md` to `CHANGELOG.md` coordination is declared but not operationalized.
  - Evidence: Backlog claims completed tasks move to changelog, while release/workflow automation only handles changelog-facing behavior.
  - Recommended minimal fix: Add a closure or release checkpoint for backlog reconciliation.
- Gap: Active spec/plan selection is required by governance but not backed by a canonical selector.
  - Evidence: Governance requires approved active artifacts, but the repo contains multiple loose unreleased specs and plans with no single active-work index.
  - Recommended minimal fix: Add a deterministic active-work selection rule or index referenced by governance and README.
- Gap: README still duplicates governance and release-summary content instead of routing to owner docs.
  - Evidence: README contains both release summary and workflow rules already owned elsewhere.
  - Recommended minimal fix: Trim README to orientation and pointers only.
- Gap: Markdown governance has an undeclared exception in `CHANGELOG.md`.
  - Evidence: Governance forbids markdownlint-disable directives by default, but changelog uses them without a documented exception.
  - Recommended minimal fix: Make the changelog exception explicit only where
    it is actually needed and remove the undeclared `MD022` carve-out.

## Rewrite Plan

- Step: Separate authority bands between project instructions and agent instructions.
  - Goal: Remove structural duplication between the top two governance files.
  - Files primarily affected: `docs/PROJECT_INSTRUCTIONS.md`, `AGENTS.md`
- Step: Remove release-history and governance leakage from README.
  - Goal: Keep README focused on current-state orientation and repo navigation.
  - Files primarily affected: `README.md`
- Step: Operationalize or relax manual-only coordination claims.
  - Goal: Stop relying on memory for backlog/changelog and active spec/plan selection.
  - Files primarily affected: `BACKLOG.md`, `README.md`, governance docs, release or closure workflow docs
- Step: Simplify the SDD artifact template.
  - Goal: Reduce ceremonial repetition and keep plans task-specific.
  - Files primarily affected: `plans/TEMPLATE.md`, related governance docs
- Step: Resolve markdown-governance exceptions explicitly.
  - Goal: Align actual changelog practice with declared markdown rules.
  - Files primarily affected: `CHANGELOG.md`, governance docs if an exception is kept

## Open Questions

- None.
