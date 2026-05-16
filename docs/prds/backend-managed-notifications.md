# Backend-Managed In-App Notifications

## Problem Statement

The current navigation badge for new matches is session-based and only reflects
match state that each view manually passes into the template. It is not a
durable notification system, does not provide persistent history, and cannot
support future browser or native push delivery cleanly.

`docs/pre-specs/notifications.md` requests backend-managed match, ranking, and
system notifications, an in-app notification center, a global navbar bell, and
future web push. The first durable product step is to replace the transient
badge with authenticated, group-aware in-app notifications while keeping browser
push delivery out of the initial scope.

## Goals

- Provide a persistent in-app notification history for authenticated users.
- Replace the old session-based match badge with a backend unread count.
- Support group-scoped notification fanout without cross-group leakage.
- Generate notifications for match, ranking, player, registered-player, and
  system/admin events.
- Keep the notification data model compatible with future push delivery.
- Keep backend services responsible for state and templates responsible for
  rendering only.
- Preserve a phase path that can later add web push without reworking the core
  notification domain.

## Non-Goals

- No browser Push API, Service Worker, VAPID, push subscription endpoint, or
  push delivery dependency in v1.
- No native Android or iOS push in v1.
- No email or SMS notifications.
- No tournament notification generation.
- No historical backfill for existing matches, rankings, or session badge state.
- No navbar dropdown feed, live polling, or JavaScript read flow.
- No custom staff notification authoring UI outside Django admin.
- No DRF/API extension.

## Users and Use Cases

- **Registered players** need to see relevant match, ranking, and community
  activity for their own group.
- **Staff users** need to publish system/admin notifications through Django
  admin to one group or all users.
- **Anonymous visitors** should not see private notification counts or access
  notification history.
- **Future mobile or push delivery work** needs stable notification event and
  recipient state to reuse.

## User Stories

- As a registered player, I can open a notification center and review my newest
  notifications first.
- As a registered player, I can see an unread count in the navbar from any page.
- As a registered player, I can mark one notification as read and continue to
  the related page.
- As a registered player, I can mark all of my notifications as read.
- As a match participant, I can be notified when another participant creates or
  deletes one of my matches.
- As a player with a linked account, I can be notified when my own ranking
  position changes.
- As a group member, I can be notified when a new player is added through the
  main match flow or when an existing player becomes linked to a registered
  user.
- As staff, I can create a system notification from Django admin and fan it out
  to a selected group or everyone.

## Product Requirements

- The notification center is available only to authenticated users at a
  dedicated route such as `/notifications/`.
- Notification history is persistent, newest first, paginated, and retained
  indefinitely.
- Opening the notification center does not automatically mark notifications as
  read.
- Single-notification read actions use POST, require CSRF protection, mark only
  the current user's notification row read, and redirect to the event target
  URL.
- The "mark all as read" action uses POST and only affects the current user's
  notifications.
- The navbar bell count comes from a notification context processor and is `0`
  for anonymous users.
- Automated notification copy is generated on the server in Spanish and stored
  at event creation time.
- `system` notifications use staff-authored Spanish title/body from Django
  admin.
- Group-scoped fanout is the default for normal user-facing events.
- Admin system events may target one group or all users.
- No historical notifications are created during migration or deployment.

## Implementation Decisions

- Create a new Django app named `notifications`.
- Add `NotificationEvent` for event type, stored title/body, target URL,
  nullable group, nullable `created_by`, metadata JSON, optional unique
  `event_key`, and timestamps.
- Add `UserNotification` for user, event, nullable `read_at`, reserved nullable
  `delivered_at`, and timestamps.
- Enforce uniqueness for `(user, event)` on `UserNotification`.
- Use notification services for idempotent event creation and recipient fanout.
- Use optional unique `event_key` values for automated events so repeated
  service calls do not duplicate logical notifications.
- Use `get_or_create` or equivalent idempotent logic for recipient rows.
- Avoid Django signals for match and ranking notification generation.
- Add a match-domain orchestration service around match create/delete paths so
  notification generation can compare before/after ranking positions
  transactionally.
- Keep ranking notification logic out of templates and frontend JavaScript.
- Keep the existing `frontend.views` facade thin if notification views are
  exposed through their own app URLs.
- Add a `notifications` context processor for navbar unread count.
- Keep the old session-based match badge out of the final navbar path once
  match notifications cover that behavior.

Automated event defaults:

- `match_created`: notify other registered participants in the match.
- `match_deleted`: notify registered participants in the match except the
  deleter.
- `ranking_position_up`: notify the linked user whose own position improved.
- `ranking_position_down`: notify the linked user whose own position worsened.
- `ranking_position_entered`: notify the linked user who entered the ranking.
- `ranking_position_left`: notify the linked user who left the ranking.
- `player_added`: only for new players created during the main match flow;
  notify same-group registered users except the creator.
- `registered_player_linked`: notify same-group registered users except the
  newly registered user.
- `system`: fan out from Django admin to one group or all users.

## Phase Plan

### Phase 1: Notification Core

Deliverable:

- New `notifications` app with models, migrations, admin registration, event
  type definitions, idempotent event creation, and recipient fanout services.

Dependencies:

- Existing Django auth users and `games.Group` ownership.

Validation focus:

- Model constraints, idempotency, admin system event fanout, and group/user
  recipient selection.

Rollout concern:

- Schema changes must be safe on SQLite development and Oracle production.
  Because v1 does not backfill, rollback can leave empty or unused tables
  without changing existing match behavior.

### Phase 2: In-App UX

Deliverable:

- Authenticated notification center, POST read actions, navbar context
  processor, bell rendering, and removal of old session badge rendering from
  the navbar.

Dependencies:

- Phase 1 models and recipient rows.

Validation focus:

- Auth access, CSRF-protected read actions, pagination, unread counts, and
  template rendering.

Rollout concern:

- Users may initially see no notifications until new events occur. This is
  expected because historical backfill is out of scope.

### Phase 3: Domain Integration

Deliverable:

- Match create/delete orchestration, ranking-delta notification generation,
  `player_added` generation from the main match flow, and
  `registered_player_linked` generation from the registration/linking flow.

Dependencies:

- Phase 1 services and Phase 2 navbar/page surfaces.

Validation focus:

- Correct recipients, actor exclusion, group isolation, before/after ranking
  comparisons, idempotency, and no tournament notification generation.

Rollout concern:

- Match and ranking flows are user-facing core behavior, so implementation must
  keep existing match creation, deletion, ranking recalculation, and redirects
  intact.

### Phase 4: Audit and Hardening

Deliverable:

- Targeted `$audit` checkpoint plus any accepted fixes before implementation
  specs close.

Dependencies:

- Draft implementation across the notification app, views, templates, admin,
  and match/ranking integrations.

Validation focus:

- Auth and authorization, group isolation, ORM/indexing, service boundaries,
  admin idempotency, and duplicate fanout protections.

Rollout concern:

- Audit findings should be addressed before release closure unless the user
  explicitly accepts the residual risk.

## Approved Spec Breakdown

The approved vertical slices are implementation traceability for this PRD. They
do not replace the phase plan or mark the PRD as shipped.

### Spec 040: Notification Core Domain

- File: `specs/040-notification-core-domain.md`
- Type: `HITL`
- Dependencies/blockers: requires human migration approval before
  implementation starts.
- PRD coverage: notification app, durable event and recipient models, event
  type definitions, idempotent services, admin system fanout, group/user
  recipient selection, and no historical backfill.
- Validation focus: model constraints, idempotency, group-scoped fanout,
  admin fanout, migration dry-run, and notification-domain tests.

### Spec 041: In-App Notification Center

- File: `specs/041-in-app-notification-center.md`
- Type: `AFK`
- Dependencies/blockers: depends on Spec 040 models and recipient rows.
- PRD coverage: authenticated notification center, newest-first paginated
  history, POST-only single-read action, POST-only mark-all action, current-user
  isolation, and no automatic read on page open.
- Validation focus: auth access, anonymous redirects, pagination, read state,
  redirects, current-user isolation, and manual center rendering.

### Spec 042: Navbar Notification Bell

- File: `specs/042-navbar-notification-bell.md`
- Type: `AFK`
- Dependencies/blockers: depends on Specs 040 and 041.
- PRD coverage: unread-count context processor, anonymous zero state,
  authenticated bell/link, server-backed navbar state, and removal of the old
  session-based match badge from the final navbar path.
- Validation focus: unread count tests, anonymous zero-state tests, base
  template rendering, and manual anonymous/authenticated navbar checks.

### Spec 043: Match Notification Orchestration

- File: `specs/043-match-notification-orchestration.md`
- Type: `HITL`
- Dependencies/blockers: depends on Specs 040 through 042 and must resolve the
  deleted-match target URL decision before implementation starts.
- PRD coverage: match create/delete orchestration, `match_created`,
  `match_deleted`, registered participant filtering, actor/deleter exclusion,
  group isolation, idempotency, and no historical generation.
- Validation focus: match create/delete integration tests, registered
  participant filtering, group isolation, idempotency, existing redirect/message
  preservation, and manual match create/delete check.

### Spec 044: Ranking Delta Notifications

- File: `specs/044-ranking-delta-notifications.md`
- Type: `AFK`
- Dependencies/blockers: depends on Spec 043.
- PRD coverage: transactional before/after ranking comparison,
  `ranking_position_up`, `ranking_position_down`, `ranking_position_entered`,
  `ranking_position_left`, linked-user-only delivery, unchanged-state
  suppression, and backend-only ranking notification logic.
- Validation focus: ranking delta tests for improved, worsened, entered, left,
  unchanged, and unlinked states plus existing ranking behavior tests.

### Spec 045: Player Lifecycle Notifications

- File: `specs/045-player-lifecycle-notifications.md`
- Type: `AFK`
- Dependencies/blockers: depends on Specs 040 through 042.
- PRD coverage: `player_added` from the main match flow only,
  `registered_player_linked` from registration/linking, actor/new-user
  exclusion, group isolation, no custom staff UI, and no Americano tournament
  generation.
- Validation focus: main match-flow player creation, registration/linking,
  group isolation, Americano non-generation, and lifecycle idempotency.

### Spec 046: Notification Audit And Hardening

- File: `specs/046-notification-audit-hardening.md`
- Type: `HITL`
- Dependencies/blockers: depends on Specs 040 through 045 being implemented or
  available as a draft implementation, and requires user decisions on
  medium/high audit findings before fixing them.
- PRD coverage: targeted audit checkpoint across notification views, services,
  admin, match/ranking integrations, auth, authorization, group isolation,
  ORM/indexing, service boundaries, admin idempotency, and duplicate fanout.
- Validation focus: audit findings with file/line references, accepted fixes,
  notification/frontend/games/Americano test scopes, and no new product or push
  scope.

## Testing Decisions

- Add model and service tests for event creation, `event_key` idempotency,
  recipient uniqueness, group-scoped fanout, and admin system event fanout.
- Add view tests for authenticated access, anonymous redirects, pagination,
  unread styling/state, POST-only read actions, CSRF behavior where practical,
  and current-user isolation.
- Add navbar/context processor tests showing authenticated unread counts and
  anonymous zero state.
- Add integration tests around main match create/delete behavior, including
  actor exclusion, registered participant filtering, and group isolation.
- Add ranking integration tests for up, down, entered, left, and unchanged
  ranking scenarios.
- Add registration/linking flow tests for `registered_player_linked`.
- Add main match-flow tests for `player_added` and explicitly avoid Americano
  tournament-generated player notifications.
- Reuse existing Django view and pytest patterns under `paddle/frontend/tests/`,
  `paddle/games/tests/`, and `paddle/americano/tests/` as appropriate while
  keeping notification-domain tests under the new app.
- Required validation for implementation specs includes the smallest relevant
  pytest scope plus configured linters for touched file types.

## Acceptance Scenarios

- An anonymous user sees no unread bell count and cannot access the notification
  center.
- A registered user sees only their own notifications.
- A user from another group is not notified by group-scoped events.
- Creating a match notifies other registered participants and does not notify
  the creator.
- Deleting a match notifies registered participants except the deleter.
- Ranking notifications are created only when a linked user's own ranking
  position changes.
- A new player created through the main match flow notifies same-group
  registered users except the creator.
- A newly linked registered player notifies same-group registered users except
  the new user.
- A staff-authored system event fans out once to the selected group or all users.
- Repeating an automated event service call with the same `event_key` does not
  duplicate the event or recipient rows.
- Clicking a notification uses POST, marks only that row read for the current
  user, and redirects to the target URL.
- Marking all notifications read only affects the current user's notifications.
- The navbar unread count updates consistently across pages through the context
  processor.
- Existing historical matches do not generate notifications on deployment.
- The targeted `$audit` checkpoint is completed before closure.

## Open Questions

- Exact Spanish body copy for each automated event type remains to be finalized
  in the phase spec or implementation review.
- Exact target URLs for match deletion notifications may use `/matches/` or the
  notification center when the original object no longer exists.
- The final module split for match orchestration may depend on how much current
  `frontend.view_modules.matches` code must move to keep views thin.
- Future web push may need a separate delivery status model instead of using
  only the reserved `delivered_at` field.

## Further Notes

- The starting pre-spec is `docs/pre-specs/notifications.md`; it is scratch
  input, not an active implementation spec.
- Phase specs must be created under `specs/` and approved before implementation
  starts.
- UI text is Spanish. Code, comments, docs, and specs are English.
- Backend owns notification state. Templates render backend-provided state only.
- The DRF/API surface is deprecated and must not be extended.
- A future push phase should build on the event and recipient state from this
  PRD rather than adding independent notification semantics.
