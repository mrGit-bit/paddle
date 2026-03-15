# Project Instructions — rankingdepadel.club

Instruction Set Version: 2.2.17  
Last Updated: 2026-03-15

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
- Codex CLI is the default tool for specs, plans, implementation, tests, and repo changes.
- Use ChatGPT only for pre-spec clarification, project tech/design/governance questions, concept clarification, or screenshot review.
- Check `README.md` when needed for repo context and keep it updated when README-covered guidance changes.
- This file must remain under 8000 characters.
- `Instruction Set Version` and `Last Updated` are mandatory here and in `AGENTS.md` and must stay aligned.

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

Before implementation, create or update an approved active-work spec in `specs/###-short-title.md`.

Before writing the spec, clarify scope in/out, UI/backend constraints, test expectations, and allowed/forbidden files.

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

After spec approval, Codex may suggest a spec-focused pre-audit only when it is needed for that approved scope. The suggestion must state why the audit is being suggested. If that audit path is used, keep it within spec scope and solve accepted findings before plan approval.

Exception before approval: spec refinements and requested governance/template markdown updates.

If repeated clarification friction appears, propose improving governance docs or templates.

### Phase B — Planning

Create an approved active-work plan in `/plans/YYYY-MM-DD_short-description.md` using `/plans/TEMPLATE.md` and the approved spec as input.

In Plan Mode: no product code changes; requested markdown governance/spec/plan/template updates are allowed.

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
- update `CHANGELOG.md` under `## [Unreleased]` for every behavior, documentation, governance, workflow, or repository-guidance change unless the change is truly formatting-only.
- recommended commit messages must describe the full accumulated uncommitted change set since the last commit, rephrased when multiple development steps are being committed together.

After implementation, Codex may suggest a scoped post-implementation audit only when it is needed. The suggestion must state why the audit is being suggested. If that audit path is used, solve accepted findings before closing the development cycle.

If recurring execution mistakes appear, tighten `PROJECT_INSTRUCTIONS.md`, `AGENTS.md`, or `/plans/TEMPLATE.md`.

### Post-Release Consolidation

After a tagged release has been completed and successfully back-merged from `main` to `develop`, consolidate the completed SDD files that supported that released deployment into:

- `specs/release-X.Y.Z-consolidated.md`
- `plans/release-X.Y.Z-consolidated.md`

Rules:

- Active development still uses one spec file and one plan file per SDD.
- The first Codex task after a successful tagged release back-merge must perform any pending consolidation before new SDD work.
- Consolidation happens only after the release/back-merge is complete.
- Each consolidated file must preserve provenance, approval context, scope, acceptance criteria, validation commands, and execution history.
- Once a released deployment has been consolidated, its released per-SDD spec and plan files must not remain as loose files outside the applicable consolidated release files.
- Unreleased or not-yet-traceable SDD files stay separate until they belong to a released deployment.

## 5. Delivery Requirements

Every implementation handoff must include technical summary, files modified, tests added/modified with command/result, exact changelog text added, human-readable summary, 3-6 manual functional checks, a recommended commit message for all uncommitted changes since the last commit, and the required continue-developing / commit-push-closure questions.

If the user wants to continue developing, do not commit yet.

If the user confirms the commit/push/closure question, perform commit/push/closure in the same flow.

ChatGPT may assist only in the approved advisory cases above and must not implement repository code directly.

## 6. Markdown Rules

For every changed Markdown file:

- do not add `markdownlint-disable` directives unless explicitly requested,
- enforce `MD022` and `MD032`,
- do not treat long lines (`MD013`) as blocking violations,
- use `-` for unordered lists,
- keep ordered lists explicit and sequential,
- avoid trailing spaces,
- end files with a single newline,
- treat generated text as authoritative output; when markdown review is needed, fix structure without rewriting or wrapping long lines into multiple lines only for line-length linting.

Validation:

1. Run markdownlint on changed Markdown files when available.
2. Fix violations in the same change set, except `MD013` line-length findings which are non-blocking.
3. If markdownlint is unavailable, perform a manual pass before delivery.
4. Do not deliver with `MD022` or `MD032` failures.

When `PROJECT_INSTRUCTIONS.md` changes, include this reminder in the handoff:

`Reminder: update ChatGPT Project Instructions version/date to match this repository.`
