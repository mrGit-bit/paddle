# Release 1.9.1 Consolidated Spec

## Release

- Tag: `1.9.1`
- Date: `2026-04-16`

## Sources

- `specs/039-ranking-sort-header-icons.md`
- `specs/040-player-trend-progress-wheels.md`
- `specs/041-anonymous-player-menu-labels.md`
- `specs/042-player-partner-progress-bar.md`
- `specs/043-player-efficiency-scope-wheels.md`
- `specs/044-player-ranking-progress-bars.md`
- `specs/045-player-partner-efficiency-cards.md`
- `specs/046-default-own-player-detail.md`
- `specs/047-player-partner-card-records.md`

## Shipped Scope

- Ranking table sort icons currently inherit Bootstrap link blue.
- On small screens, table header truncation can show ellipsis dots beside the
  sort arrows.
- Sort icons should render white and remain clean on narrow viewports.
- Replace the player detail `Tendencias` table with a new `Eficacia` section
  using three responsive Bootstrap stat cards.
- Show circular efficiency indicators for `Últimos 5`, `Últimos 10`, and
  `Total` using the existing backend-calculated win-rate percentages.
- Keep all three wheels visible while muting duplicate result windows to a
  neutral grey track-only wheel.
- Show only the wheel in each card; wins, losses, and match counts remain part
  of the backend comparison data but are not displayed in the cards.
- Anonymous users browsing the public `Jugadores` flow currently see player
  options with club/group names in the `Selecciona jugador` dropdown.
- The dropdown should show only player names for anonymous users.
- Replace the player detail `Pareja habitual` table with a Bootstrap stacked
  progress bar.
- Show the top three partners plus a grouped `Otros` remainder as a compact
  partner distribution.
- Keep partner ranking and percentage preparation in backend context; templates
  only render prepared rows.
- Extend the public player detail `Eficacia` section with selector wheels for
  `Todos`, the displayed player's gender category, and `Mixtos`.
- Update the trend wheels to show `Ultimos 5`, `Ultimos 10`, and `Ultimos 20`
  for the selected scope.
- Keep selected cards readable with selected-tab borders and an inverted `Ver`
  action instead of full-card background color.
- Replace the player detail `Posicion en los rankings` table with stacked
  Bootstrap progress rows.
- Keep backend ranking data as the source of truth and expose only
  display-ready fields to the template.
- Replace the player detail `Pareja habitual` legend with three partner
  efficiency cards below the existing stacked progress bar.
- Keep partner ranking, card values, colors, and empty slot data prepared by
  backend context.
- Clarify that the stacked bar shows play frequency and the wheels show partner
  efficiency.
- When an authenticated user opens the public players page, default the page to
  their linked player detail instead of showing the empty selector-only state.
- Keep anonymous users on the current empty players page by default.
- Keep direct player detail URLs public and unchanged.
- Add each partner efficiency card's win and match record below the partner
  name on player detail pages.
- Keep the record prepared by backend context and rendered as compact display
  text.

## Validation Summary

- Focused Hall of Fame sort-control pytest.
- Frontend views and ranking pytest.
- `markdownlint CHANGELOG.md specs/039-ranking-sort-header-icons.md`
- Manual checks on desktop and narrow mobile ranking pages.
- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `markdownlint CHANGELOG.md specs/040-player-trend-progress-wheels.md`
- Manually check zero-match, partial-history, and long-history player detail
  pages.
- Manually check mobile and desktop trend card layout.
- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `markdownlint CHANGELOG.md specs/041-anonymous-player-menu-labels.md`
- Manual check anonymous `/players/` and `/players/<id>/` dropdown labels.
- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `markdownlint CHANGELOG.md specs/042-player-partner-progress-bar.md`
- Manually check zero-match, two-partner, three-partner, and four-plus-partner
  player detail pages.
- Manually check mobile and desktop readability.
- `pytest paddle/frontend/tests/test_players_pages.py -q`
- Player pages and ranking pytest.
- `markdownlint specs/043-player-efficiency-scope-wheels.md`
- `markdownlint CHANGELOG.md specs/043-player-efficiency-scope-wheels.md`
- Manually check zero-match, sparse-history, gender-scoped, mixed-scoped, and
  mobile player detail pages.
- `pytest paddle/frontend/tests/test_players_pages.py -q`
- Player pages and ranking pytest.
- `markdownlint CHANGELOG.md specs/044-player-ranking-progress-bars.md`
  reported only non-blocking pre-existing `MD013` line-length issues in
  `CHANGELOG.md`.
- Manual check zero-match, gender-scoped, mixed fallback, mobile readability,
  and row click-through behavior.
- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `markdownlint CHANGELOG.md specs/045-player-partner-efficiency-cards.md`
- Manual check zero-partner, two-partner, three-partner, and four-plus-partner
  player detail pages.
- Manual check mobile and desktop readability.
- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `markdownlint CHANGELOG.md specs/046-default-own-player-detail.md`
- Manual check anonymous `/players/`.
- Manual check authenticated `/players/` with a linked player.
- Manual check authenticated `/players/` without a linked player.
- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `markdownlint CHANGELOG.md specs/047-player-partner-card-records.md`
- Manual check two-partner and three-partner player detail pages.
- Manual check mobile and desktop partner card readability.
