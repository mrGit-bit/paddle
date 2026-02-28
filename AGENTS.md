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

## C. Changelog Entry

Show exactly what was added to `CHANGELOG.md`.

---

## D. Functional Summary (Human-Level)

Short paragraph explaining:

- What changed
- Why it changed
- What the user will experience differently

This must NOT be a list of modified files.
It must describe behavior.

---

## E. Checks & Tests Confirmation

- Confirm checks/tests status clearly (`passed` / `failed`).
- Include the command(s) executed.
- Include concise result summary (e.g., `4 passed`, `1 failed`).

---

## F. Recommended Commit Message

Provide a Conventional Commit-style message aligned with the changelog.

---

## G. Continuous Improvement Question

End every output with:
"What should I improve next time? (plan clarity, diff granularity, test scope, commit message precision, other?)"

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
- Omit the final continuous improvement question.

---

# 12. Quality Standard

A task is considered complete only if:

- Functional summary is clear.
- Technical summary is precise.
- Diffs are minimal.
- Tests are present and passing.
- Changelog is updated.
- Commit message is provided.
- Output ends with the required sequence:
  `D. Functional Summary` → `E. Checks & Tests Confirmation` → `F. Recommended Commit Message` → `G. Continuous Improvement Question`.

If any of the above is missing, the task is incomplete.

---

# 13. Plan Mode Workflow

Use `/plan` before implementation for:

- Any multi-step change.
- Structural refactors.
- Cross-app modifications.
- Test suite changes.
- Changes affecting deployment or configuration.

Rules:

- Create a new plan file in `/plans/` using `/plans/TEMPLATE.md`.
- Use file name format: `YYYY-MM-DD_short-description.md`.
- Do not execute implementation until the plan is approved.
- Update the plan file during execution (mark completed steps).
- Add post-mortem notes at the end of execution.
- Suggest improvements to `AGENTS.md` if recurring patterns emerge.

Feedback Loop:

- After successful completion, ask: "What should I improve next time? (plan clarity, diff granularity, test scope, commit message precision, other?)"

---

# 14. Governance Docs

- Governance and workflow rules: `/docs/PROJECT_INSTRUCTIONS.md`
- Consult it when:
  - A task is ambiguous about workflow/roles/approval steps.
  - A change affects multiple apps or cross-cutting concerns (deployment, changelog discipline, plan mode).
  - A task conflicts with rules in `AGENTS.md` or the brief.
- Authority: Explicit task brief > Project Instructions > `AGENTS.md`
- Version/date synchronization rules:
  - `AGENTS.md` must mirror `Instruction Set Version` and `Last Updated` defined in `/docs/PROJECT_INSTRUCTIONS.md`.
  - Any change to `/docs/PROJECT_INSTRUCTIONS.md` must update mirrored version/date metadata in `AGENTS.md` in the same commit.
  - If version/date metadata is not aligned, stop implementation and align governance docs first.

---

# 15. Governance Metadata Mirror

- Instruction Set Version: `1.0.1`
- Last Updated: `2026-02-28`

---

# 16. Mandatory Output Reminder

Every Codex output must end with this exact line:

`Reminder: update ChatGPT Project Instructions version/date to match this repository.`
