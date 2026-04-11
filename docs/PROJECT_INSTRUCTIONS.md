# Project Instructions — rankingdepadel.club

Instruction Set Version: 2.3.6
Last Updated: 2026-04-11

## 1. Product and Stack

- Padel rankings, matches, player profiles, and Americano tournaments.
- Backend: Django
- Frontend: Django Templates + Bootstrap 5
- Mobile: Capacitor WebView
- Python: 3.10.12
- DB: SQLite in dev; Oracle Autonomous Database (TCPS) in staging/prod
- JavaScript: vanilla only when strictly necessary
- DRF/API endpoints are deprecated and must not be extended

## 2. Authority

1. Explicit task brief
2. `docs/PROJECT_INSTRUCTIONS.md`
3. `AGENTS.md`

Rules:

- Explicit task brief overrides everything else.
- `docs/PROJECT_INSTRUCTIONS.md` owns compact constraints.
- `AGENTS.md` owns Codex workflow and handoff rules.
- Version/date headers must stay aligned here and in `AGENTS.md`.
- Keep this file under 7000 characters when possible and never above 7800.
- If a governance addition would exceed that budget, keep only the portable
  rule here and move details to `AGENTS.md` or another owner doc.

## 3. Repository Constraints

- Apply DRY, KISS, SRP, YAGNI, and Explicit > Implicit.
- No speculative refactors, renames, moves, or unrelated formatting changes.
- Backend owns business logic; templates render only.
- No frontend ranking logic.
- UI text in Spanish.
- Code, comments, docs, and specs in English.
- Keep deprecated API/DRF policy centralized in governance; restate it in specs
  only when the task directly touches that surface.
- Verify current supported behavior before relying on external-tool or
  integration-dependent guidance or automation.

## 4. Mandatory SDD Gates

Before development or code changes:

1. Check the current git branch.
2. If it is not `develop`, warn clearly, ask which branch should receive the
   work, and wait for confirmation before editing files.
3. Create or update an approved active-work spec in
   `specs/###-short-title.md`.
4. Start implementation only after the current active-work spec is explicitly
   approved.

Simple-change exception:

- For small, low-risk documentation, governance, or repository-guidance edits,
  Codex CLI may skip the active-work spec and proceed directly.
- If the scope expands beyond that narrow change set, return to the standard
  approved-spec flow before continuing implementation.

Active-work rule:

- The active spec for a task is the latest approved non-release spec file
  created for that task.
- `specs/release-*.md` files are historical release artifacts, not active-work
  inputs.
- Loose non-release specs must carry explicit tracking metadata:
  `Status: approved|implemented` and `Release tag: unreleased`.
- Use `Status: approved` until scoped work is done and that development cycle
  is closing.
- Use `Status: implemented` only for work closed on `develop` but not shipped.
- Reserve `Release tag` for shipment tracking only. Before release
  consolidation, mark only actually shipped loose files with the target
  `vX.Y.Z` and `Status: shipped`. Then
  `python scripts/release_orchestrator.py <version>` folds those exact-match
  files into the shipped release record and keeps that changelog section light.
  If a planned release never reaches production, roll its unshipped specs and
  notes into the next production release that actually ships them. A loose task
  must not remain loose after any scoped behavior reaches production; use a new
  loose spec for post-release follow-up.

Additional rules:

- `/plan` may shape a spec request before approval but does not bypass the
  approved-spec requirement.
- In Plan Mode, product code stays frozen; requested Markdown updates are
  allowed.
- ChatGPT pre-spec drafts must be plain editable Markdown under ignored local
  files in `docs/pre-specs/`. They are planning inputs only, never active-work
  specs, and must not be staged, committed, or released.
- In `/plan` or other planning-only workflows, explore first, then bias toward
  a question-heavy planning loop before finalizing the plan.
- After exploration, lock product, UX, or implementation preferences unless
  choices are mechanical or already settled.
- Evaluate whether `/review` or `$audit` fits each non-trivial spec or
  implementation task.
- Prefer `/review` first when both checkpoints could fit the approved scope.
- If neither checkpoint is used, say so explicitly in the working response and
  give a brief reason for skipping it or discarding it for that scope.
- Only surface findings that are medium or high severity; do not raise low
  severity findings as active review/audit findings.
- Before advancing past the relevant gate, ask whether each surfaced finding
  should be addressed or discarded, then update the review/audit record.
- Do not fix findings directly just because they were found; implement fixes
  only after the user chooses to address them.
- When Django model/schema changes are introduced, generate and apply the
  required migrations in development before treating the task as complete.
- After a successful tagged release and back-merge from `main` to `develop`,
  consolidate released SDD files before new SDD work, using only loose specs
  marked with the shipped `vX.Y.Z`. Keep that changelog section light. A release
  is not reconciled while any loose non-release file still describes shipped
  behavior; retag, consolidate, and delete superseded loose files first.

## 5. Delivery and Coordination

- Update `CHANGELOG.md` under `## [Unreleased]` for every behavior, docs,
  governance, workflow, or guidance change unless it is formatting-only.
- Prefix changelog bullets with domain categories such as `UI/UX`,
  `Governance`, `Release`, `Backend`, `Data`, `Mobile`, `Tests`, or `Docs`.
- Before closing a development cycle, reconcile completed scoped items in
  `BACKLOG.md` and reflect them in `CHANGELOG.md`.
- During development-cycle closure, move each in-scope loose spec from
  `Status: approved` to `Status: implemented` when the scoped work is complete
  and that cycle is being closed, before staging and committing the closure.
- Backlog reconciliation belongs to development-cycle closure unless the
  release workflow explicitly says otherwise.
- Closure is complete only after requested-work changes are staged, committed,
  pushed, and `git status --short` is clean.
- Run closure git operations sequentially; do not overlap `git add`,
  `git commit`, and `git push`.
- If the user wants to continue developing, do not commit yet.
- If the user confirms commit/push/closure, do it in the same turn.
- Treat `close cycle`, `close specification`, or equivalent as direct
  commit/push/closure confirmation.

## 6. Markdown Rules

- Keep new or rewritten Markdown light and schematic by default.
- Prefer short sections, direct bullets, and compact summaries.
- `CHANGELOG.md` should record outcomes, not process narration.
- Keep `CHANGELOG.md` categories stable; prefer product or workflow domains.
- Active-work specs should capture only scope, constraints, and checks needed
  for execution.
- Consolidated release files should stay as compact provenance summaries.
- Do not add `markdownlint-disable` directives unless explicitly requested.
- Enforce `MD022` and `MD032`; treat `MD013` as non-blocking.
- `CHANGELOG.md` may keep an `MD024` disable because repeated Keep a Changelog
  category headings are intentional there.
- Run markdownlint on changed Markdown files when available and fix violations
  in the same change set, except `MD013`.

When `PROJECT_INSTRUCTIONS.md` changes, include this reminder in the handoff:

`Reminder: update ChatGPT Project Instructions version/date to match this repository.`
