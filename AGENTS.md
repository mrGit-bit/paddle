<!-- markdownlint-disable MD022 -->
<!-- markdownlint-disable MD025 -->
<!-- markdownlint-disable MD032 -->

# AGENTS.md — Spec-Driven Execution Rules

Instruction Set Version: 2.2.1  
Last Updated: 2026-03-03

---

## 1. Authority & Scope

Authority:
1) Explicit Task Brief
2) `/docs/PROJECT_INSTRUCTIONS.md`
3) `AGENTS.md`

If version/date mismatch exists between `PROJECT_INSTRUCTIONS.md` and `AGENTS.md`:
STOP and align first.

---

## 2. SDD Workflow (Mandatory A → B → C)

### Phase A — Specification
Implementation MUST NOT start unless there is an approved spec file in:
- `specs/###-short-title.md`

After creating/updating a spec file:
- STOP and request user review/approval before creating a plan or implementing.

### Phase B — Planning (Plan Mode)
Implementation MUST NOT start unless there is an approved plan file in:
- `/plans/YYYY-MM-DD_short-description.md`

Plan must be based on the spec (`specs/*.md`) and follow `/plans/TEMPLATE.md`.

In Plan Mode, the agent:
- MUST NOT write product code
- MAY update Markdown files when instructed

After creating/updating a plan file:
- STOP and request user review/approval before implementation.

### Phase C — Implementation (Execute Mode)
Only after plan approval:
- Implement step-by-step, following plan order.
- No scope expansion.
- Start only when both latest spec and latest plan are explicitly approved by the user.

---

## 3. Engineering Rules

- DRY, KISS, SRP, YAGNI
- No speculative refactors
- No unrelated formatting changes
- No file moves unless explicitly required
- No renaming unless required

Backend/Frontend separation:
- No business logic in templates
- No frontend ranking logic
- Prefer backend helpers and reuse existing ones

Language rules:
- UI text: Spanish
- Code/comments/docs: English

---

## 4. Testing & Quality

- pytest + pytest-django (+ pytest-cov when relevant)
- Target ≥ 90% coverage (project standard)
- Add/update tests for every feature/fix
- Run smallest relevant pytest scope
- Include edge cases and expected HTTP statuses (when applicable)

---

## 5. Changelog Discipline

- Update `CHANGELOG.md` under `## [Unreleased]` unless formatting-only
- Changelog entry must match the actual behavior changes
- Recommend commit message aligned with changelog

---

## 6. Manual Functional Checks (Mandatory)

Every implementation output must include:
- 3–6 manual functional checks (UI navigation + edge cases)
- Permission/regression checks when relevant

These checks complement automated tests.

---

## 7. Output Requirements (Codex Responses)

Every Codex output must include:

A) Technical Summary  
B) Files Modified  
C) Tests (added/modified + command + result summary)  
D) Changelog Entry (exact text added)
E) Human readable summary of changes  
E) Manual Functional Checks proposed (3–6)  
F) Recommended Commit Message
G) Ask for confirmation to close the development cycle  
H) Eventually, and If needed, make a Continuous Improvement Question with suggestions
I) If required, ammend markdown files to align with suggestions

---

## 8. Markdownlint Rules (Mandatory for Markdown files)

For any created/modified Markdown file:
- Avoid `markdownlint-disable` directives unless explicitly requested by the user.
- Keep one blank line around headings and lists.
- Use consistent unordered list markers (`-`).
- Avoid trailing spaces and malformed list indentation.
- Ensure numbered lists are explicit and sequential (`1.`, `2.`, `3.`).
- End files with a single newline.

Before final delivery:
1. Run markdownlint on changed Markdown files when available.
2. Fix all violations in the same change set.
3. If markdownlint is unavailable, perform a manual pass against this checklist.
