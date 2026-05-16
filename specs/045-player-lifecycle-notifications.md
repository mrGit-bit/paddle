# Player Lifecycle Notifications

Use for active SDD work only.

## Tracking

- Task ID: `player-lifecycle-notifications`
- Status: `approved`
- Release tag: `unreleased`

`approved` stays in place until the scoped work is finished and the
development cycle for this spec is being closed. Only then move the spec to
`implemented`.

## Summary

- Generate player lifecycle notifications from the user-facing flows in
  `docs/prds/backend-managed-notifications.md`.
- Notify same-group users about new match-flow players and newly linked
  registered players while excluding the actor.

## Scope

- In:
  - Generate `player_added` only when a new player is created through the main
    match flow.
  - Generate `registered_player_linked` when registration links an existing
    player to a user.
  - Exclude the creator or newly registered user from fanout.
  - Add tests for match-flow player creation, registration/linking, group
    isolation, and Americano non-generation.
- Out:
  - Match-created, match-deleted, and ranking-position notifications.
  - Staff-authored system events.
  - Custom staff notification authoring UI outside Django admin.
  - Tournament notification generation.

## Files Allowed to Change

- `paddle/frontend/forms.py`
- `paddle/frontend/view_modules/matches.py`
- `paddle/frontend/tests/**`
- `paddle/americano/tests/**`
- `paddle/notifications/**`

## Files Forbidden to Change

- `paddle/americano/models.py`
- `paddle/americano/views.py`
- `paddle/frontend/templates/frontend/base.html`
- `paddle/frontend/view_modules/ranking.py`
- `paddle/games/models.py`

## Execution Notes

- [ ] Depend on `specs/040-notification-core-domain.md`,
      `specs/041-in-app-notification-center.md`, and
      `specs/042-navbar-notification-bell.md`.
- [ ] Keep new-player detection limited to players actually created in the
      main match flow.
- [ ] Keep registration linking inside the existing transaction boundary.
- [ ] Use idempotent `event_key` values for automated lifecycle events.
- [ ] Do not add notification generation to Americano tournament flows.

## Acceptance

- [ ] A new player created through the main match flow notifies same-group
      registered users except the creator.
- [ ] Selecting an existing player in the match flow does not create
      `player_added`.
- [ ] Linking an existing player during registration notifies same-group
      registered users except the new user.
- [ ] Creating a new user/player pair during registration does not create
      `registered_player_linked`.
- [ ] Users outside the group do not receive lifecycle notifications.
- [ ] Americano tournament-generated players do not produce notifications.

## Validation

- `python manage.py test notifications paddle/frontend/tests/test_views.py`
- `python manage.py test paddle/frontend/tests/test_auth.py`
- `python manage.py test paddle/americano/tests/test_americano_views.py`
- `python scripts/validate_specs.py`
- `markdownlint-cli2 specs/045-player-lifecycle-notifications.md`
