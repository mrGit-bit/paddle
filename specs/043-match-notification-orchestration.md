# Match Notification Orchestration

Use for active SDD work only.

## Tracking

- Task ID: `match-notification-orchestration`
- Status: `approved`
- Release tag: `unreleased`

`approved` stays in place until the scoped work is finished and the
development cycle for this spec is being closed. Only then move the spec to
`implemented`.

## Summary

- Generate match-created and match-deleted notifications from the match domain
  described in `docs/prds/backend-managed-notifications.md`.
- Preserve current match creation, deletion, messages, ranking recalculation,
  and redirects.

## Scope

- In:
  - Add a match-domain orchestration service around match create/delete paths.
  - Generate `match_created` notifications for other registered participants.
  - Generate `match_deleted` notifications for registered participants except
    the deleter.
  - Preserve group isolation and actor/deleter exclusion.
  - Add integration tests around main match create/delete behavior.
- Out:
  - Ranking-position delta notifications.
  - Player-added notifications for new players from the match form.
  - Notification center, navbar, admin system events, and push delivery.
  - Tournament notification generation.

## Files Allowed to Change

- `paddle/frontend/view_modules/matches.py`
- `paddle/frontend/tests/**`
- `paddle/games/models.py`
- `paddle/games/tests/**`
- `paddle/notifications/**`

## Files Forbidden to Change

- `paddle/frontend/view_modules/ranking.py`
- `paddle/frontend/view_modules/auth_profile.py`
- `paddle/frontend/templates/frontend/base.html`
- `paddle/americano/**`

## Execution Notes

- [ ] Depend on `specs/040-notification-core-domain.md`,
      `specs/041-in-app-notification-center.md`, and
      `specs/042-navbar-notification-bell.md`.
- [ ] Resolve the HITL target URL decision for deleted matches before
      implementation starts.
- [ ] Prefer explicit service calls over Django signals.
- [ ] Keep current duplicate-match, locked-match, auth, and redirect behavior.
- [ ] Use idempotent `event_key` values for automated match events.

## Acceptance

- [ ] Creating a match notifies registered participants other than the creator.
- [ ] Deleting a match notifies registered participants except the deleter.
- [ ] Unregistered players do not receive notification rows.
- [ ] Users outside the match group do not receive notification rows.
- [ ] Repeating the automated event service with the same logical event does
      not duplicate notifications.
- [ ] Existing historical matches do not generate notifications on deployment.
- [ ] Current match page messages and redirects remain intact.

## Validation

- `python manage.py test notifications paddle/frontend/tests/test_views.py`
- `python manage.py test paddle/games/tests`
- `python scripts/validate_specs.py`
- `markdownlint-cli2 specs/043-match-notification-orchestration.md`
- Manual check: create and delete a match as a registered participant.
