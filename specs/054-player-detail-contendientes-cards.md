# Player Detail Contendientes Cards

Status: implemented
Release tag: v1.9.3

## Scope

- Add a `Contendientes` block to the player detail page after
  `Parejas rivales frecuentes`.
- Show individual head-to-head cards for:
  - `Némesis`: rivals with the most wins against the displayed player.
  - `Víctimas`: rivals the displayed player has beaten most often.
- Count each opposing player independently in doubles matches.

## Backend Context

- Extend `build_player_insights()` with per-opponent aggregation:
  - matches against the displayed player
  - displayed-player wins
  - opponent wins
  - displayed-player win rate
  - opponent win rate
  - latest match date
- Provide `player_insights["nemesis_cards"]` and
  `player_insights["victim_cards"]`.
- Sort `nemesis_cards` by opponent wins, opponent win rate, recency, then
  lower player ID.
- Sort `victim_cards` by displayed-player wins, displayed-player win rate,
  recency, then lower player ID.
- Exclude rows without a qualifying win count for that category.

## UI

- Reuse existing Bootstrap cards, partner-card classes, swatches, record labels,
  and circular progress partials.
- Show one-line row help text:
  - `Némesis: más puntos perdidos contra...`
  - `Víctimas: más puntos ganados contra...`
- Use match-level head-to-head outcomes for the points wording.
- In `Némesis`, show displayed-player losses then wins and use the loss ratio
  for the circular progress value.
- In `Víctimas`, show displayed-player wins then losses and use the win ratio
  for the circular progress value.
- Use a steep Bootstrap opacity ramp for row colors: `100`, `50`, then `25`.
- Render fewer than three cards when fewer qualifying players exist.
- Show disabled `Sin datos` cards with inactive progress wheels for empty
  rival-pair and Contendientes rows.

## Checks

- `python manage.py test paddle.frontend.tests.test_players_pages`
- `python manage.py test paddle.frontend.tests.test_views`
- `markdownlint --disable MD013 -- specs/054-player-detail-contendientes-cards.md CHANGELOG.md`
