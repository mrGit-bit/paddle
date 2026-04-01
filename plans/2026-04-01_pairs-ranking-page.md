# Pairs Ranking Page Plan

## Tracking

- Task ID: `pairs-ranking-page`
- Spec: `specs/036-pairs-ranking-page.md`
- Release tag: `unreleased`

## Summary

- Add a dedicated all-matches pairs ranking page reachable from the navbar.
- Reuse the existing ranking-table visual structure, with both players rendered
  in one cell on separate lines.

## Scope

- In:
  - pair-stat aggregation from normal match records
  - public pairs page with three tables
  - focused route/template tests
  - unreleased changelog update
- Out:
  - pagination or client-side sorting for pairs
  - player-profile links from pair rows
  - scope variants beyond all matches

## Plan

- [ ] Add backend pair aggregation helpers in `frontend.services.ranking`.
- [ ] Add a dedicated ranking view and route for the pairs page.
- [ ] Add a shared pair-table include and render the three requested sections.
- [ ] Add the `Parejas` navbar entry.
- [ ] Extend focused ranking/view pytest coverage and update `CHANGELOG.md`.

## Acceptance

- [ ] Pair rankings are computed from canonicalized team pairs regardless of
      player order within the team.
- [ ] Victory ties and rate ties are broken by more matches played together.
- [ ] The page renders top 5 / top 3 / top 3 rows in the requested sections,
      with the rate-based tables limited to pairs with at least 5 matches.
- [ ] Each pair cell shows one player per line in the same column.

## Validation

- `pytest paddle/frontend/tests/test_ranking.py`
- `pytest paddle/frontend/tests/test_views.py`
