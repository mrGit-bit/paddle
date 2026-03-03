<!-- markdownlint-disable MD025 -->

# 🏆 Rankin de padel

Production domain: rankingdepadel.club

## Governance & AI Workflow
- See /docs/PROJECT_INSTRUCTIONS.md for governance and workflow rules.
- See AGENTS.md for agent constraints.
- See /plans/ for plan-mode task histories and templates.

---

# 1️⃣ Project Purpose

Full-stack Django web application for managing:

- Padel match tracking
- Hall of Fame rankings
- Player statistics
- Americano tournaments

This repository contains TWO products:

1. Django Web App (primary product)
2. Android Mobile Wrapper (Capacitor WebView)

There is no duplicated business logic in the mobile app.

---

# 2️⃣ Architecture Overview

## Backend

- Django
- Session authentication
- Oracle Autonomous DB (staging / production)
- SQLite (development)

## Frontend

- Django Templates (NOT React)
- Bootstrap 5
- Minimal vanilla JavaScript
- No frontend framework

## Mobile

- Capacitor (Android)
- WebView loads production or staging URL
- No duplicated backend logic

## Deprecated Components Removed

- Django REST Framework API endpoints (`/api/games/`, `/api/users/`, `/api-auth/`) have been removed.
- The supported product surface is the server-rendered web app plus the mobile WebView wrapper.

---

# 3️⃣ Critical Architectural Rules (FOR AI AGENTS)

These rules must NEVER be violated.

## Version Source of Truth

Runtime version is defined ONLY in:

    paddle/config/__init__.py

Example:

    __version__ = "1.3.0"

Rules:

- CHANGELOG.md is documentation only.
- `[Unreleased]` must always remain at the top of CHANGELOG.md.
- The About page reads version from `config.__version__`.
- Never parse version from CHANGELOG.md.
- Never infer version from Git tags inside runtime code.

---

## Ranking Logic

- All ranking computation lives in:

    paddle/frontend/services/ranking.py

- Main function:

    compute_ranking(scope)

Rules:

- Do NOT move ranking logic into templates.
- Do NOT duplicate ranking computation.
- Templates must render precomputed `display_*` fields.

---

## Views Rules

- Views must remain thin.
- No heavy computation inside views.
- No business logic in templates.
- Use PRG (Post-Redirect-Get) for POST handling.

---

## Templates Rules

- Templates must not compute logic.
- Only display values passed via context.
- No ranking calculations in templates.

---

# 4️⃣ Branching Model

- develop → integration
- staging → pre-production
- main → production

Rules:

- No direct commits to main.
- Release flow defined in RELEASE.md.
- CI must pass before merging to staging or main.

---

# 5️⃣ Project Structure

High-level structure:

    /workspaces/paddle/
    ├── mobile/
    ├── paddle/
    │   ├── americano/
    │   ├── config/
    │   │   ├── __init__.py
    │   │   └── settings/
    │   ├── frontend/
    │   │   ├── services/
    │   │   ├── templates/
    │   │   └── views.py
    │   ├── games/
    │   ├── users/
    │   └── staticfiles/
    ├── CHANGELOG.md
    ├── RELEASE.md
    ├── README.md
    ├── requirements.txt
    └── .env

---

# 6️⃣ Core Functional Areas

## Hall of Fame

- Public ranking
- Scopes:
  - all
  - male
  - female
  - mixed
- Tie style: competition ("1224")
- Unranked table
- Clickable ranking rows
- Scope persistence in session

---

## Match Management

- 2 teams per match (2 players each)
- Authenticated users:
  - Create matches
  - Delete own matches
- Matches are NOT editable
- Correction = delete + recreate

---

## Americano Tournaments

- Public read
- Authenticated users can create
- Participants can edit rounds while open
- Standings recomputed from scratch
- Tie style: competition format

Models:

- AmericanoTournament
- AmericanoRound
- AmericanoMatch
- AmericanoPlayerStats

---

# 7️⃣ Testing & Coverage

Run all tests:

    pytest -q

Check coverage:

    pytest frontend/tests/ --cov=frontend.views --cov-report=term-missing
    pytest americano/tests/test_americano_views.py --cov=americano.views --cov-report=term-missing

Minimum target coverage: 90%

CI must enforce coverage threshold.

---

# 8️⃣ Environment Configuration

Environment variables loaded via:

    python-decouple

Main variable:

    DJANGO_ENVIRONMENT=dev | prod

Never commit secrets.

---

# 9️⃣ AI Editing Guardrails

When modifying this repository:

DO:

- Keep edits minimal
- Respect file boundaries
- Follow existing style
- Preserve version rules
- Preserve ranking logic structure

DO NOT:

- Move business logic into templates
- Parse version from CHANGELOG.md
- Refactor project structure without explicit instruction
- Modify workflows unless requested
- Change settings architecture

---

# 🔟 Release Summary

Release flow is documented in:

    RELEASE.md

Web and Mobile releases are independent.

Repository tags must match:

    config.__version__

---

# 1️⃣1️⃣ Production Deployment

Production stack:

- Ubuntu VM
- Gunicorn
- Nginx
- Cloudflare (Full Strict SSL)
- Oracle Autonomous DB

Deployment commands are described in RELEASE.md.

---

End of README.md
