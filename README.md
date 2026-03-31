# rankingdepadel.club

Production domain: `rankingdepadel.club`
Staging domain: `staging.rankingdepadel.club`

## Overview

This repository contains the full project for `rankingdepadel.club`, a Django
application for padel rankings, match tracking, player profiles, and Americano
tournaments. The repo ships two product surfaces:

- Web app: Django server-rendered application.
- Mobile app: Capacitor WebView wrapper around the web product.

The supported surface is the server-rendered web app plus the mobile WebView
wrapper. The deprecated DRF/API endpoints are removed and should not be
reintroduced.

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
  compact repository constraints and minimum SDD gates.
- [AGENTS.md](/workspaces/paddle/AGENTS.md): Codex execution behavior, workflow
  mechanics, and handoff rules.
- [CHANGELOG.md](/workspaces/paddle/CHANGELOG.md): release history and
  unreleased documented changes.
- [BACKLOG.md](/workspaces/paddle/BACKLOG.md): pending work inventory.
- [RELEASE.md](/workspaces/paddle/RELEASE.md): release flow and fallback tools.
  The release custom prompt command is `/prompts:release`, and the version
  argument should be passed as `x.y.z` or `vx.y.z`.
- [paddle/config/__init__.py](/workspaces/paddle/paddle/config/__init__.py):
  runtime version source.
- [paddle/frontend/services/ranking.py](/workspaces/paddle/paddle/frontend/services/ranking.py):
  ranking computation source.
- [paddle/frontend/view_modules](/workspaces/paddle/paddle/frontend/view_modules):
  main frontend view implementations.
- [paddle/frontend/VIEW_MODULES.md](/workspaces/paddle/paddle/frontend/VIEW_MODULES.md):
  notes about the view-module split.
- [plans](/workspaces/paddle/plans): active plans and consolidated release
  plans.
- [specs](/workspaces/paddle/specs): active specs and consolidated release
  specs.
- Consolidated release files represent shipped production history only. If a
  planned version never ships, its loose historical artifacts roll into the
  next production release that actually shipped them.
- Loose active specs/plans should keep `Release tag: unreleased` until the
  release command stamps the shipped version.
- Specs, plans, and consolidated release files are intentionally schematic;
  keep them compact instead of using them as long-form narrative docs.

## Codex CLI Guide

Read this repository in this order when the task touches product behavior:

1. Explicit user task brief.
2. [docs/PROJECT_INSTRUCTIONS.md](/workspaces/paddle/docs/PROJECT_INSTRUCTIONS.md).
3. [AGENTS.md](/workspaces/paddle/AGENTS.md).
4. The active-work spec and plan for the task:
   the latest approved non-release files in [specs](/workspaces/paddle/specs)
   and [plans](/workspaces/paddle/plans) created for that task, paired by
   shared `Task ID` tracking metadata and explicit `Plan` / `Spec` references.
   For small, low-risk documentation or governance updates, this may be skipped
   only when the higher-authority governance docs allow the reduced-process
   path for that request.
5. The relevant app code and tests.

Quick routing:

- Use [CHANGELOG.md](/workspaces/paddle/CHANGELOG.md) for release history.
- Use [RELEASE.md](/workspaces/paddle/RELEASE.md) for release flow.
- Use [docs/PROJECT_INSTRUCTIONS.md](/workspaces/paddle/docs/PROJECT_INSTRUCTIONS.md)
  for compact repository constraints.
- Use [AGENTS.md](/workspaces/paddle/AGENTS.md) for execution and handoff
  behavior.

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
