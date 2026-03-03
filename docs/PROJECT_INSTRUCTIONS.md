<!-- markdownlint-disable MD022 -->
<!-- markdownlint-disable MD032 -->
<!-- markdownlint-disable MD034 -->
<!-- markdownlint-disable MD041 -->

This document mirrors the governance configuration used in ChatGPT Project mode.

# Project Instructions — rankingdepadel.club

Instruction Set Version: 2.1.0  
Last Updated: 2026-03-02

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

When Codex changes PROJECT_INSTRUCTIONS.md, it must explain changes and include the reminder:

`Reminder: update ChatGPT Project Instructions version/date to match this repository.`

---

# End of Project Instructions
