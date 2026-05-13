# AGENTS.md — Codex Router

Instruction Set Version: 2.4.13
Last Updated: 2026-05-13

## Authority

1. Explicit task brief
2. `AGENTS.md`
3. Task-relevant skills under `.codex/skills/`

Keep `docs/PROJECT_INSTRUCTIONS.md` version/date aligned; it guides ChatGPT,
not Codex.

## Minimum Execution Rules

- Verify the branch before development; if not `develop`, warn and wait.
- For non-trivial implementation, use the latest approved non-release spec and
  wait.
- Small docs, governance, or repository-guidance edits may skip a new spec.
- Keep edits scoped; never revert/rewrite user changes unless requested.
- Ask before changing unclear user text/style intent.
- Prefer authoritative sources/tools first; preserve explicit user targets and
  surface fallback or conflict before broad edits.
- Keep Markdown concise.

## Skill Routing

- Product/code, SDD planning, specs, audit gates: `$sdd-workflow`.
- Grill-me planning and pressure-tests: use `$sdd-grill-me`.
- Phased PRDs: `$phased-prd`.
- Handoffs, reconciliation, commits, closure:
  `$development-cycle-closure`.
- Governance ownership, Markdown, validation: `$governance-maintenance`.
- Governance audits: `$governance-markdown-auditor`.
- Context-budget reviews: `$context-budget-review`.
- Create/update repo Codex skills: `$write-a-skill`.
- Bugs, failures, exceptions, flakes, regressions: `$debug`.
- Tests, TDD loops, test refactors, brittle assertions: `$test-design`.
- View audits: `$audit`.
- Template CSS/presentation audits: `$template-presentation-audit`.

## Required Validation

- Run `python scripts/validate_governance.py` after governance edits.
- Run markdownlint on Markdown; omit `MD013` and line reflows.
- Run configured linters for touched file types only when stable project
  commands or tool configs exist.
- Do not invent ad hoc Python, HTML/template, or JavaScript lint commands
  during implementation; report missing configured linters instead.
- For code changes, run the smallest relevant test scope and report the command
  plus result.
