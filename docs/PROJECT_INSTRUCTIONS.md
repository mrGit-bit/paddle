# Project Instructions — rankingdepadel.club

Instruction Set Version: 2.3.5  
Last Updated: 2026-04-02

This is the compact governance subset for ChatGPT Project instructions.

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
- `Instruction Set Version` and `Last Updated` must stay aligned here and in
  `AGENTS.md`.
- Keep this file under 7000 characters when possible and never above 7800.
- If a governance addition would exceed that budget, keep only the portable
  rule here and move the detail to `AGENTS.md` or another owner doc.

## 3. Repository Constraints

- Apply DRY, KISS, SRP, YAGNI, and Explicit > Implicit.
- No speculative refactors, renames, moves, or unrelated formatting changes.
- Backend owns business logic; templates render only.
- No frontend ranking logic.
- UI text in Spanish.
- Code, comments, docs, and specs in English.
- Keep deprecated API/DRF policy centralized in governance; do not restate it
  in feature specs unless the task directly touches that surface.
- Verify current supported behavior before relying on external-tool or
  integration-dependent guidance or automation.

## 4. Mandatory SDD Gates

Before any development or code change:

1. Check the current git branch.
2. If it is not `develop`, warn clearly, ask which branch should receive the
   work, and wait for confirmation before editing files.
3. Create or update an approved active-work spec in
   `specs/###-short-title.md`.
4. Start implementation only after the current active-work spec is explicitly
   approved.

Simple-change exception:

- For small, low-risk documentation, governance, or repository-guidance edits,
  Codex CLI may skip creating an active-work spec.
- If the request is clearly minor, Codex may proceed directly without an extra
  confirmation turn.
- If the scope expands beyond that narrow change set, return to the standard
  approved-spec flow before continuing implementation.

Active-work rule:

- The active spec for a task is the latest approved non-release spec file
  created for that task.
- `specs/release-*.md` files are historical release artifacts, not active-work
  inputs.
- Loose non-release specs must carry explicit tracking metadata:
  `Status: approved|implemented` and `Release tag: unreleased`.
- Use `Status: approved` for approved work that has not yet completed its
  development cycle closure.
- Move a loose spec from `approved` to `implemented` only when the scoped work
  is done and that spec's development cycle is being closed.
- Use `Status: implemented` for work whose development cycle was closed on
  `develop` but is not yet shipped.
- Reserve `Release tag` for shipment tracking only. Before release
  consolidation, mark only the actually shipped loose files with the target
  `vX.Y.Z` and update them to `Status: shipped`. During consolidation,
  `python scripts/release_orchestrator.py <version>` folds only those
  exact-match files into the shipped release record and keeps that changelog
  section as a light shipped summary. If a planned release never reaches
  production, roll its unshipped loose files and changelog notes into the next
  production release that actually ships them. A loose task must not remain
  loose after any scoped behavior from that task reaches production; any
  post-release follow-up must move to a new loose spec instead of extending
  the shipped file.

Additional rules:

- `/plan` may shape a spec request before approval but does not bypass the
  approved-spec requirement.
- In Plan Mode, product code stays frozen; requested Markdown updates are
  allowed.
- In `/plan` or other planning-only workflows, explore first, then bias toward
  a question-heavy planning loop before finalizing the plan.
- After exploration, lock product, UX, or implementation preferences with
  follow-up questions unless the remaining choices are purely mechanical or
  already settled.
- Evaluate whether `/review` or `$audit` fits each non-trivial spec or
  implementation task.
- Prefer `/review` first when both checkpoints could fit the approved scope.
- If neither checkpoint is used, say so explicitly in the working response and
  give a brief reason for skipping it or discarding it for that scope.
- Only surface findings that are medium or high severity; do not raise low
  severity findings as active review/audit findings.
- Before advancing past the relevant gate, explicitly ask the user whether each
  surfaced finding should be addressed or discarded, then update the
  review/audit record accordingly.
- Do not fix findings directly just because they were found; implement fixes
  only after the user chooses to address them.
- When Django model/schema changes are introduced, generate and apply the
  required migrations in development before treating the task as complete.
- After a successful tagged release and back-merge from `main` to `develop`,
  consolidate the released SDD files before new SDD work begins, using only
  loose spec files explicitly marked with the shipped `vX.Y.Z`. Keep that
  release changelog section simple and light. A release is not reconciled
  while any loose non-release file still describes shipped behavior; retag,
  consolidate, and delete those superseded files before new SDD work starts.

## 5. Delivery and Coordination

- Update `CHANGELOG.md` under `## [Unreleased]` for every behavior,
  documentation, governance, workflow, or repository-guidance change unless the
  change is truly formatting-only.
- Prefix changelog bullets with domain categories such as `UI/UX`,
  `Governance`, `Release`, `Backend`, `Data`, `Mobile`, `Tests`, or `Docs`
  when that keeps mixed releases scannable.
- Before closing a development cycle, reconcile completed scoped items in
  `BACKLOG.md` and reflect them in `CHANGELOG.md`.
- During development-cycle closure, move each in-scope loose spec from
  `Status: approved` to `Status: implemented` when the scoped work is complete
  and that cycle is being closed, before staging and committing the closure.
- Backlog reconciliation belongs to development-cycle closure unless the
  release workflow explicitly says otherwise.
- Closure is complete only after all requested-work changes are staged,
  committed, pushed, and `git status --short` is clean.
- Run closure git operations sequentially; do not overlap `git add`,
  `git commit`, and `git push`.
- If the user wants to continue developing, do not commit yet.
- If the user confirms commit/push/closure, do it in the same turn.
- Treat direct user commands such as `close cycle` or `close specification` as
  commit/push/closure confirmation; do not ask the extra confirmation question.

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
