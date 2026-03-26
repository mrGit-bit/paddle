# Repository Governance Audit

## Summary

- Scope: Repository-wide governance markdown review.
- Audited target: `AGENTS.md`, `docs/PROJECT_INSTRUCTIONS.md`, `README.md`,
  `CHANGELOG.md`, `BACKLOG.md`, `RELEASE.md`, `specs/`, `plans/`,
  `plans/TEMPLATE.md`, `.codex/commands/release.md`, and
  `scripts/release_orchestrator.py`.
- Audit date: 2026-03-26
- Reviewer: Codex via `governance-markdown-auditor`

The top-level authority split is materially better than the earlier audit
baseline: `docs/PROJECT_INSTRUCTIONS.md`, `AGENTS.md`, `README.md`, and
`plans/TEMPLATE.md` now have cleaner roles and less duplication. The remaining
workflow-coordination findings from the previous audit revision have now been
operationalized through explicit backlog-ownership rules, spec/plan tracking
metadata, and release-tag-based consolidation selection.

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
- Evidence: `scripts/release_orchestrator.py` now parses tracking metadata and
  consolidates only loose spec/plan files whose explicit `Release tag` matches
  the requested release version. `RELEASE.md` now documents that prerequisite
  and no longer describes consolidation as a sweep across all loose files.
- Why it matters: The release-consolidation rule has no reliable provenance
  selector. A future release can misclassify active or unreleased SDD artifacts
  as shipped history and remove the loose source files, which makes the release
  record untrustworthy.
- Recommended minimal fix: Add explicit release provenance for each spec/plan
  that should be consolidated, or require consolidation from a curated release
  manifest instead of sweeping all loose non-release artifacts.
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
  - Recommended role: Keep as release history only; avoid using it as a process
    control surface.
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
  - Recommended role: Keep as decision artifacts with explicit task pairing and
    release provenance.
- File: `plans/TEMPLATE.md`
  - Current role: Minimal active-plan scaffold.
  - Recommended role: Keep minimal and task-specific.

## Coordination Gaps

- None at the current repository-governance scope after the implemented fixes.

## Rewrite Plan

- Step: Preserve the current tracking metadata and release-tag rules on new
  loose specs and plans.
  - Goal: Keep active-work lookup and release provenance operational instead of
    drifting back to filename inference.
  - Files primarily affected: `specs/`, `plans/`, `plans/TEMPLATE.md`,
    governance docs, and release automation when touched.

## Open Questions

- None.
