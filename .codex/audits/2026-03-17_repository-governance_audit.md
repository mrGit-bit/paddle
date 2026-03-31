# Repository Governance Audit

## Summary

- Scope: Repository-wide governance markdown review.
- Audited target: `AGENTS.md`, `docs/PROJECT_INSTRUCTIONS.md`, `README.md`,
  `CHANGELOG.md`, `BACKLOG.md`, `RELEASE.md`, `specs/`, `plans/`,
  `plans/TEMPLATE.md`, `.codex/commands/release.md`, and
  `scripts/release_orchestrator.py`.
- Audit date: 2026-03-31
- Reviewer: Codex via `governance-markdown-auditor`

The top-level authority split remains materially better than the earlier audit
baseline. Most prior findings still hold as solved, but this review found one
release-consolidation regression and one README authority-drift issue in the
post-`v1.6.1` changes.

## Governance Findings

### Finding GF-001

- Status: solved
- Type: Confirmed issue
- Severity: critical
- Category: boundary
- Evidence: `docs/PROJECT_INSTRUCTIONS.md` now stays compact and points
  `AGENTS.md` to execution mechanics instead of mirroring the same full rule
  set. `AGENTS.md` is now shorter and focused on execution workflow and handoff
  behavior.
- Why it matters: The top two governance files now have a usable authority
  split, which lowers drift risk and makes updates cheaper.
- Recommended minimal fix: Keep the current split and avoid moving repository
  constraints back into `AGENTS.md`.
- Discard explanation:

### Finding GF-002

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: duplication
- Evidence: `README.md` is now current-state repository orientation and routing.
  It no longer carries a release-history summary and primarily points to owner
  docs such as `docs/PROJECT_INSTRUCTIONS.md`, `AGENTS.md`, `CHANGELOG.md`, and
  `RELEASE.md`.
- Why it matters: README is readable again as a navigation document instead of a
  second governance source of truth.
- Recommended minimal fix: Keep README limited to orientation, key paths, and
  routing.
- Discard explanation:

### Finding GF-003

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: operationalization
- Evidence: `docs/PROJECT_INSTRUCTIONS.md`, `AGENTS.md`, and `BACKLOG.md` now
  assign backlog reconciliation to development-cycle closure explicitly.
  `RELEASE.md` now states that `/prompts:release` does not own backlog
  reconciliation unless a future release workflow explicitly implements it.
- Why it matters: The repository treats backlog cleanup as mandatory, but the
  rule still depends on agent memory at the highest-friction points: release
  closure and development-cycle closure.
- Recommended minimal fix: Choose one owner for backlog reconciliation and
  either operationalize it in the release/closure automation or explicitly
  downgrade it from a mandatory workflow rule to a manual recommendation.
- Discard explanation:

### Finding GF-004

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: artifact-value
- Evidence: `plans/TEMPLATE.md` is now short and task-specific. It no longer
  requires file-by-file ceremonial detail, execution logs, or post-mortem
  sections for every task by default.
- Why it matters: The SDD plan artifact now has clearer execution value and less
  low-signal process overhead.
- Recommended minimal fix: Keep the template minimal and add extra sections only
  when a task actually needs them.
- Discard explanation:

### Finding GF-005

- Status: solved
- Type: Possible risk
- Severity: major
- Category: coordination
- Evidence: Loose non-release specs and plans now carry explicit `Tracking`
  blocks with `Task ID`, `Plan` / `Spec`, and `Release tag` fields. README,
  `docs/PROJECT_INSTRUCTIONS.md`, and `AGENTS.md` now point active-work lookup
  to shared `Task ID` metadata and explicit cross-references rather than
  filename similarity alone.
- Why it matters: The rule is clearer than before, but not fully operational.
  Agents can still pick the wrong artifact pair when multiple governance-heavy
  tasks exist in parallel.
- Recommended minimal fix: Add a lightweight task identifier or explicit plan
  reference field that makes the spec-plan pairing and active-work lookup
  inspectable without name guessing.
- Discard explanation:

### Finding GF-006

- Status: solved
- Type: Confirmed issue
- Severity: minor
- Category: operationalization
- Evidence: The markdown-governance exception for `CHANGELOG.md` is now explicit
  and limited to `MD024`, matching the actual file header.
- Why it matters: The declared markdown rules now match the observable
  repository practice.
- Recommended minimal fix: Keep changelog exceptions explicit and narrow.
- Discard explanation:

### Finding GF-007

- Status: solved
- Type: Confirmed issue
- Severity: critical
- Category: coordination
- Evidence: [scripts/release_orchestrator.py](/workspaces/paddle/scripts/release_orchestrator.py#L512)
  now consolidates only loose files whose `Release tag` exactly matches the
  requested `vX.Y.Z`. [RELEASE.md](/workspaces/paddle/RELEASE.md#L40),
  [AGENTS.md](/workspaces/paddle/AGENTS.md#L60), and
  [docs/PROJECT_INSTRUCTIONS.md](/workspaces/paddle/docs/PROJECT_INSTRUCTIONS.md#L84)
  now align on the same explicit shipped-work selector.
- Why it matters: The release-consolidation rule has no reliable provenance
  selector. A future release can misclassify active or unreleased SDD artifacts
  as shipped history and remove the loose source files, which makes the release
  record untrustworthy.
- Recommended minimal fix: Restore an explicit shipped-work selector for
  consolidation. For example, require a curated release manifest or a
  pre-consolidation step that marks only the actually shipped loose files with
  the requested `vX.Y.Z`, then consolidate only exact matches.
- Discard explanation:

### Finding GF-008

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: verbosity
- Evidence: `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md` now require light,
  schematic Markdown by default. `CHANGELOG.md`, active specs/plans,
  `plans/TEMPLATE.md`, and consolidated release files have been shortened to
  compact summaries and provenance records.
- Why it matters: Verbose process Markdown slows agent lookup, hides the actual
  rule or shipped fact, and inflates release-history files with low-value
  narrative.
- Recommended minimal fix: Keep Markdown compact by default, especially in
  changelog entries, active specs/plans, and consolidated release history.
- Discard explanation:

### Finding GF-009

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: boundary
- Evidence: [README.md](/workspaces/paddle/README.md#L107) now defers the
  reduced-process rule to the higher-authority governance docs instead of
  restating the stale “explicit approval first” variant.
- Why it matters: README is the repository orientation document that agents are
  told to read early. When it restates execution mechanics incorrectly, it
  becomes a competing source of truth and can drive inconsistent behavior on
  minor documentation or governance tasks.
- Recommended minimal fix: Remove that execution-detail sentence from README or
  align it exactly with the higher-authority rule instead of restating a stale
  variant.
- Discard explanation:

## Ownership Map

- File: `docs/PROJECT_INSTRUCTIONS.md`
  - Current role: Compact repository constraints and minimum SDD gates.
  - Recommended role: Keep as the compact, high-priority repository authority.
- File: `AGENTS.md`
  - Current role: Codex execution behavior, workflow mechanics, and handoff
    rules.
  - Recommended role: Keep as execution and delivery behavior only.
- File: `README.md`
  - Current role: Current-state repository orientation and owner-doc routing.
  - Recommended role: Keep as orientation, path guide, and reading order.
- File: `CHANGELOG.md`
  - Current role: Release history and unreleased documented changes.
  - Recommended role: Keep as release history only; use compact outcome
    bullets instead of process narration.
- File: `BACKLOG.md`
  - Current role: Public pending-work inventory with closure-owned
    reconciliation.
  - Recommended role: Keep as pending-work inventory with explicit closure
    ownership.
- File: `RELEASE.md`
  - Current role: Human-readable release workflow and prerequisites, limited to
    what the release command actually owns.
  - Recommended role: Keep as release operator guidance and explicit release
    prerequisite documentation.
- File: `.codex/commands/release.md`
  - Current role: Thin release-command contract.
  - Recommended role: Keep as invocation contract only.
- File: `specs/` and `plans/`
  - Current role: Active-work and historical release artifacts stored in the
    same directories, with explicit task and release tracking metadata on loose
    non-release files.
  - Recommended role: Keep as schematic decision artifacts with explicit task
    pairing and release provenance.
- File: `plans/TEMPLATE.md`
  - Current role: Minimal active-plan scaffold.
  - Recommended role: Keep minimal and task-specific.

## Coordination Gaps

- Gap: Release consolidation no longer has a reliable shipped-work selector
  once multiple loose files share `Release tag: unreleased`.
  - Evidence: [scripts/release_orchestrator.py](/workspaces/paddle/scripts/release_orchestrator.py#L527)
    selects `unreleased` sources for any requested version and
    [scripts/release_orchestrator.py](/workspaces/paddle/scripts/release_orchestrator.py#L616)
    rewrites and deletes them during consolidation.
  - Recommended minimal fix: Select shipped loose files explicitly before
    consolidation instead of treating all `unreleased` files as part of the
    current release.
- Gap: README repeats an execution rule that has already changed in the owner
  docs.
  - Evidence: [README.md](/workspaces/paddle/README.md#L107),
    [AGENTS.md](/workspaces/paddle/AGENTS.md#L71), and
    [docs/PROJECT_INSTRUCTIONS.md](/workspaces/paddle/docs/PROJECT_INSTRUCTIONS.md#L67)
    disagree on whether an extra confirmation turn is required for clearly
    minor reduced-process edits.
  - Recommended minimal fix: Keep README focused on routing, or align any
    execution-detail restatements exactly with the owner docs.

## Rewrite Plan

- Step: Restore explicit provenance selection before release consolidation.
  - Goal: Prevent unrelated in-progress loose specs/plans from being stamped,
    archived, and deleted as shipped history.
  - Files primarily affected: `scripts/release_orchestrator.py`, `RELEASE.md`,
    `AGENTS.md`, and `docs/PROJECT_INSTRUCTIONS.md`.
- Step: Remove stale execution-detail duplication from README.
  - Goal: Keep README as routing/orientation instead of a competing execution
    authority.
  - Files primarily affected: `README.md`.
- Step: Preserve the compact Markdown rule on new governance/history edits.
  - Goal: Keep changelog/spec/plan artifacts fast to scan.
  - Files primarily affected: `CHANGELOG.md`, `specs/`, `plans/`,
    `plans/TEMPLATE.md`, and governance docs.

## Open Questions

- None.
