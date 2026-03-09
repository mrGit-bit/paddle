<!-- markdownlint-disable MD025 -->
# Project Instructions — rankingdepadel.club

Instruction Set Version: 2.2.4  
Last Updated: 2026-03-09

---

This document mirrors the governance configuration used in ChatGPT Project mode.

---

# 1. Purpose

Web application for padel rankings, matches and tournaments.

Includes Android/iOS WebView wrappers using the same backend and frontend (no duplicated business logic).

Stack overview:

- Backend: Django
- Frontend: Django Templates + Bootstrap 5
- Mobile: Capacitor WebView (same URLs)
- API endpoints and DRF use in the backend for those API endpoints are deprecated.

---

# 2. Technology Stack

Python 3.10.12

Databases:

- Development: SQLite
- Staging/Production: Oracle Autonomous Database (TCPS)

Frontend:

- Django Templates
- Bootstrap 5
- Bootstrap Icons
- Vanilla JavaScript only when strictly necessary

---

# 3. Core Governance Principles

- DRY
- KISS
- SRP (Single Responsibility Principle)
- YAGNI (No speculative functionality)
- Explicit > Implicit
- Backend computes business logic
- Templates render only
- No business logic in templates
- No frontend ranking logic
- No speculative refactors

Authority hierarchy:

1. Explicit Task Brief
2. Project Instructions
3. AGENTS.md

If conflict exists:

- Explicit Task Brief prevails.
- Project Instructions prevail over AGENTS.md.

Version control rules for governance docs:

- `Instruction Set Version` and `Last Updated` at the top of this file are mandatory.
- Every change to this file must update both fields in the same commit.
- Every change to this file must also update the mirrored version/date reference in `AGENTS.md`.
- If version/date values differ between this file and `AGENTS.md`, implementation tasks must pause until aligned.

---

# 4. Spec-Driven Development (SDD) — Mandatory Flow (A → B → C)

All work follows three phases: **A) Specification**, **B) Planning**, **C) Implementation**.

No code implementation starts without:

- A written spec in `specs/`
- An approved plan in `/plans/`
- Clear acceptance criteria and validation commands

Before starting any development/implementation/code-change request, Codex MUST check the current git branch.

If the active branch is not `develop`, Codex MUST:

- Warn clearly that work is not currently on `develop`.
- Ask explicitly which branch the user wants the changes applied to.
- Wait for user confirmation before implementing changes.

---

## Phase A — Specification (ChatGPT)

ChatGPT is used for:

- Complex reasoning
- High-level design
- Clarifying requirements

### A1. Clarification First (Mandatory)

Before writing or updating any spec, ChatGPT MUST:

- Ask enough precise questions to obtain a complete, unambiguous specification.
- Clarify scope boundaries (In/Out).
- Clarify constraints (UI, backend, performance, testing).
- Clarify allowed and forbidden files.

No plan is created before specification clarity.

### A2. Spec File (Mandatory)

Once clear, ChatGPT MUST produce a Markdown spec file in:

- `specs/###-short-title.md` (example: `specs/001-auth.md`)

### A2.1. Mandatory Stop After Spec Creation

After creating or updating a spec file, Codex MUST stop implementation work and ask for explicit user review/approval.

Allowed before approval:

- Clarifications and refinements to the spec file
- Other Markdown governance adjustments requested by the user

Forbidden before approval:

- Plan creation
- Product code changes
- Test execution tied to implementation

Each spec MUST include (minimum):

- Functional Goal
- Scope (In / Out)
- UI/UX Requirements
- Backend Requirements
- Data Rules (ordering/tie-breakers/null handling)
- Reuse Rules
- Acceptance Criteria (binary, testable)
- Manual Functional Checks (3–6)
- Files Allowed to Change
- Files Forbidden to Change

### A3. Refinement Antipattern (Continuous Improvement Trigger)

If the ChatGPT clarification cycle requires many corrections AND a recurring cause is identified:
ChatGPT MUST suggest updating `PROJECT_INSTRUCTIONS.md` (and/or `AGENTS.md` / `plans/TEMPLATE.md`) to prevent repetition.

---

## Phase B — Planning (Codex CLI in Plan Mode)

Planning happens in the terminal using Codex CLI **Plan Mode**.

### B1. Plan Template (Mandatory)

All plans must use:

- `/plans/TEMPLATE.md`

### B2. Create Plan File (Mandatory)

The plan must live in:

- `/plans/YYYY-MM-DD_short-description.md`

### B2.1. Mandatory Stop After Plan Creation

After creating or updating a plan file, Codex MUST stop implementation work and ask for explicit user review/approval of the plan.

Allowed before approval:

- Plan refinements requested by the user
- Other Markdown governance/template adjustments requested by the user

Forbidden before approval:

- Product code changes
- Implementation test execution

### B3. Plan Input Source

Codex Plan Mode MUST be instructed to base the plan on:

- the relevant `specs/*.md` file

Codex in Plan Mode:

- MUST NOT write product code
- MAY update repository Markdown files (project/agents/template/spec/plan) when instructed

### B4. Plan Review Loop (Mandatory)

The plan is iterated until approved:

- ChatGPT can review plan quality and completeness
- User edits or requests adjustments
- Repeat until fully agreed

If planning becomes difficult or repeats the same friction:
ChatGPT should recommend improving governance docs or templates.

---

## Phase C — Implementation (Codex CLI Execute Mode)

Only after the plan is approved:

- The latest spec must be explicitly approved by the user.
- The latest plan must be explicitly approved by the user.

### C1. Execute Step-by-Step

Codex is instructed using the plan:

- “Implement Step 1 of `/plans/...md` following `AGENTS.md` rules.”

### C2. Optimization to Reduce Iterations (Continuous Improvement)

C2.1. Capture of Errors:

- If Codex repeats a mistake, add a constraint to `PROJECT_INSTRUCTIONS.md` and/or `AGENTS.md`.

C2.2. Dynamic Checklists:

- After a complex task is completed successfully, request:

  - “Based on this session, propose updates to `/plans/TEMPLATE.md` to avoid the problems we had.”

### C3. Testing & Changelog (Mandatory)

- Tests must be updated/added and executed.
- Coverage target: ≥ 90%.
- `CHANGELOG.md` updated under `## [Unreleased]` unless formatting-only.
- Commit message suggestions must be provided only after the user confirms the current spec implementation cycle is closed.
- Immediately after the recommended commit message, Codex must ask whether to proceed with staging changes, committing with that message, and pushing to the remote branch.

---

# 5. ChatGPT Availability Throughout

ChatGPT remains available in any phase for:

- Clarifications
- Edge cases
- Architectural validation
- Risk evaluation
- Suggesting manual checks

ChatGPT must NOT implement repository code.

---

# 6. Markdown Output Discipline

To avoid truncation and broken paste:

1. Only one fenced block per copy artifact.
2. No nested fences.
3. No partial markdown blocks.
4. If formatting breaks, return flat markdown text.
5. After creating or amending a markdown file, fix all markdownlint violations detected in the document.

## 6.1 Markdownlint Compliance (Mandatory)

For every new or modified Markdown file:

- Do not add `markdownlint-disable` directives unless the user explicitly requests them.
- `MD022` is mandatory: keep exactly one blank line before and after headings.
- `MD032` is mandatory: keep exactly one blank line before and after lists.
- Use consistent list markers (`-` for unordered lists).
- Avoid trailing spaces.
- Keep ordered lists sequential and explicit (`1.`, `2.`, `3.`).
- Ensure files end with a single trailing newline.

Validation workflow:

1. Run markdownlint on the changed Markdown files.
2. Fix violations in the same commit.
3. If markdownlint CLI is unavailable, perform a manual checklist pass using the rules above before delivering.
4. If `MD022` or `MD032` fails, do not deliver until fixed.

When Codex changes PROJECT_INSTRUCTIONS.md, it must explain changes and include the reminder:

`Reminder: update ChatGPT Project Instructions version/date to match this repository.`

---

# End of Project Instructions
