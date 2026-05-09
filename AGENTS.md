# AGENTS.md — Codex Router

Instruction Set Version: 2.4.7
Last Updated: 2026-05-09

## Authority

1. Explicit task brief
2. `AGENTS.md`
3. Task-relevant skills under `.codex/skills/`

Keep `docs/PROJECT_INSTRUCTIONS.md` and this file aligned by version/date.
`docs/PROJECT_INSTRUCTIONS.md` guides ChatGPT, not Codex execution.

## Minimum Execution Rules

- Verify the branch before development; if not on `develop`, warn and wait
  before editing.
- For non-trivial implementation, use the latest approved non-release spec and
  do not start before approval.
- Small, low-risk docs, governance, or repository-guidance edits may skip a new
  active-work spec.
- Keep edits scoped and never revert user changes unless explicitly requested.
- Keep Markdown concise and specific.

## Skill Routing

- Product, code, SDD planning, specs, audit gates, and repo constraints:
  `$sdd-workflow`.
- Grill-me planning and pressure-tests: use `$sdd-grill-me`.
- Handoffs, reconciliation, commits, pushes, and closure:
  `$development-cycle-closure`.
- Governance ownership, markdown rules, versioning, and validation:
  `$governance-maintenance`.
- Governance markdown audits: `$governance-markdown-auditor`.
- Low-context/token-budget reviews: `$context-budget-review`.
- Creating, adapting, or updating repository Codex skills: `$write-a-skill`.
- Test creation, TDD loops, test refactors, and brittle assertion reviews:
  `$test-design`.
- Django view audits: `$audit`.
- Django template CSS and presentation audits: `$template-presentation-audit`.

## Required Validation

- Run `python scripts/validate_governance.py` after governance edits.
- Run markdownlint on changed Markdown; `MD013` is non-blocking.
- For code changes, run the smallest relevant test scope and report the command
  plus result.
