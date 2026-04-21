# Recent Form Balance Labels

## Tracking

- Task ID: `recent-form-balance-labels`
- Status: `implemented`
- Release tag: `unreleased`

## Summary

- Replace the explicit `Últimos partidos` balance formula with a qualitative
  Spanish balance label.
- Keep the chart data and balance calculation in the backend.

## Scope

- In:
  - Map the last-ten match balance to a qualitative display label.
  - Preserve wins, losses, numeric balance, chart points, and aria context in
    backend-prepared data.
  - Add focused player detail tests and an Unreleased changelog entry.
- Out:
  - Chart geometry, axes, fill colors, JavaScript, rival pairs, partner cards,
    API, or database changes.

## Files Allowed to Change

- `CHANGELOG.md`
- `paddle/frontend/tests/test_players_pages.py`
- `paddle/frontend/view_modules/players.py`
- `specs/052-recent-form-balance-labels.md`

## Files Forbidden to Change

- Django model and migration files.
- Deprecated DRF/API files.
- Unrelated frontend templates, static assets, governance files, or release
  records.

## Implementation Plan

- [x] Add a backend helper that maps balance bands to Spanish labels.
- [x] Use the qualitative label for `recent_form_chart.record_label`.
- [x] Update tests for neutral, positive, and negative balance labels.
- [x] Update `CHANGELOG.md` under `Unreleased`.

## Acceptance

- [x] The `Últimos partidos` header no longer shows the explicit
  `Balance = wins - losses = total` formula.
- [x] Positive balances show `Balance positivo`, `Balance muy positivo`, or
  `Balance excelente` based on the numeric balance.
- [x] Negative balances show `Balance negativo`, `Balance muy negativo`, or
  `Balance crítico` based on the numeric balance.
- [x] A zero balance shows `Balance neutro`.
- [x] Existing chart data, axes, points, and accessibility context remain
  backend-owned.

## Validation

- [x] `pytest paddle/frontend/tests/test_players_pages.py -q`
- [x] `markdownlint --disable MD013 -- CHANGELOG.md specs/052-recent-form-balance-labels.md`
