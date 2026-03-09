# Frontend View Modules

## Purpose

This document explains how frontend views are organized after modularization and how modules collaborate.

The public import path remains `frontend.views`.
`frontend.views` is a compatibility facade and should stay thin.

## Runtime Flow

1. `paddle/frontend/urls.py` imports callables from `frontend.views`.
2. `frontend.views` re-exports functions/classes from `frontend.view_modules.*`.
3. Domain modules implement actual logic.
4. Shared helpers live in `frontend.view_modules.common`.

## Module Responsibilities

### `frontend/views.py` (facade)

- Re-export stable public callables used by URL routing and tests.
- Avoid business logic.
- Preserve backward compatibility for imports and monkeypatching.

### `frontend/view_modules/common.py`

- Shared helpers/forms used by multiple domains.
- Pagination helpers, ranking redirects, player utility lookups, and version label retrieval.

### `frontend/view_modules/ranking.py`

- Ranking page orchestration and scope behavior.
- Ranking home redirect, hall of fame wrapper, scoped ranking rendering, and scoped player page helpers.

### `frontend/view_modules/players.py`

- Public players pages (`/players/` and `/players/<id>/`).
- Player match query helpers and player insights computation (trend/partner/rivals).

### `frontend/view_modules/matches.py`

- Authenticated matches workflow (`/matches/`).
- Match create/delete orchestration and match list presentation formatting.

### `frontend/view_modules/auth_profile.py`

- Registration, login/logout, user profile update, and about page handlers.
- Request form parsing and auth/profile response handling.

## Design Rules

- Keep URL-visible behavior unchanged unless explicitly requested.
- Put cross-cutting helpers in `common.py`.
- Do not duplicate helpers across modules.
- Keep `frontend.views` as a facade only.
