# Governance Audit Report

## Summary

- Scope: Repository governance markdown, focused on duplication and verbosity
  between `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md`.
- Audited target: `docs/PROJECT_INSTRUCTIONS.md`, `AGENTS.md`, `README.md`,
  `BACKLOG.md`, `RELEASE.md`, `.codex/commands/release.md`, `specs/TEMPLATE.md`,
  and prior repository-governance audits.
- Audit date: `2026-04-12`
- Reviewer: Codex

## Governance Findings

### Finding GF-001

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: duplication
- Evidence: `docs/PROJECT_INSTRUCTIONS.md` defines the active-work and loose
  spec lifecycle in lines 46-84. `AGENTS.md` repeats the same lifecycle and
  release-consolidation details in lines 56-87. `README.md` repeats a shorter
  version of the same loose-spec lifecycle in lines 89-101.
- Why it matters: Three files now teach the same SDD lifecycle. Any future
  lifecycle edit has to be made in several places, and the compact ChatGPT
  Project Instructions file is forced to carry detail that `AGENTS.md`,
  `README.md`, and release docs can already point to.
- Recommended minimal fix: Make `docs/PROJECT_INSTRUCTIONS.md` the only compact
  lifecycle contract. In `AGENTS.md`, replace the repeated lifecycle paragraph
  with execution-only behavior that says to follow the project-instructions
  lifecycle. In `README.md`, keep only routing text and remove lifecycle bullets.
- Discard explanation:

### Finding GF-002

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: boundary
- Evidence: `docs/PROJECT_INSTRUCTIONS.md` lines 86-118 contain Plan Mode,
  pre-spec, review/audit, migration, and post-release behavior. `AGENTS.md`
  repeats and expands the same areas in lines 99-155.
- Why it matters: The stated ownership split says `PROJECT_INSTRUCTIONS.md`
  owns compact constraints while `AGENTS.md` owns workflow mechanics. The
  current split leaks mechanics into the compact file and repeats compact rules
  in the long-form file.
- Recommended minimal fix: Keep only short gate-level rules in
  `PROJECT_INSTRUCTIONS.md`: Plan Mode may update Markdown, ChatGPT pre-specs
  are concise starting points, checkpoints must be considered, migrations must
  be applied, and post-release reconciliation blocks new SDD work. Move the
  detailed question-loop, finding-handling, and consolidation prose to
  `AGENTS.md`.
- Discard explanation:

### Finding GF-003

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: verbosity
- Evidence: `docs/PROJECT_INSTRUCTIONS.md` is exactly 7800 characters, the hard
  maximum declared in lines 29-31. It still includes git sequencing, no-GPG
  commit behavior, closure confirmation wording, changelog category examples,
  lint exceptions, and handoff reminder text in lines 120-161. `AGENTS.md`
  covers the same operational areas in lines 157-223.
- Why it matters: The compact file has no remaining budget. Each small process
  fix now triggers compression work, version churn, and risk of crossing the
  ChatGPT Project Instructions limit.
- Recommended minimal fix: Shrink `PROJECT_INSTRUCTIONS.md` below 7000
  characters by moving command mechanics, detailed closure flow, and Markdown
  lint detail to `AGENTS.md`. Keep only portable rules that ChatGPT needs before
  handing work to Codex CLI.
- Discard explanation:

### Finding GF-004

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: duplication
- Evidence: Closure and backlog reconciliation appear in
  `docs/PROJECT_INSTRUCTIONS.md` lines 120-141, `AGENTS.md` lines 170-197, and
  `BACKLOG.md` lines 24-29. `RELEASE.md` also states that backlog
  reconciliation is not owned by release automation.
- Why it matters: The same closure rule is scattered across four files. The
  repeated text is not identical in scope, which makes it harder to know which
  file should be changed when closure behavior changes.
- Recommended minimal fix: Make `AGENTS.md` own closure mechanics, make
  `BACKLOG.md` own backlog table maintenance, and make `RELEASE.md` only state
  that release automation does not own backlog reconciliation. In
  `PROJECT_INSTRUCTIONS.md`, keep one short closure outcome rule.
- Discard explanation:

### Finding GF-005

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: coordination
- Evidence: Both governance headers must stay aligned, and
  `PROJECT_INSTRUCTIONS.md` line 159 adds a manual handoff reminder to sync
  ChatGPT Project Instructions. There is no observed command, check, or script
  that verifies version/date parity or the 7800-character cap before closure.
- Why it matters: The repo depends on manual sync between a checked-in file,
  another checked-in file, and external ChatGPT Project Instructions. Manual
  reminders have already caused small governance edits to touch multiple files.
- Recommended minimal fix: Add a lightweight validation command or script that
  checks `PROJECT_INSTRUCTIONS.md` size and header alignment with `AGENTS.md`.
  Then shorten the prose reminders to point at that check.
- Discard explanation:

## Ownership Map

- File: `docs/PROJECT_INSTRUCTIONS.md`
  - Current role: Compact constraints plus a large portion of execution,
    closure, planning, audit, release, and Markdown handling rules.
  - Recommended role: Compact ChatGPT-loadable authority: product constraints,
    minimum gates, one-line lifecycle rules, and pointers to owner docs.
- File: `AGENTS.md`
  - Current role: Long-form execution guide that repeats many compact rules.
  - Recommended role: Sole owner for Codex mechanics, planning-loop behavior,
    closure prompts, git sequencing, no-GPG commits, and handoff details.
- File: `README.md`
  - Current role: Repository orientation plus some SDD lifecycle explanation.
  - Recommended role: Current-state orientation and routing only; link to the
    governance owners instead of restating lifecycle rules.
- File: `BACKLOG.md`
  - Current role: Pending work inventory plus backlog reconciliation rule.
  - Recommended role: Own backlog table semantics and removal rules only.
- File: `RELEASE.md`
  - Current role: Primary release-flow source with some boundaries against
    closure-owned backlog work.
  - Recommended role: Own release automation behavior and avoid restating
    development-cycle closure except where a release boundary is needed.
- File: `.codex/commands/release.md`
  - Current role: Optional wrapper around release automation.
  - Recommended role: Thin command wrapper that mirrors `RELEASE.md` without
    independent governance.
- File: `specs/TEMPLATE.md`
  - Current role: Compact active-work spec template.
  - Recommended role: Keep compact; do not absorb governance narrative.

## Coordination Gaps

- Gap: No automated check guards governance size and header alignment.
  - Evidence: Size and version rules exist in prose in
    `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md`, but no matching validation
    command was observed.
  - Recommended minimal fix: Add a small governance validation script and run it
    for governance-doc changes.
- Gap: README repeats lifecycle rules that should be discoverable through owner
  docs.
  - Evidence: `README.md` lines 89-101 repeat spec lifecycle rules already
    covered by `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md`.
  - Recommended minimal fix: Replace those bullets with a single pointer to the
    project instructions and release docs.

## Rewrite Plan

- Step: Reassert file ownership.
  - Goal: Keep `PROJECT_INSTRUCTIONS.md` compact and make `AGENTS.md` the
    execution-detail owner.
  - Files primarily affected: `docs/PROJECT_INSTRUCTIONS.md`, `AGENTS.md`
- Step: Remove repeated lifecycle prose from orientation docs.
  - Goal: Keep README useful for navigation without teaching SDD policy.
  - Files primarily affected: `README.md`
- Step: Collapse closure/backlog wording.
  - Goal: Leave one source of truth for closure mechanics and one for backlog
    table maintenance.
  - Files primarily affected: `docs/PROJECT_INSTRUCTIONS.md`, `AGENTS.md`,
    `BACKLOG.md`, `RELEASE.md`
- Step: Add a governance validation hook.
  - Goal: Replace manual size/header reminders with a checkable command.
  - Files primarily affected: `scripts/`, `docs/PROJECT_INSTRUCTIONS.md`,
    `AGENTS.md`

## Open Questions

- None.
