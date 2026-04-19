# Player Detail Rankings Colors

## Tracking

- Task ID: `player-detail-ranking-efficiency-colors`
- Status: `implemented`
- Release tag: `unreleased`

## Summary

- Rework the player detail ranking and efficiency sections under a single
  `Rankings` heading with partner-style subsection labels.
- Keep the current ranking progress bars and efficiency selector behavior.
- Use the same blue, green, and yellow color palette as `Pareja habitual`.

## Scope

- In:
  - Color-code the three ranking scopes consistently across ranking bars,
    efficiency cards, and circular progress wheels with the partner palette.
  - Show compact wins/matches records in efficiency cards.
  - Use efficiency cards as the visible legends for the ranking color code.
  - Remove redundant ranking-position cards after the progress bars.
  - Keep ranking efficiency card typography, legend markup, and internal
    spacing aligned with the `Eficacia por pareja` cards.
  - Show inactive `--%` wheels for empty scopes or insufficient trend history.
  - Style inactive ranking efficiency cards with Bootstrap disabled
    form-control colors while keeping selector buttons clickable.
  - Apply the same inactive card styling and `--%` wheel label to placeholder
    partner-efficiency cards.
  - Add focused player-detail rendering tests.
- Out:
  - Changing ranking, match, or efficiency calculations.
  - Adding JavaScript beyond the current efficiency selector behavior.
  - Database or API changes.

## Files Allowed to Change

- `CHANGELOG.md`
- `paddle/frontend/static/frontend/css/styles.css`
- `paddle/frontend/templates/frontend/_circular_progress.html`
- `paddle/frontend/templates/frontend/player_detail.html`
- `paddle/frontend/tests/test_players_pages.py`
- `paddle/frontend/view_modules/players.py`
- `specs/049-player-detail-ranking-efficiency-colors.md`

## Implementation Plan

- Add ranking-specific scope color and record-label context fields in the player
  detail view and efficiency helpers.
- Update ranking and efficiency markup to render `Rankings`, `Posición`, and
  `Eficacia por ranking` with partner-style subsection labels.
- Extend CSS with narrow ranking/efficiency card styles that reuse the partner
  card visual language.
- Update focused tests for color classes, records, and unchanged links/toggles.

## Acceptance

- Ranking progress bars remain visible and use the scope color code.
- Ranking-position cards no longer render after the progress bars.
- Efficiency cards act as ranking legends with matching swatches.
- Efficiency cards show wins/matches records.
- Efficiency circular progress strokes use the matching scope color.
- Ranking efficiency cards use the same legend markup, title typography, and
  row spacing as partner efficiency cards.
- Empty or insufficient-history wheels render inactive with `--%`.
- Inactive ranking efficiency cards use disabled Bootstrap control colors.
- Placeholder partner-efficiency cards use the same inactive styling and `--%`
  wheel label.
- Existing player-detail behavior remains covered by focused tests.

## Validation

- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `markdownlint CHANGELOG.md specs/049-player-detail-ranking-efficiency-colors.md`
