# Project Instructions — rankingdepadel.club

Instruction Set Version: 2.2.10  
Last Updated: 2026-03-10

This file mirrors the repository governance subset kept in ChatGPT Project instructions and must remain explicitly under 8000 characters so it fits within ChatGPT Project instruction limits.

## 1. Product and Stack

Padel rankings, matches, and tournament web app with Android/iOS WebView wrappers using the same backend/frontend.

- Backend: Django
- Frontend: Django Templates + Bootstrap 5
- Mobile: Capacitor WebView
- Python: 3.10.12
- Dev DB: SQLite
- Staging/Prod DB: Oracle Autonomous Database (TCPS)
- JavaScript: vanilla only when strictly necessary
- DRF/API endpoints are deprecated and should not be extended
- Deprecated API/DRF constraints must be enforced centrally in governance and should not be repeated in feature specs unless the task directly touches that deprecated surface

## 2. Authority and Governance

Authority order:

1. Explicit task brief
2. `docs/PROJECT_INSTRUCTIONS.md`
3. `AGENTS.md`

Rules:

- Explicit task brief overrides everything else.
- Project Instructions override `AGENTS.md`.
- Codex CLI is the default tool for spec drafting, planning, implementation, tests, and repository changes.
- ChatGPT is not required in the normal delivery path when Codex CLI can cover the task end to end.
- Use ChatGPT only for pre-spec clarification of ambiguous work, project-related technology/solution/computer-science questions, design/architecture/governance decisions, development-concept clarification, or screenshot review.
- This file must remain under 8000 characters after every edit.
- `Instruction Set Version` and `Last Updated` are mandatory here and in `AGENTS.md`.
- Any change to this file must update version/date in both files in the same commit.
- If version/date differ between these files, implementation must stop until aligned.

## 3. Engineering Rules

- Apply DRY, KISS, SRP, YAGNI, and Explicit > Implicit.
- No speculative refactors, renames, moves, or unrelated formatting changes.
- Backend owns business logic; templates render only.
- No business logic in templates.
- No frontend ranking logic.
- Keep deprecated API/DRF policy centralized in governance; do not restate it in feature specs unless the task directly involves that deprecated surface.
- UI text in Spanish.
- Code, comments, docs, specs, and plans in English.

## 4. Mandatory SDD Flow

Before any development or code change, check the current git branch.

If the branch is not `develop`:

- warn clearly,
- ask which branch should receive the work,
- wait for user confirmation before changing files.

Work follows Phase A -> Phase B -> Phase C.

### Phase A — Specification

Before implementation, create or update an approved spec in `specs/###-short-title.md`.

Before writing the spec, clarify:

- scope in/out,
- UI/backend constraints,
- test expectations,
- allowed and forbidden files.

Each spec must include:

- functional goal,
- scope in/out,
- UI/UX requirements,
- backend requirements,
- data rules,
- reuse rules,
- acceptance criteria,
- manual functional checks (3-6),
- allowed files,
- forbidden files.

After creating or updating a spec:

- stop and request explicit approval,
- do not create a plan,
- do not change product code,
- do not run implementation tests.

Exception before approval:

- spec refinements,
- requested governance/template markdown updates.

If repeated clarification friction appears, propose improving governance docs or templates.

### Phase B — Planning

Create an approved plan in `/plans/YYYY-MM-DD_short-description.md` using `/plans/TEMPLATE.md` and the approved spec as input.

In Plan Mode:

- no product code changes,
- markdown governance/spec/plan/template updates are allowed when requested.

After creating or updating a plan:

- stop and request explicit approval,
- do not implement,
- do not run implementation tests.

If planning friction repeats, propose improving governance docs or templates.

### Phase C — Implementation

Start only when the latest spec and latest plan are both explicitly approved.

Implementation rules:

- follow the approved plan step by step,
- no scope expansion,
- update/add tests and run the smallest relevant scope,
- target at least 90% coverage when relevant,
- update `CHANGELOG.md` under `## [Unreleased]` unless the change is formatting-only.
- recommended commit messages must describe the full accumulated uncommitted change set since the last commit, rephrased when multiple development steps are being committed together.

If recurring execution mistakes appear, tighten `PROJECT_INSTRUCTIONS.md`, `AGENTS.md`, or `/plans/TEMPLATE.md`.

## 5. Delivery Requirements

Every implementation handoff must include:

- technical summary,
- files modified,
- tests added/modified, command run, and result summary,
- exact changelog text added,
- human-readable summary,
- 3-6 manual functional checks,
- recommended commit message covering all changes since the last commit, not only the latest edit,
- a question asking whether the user wants to continue developing before any commit/push/closure step,
- if the user does not want to continue developing, the exact question asking whether to stage, commit, push, and close the development cycle.

If the user wants to continue developing, do not commit yet.

If the user confirms the commit/push/closure question, perform commit/push/closure in the same flow.

ChatGPT may assist only in the approved advisory cases above and must not implement repository code directly.

## 6. Markdown Rules

For every changed Markdown file:

- do not add `markdownlint-disable` directives unless explicitly requested,
- enforce `MD022` and `MD032`,
- use `-` for unordered lists,
- keep ordered lists explicit and sequential,
- avoid trailing spaces,
- end files with a single newline.

Validation:

1. Run markdownlint on changed Markdown files when available.
2. Fix violations in the same change set.
3. If markdownlint is unavailable, perform a manual pass before delivery.
4. Do not deliver with `MD022` or `MD032` failures.

When `PROJECT_INSTRUCTIONS.md` changes, include this reminder in the handoff:

`Reminder: update ChatGPT Project Instructions version/date to match this repository.`
