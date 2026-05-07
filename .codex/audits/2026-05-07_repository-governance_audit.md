# Governance Audit Report

## Summary

- Scope: repository governance after the TDD routing update.
- Audited target: `AGENTS.md`, `docs/PROJECT_INSTRUCTIONS.md`, `README.md`,
  `BACKLOG.md`, `RELEASE.md`, `specs/`, `.codex/commands/`,
  `.codex/skills/`, release workflows, and governance validation.
- Audit date: 2026-05-07.
- Reviewer: Codex using `$governance-markdown-auditor`.

## Governance Findings

### Finding GF-001

- Status: solved
- Type: Confirmed issue
- Severity: minor
- Category: verbosity
- Evidence: `scripts/validate_governance.py` reports
  `AGENTS.md is 1967 characters; target is under 1800`. The router has stayed
  below the hard maximum, but the new TDD route increased a file already above
  the preferred target.
- Why it matters: `AGENTS.md` is always-loaded Codex context. Small routing
  additions are appropriate, but the warning shows the router needs periodic
  tightening to preserve the progressive-disclosure model.
- Recommended minimal fix: Shorten `AGENTS.md` by compressing the minimum
  execution rules or skill routing bullets without changing ownership.
- Discard explanation: Solved by compressing `AGENTS.md` while preserving the
  same routing and safety ownership.

### Finding GF-002

- Status: solved
- Type: Possible risk
- Severity: major
- Category: coordination
- Evidence: Release and backlog responsibility is split across
  `BACKLOG.md`, `RELEASE.md`, `.codex/skills/development-cycle-closure`, and
  `scripts/release_orchestrator.py`. `BACKLOG.md` says closure removes
  completed in-scope items and release consolidation may use completed backlog
  descriptions. The closure skill repeats backlog reconciliation rules.
  `RELEASE.md` says backlog reconciliation is owned by development-cycle
  closure and release consolidation only uses completed wording when available.
- Why it matters: The ownership split is mostly intentional, but it is
  drift-prone because backlog cleanup depends on manual closure behavior while
  release automation consumes only whatever wording remains available.
- Recommended minimal fix: Keep backlog ownership in
  `.codex/skills/development-cycle-closure` and reduce `BACKLOG.md` to one
  pointer plus ordering rules. Keep `RELEASE.md` focused on what the
  orchestrator actually does.
- Discard explanation: Solved by reducing `BACKLOG.md` to ordering plus a
  closure-skill pointer and keeping `RELEASE.md` focused on release behavior.

### Finding GF-003

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: boundary
- Evidence: `.github/workflows/release-prep-codex.yml` still defines
  `Release Prep (Codex)` and instructs Codex to modify `CHANGELOG.md` and
  `BACKLOG.md`. `RELEASE.md` documents `.github/workflows/release-prep-no-ai.yml`
  as the manual dispatch workflow used by the active release flow and says the
  direct orchestrator is the primary supported entrypoint.
- Why it matters: The older Codex workflow preserves an alternate release-prep
  path with broader behavior than the documented no-AI release flow. Even if it
  is unused, its presence makes release ownership less clear.
- Recommended minimal fix: Either delete the obsolete workflow or document it
  explicitly as deprecated and not part of the supported release process.
- Discard explanation: Solved by deleting the obsolete
  `.github/workflows/release-prep-codex.yml` workflow and marking
  `release-prep-no-ai.yml` as the active release-prep workflow in `RELEASE.md`.

### Finding GF-004

- Status: solved
- Type: Suggestion
- Severity: minor
- Category: artifact-value
- Evidence: `specs/TEMPLATE.md` includes an `Implementation Plan` checklist,
  while `.codex/skills/sdd-workflow` says active specs should capture only
  scope, constraints, acceptance checks, and validation needed to execute
  safely.
- Why it matters: Implementation-plan checklists can be useful for larger
  specs, but they can also duplicate Codex planning and become stale when the
  implementation path changes during TDD or code discovery.
- Recommended minimal fix: Make the template's `Implementation Plan` section
  optional or rename it to `Execution Notes` with guidance to keep only stable
  sequencing constraints.
- Discard explanation: Solved by renaming `Implementation Plan` to
  `Execution Notes` in `specs/TEMPLATE.md` and limiting it to stable sequencing
  constraints or required checkpoints.

## Ownership Map

- `AGENTS.md`:
  - Current role: compact Codex router for authority, branch/spec safety, skill
    routing, and validation pointers.
  - Recommended role: Keep as router only; compress enough to clear the
    preferred size target.
- `docs/PROJECT_INSTRUCTIONS.md`:
  - Current role: ChatGPT conversational design and copy-paste pre-spec
    guidance.
  - Recommended role: Keep as ChatGPT-only and aligned by metadata with
    `AGENTS.md`.
- `README.md`:
  - Current role: repository orientation, product map, important paths, and
    testing commands.
  - Recommended role: Keep as current-state orientation and owner-doc index.
- `.codex/skills/sdd-workflow`:
  - Current role: product constraints, SDD gate, planning behavior, checkpoint
    routing, and model/schema change handling.
  - Recommended role: Keep as product/code workflow owner.
- `.codex/skills/test-design`:
  - Current role: test design, brittle assertion guidance, and TDD loop owner.
  - Recommended role: Keep as the detailed owner for test-first execution.
- `.codex/skills/development-cycle-closure`:
  - Current role: implementation handoff, changelog/backlog reconciliation,
    spec closure, commits, pushes, and release consolidation.
  - Recommended role: Keep as the source of truth for cycle closure and
    backlog cleanup.
- `.codex/skills/governance-maintenance`:
  - Current role: governance ownership, progressive disclosure, versioning,
    validation, and markdown style.
  - Recommended role: Keep as governance edit owner.
- `BACKLOG.md`:
  - Current role: manually maintained pending-work inventory plus closure and
    release-consolidation rules.
  - Recommended role: Keep pending-work inventory and ordering rules; point to
    closure skill for reconciliation behavior.
- `RELEASE.md`:
  - Current role: supported release entrypoint, prerequisites, orchestration
    steps, checks, and fallbacks.
  - Recommended role: Keep as release operator guide for the active
    orchestrator only.
- `.codex/commands/release.md`:
  - Current role: optional prompt wrapper around the release orchestrator.
  - Recommended role: Keep as thin wrapper with no independent release logic.
- `specs/`:
  - Current role: active-work specs, template, and consolidated release
    history.
  - Recommended role: Keep active specs concise and consolidate only shipped
    release records.
- `scripts/validate_governance.py`:
  - Current role: header alignment, size-budget warnings/errors, and required
    routed-skill existence checks.
  - Recommended role: Keep as the minimum automated guard for governance
    drift.

## Coordination Gaps

- Gap: Router size is guarded but still above target.
  - Evidence: Governance validation passes with an `AGENTS.md` target warning.
  - Recommended minimal fix: Solved by compressing router wording.
- Gap: Backlog cleanup is manual closure behavior, while release automation
  consumes leftover wording opportunistically.
  - Evidence: `BACKLOG.md`, closure skill, and `RELEASE.md` all describe parts
    of the same lifecycle.
  - Recommended minimal fix: Solved by keeping detailed lifecycle behavior in
    the closure skill and leaving short pointers in `BACKLOG.md` and
    `RELEASE.md`.
- Gap: Supported release prep and legacy Codex release prep coexist.
  - Evidence: `RELEASE.md` documents `release-prep-no-ai.yml`; the repository
    also contains `release-prep-codex.yml`.
  - Recommended minimal fix: Solved by removing the older workflow.

## Rewrite Plan

- Step: Compress the Codex router.
  - Goal: Clear the `AGENTS.md` preferred size target without moving detailed
    behavior back into always-loaded docs.
  - Files primarily affected: `AGENTS.md`.
  - Status: solved.
- Step: Consolidate backlog lifecycle wording.
  - Goal: Make closure skill the source of truth for backlog cleanup.
  - Files primarily affected: `BACKLOG.md`,
    `.codex/skills/development-cycle-closure/SKILL.md`, `RELEASE.md`.
  - Status: solved.
- Step: Resolve the legacy release-prep workflow.
  - Goal: Keep one supported release-prep path visible to operators.
  - Files primarily affected: `.github/workflows/release-prep-codex.yml`,
    `RELEASE.md`.
  - Status: solved.
- Step: Loosen implementation-plan wording in the spec template.
  - Goal: Avoid stale plan checklists while preserving useful execution
    constraints.
  - Files primarily affected: `specs/TEMPLATE.md`,
    `.codex/skills/sdd-workflow/SKILL.md`.
  - Status: solved.

## Open Questions

- Resolved: `.github/workflows/release-prep-codex.yml` was deleted.
