# AGENTS.md — Codex Router

Instruction Set Version: 2.4.9
Last Updated: 2026-05-10

## Authority

1. Explicit task brief
2. `AGENTS.md`
3. Task-relevant skills under `.codex/skills/`

Keep `docs/PROJECT_INSTRUCTIONS.md` aligned by version/date.
`docs/PROJECT_INSTRUCTIONS.md` guides ChatGPT, not Codex.

## Minimum Execution Rules

- Verify the branch before development; if not `develop`, warn and wait.
- For non-trivial implementation, use the latest approved non-release spec and
  wait for approval.
- Small docs, governance, or repository-guidance edits may skip a new spec.
- Keep edits scoped; never revert/rewrite user changes unless requested.
- Ask before changing unclear user text/style intent.
- Keep Markdown concise.

## Skill Routing

- Product/code work, SDD planning, specs, audit gates, and repo constraints:
  `$sdd-workflow`.
- Grill-me planning and pressure-tests: use `$sdd-grill-me`.
- Handoffs, reconciliation, commits, pushes, and closure:
  `$development-cycle-closure`.
- Governance ownership, Markdown rules, validation: `$governance-maintenance`.
- Governance markdown audits: `$governance-markdown-auditor`.
- Context-budget reviews: `$context-budget-review`.
- Creating, adapting, or updating repo Codex skills: `$write-a-skill`.
- Debugging bugs, failures, exceptions, flakes, and regressions: `$debug`.
- Test creation, TDD loops, test refactors, and brittle assertion reviews:
  `$test-design`.
- Django view audits: `$audit`.
- Django template CSS/presentation audits: `$template-presentation-audit`.

## Required Validation

- Run `python scripts/validate_governance.py` after governance edits.
- Run markdownlint on changed Markdown; `MD013` is non-blocking.
- For code changes, run the smallest relevant test scope and report the command
  plus result.
