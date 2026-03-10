# User Profile Email Confirmation and Account Deletion

## Context

- The current registration and profile flows are implemented in `paddle/frontend/view_modules/auth_profile.py` and rendered through shared templates in `paddle/frontend/templates/frontend/`.
- Registration already includes password confirmation and a small dedicated validator in `paddle/frontend/static/frontend/js/passwordValidation.js`.
- Profile editing currently depends on `paddle/frontend/static/frontend/js/editUserProfile.js` plus a JSON `PATCH` flow that only updates email, which conflicts with the approved direction to favor HTML and Django template form handling over JavaScript for profile editing.
- The profile page at `paddle/frontend/templates/frontend/user.html` and the shared form partial at `paddle/frontend/templates/frontend/_user_form.html` do not yet support editable `username`, server-validated email confirmation, or account deletion.
- The existing frontend test coverage for auth/profile behavior lives mainly in `paddle/frontend/tests/test_views.py` and `paddle/frontend/tests/test_auth.py`.
- Discovery files read first:
  - `specs/009-user-profile-edit-email-confirmation-account-deletion.md`
  - `paddle/frontend/view_modules/auth_profile.py`
  - `paddle/frontend/templates/frontend/_user_form.html`
  - `paddle/frontend/templates/frontend/register.html`
  - `paddle/frontend/templates/frontend/user.html`
  - `paddle/frontend/static/frontend/js/passwordValidation.js`
  - `paddle/frontend/static/frontend/js/editUserProfile.js`
  - `paddle/frontend/urls.py`
  - `paddle/frontend/tests/test_views.py`
  - `paddle/frontend/tests/test_auth.py`

## Spec Reference

- Exact spec file:
  - `specs/009-user-profile-edit-email-confirmation-account-deletion.md`

## Objectives

- Enable authenticated users to edit their own `username` and `email` through standard server-rendered Django forms.
- Add duplicated email confirmation to registration and profile editing, using normalized comparison rules and avoiding JavaScript dependency in the profile flow.
- Replace the current JavaScript/AJAX profile edit path with HTML and Django template form handling.
- Add a dedicated account deletion confirmation flow that unlinks any related `Player`, deletes the `User`, logs out the user, shows a goodbye message, and redirects home.
- Extend automated coverage for registration validation, own-profile updates, access restrictions, and account deletion behavior.
- Record the behavior change in `CHANGELOG.md`.

## Scope

### In

- Update backend auth/profile handling so profile editing uses normal Django form submission and server-side validation.
- Update registration and profile templates/forms to support email confirmation and Spanish password-recovery warning text.
- Replace the current JavaScript-driven profile edit behavior with server-rendered HTML/Django handling.
- Keep or adapt JavaScript only where justified for registration-side confirmation matching.
- Add own-account deletion routing, confirmation template, and backend unlink/delete/logout flow.
- Add or update focused frontend tests for the new behavior.
- Update `CHANGELOG.md` under `## [Unreleased]`.

### Out

- Password reset or password change redesign.
- Admin or staff-facing user management.
- JavaScript-driven profile editing or AJAX-only profile updates.
- Unrelated ranking, match, tournament, or player behavior changes.
- Model changes unless implementation discovery proves them strictly necessary.

## Risks

- Changing `username` for users linked to `Player` records may need coordinated updates so the player remains consistent with current app assumptions.
  - Mitigation: verify the existing user-player naming expectations during implementation and only update the linked `Player` name if the current app behavior requires that consistency.
- Migrating from `PATCH`/AJAX to standard form posts can break current profile tests and user feedback behavior.
  - Mitigation: preserve self-only authorization checks, reuse Django form errors/messages, and add focused tests for GET, POST success, POST validation failure, and forbidden access.
- Reworking the shared form partial can unintentionally affect registration behavior.
  - Mitigation: keep registration and profile conditions explicit in the template and add targeted registration coverage for the new confirmation rules.
- Account deletion can leave the session or linked player in an inconsistent state if unlink and logout ordering is wrong.
  - Mitigation: implement deletion in a dedicated backend path with tests asserting unlinking, user removal, logout, message, and redirect.

## Files Allowed to Change

- `paddle/frontend/view_modules/auth_profile.py`
- `paddle/frontend/templates/frontend/_user_form.html`
- `paddle/frontend/templates/frontend/register.html`
- `paddle/frontend/templates/frontend/user.html`
- `paddle/frontend/templates/frontend/` account-deletion confirmation template if added
- `paddle/frontend/static/frontend/js/passwordValidation.js`
- `paddle/frontend/static/frontend/js/editUserProfile.js`
- `paddle/frontend/urls.py`
- `paddle/frontend/tests/test_views.py`
- `paddle/frontend/tests/test_auth.py`
- additional focused frontend test files if needed
- `CHANGELOG.md`

## Files Forbidden to Change

- Django admin customization files
- ranking, match, tournament, or unrelated player business-logic files
- unrelated templates, styles, or scripts
- model files unless strictly necessary

## Proposed Changes (Step-by-Step by File)

- `paddle/frontend/view_modules/auth_profile.py`
  - Change: replace the current profile `PATCH` update path with standard Django form handling for authenticated self-service updates to `username` and `email`, including server-side normalized email confirmation validation when the email changes.
  - Why: this file currently owns registration and profile behavior and is the correct place to remove the JavaScript/AJAX dependency from profile editing.
  - Notes: preserve self-only authorization checks and implement account deletion here with unlink, logout, message, and redirect behavior.

- `paddle/frontend/templates/frontend/_user_form.html`
  - Change: add the confirm-email field, Spanish email recovery warning text, editable profile inputs, and server-rendered Bootstrap validation states for profile errors.
  - Why: this shared partial already renders both registration and profile forms and is the best place to avoid duplicated markup.
  - Notes: keep logic limited to presentation and backend-provided state.

- `paddle/frontend/templates/frontend/register.html`
  - Change: keep the registration layout and wire the confirmation behavior needed for password and email matching on the registration form.
  - Why: registration still benefits from immediate client-side confirmation feedback.
  - Notes: keep all user-facing text in Spanish.

- `paddle/frontend/templates/frontend/user.html`
  - Change: update the profile page to use normal POST submission, render form errors/messages, and add the account deletion entry point.
  - Why: the current page is built around a JavaScript edit flow and needs to become server-rendered for edits.
  - Notes: preserve the current page structure and Bootstrap style where practical.

- `paddle/frontend/templates/frontend/<account deletion template>.html`
  - Change: add a dedicated confirmation page explaining account deletion, player preservation, unlinking, and irreversibility in Spanish.
  - Why: the spec requires a separate confirmation page before deletion.
  - Notes: keep backend decisions in the view, not in template logic.

- `paddle/frontend/static/frontend/js/passwordValidation.js`
  - Change: review whether this file can be minimally generalized for registration-side matching of password confirmation and email confirmation.
  - Why: reuse is still desirable for registration, but profile editing must not depend on JavaScript.
  - Notes: keep the scope narrow and avoid introducing JS-driven profile behavior.

- `paddle/frontend/static/frontend/js/editUserProfile.js`
  - Change: remove profile-edit responsibilities from this file and either stop using it or reduce it to nothing if the server-rendered form fully replaces it.
  - Why: the approved direction is to amend JavaScript-driven profile editing into a Django/HTML form flow.
  - Notes: implementation should prefer removal from the page over preserving dead behavior.

- `paddle/frontend/urls.py`
  - Change: add route wiring for the dedicated account deletion confirmation/execution flow if current URLs do not already support it.
  - Why: the delete flow needs an explicit user-accessible route.
  - Notes: keep URL naming consistent with the existing frontend namespace style.

- `paddle/frontend/tests/test_views.py`
  - Change: extend view-level coverage for registration email confirmation requirements, successful own-profile updates through POST, validation failures for changed email mismatch, forbidden profile access, and own-account deletion with linked-player unlinking and redirect/message behavior.
  - Why: this file already covers most registration/profile paths and is the best place for end-to-end frontend view assertions.
  - Notes: update existing expectations that currently assume the email-only `PATCH` behavior.

- `paddle/frontend/tests/test_auth.py`
  - Change: add or adjust auth-focused tests if logout or post-deletion session expectations fit better here.
  - Why: session/logout assertions may belong with existing auth coverage.
  - Notes: keep the test scope minimal and targeted.

- `CHANGELOG.md`
  - Change: add an `Unreleased` entry summarizing the self-service profile editing, email confirmation, and account deletion behavior.
  - Why: governance requires changelog updates for behavior changes.
  - Notes: keep the entry aligned with the final implementation only.

## Plan Steps (Execution Order)

- [ ] Step 1: Replace the profile edit backend flow with standard Django form handling for self-only `username` and `email` updates, including normalized server-side email confirmation checks.
- [ ] Step 2: Update shared templates and add the dedicated deletion confirmation template while keeping profile editing server-rendered and all user-facing copy in Spanish.
- [ ] Step 3: Limit JavaScript to registration-side confirmation behavior only, removing or disabling the current profile-edit JavaScript path.
- [ ] Step 4: Add or update focused tests for registration mismatch handling, profile POST update behavior, access restrictions, deletion flow, and session redirect/message outcomes.
- [ ] Step 5: Update `CHANGELOG.md` and run the smallest relevant validation commands.

## Acceptance Criteria (Testable)

- [ ] AC1: Authenticated users can edit their own `username`.
- [ ] AC2: Authenticated users can edit their own `email`.
- [ ] AC3: Registration includes `email` plus email confirmation and blocks submission until normalized values match.
- [ ] AC4: Profile editing uses a standard server-rendered form flow rather than JavaScript or AJAX submission.
- [ ] AC5: Profile editing requires email confirmation only when the normalized email changes and the backend rejects changed emails whose normalized values do not match.
- [ ] AC6: Registration email confirmation shows live Bootstrap valid/invalid feedback while typing.
- [ ] AC7: Registration and profile views show the Spanish warning about email being required for password recovery.
- [ ] AC8: A user cannot edit another user's profile.
- [ ] AC9: A user can access a dedicated own-account deletion confirmation page and must explicitly confirm deletion.
- [ ] AC10: Deleting an account unlinks any related `Player`, preserves the player, deletes the user, logs out the session, shows a goodbye message, and redirects home.

## Validation Commands

- `pytest paddle/frontend/tests/test_views.py -k "register or user or delete"`
- `pytest paddle/frontend/tests/test_auth.py`

## Manual Functional Checks

1. Register a new account with different email values and verify the email confirmation shows invalid feedback and the submit button remains disabled.
2. Register a new account with emails that differ only by spaces or uppercase/lowercase and verify the normalized comparison accepts them as matching.
3. Edit the profile `username` without changing the email and verify the normal HTML form submits successfully without requiring email confirmation.
4. Edit the profile email with a mismatched confirmation and verify the page reloads with server-rendered Bootstrap validation errors.
5. Open another user's profile URL directly while authenticated and verify access is blocked.
6. Delete an account linked to a player and verify the user is removed, the player remains, the link is cleared, the session ends, a goodbye message appears, and the app redirects home.

## Execution Log

- 2026-03-10 17:48 — Spec created.
- 2026-03-10 17:48 — Spec approved.
- 2026-03-10 17:48 — Initial plan created.
- 2026-03-10 17:48 — Spec revised to replace JavaScript-driven profile editing with a server-rendered Django form flow.
- 2026-03-10 17:48 — Revised spec approved.
- 2026-03-10 17:48 — Plan rewritten to align with the revised spec.

## Post-Mortem / Improvements

- What worked well:
  - The rewritten spec made the preferred implementation direction explicit before code changes started.
- What caused friction:
  - The original feature framing allowed JavaScript to expand into profile editing even though the project direction favors server-rendered Django forms there.
- Suggested updates to:
  - `/docs/PROJECT_INSTRUCTIONS.md`: clarify once, centrally, that deprecated API/DRF concerns should not be repeated in feature specs unless a task directly touches that deprecated surface.
  - `/AGENTS.md`: same clarification, so feature specs stay focused on relevant scope.
  - `/plans/TEMPLATE.md`: remove the markdownlint-disable directives and make the template itself compliant with the project Markdown rules.
