# rankingdepadel.club

Production domains: `rankingdepadel.club` and `staging.rankingdepadel.club`

## Overview

This repository contains the full project for `rankingdepadel.club`, a Django
application for padel rankings, match tracking, player profiles, and Americano
tournaments. The repo ships two product surfaces:

- Web app: Django server-rendered application.
- Mobile app: Capacitor WebView wrapper around the web product.

The supported surface is the server-rendered web app plus the mobile WebView
wrapper. The deprecated DRF/API endpoints are removed and should not be
reintroduced.

## Recent Changes

Use [CHANGELOG.md](/workspaces/paddle/CHANGELOG.md) for the full release
history. The most relevant current changes are:

- `Unreleased`: the GitHub release workflow now sets a valid Git identity for
  repository workflow keeps one spec and one plan per active SDD, then
  consolidates the completed release batch only after a successful tagged
  release back-merge from `main` to `develop`.
- `1.4.1`:
  - the GitHub release workflow now sets a valid Git identity for tag creation
    and verifies that `paddle/config/__init__.py` matches the latest released
    version in `CHANGELOG.md` before extracting release notes.
  - `README.md` and governance docs were refreshed to improve repository
    guidance, README maintenance expectations, and Markdown line-length rules.
- `1.4.0`:
  - account management now uses standard form submissions for profile editing,
    confirmed email on registration, and a dedicated account-deletion
    confirmation flow.
  - governance rules were tightened around branch checks, spec/plan approval
    gates, markdownlint compliance, and changelog-aligned commit messaging.
  - release automation now derives the release version from
    `paddle/config/__init__.py`.
- `1.3.1` and `1.3.0`:
  - player profile pages were expanded with player insights, match history, and
    navigation from ranking pages.
  - ranking behavior was consolidated around one canonical policy and shared
    query helpers.
  - `frontend.views` was split into internal `view_modules` while keeping the
    external route surface stable.

## Product Areas

### Rankings

- Public ranking pages for `all`, `male`, `female`, and `mixed`.
- Competition-style tie positions (`1224`).
- Unranked players shown separately.
- Clickable ranking rows linking to player profiles.

### Players

- Public player directory and player profile pages.
- Player trend summaries, frequent partner, and top rival pairs.
- Authenticated account management with profile edit and account deletion
  flows.

### Matches

- Authenticated users can create matches.
- Match correction is handled as delete-and-recreate; match editing is not part
  of the active surface.

### Americano Tournaments

- Public tournament visibility.
- Logged-in users can create tournaments.
- Participants, creators, and staff have scoped edit permissions.
- Standings are recomputed from persisted match results.

## Architecture

### Backend

- Django
- Session authentication
- SQLite in development
- Oracle Autonomous Database in staging/production

### Frontend

- Django templates
- Bootstrap 5
- Minimal vanilla JavaScript when needed

### Mobile

- Capacitor wrapper
- Shared backend and frontend with the web app

## Important Repository Paths

- [docs/PROJECT_INSTRUCTIONS.md](/workspaces/paddle/docs/PROJECT_INSTRUCTIONS.md):
  primary repository governance after the explicit task brief.
- [AGENTS.md](/workspaces/paddle/AGENTS.md): agent workflow and output rules.
- [CHANGELOG.md](/workspaces/paddle/CHANGELOG.md): release history and recent
  documented changes.
- [RELEASE.md](/workspaces/paddle/RELEASE.md): release flow and fallback tools.
- [paddle/config/__init__.py](/workspaces/paddle/paddle/config/__init__.py):
  runtime version source.
- [paddle/frontend/services/ranking.py](/workspaces/paddle/paddle/frontend/services/ranking.py):
  ranking computation source.
- [paddle/frontend/view_modules](/workspaces/paddle/paddle/frontend/view_modules):
  main frontend view implementations.
- [paddle/frontend/VIEW_MODULES.md](/workspaces/paddle/paddle/frontend/VIEW_MODULES.md):
  notes about the view-module split.
- [plans](/workspaces/paddle/plans): approved execution plans.
- [specs](/workspaces/paddle/specs): approved task specifications and
  post-release consolidated deployment specs.

## Codex CLI Guide

Read this repository in this order when the task touches product behavior:

1. Explicit user task brief.
2. [docs/PROJECT_INSTRUCTIONS.md](/workspaces/paddle/docs/PROJECT_INSTRUCTIONS.md).
3. [AGENTS.md](/workspaces/paddle/AGENTS.md).
4. Relevant spec in [specs](/workspaces/paddle/specs) and plan in
   [plans](/workspaces/paddle/plans), if the workflow requires them.
5. The relevant app code and tests.

Key rules for safe edits:

- Check the current git branch before implementation work. Repository workflow
  expects development work from `develop` unless the user confirms otherwise.
- Follow the mandatory Spec -> Plan -> Implementation flow for code changes.
- After spec approval, suggest a spec-focused pre-audit only when it is needed
  for that approved scope, and briefly state why it is needed or not needed.
- After implementation, suggest a scoped post-implementation audit only when
  it is needed, and briefly state why it is needed or not needed.
- Keep one spec and one plan per active SDD. After a successful tagged release
  and back-merge from `main` to `develop`, consolidate that deployment into
  `specs/release-X.Y.Z-consolidated.md` and
  `plans/release-X.Y.Z-consolidated.md`.
- The first Codex task after that successful back-merge must perform any
  pending consolidation before starting new SDD work.
- After a deployment has been consolidated, its released per-SDD spec and plan
  files must no longer remain as separate loose files.
- Keep business logic out of templates.
- Do not duplicate ranking logic outside
  [paddle/frontend/services/ranking.py](/workspaces/paddle/paddle/frontend/services/ranking.py).
- Keep views thin and prefer existing helpers/services over new parallel logic.
- Do not expand or restore the removed DRF/API surface.
- UI text stays in Spanish; code, comments, docs, specs, and plans stay in
  English.
- Update or add targeted pytest coverage for behavior changes.
- Update `CHANGELOG.md` for behavior, documentation, governance, workflow, and
  repository-guidance changes unless they are truly formatting-only.
- Treat "close cycle" as complete only after all remaining requested-work
  changes have been staged, committed, pushed, and `git status --short` is
  clean.

## Project Structure

```text
/workspaces/paddle/
├── mobile/
├── paddle/
│   ├── americano/
│   ├── config/
│   ├── frontend/
│   │   ├── services/
│   │   ├── templates/
│   │   ├── tests/
│   │   ├── view_modules/
│   │   └── views.py
│   └── users/
├── docs/
├── plans/
├── specs/
├── CHANGELOG.md
├── RELEASE.md
└── README.md
```

## Testing

Run the smallest relevant pytest scope for the change. Common commands:

```bash
pytest -q
pytest paddle/frontend/tests/test_ranking.py -q
pytest paddle/frontend/tests/test_players_pages.py -q
pytest paddle/americano/tests/test_americano_views.py -q
```

The project standard is at least 90% coverage when coverage is relevant to the
task.

## Environment Notes

- Python: `3.10.12`
- Development database: SQLite
- Production/staging database: Oracle Autonomous Database over TCPS
- Environment selection is controlled through `DJANGO_ENVIRONMENT`

Never commit secrets or local environment values.
