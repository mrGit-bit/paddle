# Governance Audit Report

## Summary

- Scope: progressive governance split in the current uncommitted change set.
- Audited target: `AGENTS.md`, `docs/PROJECT_INSTRUCTIONS.md`, README routing,
  workflow skills, validation script, and related audit skills.
- Audit date: 2026-04-27.
- Reviewer: Codex using `$governance-markdown-auditor`.

## Governance Findings

### Finding GF-001

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: boundary
- Evidence: `AGENTS.md` lists `docs/PROJECT_INSTRUCTIONS.md` above `AGENTS.md`
  in the authority order while the same file now says it is for ChatGPT
  conversational design only and must not be used as the Codex execution
  workflow.
- Why it matters: The new model is intended to make `AGENTS.md` the Codex
  router and `docs/PROJECT_INSTRUCTIONS.md` a ChatGPT-memory artifact. Keeping
  the ChatGPT file in Codex authority order makes the ownership boundary fuzzy
  and invites future edits to put Codex rules back into the ChatGPT file.
- Recommended minimal fix: Change `AGENTS.md` authority wording so Codex
  execution authority is explicit: task brief, `AGENTS.md`, then
  task-relevant skills. Keep `docs/PROJECT_INSTRUCTIONS.md` described as a
  ChatGPT companion file whose version/date must stay aligned, not as Codex
  execution authority.
- Discard explanation: Addressed by removing `docs/PROJECT_INSTRUCTIONS.md`
  from the Codex authority order and describing it as a ChatGPT design
  companion only.

### Finding GF-002

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: operationalization
- Evidence: `scripts/validate_governance.py` now enforces the smaller
  `docs/PROJECT_INSTRUCTIONS.md` budget but does not enforce a size budget for
  `AGENTS.md` or verify that router-required workflow skills exist.
- Why it matters: The requested governance model depends on progressive
  disclosure. Without a validation hook, `AGENTS.md` can quietly grow back into
  a long-form workflow document, or a router entry can point to a missing skill,
  recreating the token-consumption problem the change is meant to solve.
- Recommended minimal fix: Extend `scripts/validate_governance.py` with an
  `AGENTS.md` character target/max and required-skill existence checks for the
  skills named by the router.
- Discard explanation: Addressed by adding `AGENTS.md` target/max checks and
  required routed-skill existence checks to `scripts/validate_governance.py`.

## Ownership Map

- `docs/PROJECT_INSTRUCTIONS.md`:
  - Current role: ChatGPT conversational design and copy-paste pre-spec
    guidance.
  - Recommended role: Keep as ChatGPT-only; remove it from Codex execution
    authority wording.
- `AGENTS.md`:
  - Current role: compact Codex router with branch/spec safety and skill
    routing.
  - Recommended role: Keep as Codex authority/router and validate its size.
- `.codex/skills/sdd-workflow`:
  - Current role: product constraints, SDD gate, planning behavior, and
    checkpoint routing.
  - Recommended role: Keep as the detailed workflow owner for product/code
    tasks.
- `.codex/skills/development-cycle-closure`:
  - Current role: handoff format, changelog/backlog/spec reconciliation,
    closure, commits, pushes, and release consolidation.
  - Recommended role: Keep as the detailed closure owner.
- `.codex/skills/governance-maintenance`:
  - Current role: governance ownership, progressive disclosure, versioning, and
    markdown rules.
  - Recommended role: Keep as the detailed governance-maintenance owner.
- `README.md`:
  - Current role: repository orientation and owner-doc pointers.
  - Recommended role: Keep as current-state orientation only.
- `scripts/validate_governance.py`:
  - Current role: header alignment and ChatGPT instruction size validation.
  - Recommended role: Also validate router size and required skill existence.

## Coordination Gaps

- Gap: Codex authority wording still references the ChatGPT-only file as an
  authority source.
  - Evidence: `AGENTS.md` authority list includes
    `docs/PROJECT_INSTRUCTIONS.md` before `AGENTS.md`.
  - Recommended minimal fix: Solved by rewording the authority section around
    Codex execution ownership.
- Gap: Progressive disclosure is partly policy-only.
  - Evidence: `governance-maintenance` says always-loaded governance should
    stay short, but validation only enforces `docs/PROJECT_INSTRUCTIONS.md`.
  - Recommended minimal fix: Solved by adding automated checks for
    `AGENTS.md` size and required router skills.

## Rewrite Plan

- Step: Clarify Codex authority.
  - Goal: Keep `docs/PROJECT_INSTRUCTIONS.md` out of Codex execution
    authority while preserving metadata alignment.
  - Files primarily affected: `AGENTS.md`, optionally `README.md`.
- Step: Operationalize router validation.
  - Goal: Prevent `AGENTS.md` token creep and stale skill routes.
  - Files primarily affected: `scripts/validate_governance.py`.
- Step: Re-run governance checks.
  - Goal: Confirm the audit fixes preserve the progressive-disclosure model.
  - Files primarily affected: validation output only.

## Open Questions

- None.
