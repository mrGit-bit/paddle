# Notification Core Domain

Use for active SDD work only.

## Tracking

- Task ID: `notification-core-domain`
- Status: `approved`
- Release tag: `unreleased`

`approved` stays in place until the scoped work is finished and the
development cycle for this spec is being closed. Only then move the spec to
`implemented`.

## Summary

- Build the durable backend notification domain from
  `docs/prds/backend-managed-notifications.md`.
- Add persistent notification events, per-user recipient rows, admin system
  fanout, and idempotent services without changing existing match behavior.

## Scope

- In:
  - Create a new Django app named `notifications`.
  - Add `NotificationEvent` and `UserNotification` models and migrations.
  - Add event type definitions for match, ranking, player, registered-player,
    and system/admin events.
  - Add backend services for idempotent event creation and recipient fanout.
  - Register admin surfaces needed for staff-authored `system` events.
  - Add tests for model constraints, idempotency, group/user recipient
    selection, and admin system fanout.
- Out:
  - Notification center pages, navbar bell UI, and read actions.
  - Match, ranking, registration, and player-flow event generation.
  - Browser Push API, service workers, VAPID, email, SMS, or native push.
  - Historical notification backfill.

## Files Allowed to Change

- `paddle/config/settings/base.py`
- `paddle/notifications/**`

## Files Forbidden to Change

- `paddle/frontend/view_modules/matches.py`
- `paddle/frontend/view_modules/ranking.py`
- `paddle/frontend/view_modules/auth_profile.py`
- `paddle/frontend/templates/frontend/base.html`
- `paddle/frontend/urls.py`
- `paddle/config/urls.py`
- `paddle/americano/**`

## Execution Notes

- [ ] Add `notifications` to `INSTALLED_APPS`.
- [ ] Keep schema safe for SQLite development and Oracle production.
- [ ] Store Spanish title/body copy on the event at creation time.
- [ ] Keep `delivered_at` reserved and nullable for future delivery work.
- [ ] Use optional unique `event_key` values for automated event idempotency.
- [ ] Use idempotent recipient creation so repeated fanout does not duplicate
      `(user, event)` rows.
- [ ] Do not use Django signals for this notification domain.
- [ ] Require human migration approval before implementation starts.

## Acceptance

- [ ] `NotificationEvent` stores event type, title, body, target URL, nullable
      group, nullable `created_by`, metadata JSON, optional unique
      `event_key`, and timestamps.
- [ ] `UserNotification` stores user, event, nullable `read_at`, nullable
      `delivered_at`, and timestamps.
- [ ] `(user, event)` is unique for `UserNotification`.
- [ ] Repeating an automated service call with the same `event_key` does not
      duplicate event or recipient rows.
- [ ] Group-scoped fanout never creates rows for users outside the target
      group.
- [ ] Staff-authored system events can fan out once to a selected group or all
      users through Django admin.
- [ ] No historical notifications are created by migration or deployment.

## Validation

- `python manage.py makemigrations --check --dry-run`
- `python manage.py test notifications`
- `python scripts/validate_specs.py`
- `markdownlint-cli2 specs/040-notification-core-domain.md`
