<!-- markdownlint-disable MD025 -->
# AGENTS.md — Minimal AI Coding Guidance (Refined)

This file defines **baseline constraints and output standards** for AI coding agents (e.g., Codex CLI) working on the `rankingdepadel.club` project.

It is intentionally minimal in architecture.
All detailed feature instructions are provided explicitly per task.

---

# 1. Project Context

- Stack: Django + Django REST Framework
- Frontend: Django Templates + Bootstrap 5
- JavaScript: Vanilla JS only when strictly necessary
- Databases:
  - Dev: SQLite
  - Staging/Prod: Oracle Autonomous DB (TCPS)

---

# 2. Core Coding Principles (Mandatory)

- **DRY** — Do not duplicate logic.
- **KISS** — Prefer the simplest working solution.
- **SRP** — Single Responsibility Principle.
- **YAGNI** — No speculative functionality.
- **Explicit > Implicit** — Readability over cleverness.

Avoid speculative refactors and large rewrites unless explicitly requested.

---

# 3. Language Rules

- **UI text:** Spanish  
- **Code, variables, comments, documentation:** English  

---

# 4. Backend Rules

- Prefer model properties for computed data.
- Keep business logic in backend code, not templates.
- No frontend ranking logic.
- Reuse existing helpers before introducing new ones.
- Do not duplicate query logic across views.

---

# 5. Frontend Rules

- Use Django templates by default.
- Prefer Bootstrap 5 over custom CSS or JavaScript.
- No business logic in templates.
- Avoid unnecessary JavaScript.
- Do not duplicate template structures if a partial can be reused.

---

# 6. Testing Rules

- Framework: pytest + pytest-django
- Maintain ≥90% coverage.
- Every feature or fix must include tests or test updates.
- Run the smallest relevant pytest scope after changes.
- Tests must validate:
  - Functional behavior
  - Edge cases
  - Expected HTTP status codes

---

# 7. Changelog Discipline

- `CHANGELOG.md` follows *Keep a Changelog*.
- During development: add entries under `## [Unreleased]`.
- On release: move entries to `## [X.Y.Z] - YYYY-MM-DD`.
- Every feature or fix must update the changelog unless purely formatting/comments.

---

# 8. Workflow Expectations

- Architectural decisions are made outside the agent.
- The agent executes **explicit tasks only**.
- If something is unclear or ambiguous, the agent must stop and ask.
- The agent must not introduce improvements beyond the defined scope.

---

# 9. Output Requirements (Strict Format)

Every Codex output must follow this structure:

---

## A. Technical Summary

Bullet list explaining:

- Which components were modified
- Why changes were necessary
- How logic was reused
- Whether any helpers were extracted
- Any performance implications

---

## B. Files Modified

List modified, added or removed files. Do NOT repeat entire files.

---

## C. Tests

- List tests added or modified.
- Explain what behavior is validated.
- Show the pytest command used.
- Show the test result summary (e.g., `4 passed`).

---

## D. Functional Summary (Human-Level)

Short paragraph explaining:

- What changed
- Why it changed
- What the user will experience differently

This must NOT be a list of modified files.
It must describe behavior.

---

## E. Changelog Entry

Show exactly what was added to `CHANGELOG.md`.

---

## F. Recommended Commit Message

Provide a Conventional Commit-style message aligned with the changelog.

---

# 10. Diff Discipline

- No unrelated changes.
- No formatting-only changes unless requested.
- No import reordering unless necessary.
- No variable renaming unless required.
- No file moves unless explicitly requested.

---

# 11. Forbidden Output Patterns

The agent must NOT:

- Output only “modified sections” without summary.
- Output vague descriptions like “Updated view logic”.
- Omit explanation of behavior changes.
- Mix summary with diff.
- Omit test explanation.
- Omit changelog content.

---

# 12. Quality Standard

A task is considered complete only if:

- Functional summary is clear.
- Technical summary is precise.
- Diffs are minimal.
- Tests are present and passing.
- Changelog is updated.
- Commit message is provided.

If any of the above is missing, the task is incomplete.
