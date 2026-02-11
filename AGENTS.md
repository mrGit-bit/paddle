# AGENTS.md — Minimal AI Coding Guidance

This file defines **baseline constraints** for AI coding agents (e.g. Codex CLI)
working on the `rankingdepadel.club` project.

It is intentionally minimal.
All detailed instructions are provided explicitly per task.

---

## Project Context

- Stack: Django + Django REST Framework
- Frontend: Django Templates + Bootstrap 5
- JavaScript: Vanilla JS only when strictly necessary
- Databases:
  - Dev: SQLite
  - Staging/Prod: Oracle Autonomous DB (TCPS)

---

## Core Coding Principles (Mandatory)

- **DRY** — Do not duplicate logic.
- **KISS** — Prefer the simplest working solution.
- **SRP** — Single Responsibility Principle: One responsibility per module/file.
- **YAGNI** — You aren't gonna need it: Do not add any functionality without a current need.
- **Explicit > Implicit** — Readability over cleverness.

Avoid speculative refactors and large rewrites unless explicitly requested.

---

## Language Rules

- **UI text:** Spanish
- **Code, variables, comments, documentation:** English

---

## Backend Rules

- Prefer model properties for computed data.
- Keep business logic in backend code, not templates.
- No frontend ranking logic.

---

## Frontend Rules

- Use Django templates by default.
- Prefer Bootstrap 5 over custom CSS or JavaScript.
- No business logic in templates.
- Avoid unnecessary JavaScript.

---

## Testing Rules

- Framework: pytest + pytest-django
- Maintain ≥90% coverage.
- Every feature or fix must include tests or test updates.
- Run the smallest relevant pytest scope after changes.

---

## Changelog Discipline

- `CHANGELOG.md` follows *Keep a Changelog*.
- During development: add entries under `## [Unreleased]`.
- On release: move entries to `## [X.Y.Z] - YYYY-MM-DD`.
- Every feature or fix must update the changelog unless purely formatting/comments.

---

## Workflow Expectations

- Architectural decisions are made outside the agent.
- The agent executes **explicit tasks only**.
- If something is unclear or ambiguous, the agent must stop and ask.

---

## Output Requirements

- Show file path + only modified sections.
- Keep diffs minimal and focused.
- No unrelated changes.

---

## Commit Message Suggestions (for Codex output)

When a task produces a standalone change that should be committed independently
(e.g., a feature, fix, refactor, or test reorganization), include a recommended
`git commit` message in the Codex output using **Conventional Commits** style.

Follow these prefixes:

- **feat:** for new features or enhancements
- **fix:** for bug fixes and small behavior corrections
- **refactor:** for code restructuring without behavior change
- **test:** for test file moves, renames, or additions
- **chore:** for non-user-visible tasks (e.g., documentation)

After the prefix, include a concise description. Commit message subjects should align with the corresponding CHANGELOG entry, using technical wording in commits and user-facing wording in the changelog.
Examples of templates Codex should output:

- `feat(frontend): add favicon and corresponding test`
- `fix(frontend): enforce ordering before pagination`
- `refactor(tests): harmonize frontend test structure`
- `test(games): reorganize games API tests`
- `chore: update CHANGELOG.md for About page version`