# AGENTS.md — Codex Router

Instruction Set Version: 2.4.1
Last Updated: 2026-05-03

## Authority

1. Explicit task brief
2. `AGENTS.md`
3. Task-relevant skills under `.codex/skills/`

Keep `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` version/date headers
aligned. `docs/PROJECT_INSTRUCTIONS.md` is a ChatGPT design companion, not a
Codex execution authority.

## Minimum Execution Rules

- Verify the current branch before development or implementation.
- If not on `develop`, warn and wait for confirmation before editing.
- Use the latest approved non-release spec for non-trivial implementation work.
- Do not implement before the active-work spec is approved.
- Small, low-risk docs, governance, or repository-guidance edits may skip a new
  active-work spec.
- Keep edits scoped to the task and never revert user changes unless explicitly
  requested.

## Skill Routing

- Product, code, SDD planning, specs, audits gate selection, and repository
  constraints: use `$sdd-workflow`.
- Grill-me planning and pressure-tests: use `$sdd-grill-me`.
- Handoffs, changelog/backlog/spec reconciliation, commits, pushes, and cycle
  closure: use `$development-cycle-closure`.
- Governance ownership, markdown rules, versioning, and validation: use
  `$governance-maintenance`.
- Governance markdown audits: use `$governance-markdown-auditor`.
- Django view behavior/security/reuse audits: use `$audit`.
- Django template CSS and presentation audits: use
  `$template-presentation-audit`.

## Required Validation

- Run `python scripts/validate_governance.py` after governance edits.
- Run markdownlint on changed Markdown files when available; `MD013` is
  non-blocking.
- For code changes, run the smallest relevant test scope and report the command
  plus result.
