# Multi-Group Support With Hall Of Fame Aggregation

## Tracking

- Task ID: `multi-group-hall-of-fame`
- Status: `shipped`
- Release tag: `v1.9.0`

## Summary

- Replace the single hardcoded club data model with real groups while keeping
  each user/player linked to exactly one group in v1.
- Preserve public browsing through an aggregated `Hall of Fame` context for
  anonymous users.

## Scope

- In:
  - Group model plus group foreign keys for players, matches, and Americano
    tournaments.
  - Legacy data migration into `club moraleja`.
  - Registration updates for joining or creating a group.
  - One unified `Grupo/club` selector in registration with existing groups
    listed first plus a `Crear nuevo grupo/club` option.
  - Conditional registration fields so `new_group_name` appears only for the
    create path and the existing-player selector appears only for a selected
    existing group with players from that same group.
  - Anonymous `crea un grupo` entry reusing the register page and preselecting
    the create-group path.
  - Group-scoped rankings, matches, players, pair rankings, and tournaments.
  - Anonymous `Hall of Fame` aggregate browsing.
  - Release/doc updates needed to require migrations for this change.
- Out:
  - Multi-group membership for one user.
  - Invite codes or approval-based group joins.
  - Separate create-group route outside registration.

## Files Allowed to Change

- `specs/038-multi-group-support-with-hall-of-fame.md`
- `CHANGELOG.md`
- `RELEASE.md`
- `paddle/games/`
- `paddle/frontend/`
- `paddle/americano/`

## Files Forbidden to Change

- Deprecated API/DRF surfaces.
- Deployment credentials or SSH assets.

## Implementation Plan

- [ ] Add the real group model, grouped data migration, and group-scoped model
      constraints.
- [ ] Introduce shared request/group-context helpers for scoped and aggregate
      reads.
- [ ] Update registration, rankings, matches, players, templates, and Hall of
      Fame CTAs for group-aware behavior.
- [ ] Scope Americano list/detail/create flows to the current group or
      aggregate public context.
- [ ] Add migrations, focused tests, changelog, and release-process migration
      guidance.

## Acceptance

- [ ] Existing data is migrated into `club moraleja`.
- [ ] Logged-in users see only their own group data across core app flows.
- [ ] Anonymous users see aggregate `Hall of Fame` data across public pages.
- [ ] Registration supports joining an existing group or creating a new one.
- [ ] Registration uses one `Grupo/club` dropdown with existing groups listed
      before `Crear nuevo grupo/club`.
- [ ] The registration form shows only the dependent field relevant to the
      selected path: `new_group_name` for create, group-scoped `player_id` for
      join.
- [ ] Hall of Fame shows `Inicia sesión`, `regístrate`, and `crea un grupo`,
      with both registration CTAs pointing to the register page.
- [ ] Release guidance explicitly includes running migrations on staging and
      production.

## Validation

- `pytest paddle/frontend/tests/test_ranking.py -q`
- `pytest paddle/frontend/tests/test_views.py -q`
- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `pytest paddle/americano/tests/test_americano_views.py -q`
- `node --test paddle/frontend/tests/js/registerForm.test.js paddle/frontend/tests/js/passwordValidation.test.js`
- Manually confirm anonymous landing page shows aggregate `Hall of Fame`
  branding and the extra `crea un grupo` CTA.
- Manually confirm existing records appear under `club moraleja` after
  migration.
