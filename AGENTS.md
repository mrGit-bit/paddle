# AGENTS.md — Spec-Driven Execution Rules

Instruction Set Version: 2.2.18  
Last Updated: 2026-03-15

---

## 1. Authority & Scope

Authority:

1) Explicit Task Brief
2) `/docs/PROJECT_INSTRUCTIONS.md`
3) `AGENTS.md`

If version/date mismatch exists between `PROJECT_INSTRUCTIONS.md` and `AGENTS.md`:
STOP and align first.

Tool roles:

- Codex CLI is the default tool for spec drafting, planning, implementation, tests, and repository changes.
- ChatGPT is not required in the normal delivery path when Codex CLI can cover the task end to end.
- Use ChatGPT only for pre-spec clarification of ambiguous work, project-related technology/solution/computer-science questions, design/architecture/governance decisions, development-concept clarification, or screenshot review.
- Check `README.md` when necessary for current repository context, architecture orientation, or safe repository navigation.
- Keep `README.md` updated when repository guidance, architecture orientation, or other README-covered project context changes.

---

## 2. SDD Workflow (Mandatory A → B → C)

## 2.1 Mandatory Branch Check Before Development

Before starting any development/implementation/code-change request, Codex MUST check the current git branch.

If the active branch is not `develop`, Codex MUST:

- Warn clearly that work is not currently on `develop`.
- Ask explicitly which branch the user wants the changes applied to.
- Wait for user confirmation before implementing changes.

### Phase A — Specification

Implementation MUST NOT start unless there is an approved spec file in:

- `specs/###-short-title.md`

After creating/updating a spec file:

- STOP and request user review/approval before creating a plan or implementing.

After spec approval, Codex MAY suggest a spec-focused pre-audit only when it is needed for that approved scope. The suggestion MUST state why the audit is being suggested. If that audit path is used, keep it within spec scope and solve accepted findings before plan approval.

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

After implementation, Codex MAY suggest a scoped post-implementation audit only when it is needed. The suggestion MUST state why the audit is being suggested. If that audit path is used, solve accepted findings before closing the development cycle.

### Post-Release Consolidation

After a tagged release has been completed and successfully back-merged from
`main` to `develop`, Codex MUST consolidate the completed SDD artifacts for
that released deployment into:

- `specs/release-X.Y.Z-consolidated.md`
- `plans/release-X.Y.Z-consolidated.md`

Rules:

- Active development MUST continue using one spec file and one plan file per
  SDD.
- The first Codex task after a successful tagged release back-merge MUST start
  by performing any pending consolidation for that released deployment before
  beginning new SDD work.
- Consolidation MUST happen only after the tagged release and back-merge are
  complete.
- Consolidated files MUST preserve source-file provenance, approval context,
  scope, acceptance criteria, validation commands, and execution history for
  the released deployment.
- Once a released deployment has been consolidated, released per-SDD spec and
  plan files for that deployment MUST NOT remain as loose files outside the
  applicable consolidated release files.
- Unreleased or not-yet-traceable SDD files MUST remain separate until they
  belong to a released deployment.

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
- Keep deprecated API/DRF policy centralized in governance; do not repeat it in feature specs unless the task directly involves that deprecated surface

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

- Update `CHANGELOG.md` under `## [Unreleased]` for every behavior, documentation, governance, workflow, or repository-guidance change unless the change is truly formatting-only
- Changelog entry must match the actual behavior changes
- Recommend a commit message aligned with the changelog and covering the full accumulated uncommitted change set since the last commit; if multiple development steps were done before committing, rephrase the message to cover all of them together

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
F) Recommended Commit Message covering all accumulated changes since the last commit, not just the latest edit
G) Before any commit/push/closure step, ask whether the user wants to continue developing
H) If the user does not want to continue developing, ask: "Do you want me to proceed with staging changes, committing with the recommended commit message, pushing to the remote branch, and closing the current development cycle?"
I) If user confirms Step H, perform commit/push in the same flow and keep processing any remaining unstaged or uncommitted changes that belong to the requested work until `git status --short` is clean before declaring the development cycle closed
J) After closure, provide a suggestion of next steps (if relevant)
K) If required, ammend markdown files to align with suggestions

---

## 8. Markdownlint Rules (Mandatory for Markdown files)

For any created/modified Markdown file:

- Do not add `markdownlint-disable` directives unless explicitly requested by the user.
- `MD022` is mandatory: keep exactly one blank line before and after every heading.
- `MD032` is mandatory: keep exactly one blank line before and after every list.
- Do not treat long lines (`MD013`) as blocking violations.
- Use consistent unordered list markers (`-`).
- Avoid trailing spaces and malformed list indentation.
- Ensure numbered lists are explicit and sequential (`1.`, `2.`, `3.`).
- End files with a single newline.
- Treat generated text as authoritative output; when markdown review is needed, fix structure without rewriting or wrapping long lines into multiple lines only for line-length linting.

Before final delivery:

1. Run markdownlint on changed Markdown files when available.
2. Fix all violations in the same change set except `MD013` line-length findings, which are non-blocking.
3. If markdownlint is unavailable, perform a manual pass against this checklist.
4. If `MD022` or `MD032` fails, do not deliver until fixed.
