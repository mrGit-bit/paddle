# Medallero Public Page

Use for active SDD work only.

## Tracking

- Task ID: `medallero-public-page`
- Status: `implemented`
- Release tag: `v1.10.0`

## Summary

- Add a public `Medallero` page showing medals earned from the first page of
  each ranking scope.
- Keep medal assignment backend-owned and consistent with existing group-aware
  ranking behavior.

## Scope

- In:
  - Centralized medal metadata for names, icons, descriptions, categories,
    scope labels, scope classes, and display order.
  - Backend medal assignment from `all`, `male`, `female`, and `mixed` ranking
    scopes.
  - Public `/medallero/` page and navbar entry after `Parejas` and before
    `Torneos`.
  - Template-ready rows with stable 3-column medal grids and visible scope
    labels.
  - Focused tests for metadata, service rules, public rendering, navbar order,
    incomplete rows, and group context.
- Out:
  - Database schema changes.
  - Clickable medal detail pages.
  - API or DRF changes.
  - Changes to ranking formulas outside the medal service.

## Files Allowed to Change

- `paddle/frontend/medals/__init__.py`
- `paddle/frontend/medals/config.py`
- `paddle/frontend/services/medals.py`
- `paddle/frontend/templates/frontend/base.html`
- `paddle/frontend/templates/frontend/medallero.html`
- `paddle/frontend/static/frontend/css/styles.css`
- `paddle/frontend/urls.py`
- `paddle/frontend/views.py`
- `paddle/frontend/view_modules/ranking.py`
- `paddle/frontend/tests/test_medals.py`
- `paddle/frontend/tests/test_views.py`
- `paddle/frontend/tests/test_templates.py`
- `paddle/frontend/tests/test_players_pages.py`
- `specs/036-medallero-public-page.md`

## Files Forbidden to Change

- Database migrations.
- Deprecated DRF/API endpoints.
- Release consolidation specs.

## Implementation Plan

- [x] Add medal metadata config with six medal definitions and four scopes.
- [x] Add medal assignment service using existing ranking computations and
      group context.
- [x] Add URL, view, navbar link, template, and scoped CSS.
- [x] Add focused tests for config, service, view, template, navbar, and group
      behavior.
- [x] Run required validation.

## Acceptance

- [x] `/medallero/` renders for anonymous users.
- [x] Authenticated users linked to a player see medals for their player's
      group context.
- [x] Eligible players are those with `display_position <= 12`, including ties
      at rank 12.
- [x] Rank medals use existing `display_position`, including ties at ranks 1,
      2, and 3.
- [x] `Top 3 eficacia` and `Top 3 partidos` include ties at the third sorted
      eligible row and exclude non-eligible players.
- [x] Efficacy comparisons use existing canonical rounded win-rate precision.
- [x] Medal cards render in stable 3-column rows with empty slots preserved.
- [x] The navbar link appears after `Parejas` and before `Torneos`.

## Validation

- `python scripts/validate_governance.py`
- `markdownlint specs/036-medallero-public-page.md` when available; `MD013` is
  non-blocking.
- Focused Django tests for medal config, medal service, and public rendering.
