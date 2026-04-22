# Template Presentation Audit Report

## Summary

- Scope: Player detail presentation audit with loaded base and shared partial
  templates.
- Audited target: `paddle/frontend/templates/frontend/player_detail.html`,
  `base.html`, `_circular_progress.html`, `_match_card.html`, and
  `_pagination.html`.
- Audit date: 2026-04-22
- Reviewer: Codex
- Verification: Source cascade tracing across templates, shared CSS, and
  existing player-detail tests. Browser computed-style verification was not
  run.

## Presentation Findings

### Finding TPA-001

- Status: solved
- Type: Confirmed issue
- Severity: medium
- Location: `paddle/frontend/templates/frontend/player_detail.html` lines 66-71
  and 384-386; `paddle/frontend/static/frontend/css/styles.css` lines 290-309.
- Evidence: Inactive efficiency selector cards receive
  `player-efficiency-card-disabled` and `aria-disabled="true"`, and CSS gives
  them muted disabled styling. The click handler still attaches to every
  `[data-efficiency-scope]` button and calls `selectScope()` without checking
  `aria-disabled` or a native `disabled` attribute, so a visually disabled card
  can become `player-efficiency-selector-card-active` and reveal its trend row.
- Root cause: State class and ARIA state are not synchronized with the
  JavaScript interaction state.
- Recommended minimal fix: Prevent disabled selector cards from activating,
  either by rendering a native `disabled` attribute for inactive selector
  buttons and styling the disabled state, or by guarding the click handler
  against `aria-disabled="true"` before calling `selectScope()`.
- Tests or manual checks: Added rendered-template regressions for the native
  disabled contract and JavaScript disabled guard, then verified the focused
  player-detail tests pass.
- Discard explanation:

## Residual Risk

- Browser-computed-style verification was not run, so the audit is based on
  source cascade tracing rather than measured computed styles.
- `_match_card.html` contains locked-match action markup, but
  `player_detail_view` passes empty `user_matches`, so that branch is not active
  in the audited player-detail render path.

## Open Questions

- None.
