# Navbar Notification Bell

Use for active SDD work only.

## Tracking

- Task ID: `navbar-notification-bell`
- Status: `approved`
- Release tag: `unreleased`

`approved` stays in place until the scoped work is finished and the
development cycle for this spec is being closed. Only then move the spec to
`implemented`.

## Summary

- Replace the session-based match badge with a backend unread notification
  count from `docs/prds/backend-managed-notifications.md`.
- Keep the navbar backed by server state while avoiding notification feed or
  polling behavior.

## Scope

- In:
  - Add a `notifications` context processor for unread count.
  - Return `0` for anonymous users.
  - Render a navbar bell/link to the notification center for authenticated
    users.
  - Remove the old session-based match badge from the final navbar path.
  - Add tests for authenticated unread counts, anonymous zero state, and base
    template rendering.
- Out:
  - Notification center read actions beyond linking to the center.
  - Match, ranking, registration, or player notification generation.
  - Navbar dropdown feed, live polling, JavaScript read flow, or push delivery.

## Files Allowed to Change

- `paddle/config/settings/base.py`
- `paddle/frontend/templates/frontend/base.html`
- `paddle/frontend/tests/**`
- `paddle/notifications/**`

## Files Forbidden to Change

- `paddle/frontend/view_modules/matches.py`
- `paddle/frontend/view_modules/ranking.py`
- `paddle/frontend/view_modules/auth_profile.py`
- `paddle/games/models.py`
- `paddle/americano/**`

## Execution Notes

- [ ] Depend on `specs/040-notification-core-domain.md` and
      `specs/041-in-app-notification-center.md`.
- [ ] Keep backend services responsible for state and templates responsible for
      rendering only.
- [ ] Preserve existing Spanish navbar labels unless the user approves copy
      changes.
- [ ] Do not remove `get_new_match_ids()` from page code in this slice unless
      it is no longer referenced by the final navbar path.

## Acceptance

- [ ] Anonymous users see no private unread notification count.
- [ ] Authenticated users see a bell/link to the notification center.
- [ ] Authenticated unread count comes from `UserNotification.read_at`.
- [ ] The old session-based match badge no longer drives navbar unread state.
- [ ] The unread count renders consistently on pages that do not pass
      `new_matches_number`.

## Validation

- `python manage.py test notifications paddle/frontend/tests`
- `python scripts/validate_specs.py`
- `markdownlint-cli2 specs/042-navbar-notification-bell.md`
- Manual check: navbar on anonymous and authenticated pages.
