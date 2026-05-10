# Release 1.10.2 Consolidated Spec

## Release

- Tag: `1.10.2`
- Date: `2026-05-10`

## Sources

- `specs/040-faster-release-orchestrator.md`
- `specs/038-player-detail-medallas-accordion.md`
- `specs/039-player-detail-stats-accordion.md`

## Shipped Scope

- Move release-prep work into the local release orchestrator so normal
  releases prepare `CHANGELOG.md` and `paddle/config/__init__.py` locally.
- Add `--next-patch` and `--skip-local-validation` controls to the release
  orchestrator.
- Fail promotion checks deterministically when no required or visible checks
  are reported.
- Block completed releases when closure-complete loose specs remain at
  `Release tag: unreleased`.
- Add a player-detail `Medallas` category before existing statistics and
  matches sections.
- Show the selected player's medal card expanded by default and collapsible on
  click.
- Start the player-detail `Medallas` card collapsed by default.
- Convert all `Estadísticas` cards into collapsed Bootstrap panels where
  opening one statistics card closes the previously opened statistics card.
- Keep `Medallas` independent from the `Estadísticas` collapse group.
- Keep header summaries compact and ellipsis-safe so summary pills do not
  overlap card names.

## Validation Summary

- `pytest paddle/frontend/tests/test_release_orchestrator.py`
- `pytest paddle/frontend/tests/test_release_pr_body_script.py`
- `pytest paddle/frontend/tests/test_players_pages.py`
- `pytest paddle/frontend/tests/test_medals.py`
- `python scripts/validate_governance.py`
- `markdownlint specs/040-faster-release-orchestrator.md`; `MD013` is
  non-blocking.
- `markdownlint specs/038-player-detail-medallas-accordion.md`; `MD013` is
  non-blocking.
- `pytest paddle/frontend/tests/test_players_pages.py` passed.
- `pytest paddle/frontend/tests/test_medals.py` passed.
- `pytest paddle/frontend/tests/test_release_orchestrator.py` passed.
- `pytest paddle/frontend/tests/test_release_pr_body_script.py` passed.
- `python scripts/validate_governance.py` passed.
- `markdownlint specs/040-faster-release-orchestrator.md` passed; `MD013` is
  non-blocking.
- `markdownlint specs/039-player-detail-stats-accordion.md` passed; `MD013` is
  non-blocking.
