# Governance Audit Report

## Summary

- Scope: default repository governance audit.
- Audited target: `AGENTS.md`, `docs/PROJECT_INSTRUCTIONS.md`, `README.md`,
  `CHANGELOG.md`, `BACKLOG.md`, `RELEASE.md`, `specs/`,
  `.codex/commands/`, `.codex/skills/`, and governance validation.
- Audit date: 2026-05-16.
- Reviewer: Codex using `$governance-markdown-auditor`.

## Governance Findings

### Finding GF-001

- Status: solved
- Type: Confirmed issue
- Severity: minor
- Category: verbosity
- Evidence: `python scripts/validate_governance.py` passes but reports
  `AGENTS.md is 2099 characters; target is under 1800`. The previous
  repository governance audit recorded the same router-size concern as solved,
  but the current router is again above the preferred target. `AGENTS.md`
  still owns only router-level content, but the skill-routing list has grown to
  14 bullets.
- Why it matters: `AGENTS.md` is always-loaded Codex context. The hard limit is
  not exceeded, but recurring warnings show that each new skill route can
  slowly erode the progressive-disclosure budget.
- Recommended minimal fix: Compress the `Skill Routing` section by grouping
  adjacent planning skills and audit/review skills, or raise the preferred
  target only if the larger router is now intentional.
- Discard explanation: Solved by compressing `AGENTS.md` to 1552 characters
  while preserving all routed skills.

### Finding GF-002

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: operationalization
- Evidence: `AGENTS.md` routes `$sdd-grill-me`, `$phased-prd`,
  `$prd-to-specs`, `$context-budget-review`, `$write-a-skill`, and `$debug`.
  `scripts/validate_governance.py` only requires seven skill files:
  `$sdd-workflow`, `$development-cycle-closure`, `$governance-maintenance`,
  `$governance-markdown-auditor`, `$test-design`, `$audit`, and
  `$template-presentation-audit`.
- Why it matters: The router now depends on skills that the governance
  validator does not require. A routed skill can be renamed or deleted while
  validation still passes, leaving an always-loaded instruction that points to
  a missing workflow.
- Recommended minimal fix: Make `scripts/validate_governance.py` derive
  required routed skills from `AGENTS.md`, or add every routed skill to
  `REQUIRED_SKILLS` and keep that list updated when routing changes.
- Discard explanation: Solved by deriving required routed skills from
  `$skill` references in `AGENTS.md`.

### Finding GF-003

- Status: solved
- Type: Confirmed issue
- Severity: major
- Category: operationalization
- Evidence: `BACKLOG.md` defines `Priority = Importance x Simplicity`, but the
  first pending task has `IMP. 2`, `SIMP. 1`, and `PRI. 1`; the calculated
  priority should be `2`. The same table is also broken by a blank line between
  the first and second task rows, which splits one Markdown table into two
  separate table fragments.
- Why it matters: Backlog ordering is manual but still used as the pending-work
  inventory for closure and future planning. A malformed table and incorrect
  priority make the stated ordering rule unreliable.
- Recommended minimal fix: Correct the first task priority, remove the blank
  line inside the table, and add a small governance validation check for backlog
  table shape plus `PRI = IMP * SIMP`.
- Discard explanation: Solved by fixing the backlog table, correcting the
  first task priority, reordering equal-priority rows by simplicity, and adding
  backlog table/scoring validation.

### Finding GF-004

- Status: solved
- Type: Possible risk
- Severity: minor
- Category: coordination
- Evidence: `README.md` points to `docs/PROJECT_INSTRUCTIONS.md`,
  `AGENTS.md`, `.codex/skills`, `CHANGELOG.md`, `BACKLOG.md`, `RELEASE.md`,
  and `specs/` as governance surfaces. `$phased-prd` now creates persistent
  PRDs under `docs/prds/`, and `$prd-to-specs` expects source material there,
  but `README.md` does not identify `docs/prds/` as a planning artifact
  location.
- Why it matters: The phased-PRD workflow is new enough that users and agents
  may not discover where durable PRDs live from the repository orientation
  guide. This is not blocking today because the skills name the path directly,
  but it is an ownership-map gap.
- Recommended minimal fix: Add `docs/prds/` to `README.md` only if the
  repository intends PRDs to become a durable planning surface; otherwise state
  in `$phased-prd` that the directory is created on demand and not part of the
  standing repository guide.
- Discard explanation: Solved by keeping `docs/prds/` as an on-demand,
  skill-owned planning directory and documenting that in the PRD skills instead
  of adding it to `README.md`.

## Ownership Map

- `AGENTS.md`:
  - Current role: compact Codex router for authority, branch/spec safety,
    skill routing, and validation pointers.
  - Recommended role: Solved by keeping the 1800-character target and
    compressing route wording.
- `docs/PROJECT_INSTRUCTIONS.md`:
  - Current role: ChatGPT conversational design and copy-paste pre-spec
    guidance.
  - Recommended role: Keep as ChatGPT-only guidance aligned by metadata with
    `AGENTS.md`.
- `README.md`:
  - Current role: current-state repository orientation, important paths,
    product map, and common testing commands.
  - Recommended role: Keep as orientation and owner-doc index; `docs/prds/`
    remains skill-owned and on demand.
- `.codex/skills/sdd-workflow`:
  - Current role: product/code workflow, SDD gate, repository constraints,
    planning behavior, and checkpoint routing.
  - Recommended role: Keep as product/code workflow owner.
- `.codex/skills/phased-prd`:
  - Current role: durable PRD creation before phased implementation specs.
  - Recommended role: Keep as PRD owner and clarify that `docs/prds/` is
    on-demand skill-owned planning storage.
- `.codex/skills/prd-to-specs`:
  - Current role: converting approved PRDs into vertical-slice active specs.
  - Recommended role: Keep as bridge from PRD planning to normal SDD gating.
- `.codex/skills/development-cycle-closure`:
  - Current role: implementation handoff, changelog/backlog reconciliation,
    spec closure, commits, pushes, and release consolidation.
  - Recommended role: Keep as closure source of truth.
- `.codex/skills/governance-maintenance`:
  - Current role: governance ownership, progressive disclosure, versioning,
    validation, and Markdown style.
  - Recommended role: Keep as governance edit owner.
- `.codex/skills/governance-markdown-auditor`:
  - Current role: governance markdown audit workflow and exported report shape.
  - Recommended role: Keep as audit owner.
- `CHANGELOG.md`:
  - Current role: compact unreleased and shipped outcome history.
  - Recommended role: Keep outcome-focused, grouped by stable domains.
- `BACKLOG.md`:
  - Current role: public pending-work inventory with manual priority ordering.
  - Recommended role: Keep as pending inventory with mechanically checked
    scoring and ordering rules.
- `RELEASE.md`:
  - Current role: release operator guide for the orchestrator and fallbacks.
  - Recommended role: Keep as active release-flow owner.
- `.codex/commands/release.md`:
  - Current role: thin optional prompt wrapper around the release orchestrator.
  - Recommended role: Keep as wrapper only.
- `specs/`:
  - Current role: active work template and consolidated release records.
  - Recommended role: Keep active specs concise and release records compact.
- `scripts/validate_governance.py`:
  - Current role: metadata alignment, size-budget checks, and selected required
    skill existence checks.
  - Recommended role: Keep routed-skill and backlog-invariant validation.

## Coordination Gaps

- Gap: Router skill routing and governance validation are out of sync.
  - Evidence: `AGENTS.md` routes more skills than
    `scripts/validate_governance.py` requires.
  - Recommended minimal fix: Solved by deriving routed skills in the validator.
- Gap: Backlog priority rules are prose-only.
  - Evidence: `BACKLOG.md` states a priority formula, but the current table
    includes an incorrect calculated value and malformed Markdown table shape.
  - Recommended minimal fix: Solved by adding validator checks for backlog row
    shape, numeric columns, formula correctness, and descending priority order.
- Gap: PRD planning paths are skill-owned but not listed in the README
  ownership map.
  - Evidence: `$phased-prd` and `$prd-to-specs` use `docs/prds/`; `README.md`
    does not mention the path.
  - Recommended minimal fix: Solved by documenting `docs/prds/` as on-demand
    skill-owned storage in the PRD skills.

## Rewrite Plan

- Step: Reconcile router size.
  - Goal: Bring `AGENTS.md` under the preferred target or update the target
    intentionally.
  - Files primarily affected: `AGENTS.md`,
    `scripts/validate_governance.py`.
  - Status: solved.
- Step: Close the routed-skill validation gap.
  - Goal: Ensure every `$skill` route in `AGENTS.md` has a required local
    `SKILL.md` validation check.
  - Files primarily affected: `scripts/validate_governance.py`.
  - Status: solved.
- Step: Repair and validate backlog ordering.
  - Goal: Make the pending-work inventory match its stated priority formula.
  - Files primarily affected: `BACKLOG.md`,
    `scripts/validate_governance.py`.
  - Status: solved.
- Step: Decide PRD discoverability.
  - Goal: Keep new phased-PRD artifacts discoverable without bloating
    always-loaded router docs.
  - Files primarily affected: `README.md`,
    `.codex/skills/phased-prd/SKILL.md`,
    `.codex/skills/prd-to-specs/SKILL.md`.
  - Status: solved.

## Open Questions

- Resolved: keep `AGENTS.md` under the 1800-character preferred target.
- Resolved: keep `docs/prds/` out of `README.md`; document it as on-demand
  skill-owned storage in the PRD skills.
