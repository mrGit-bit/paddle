<!-- markdownlint-disable MD032 -->
<!-- markdownlint-disable MD022 -->
# Repository Governance Docs

## Context
- Governance rules were split across chat context and repository docs.
- Agents need an in-repo source of truth and clear pointers for when to consult it.

## Objectives
- Add `/docs/PROJECT_INSTRUCTIONS.md` with the exact project instruction text.
- Add short governance references in `README.md`.
- Add a minimal governance lookup section in `AGENTS.md` with authority hierarchy.

## Scope
### In
- Create `/docs/PROJECT_INSTRUCTIONS.md`.
- Update `README.md` with a concise `Governance & AI Workflow` section.
- Update `AGENTS.md` with a minimal `Governance Docs` section.
- Validate diff scope is limited to requested files.

### Out
- No Python code changes.
- No tests changes.
- No CI changes.
- No refactors outside documentation.

## Risks
- Doc drift between ChatGPT Project-mode config and repository copy.
- Scope drift if unrelated files are modified during edits.

## Plan Steps
- [x] Create plan file using `/plans/TEMPLATE.md` structure.
- [x] Create `/docs/PROJECT_INSTRUCTIONS.md` with mirror note and exact provided instructions.
- [x] Add `Governance & AI Workflow` references near the top of `README.md`.
- [x] Add minimal `Governance Docs` section to `AGENTS.md`.
- [x] Validate only requested files were changed.
- [x] Record post-mortem notes.

## Acceptance Criteria
- `/docs/PROJECT_INSTRUCTIONS.md` exists and includes full provided instructions plus mirror note.
- `README.md` references `/docs/PROJECT_INSTRUCTIONS.md`, `AGENTS.md`, and `/plans/`.
- `AGENTS.md` includes minimal `Governance Docs` section with consult triggers and authority order.
- No unrelated files modified for this task.

## Validation Commands
- `git -C /workspaces/paddle diff -- README.md AGENTS.md docs/PROJECT_INSTRUCTIONS.md plans/2026-02-28_repository_governance_docs.md`
- `git -C /workspaces/paddle status --short README.md AGENTS.md docs/PROJECT_INSTRUCTIONS.md plans/2026-02-28_repository_governance_docs.md`

## Execution Log
- 2026-02-28 10:56 UTC - Plan execution started.
- 2026-02-28 10:57 UTC - Added governance section to `README.md`.
- 2026-02-28 10:57 UTC - Added minimal `Governance Docs` section to `AGENTS.md`.
- 2026-02-28 11:00 UTC - Created `/docs/PROJECT_INSTRUCTIONS.md` from provided source text.
- 2026-02-28 11:01 UTC - Created this task plan record.
- 2026-02-28 11:02 UTC - Ran path-scoped diff/status validation for requested files.

## Post-Mortem / Improvements
- Required scope was met with documentation-only edits and explicit path-scoped validation.
- Main risk remains future drift between ChatGPT Project-mode config and repo copy; keep this file updated when governance changes.
