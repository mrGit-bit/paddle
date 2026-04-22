# Project Instructions — rankingdepadel.club

Instruction Set Version: 2.3.13
Last Updated: 2026-04-22

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
- Run `python scripts/validate_governance.py` after governance edits.
- Keep this file under 7000 characters when possible and never above 7800
  characters.
- If a governance addition would exceed that budget, keep only the portable
  rule here and move details to `AGENTS.md` or another owner doc.

## 3. Repository Constraints

- Apply DRY, KISS, SRP, YAGNI, and Explicit > Implicit.
- No speculative refactors, renames, moves, or unrelated formatting changes.
- Backend owns business logic; templates render only.
- No frontend ranking logic.
- Reuse existing presentation classes/components before adding parallel styling
  when sections should look or behave alike.
- When a shared state class must override a component base class, account for
  CSS cascade order with a colocated combined selector.
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

Additional rules:

- Active work uses the latest approved non-release spec for the task;
  `specs/release-*.md` files are historical release records only.
- Loose non-release specs carry `Status: approved|implemented` and
  `Release tag: unreleased`; release consolidation uses only files explicitly
  marked for the shipped `vX.Y.Z`.
- `/plan` may shape a spec request before approval but does not bypass the
  approved-spec requirement.
- ChatGPT pre-spec handoffs must produce one concise Markdown file under
  ignored `docs/pre-specs/`. Use a short descriptive task filename without
  `pre-spec`, for example `player-ranking-chart.md`.
- Pre-specs are Codex CLI `/plan` starting points, not active-work specs. Do
  not include `Status`, `Release tag`, current-behavior sections, repeated
  instructions, code, or answers to questions Codex CLI can ask in Plan Mode.
- Pre-specs should use only this minimal schema: `# Title`, `Goal`,
  `Requested outcome`, and `Known constraints`. Keep them concise, avoid
  assumptions about unseen repository behavior, and leave questions,
  implementation discovery, and test planning for Codex CLI.
- Evaluate whether `/review`, `$audit`, or a focused audit skill fits each
  non-trivial spec or implementation task before advancing.
- When Django model/schema changes are introduced, generate and apply the
  required migrations in development before treating the task as complete.
- After a successful tagged release and back-merge from `main` to `develop`,
  consolidate released SDD files before new SDD work.
- Release consolidation must leave `CHANGELOG.md` as compact grouped category
  summaries built from shipped specs, completed backlog outcomes, and existing
  changelog notes.

## 5. Delivery and Coordination

- Update `CHANGELOG.md` under `## [Unreleased]` for every behavior, docs,
  governance, workflow, or guidance change unless it is formatting-only.
- Prefix changelog bullets with domain categories such as `UI/UX`,
  `Governance`, `Release`, `Backend`, `Data`, `Mobile`, `Tests`, or `Docs`.
- Closure must reconcile in-scope backlog/spec metadata, commit with
  `--no-gpg-sign`, push, and leave `git status --short` clean.

## 6. Markdown Rules

- Keep new or rewritten Markdown light and schematic.
- `CHANGELOG.md` should record outcomes, not process narration.
- Keep `CHANGELOG.md` categories stable; prefer product or workflow domains.
- Active-work specs should capture only scope, constraints, and checks needed
  for execution.
- Consolidated release files should stay as compact provenance summaries.
- Enforce `MD022` and `MD032`; treat `MD013` as non-blocking.
- Run markdownlint on changed Markdown files when available.
