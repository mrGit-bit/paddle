# Project Instructions — rankingdepadel.club

Instruction Set Version: 2.2.27  
Last Updated: 2026-03-29

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
- For external-tool or integration-dependent features, verify the supported
  behavior in the current tool or current official docs before relying on it in
  repository guidance or automation.

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
- In those cases, if the request is clearly minor, Codex may proceed directly
  with the requested Markdown or repository-doc edits without an extra
  confirmation turn.
- If the scope expands beyond that narrow change set, return to the standard
  approved spec and plan flow before continuing implementation.

Active-work rule:

- The active spec and plan for a task are the latest approved non-release files
  created for that task.
- Pair loose specs and plans by shared `Task ID` tracking metadata and explicit
  `Plan` / `Spec` references instead of filename similarity alone.
- `specs/release-*.md` and `plans/release-*.md` are historical release
  artifacts, not active-work inputs.
- When repository context is needed, README should point to this lookup rule
  instead of requiring generic manual discovery.
- Loose non-release specs and plans must carry explicit `Release tag` tracking
  metadata and default to `unreleased` while work is still pending release.
  Before release consolidation, mark only the actually shipped loose files with
  the target `vX.Y.Z`. During consolidation, `/prompts:release <version>`
  folds only those exact-match files into the shipped release record, reviews
  the changelog section for that release, and keeps that section as a light
  summary of shipped changes. If a planned release never reaches production, do
  not keep a standalone release record for it; roll its unshipped loose files
  and changelog notes into the next production release that actually ships
  them.

Additional rules:

- `/plan` may help shape a spec request before spec approval but does not bypass
  the approved-spec requirement.
- In Plan Mode, product code stays frozen; requested Markdown updates are
  allowed.
- In `/plan` or other planning-only workflows, explore first, then bias toward
  a question-heavy planning loop before finalizing the plan.
- After exploration, summarize the discovered context and ask follow-up
  questions to lock product, UX, or implementation preferences when the work is
  non-trivial, even if a reasonable default seems likely.
- Only skip those extra planning questions when the remaining decisions are
  truly mechanical or already explicitly settled by the user or repository
  governance.
- Evaluate whether `/review` or `$audit` should be used for each non-trivial
  spec or implementation task, especially when the target flow already exists.
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
- Do not treat a checked-in integration file as proof that the current tool
  auto-discovers or supports it. Verify the current environment first.
- After a successful tagged release and back-merge from `main` to `develop`,
  consolidate the released SDD files into `specs/release-X.Y.Z-consolidated.md`
  and `plans/release-X.Y.Z-consolidated.md` before new SDD work begins, using
  only loose files explicitly marked with the shipped `vX.Y.Z`. Review the
  release changelog section in the same step and keep it simple and light.

## 5. Delivery and Coordination

- Update `CHANGELOG.md` under `## [Unreleased]` for every behavior,
  documentation, governance, workflow, or repository-guidance change unless the
  change is truly formatting-only.
- Before closing a development cycle, reconcile any completed backlog items in
  `BACKLOG.md` that belong to the requested scope: remove them from backlog and
  ensure the implemented outcome is reflected in `CHANGELOG.md`.
- Backlog reconciliation is owned by development-cycle closure. Release
  automation does not perform it unless the release workflow explicitly says so.
- Closure is complete only after all requested-work changes are staged,
  committed, pushed, and `git status --short` is clean.
- If the user wants to continue developing, do not commit yet.
- If the user confirms commit/push/closure, perform that flow in the same turn.
- Treat direct user commands such as `close cycle`, `close specification`, or
  equivalent explicit closure wording as commit/push/closure confirmation; do
  not ask the extra confirmation question in that case.

## 6. Markdown Rules

- Keep new or rewritten Markdown light and schematic by default.
- Prefer short sections, direct bullets, and compact summaries over narrative
  expansion.
- `CHANGELOG.md` should record outcomes, not process narration.
- Specs/plans should capture only the scope, constraints, and checks needed
  for execution.
- Consolidated release files should stay as compact provenance summaries.
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
