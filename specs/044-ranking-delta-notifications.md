# Ranking Delta Notifications

Use for active SDD work only.

## Tracking

- Task ID: `ranking-delta-notifications`
- Status: `approved`
- Release tag: `unreleased`

`approved` stays in place until the scoped work is finished and the
development cycle for this spec is being closed. Only then move the spec to
`implemented`.

## Summary

- Generate ranking-position notifications when a linked user's own position
  changes, as required by `docs/prds/backend-managed-notifications.md`.
- Keep ranking logic in backend services and out of templates or JavaScript.

## Scope

- In:
  - Compare before/after ranking positions transactionally around match
    create/delete effects.
  - Generate `ranking_position_up`, `ranking_position_down`,
    `ranking_position_entered`, and `ranking_position_left`.
  - Notify only the linked user whose own ranking position changed.
  - Add integration tests for changed and unchanged ranking scenarios.
- Out:
  - Match-created and match-deleted notification fanout.
  - Player-added and registered-player-linked notifications.
  - UI changes to ranking pages.
  - Tournament notification generation.

## Files Allowed to Change

- `paddle/frontend/services/ranking.py`
- `paddle/frontend/view_modules/matches.py`
- `paddle/frontend/tests/**`
- `paddle/games/models.py`
- `paddle/games/tests/**`
- `paddle/notifications/**`

## Files Forbidden to Change

- `paddle/frontend/templates/frontend/**`
- `paddle/frontend/static/**`
- `paddle/frontend/view_modules/auth_profile.py`
- `paddle/americano/**`

## Execution Notes

- [ ] Depend on `specs/043-match-notification-orchestration.md`.
- [ ] Keep canonical ranking behavior unchanged.
- [ ] Capture ranking state before and after match effects inside the same
      orchestration boundary.
- [ ] Treat `0` as unranked for entered/left classification.
- [ ] Use idempotent `event_key` values for automated ranking events.

## Acceptance

- [ ] A linked user is notified when their own ranking position improves.
- [ ] A linked user is notified when their own ranking position worsens.
- [ ] A linked user is notified when they enter the ranking.
- [ ] A linked user is notified when they leave the ranking.
- [ ] No notification is created for unchanged ranking state.
- [ ] Unlinked players do not receive ranking notifications.
- [ ] Ranking notification logic is not implemented in templates or frontend
      JavaScript.

## Validation

- `python manage.py test notifications paddle/games/tests/test_ranking_positions.py`
- `python manage.py test paddle/frontend/tests/test_ranking.py`
- `python scripts/validate_specs.py`
- `markdownlint-cli2 specs/044-ranking-delta-notifications.md`
