# Notification Audit And Hardening

Use for active SDD work only.

## Tracking

- Task ID: `notification-audit-hardening`
- Status: `approved`
- Release tag: `unreleased`

`approved` stays in place until the scoped work is finished and the
development cycle for this spec is being closed. Only then move the spec to
`implemented`.

## Summary

- Run the targeted audit checkpoint required by
  `docs/prds/backend-managed-notifications.md` before notification work closes.
- Address only accepted medium/high-severity findings across the implemented
  notification surfaces.

## Scope

- In:
  - Run `$audit` against notification app views, services, admin behavior, and
    match/ranking integrations.
  - Review auth, authorization, group isolation, ORM/indexing, service
    boundaries, admin idempotency, and duplicate fanout protections.
  - Implement accepted fixes from the audit.
  - Add or adjust tests only for accepted fixes.
- Out:
  - New notification product behavior beyond previously approved specs.
  - Browser Push API, service workers, VAPID, email, SMS, or native push.
  - Release consolidation or marking the source PRD as shipped.
  - Low-severity style churn or speculative refactors.

## Files Allowed to Change

- `paddle/notifications/**`
- `paddle/frontend/forms.py`
- `paddle/frontend/view_modules/matches.py`
- `paddle/frontend/services/ranking.py`
- `paddle/frontend/templates/frontend/base.html`
- `paddle/frontend/tests/**`
- `paddle/games/models.py`
- `paddle/games/tests/**`
- `paddle/americano/tests/**`

## Files Forbidden to Change

- `docs/prds/backend-managed-notifications.md`
- `specs/release-*.md`
- `CHANGELOG.md`
- `BACKLOG.md`

## Execution Notes

- [ ] Depend on specs `040` through `045` being implemented or available as a
      draft implementation for review.
- [ ] Present audit findings first, ordered by severity, with file and line
      references.
- [ ] Ask the user whether to address or discard each medium/high finding
      before fixing it.
- [ ] Do not close implementation specs, consolidate release notes, or mark the
      PRD shipped in this slice.

## Acceptance

- [ ] `$audit` checkpoint is completed for notification views, services, admin,
      and domain integrations.
- [ ] Medium/high findings are either fixed or explicitly accepted as residual
      risk by the user.
- [ ] Accepted fixes preserve current match, ranking, registration, navbar, and
      notification behavior.
- [ ] Duplicate fanout and cross-group leakage protections remain covered by
      tests.
- [ ] No browser or native push scope is introduced.

## Validation

- `python manage.py test notifications`
- `python manage.py test paddle/frontend/tests paddle/games/tests`
- `python manage.py test paddle/americano/tests/test_americano_views.py`
- `python scripts/validate_specs.py`
- `markdownlint-cli2 specs/046-notification-audit-hardening.md`
