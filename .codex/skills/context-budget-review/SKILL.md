---
name: context-budget-review
description: Review governance, skills, scripts, and repository files for context bloat, token-heavy workflows, and progressive-disclosure gaps. Use when the user asks to keep conversations under a context budget, reduce token consumption, or audit files for context efficiency.
---

# Context Budget Review

Use this skill when the requested outcome is lower conversation context usage,
fewer loaded files, or governance and skill changes that keep Codex under a
managed context budget.

## Review Scope

Default review targets:

- `AGENTS.md`
- `docs/PROJECT_INSTRUCTIONS.md`
- `.codex/skills/`
- `.codex/commands/`
- `scripts/`
- task-relevant specs, docs, and templates named by the user

Stay inside narrower user-provided scope. Prefer file lists, `rg`, and short
targeted excerpts over broad reads.

## Context Budget Rules

- Aim to keep active context below 60%.
- Warn the user when estimated context reaches 40%.
- Stop for a compaction or scope decision when estimated context reaches 60%,
  unless the user explicitly asks to continue.
- After each review or implementation iteration, report the estimated context
  consumed as a percentage.
- If no exact context meter is available, clearly label the value as an
  estimate and base it on visible conversation size, loaded files, and outputs.
- Suggest context-saving moves during long conversations, especially narrowing
  scope, deferring unrelated files, summarizing prior findings, or exporting
  durable notes to repository files.

## Review Workflow

1. Verify the branch before editing. If not on `develop`, warn and wait.
2. Define the current iteration in one sentence: scope, files, and intended
   output.
3. Inventory candidate files with `rg --files` or targeted `rg` searches.
4. Read only the smallest excerpts needed to judge context load or ownership.
5. Identify context bloat:
   - duplicated rules across always-loaded governance and skills
   - long skill bodies that should move optional detail into references
   - scripts or docs that require agents to reread large files repeatedly
   - commands that print excessive output by default
   - workflows missing a compact summary or validation hook
6. Recommend or implement the smallest change that reduces future context use.
7. End each iteration with:
   - changed or reviewed files
   - remaining scope, if any
   - validation run, if edits occurred
   - estimated context consumed percentage

## Editing Guidance

- Keep always-loaded router changes minimal.
- Prefer one concise skill over repeated governance text.
- Add references only when they keep `SKILL.md` compact and are directly linked.
- Add scripts only for deterministic summaries or checks that prevent repeated
  manual reading.
- Do not add broad audits, reports, or checklists unless the user asks for an
  exported artifact.

## Validation

- Run `python scripts/validate_governance.py` after governance or router edits.
- Run markdownlint on changed Markdown files when available; `MD013` is
  non-blocking.
- For scripts added or changed, run their smallest meaningful check.
