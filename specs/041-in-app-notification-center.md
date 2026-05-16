# In-App Notification Center

Use for active SDD work only.

## Tracking

- Task ID: `in-app-notification-center`
- Status: `approved`
- Release tag: `unreleased`

`approved` stays in place until the scoped work is finished and the
development cycle for this spec is being closed. Only then move the spec to
`implemented`.

## Summary

- Add the authenticated notification history and read flows from
  `docs/prds/backend-managed-notifications.md`.
- Let users review persistent notifications without automatically marking them
  read.

## Scope

- In:
  - Add an authenticated notification center route such as `/notifications/`.
  - Render newest-first, paginated notification history for the current user.
  - Add POST-only single-notification read action that redirects to the event
    target URL.
  - Add POST-only "mark all as read" action for the current user.
  - Add tests for auth access, pagination, read state, redirects, and current
    user isolation.
- Out:
  - Navbar bell rendering and unread context processor.
  - Domain event generation from matches, rankings, registration, or players.
  - JavaScript read flows, live polling, or dropdown feeds.
  - Browser Push API, service workers, email, SMS, or native push.

## Files Allowed to Change

- `paddle/config/urls.py`
- `paddle/notifications/**`

## Files Forbidden to Change

- `paddle/frontend/templates/frontend/base.html`
- `paddle/frontend/view_modules/matches.py`
- `paddle/frontend/view_modules/ranking.py`
- `paddle/frontend/view_modules/auth_profile.py`
- `paddle/games/models.py`
- `paddle/americano/**`

## Execution Notes

- [ ] Depend on the models and services from
      `specs/040-notification-core-domain.md`.
- [ ] Use Django auth, CSRF, and POST for all state-changing read actions.
- [ ] Opening the center must not mark notifications as read.
- [ ] Templates render backend-provided notification state only.
- [ ] Visible UI text must be Spanish.

## Acceptance

- [ ] Anonymous users cannot access the notification center.
- [ ] Authenticated users see only their own notifications.
- [ ] Notification history is newest first and paginated.
- [ ] Single read action marks only the current user's row read.
- [ ] Single read action redirects to the event target URL.
- [ ] Mark-all action marks only the current user's notifications read.
- [ ] GET requests do not mutate read state.

## Validation

- `python manage.py test notifications`
- `python scripts/validate_specs.py`
- `markdownlint-cli2 specs/041-in-app-notification-center.md`
- Manual check: anonymous redirect and authenticated center rendering.
