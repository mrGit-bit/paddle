# Since Last Merge Code Audit

## Summary

- Scope: repository code audit since last merge commit
  `d1f1e3b9ac634a60c2524dea93c5ecc561b05bb3`
  (`merge(release): backmerge main into develop after v1.9.4`).
- Audited target: changed Django view, service, model, URL, template, and test
  surface in `paddle/americano`, `paddle/frontend`, and `paddle/games`,
  including current untracked Medallero implementation files.
- Audit date: 2026-05-06.
- Reviewer: Codex using `$audit`.
- Verification: static source review and cascade to related tests. Runtime
  profiling was not performed. Presentation-only risk is tracked separately in
  `.codex/audits/2026-05-06_medallero-hof-player-detail_template-presentation_audit.md`.

## View Audit Report

No medium/high view findings surfaced.

- Reviewed `paddle/americano/views.py` and
  `paddle/frontend/templates/frontend/americano/americano_detail.html` for the
  POST-only new-round change. The view now uses `@require_POST`, keeps the
  existing edit authorization check, and the template submits through a
  CSRF-protected form.
- Reviewed `paddle/frontend/view_modules/ranking.py`,
  `paddle/frontend/urls.py`, `paddle/frontend/views.py`,
  `paddle/frontend/templates/frontend/base.html`, and
  `paddle/frontend/templates/frontend/medallero.html` for the public Medallero
  route. The route is intentionally public, uses the existing group-context
  helper, and keeps medal assignment out of the template.
- Reviewed changed tests in `paddle/americano/tests/test_americano_views.py`,
  `paddle/frontend/tests/test_views.py`, `paddle/frontend/tests/test_players_pages.py`,
  and `paddle/frontend/tests/test_medals.py`; the changed view behavior has
  coverage for POST-only round creation, ranking batching, new-match ID loading,
  Medallero public rendering, navbar placement, and group context.

## Architecture Review Report

No medium/high architecture findings surfaced.

- Reviewed `paddle/games/models.py` for the match-save side-effect change. The
  new validation-before-revert order and `transaction.atomic()` wrapper address
  the prior repository-code audit finding without introducing a new app-boundary
  issue.
- Reviewed `paddle/frontend/services/ranking.py` and
  `paddle/frontend/view_modules/players.py` for batched scope ranking reuse.
  Ranking policy remains centralized in `frontend.services.ranking`, and player
  detail now consumes the batched helper instead of duplicating ranking scans.
- Reviewed `paddle/frontend/medals/config.py` and
  `paddle/frontend/services/medals.py` for the new medal-board service. Medal
  assignment is backend-owned, metadata is centralized, and the Medallero
  template only renders prepared rows.

## Performance Audit Report

No medium/high performance findings surfaced.

- Reviewed `paddle/frontend/services/ranking.py`; `compute_rankings_for_scopes()`
  consolidates multi-scope ranking work into one match scan and one population
  load per group, preserving the previous single-scope `compute_ranking()`
  contract.
- Reviewed `paddle/frontend/view_modules/common.py`; `get_new_match_ids()` now
  filters seen IDs and reads `values_list("id", flat=True)` instead of loading
  full `Match` objects.
- Reviewed `paddle/frontend/services/medals.py`; Medallero computes medals from
  the batched ranking helper rather than running one independent ranking query
  per medal scope.

## Open Questions

None.
