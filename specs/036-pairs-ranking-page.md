# Pairs Ranking Page

## Tracking

- Task ID: `pairs-ranking-page`
- Plan: `plans/2026-04-01_pairs-ranking-page.md`
- Release tag: `unreleased`

## Goal

- Add a new public `Parejas` ranking page in the main navbar.
- Show pair rankings for all matches using the existing ranking-table visual
  language.

## Scope

- In:
  - navbar link for `Parejas`
  - dedicated all-matches pairs ranking page
  - top 5 pairs by victories
  - top 3 best-rate pairs with at least 4 matches
  - top 3 worst-rate pairs with at least 4 matches
  - focused tests and changelog update
- Out:
  - gender-scoped pairs rankings
  - clickable pair rows
  - DRF/API changes

## Files

- Allowed:
  - `paddle/frontend/services/ranking.py`
  - `paddle/frontend/view_modules/ranking.py`
  - `paddle/frontend/views.py`
  - `paddle/frontend/urls.py`
  - `paddle/frontend/templates/frontend/base.html`
  - `paddle/frontend/templates/frontend/pairs_ranking.html`
  - `paddle/frontend/templates/frontend/_pair_ranking_table.html`
  - `paddle/frontend/tests/test_ranking.py`
  - `paddle/frontend/tests/test_views.py`
  - `CHANGELOG.md`
- Forbidden:
  - `paddle/games/**`
  - `.github/**`
  - `mobile/**`

## Acceptance

- [ ] The navbar shows a `Parejas` link to a dedicated public page.
- [ ] `Ranking de parejas` shows the top 5 pairs by victories.
- [ ] `Parejas del siglo` and `Parejas catastróficas` show only pairs with at
      least 5 matches.
- [ ] All pair-name cells show both players in the same column on separate
      lines.
- [ ] Focused frontend tests cover pair aggregation, ordering, and page
      rendering.

## Checks

- Run focused frontend pytest scopes for rankings and views.
