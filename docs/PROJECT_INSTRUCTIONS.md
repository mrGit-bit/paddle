# Project Instructions — rankingdepadel.club

Instruction Set Version: 2.2.20  
Last Updated: 2026-03-17

This file mirrors the repository governance subset kept in ChatGPT Project
instructions and must remain under 8000 characters.

## 1. Product and Stack

- Padel rankings, matches, player profiles, and Americano tournaments.
- Backend: Django
- Frontend: Django Templates + Bootstrap 5
- Mobile: Capacitor WebView
- Python: 3.10.12
- Dev DB: SQLite
- Staging/Prod DB: Oracle Autonomous Database (TCPS)
- JavaScript: vanilla only when strictly necessary
- DRF/API endpoints are deprecated and must not be extended

## 2. Authority

1. Explicit task brief
2. `docs/PROJECT_INSTRUCTIONS.md`
3. `AGENTS.md`

Rules:

- Explicit task brief overrides everything else.
- `docs/PROJECT_INSTRUCTIONS.md` owns compact repository constraints.
- `AGENTS.md` owns Codex execution behavior, workflow mechanics, and handoff
  rules.
- Check `README.md` for repository orientation and owner-doc pointers.
- `Instruction Set Version` and `Last Updated` must stay aligned here and in
  `AGENTS.md`.

## 3. Repository Constraints

- Apply DRY, KISS, SRP, YAGNI, and Explicit > Implicit.
- No speculative refactors, renames, moves, or unrelated formatting changes.
- Backend owns business logic; templates render only.
- No business logic in templates.
- No frontend ranking logic.
- UI text in Spanish.
- Code, comments, docs, specs, and plans in English.
- Keep deprecated API/DRF policy centralized in governance; do not restate it
  in feature specs unless the task directly touches that surface.

## 4. Mandatory SDD Gates

Before any development or code change:

1. Check the current git branch.
2. If it is not `develop`, warn clearly, ask which branch should receive the
   work, and wait for confirmation before editing files.
3. Create or update an approved active-work spec in `specs/###-short-title.md`.
4. Create or update an approved active-work plan in
   `plans/YYYY-MM-DD_short-description.md`.
5. Start implementation only after both the current spec and current plan are
   explicitly approved.

Simple-change exception:

- For small, low-risk changes with narrow scope, such as straightforward
  documentation, governance, or repository-guidance edits, Codex CLI may skip
  creating spec and plan files.
- In those cases, Codex must first confirm the reduced-process path with the
  user, then proceed directly with the requested Markdown or repository-doc
  edits.
- If the scope expands beyond that narrow change set, return to the standard
  approved spec and plan flow before continuing implementation.

Active-work rule:

- The active spec and plan for a task are the latest approved non-release files
  created for that task.
- `specs/release-*.md` and `plans/release-*.md` are historical release
  artifacts, not active-work inputs.
- When repository context is needed, README should point to this lookup rule
  instead of requiring generic manual discovery.

Additional rules:

- `/plan` may help shape a spec request before spec approval but does not bypass
  the approved-spec requirement.
- In Plan Mode, product code stays frozen; requested Markdown updates are
  allowed.
- Use `/review` and `audit` only when useful for the approved scope, and fix
  accepted findings before advancing past the relevant gate or closing the work.
- After a successful tagged release and back-merge from `main` to `develop`,
  consolidate the released SDD files into `specs/release-X.Y.Z-consolidated.md`
  and `plans/release-X.Y.Z-consolidated.md` before new SDD work begins.

## 5. Delivery and Coordination

- Update `CHANGELOG.md` under `## [Unreleased]` for every behavior,
  documentation, governance, workflow, or repository-guidance change unless the
  change is truly formatting-only.
- Before closing a development cycle, reconcile any completed backlog items in
  `BACKLOG.md` that belong to the requested scope: remove them from backlog and
  ensure the implemented outcome is reflected in `CHANGELOG.md`.
- Closure is complete only after all requested-work changes are staged,
  committed, pushed, and `git status --short` is clean.
- If the user wants to continue developing, do not commit yet.
- If the user confirms commit/push/closure, perform that flow in the same turn.

## 6. Markdown Rules

- Do not add `markdownlint-disable` directives unless explicitly requested.
- Enforce `MD022` and `MD032`.
- Treat `MD013` as non-blocking.
- `CHANGELOG.md` may keep an `MD024` disable because repeated Keep a Changelog
  category headings are intentional there.
- Use `-` for unordered lists.
- Keep ordered lists explicit and sequential.
- Avoid trailing spaces.
- End files with a single newline.
- Run markdownlint on changed Markdown files when available and fix violations
  in the same change set, except `MD013`.

When `PROJECT_INSTRUCTIONS.md` changes, include this reminder in the handoff:

`Reminder: update ChatGPT Project Instructions version/date to match this repository.`
