# AGENTS.md — Codex Router

Instruction Set Version: 2.4.15
Last Updated: 2026-05-16

## Authority

1. Explicit task brief
2. `AGENTS.md`
3. Task-relevant skills under `.codex/skills/`

Keep `docs/PROJECT_INSTRUCTIONS.md` metadata aligned; it guides ChatGPT.

## Minimum Execution Rules

- Verify the branch before development; if not `develop`, warn and wait.
- Non-trivial implementation needs the latest approved non-release spec.
- Small docs, governance, or repository-guidance edits may skip a spec.
- Keep edits scoped; never revert/rewrite user changes unless requested.
- Ask before changing unclear user text/style intent.
- Prefer authoritative sources/tools; preserve explicit targets and surface
  fallback or conflict before broad edits.
- Keep Markdown concise.

## Skill Routing

- Product/code, SDD, specs, audit gates: `$sdd-workflow`.
- Planning: `$sdd-grill-me`, `$phased-prd`, `$prd-to-specs`.
- Closure, commits, releases: `$development-cycle-closure`.
- Governance: `$governance-maintenance`,
  `$governance-markdown-auditor`, `$context-budget-review`,
  `$write-a-skill`.
- Debug/tests: `$debug`, `$test-design`.
- Audits: `$audit`, `$template-presentation-audit`.

## Required Validation

- Run `python scripts/validate_governance.py` after governance edits.
- Run markdownlint on Markdown; omit `MD013` and line reflows.
- Run configured linters for touched file types only; do not invent ad hoc
  Python, HTML/template, or JavaScript lint commands.
- For code changes, run the smallest relevant test scope and report result.
