# Spec 009: User Profile Edit, Email Confirmation, and Account Deletion

## Functional Goal

Allow authenticated users to manage their own account from the app by editing `username` and `email`, requiring duplicated email confirmation in registration and profile edit flows, and deleting their own account from a dedicated confirmation page while preserving any linked `Player` by unlinking it before deleting the `User`, while avoiding JavaScript-driven profile editing.

## Scope

### In

- Allow authenticated users to edit only their own `username` and `email`.
- Keep password changes in the existing separate flow.
- Add duplicated email confirmation fields to registration and profile edit forms.
- Replace the current JavaScript-driven or AJAX-based profile editing path with a standard HTML and Django template form flow that uses as much server-rendered behavior as practical.
- Keep profile editing as a normal server-rendered form submission rather than an AJAX or JavaScript-driven edit flow.
- Reuse the current password confirmation JavaScript behavior only where still justified, prioritizing registration and avoiding JavaScript dependence for profile editing.
- Add normalized email confirmation comparison rules:
  - trim spaces before comparison
  - lowercase before comparison
- Add live client-side validation for registration email confirmation using normalized values:
  - show Bootstrap valid/invalid feedback
  - disable submit until both emails match
- Add server-side validation for profile email confirmation using the same normalized comparison rules.
- Show a Spanish warning that the email is needed for password recovery and should be accessible to the user.
- Allow authenticated users to delete only their own account through a separate confirmation page.
- On deletion:
  - require explicit confirmation
  - unlink any related `Player`
  - delete the Django `User`
  - preserve the `Player` record and existing related history
  - log the user out immediately
  - show a goodbye message
  - redirect to home

### Out

- Password flow redesign.
- Standalone unlink-player functionality outside account deletion.
- Admin or staff user management in the app.
- Django admin customization.
- JavaScript-driven profile editing or AJAX-only profile updates.
- Ranking, match, tournament, or unrelated player business logic changes.
- Email delivery or verification-by-email workflows.
- Model changes unless strictly necessary.

## UI/UX Requirements

- All user-facing text must be in Spanish.
- Use existing Bootstrap 5 patterns already present in the project.
- Reuse the current registration and profile page structure where practical.
- Registration form must include:
  - `email`
  - `confirm_email`
  - warning text explaining email is needed for password recovery
- Profile edit form must allow editing:
  - `username`
  - `email`
- In profile edit, email confirmation is required only when the email value changes.
- If the email is unchanged, email confirmation must not block submission.
- Registration email confirmation UX should mirror the current password confirmation UX as closely as possible:
  - live validation while typing
  - Bootstrap valid/invalid feedback
  - submit disabled until a valid match is reached
- Profile editing must work without JavaScript.
- In profile edit, mismatched changed emails must be handled through normal form validation and rendered Bootstrap error states after submission.
- Account deletion must use a dedicated confirmation page that clearly explains:
  - the account will be deleted
  - the linked player, if any, will be preserved
  - the link between user and player will be removed
  - the action is irreversible

## Backend Requirements

- Keep the current Django structure and reuse existing forms, views, templates, and messages where possible.
- Users may edit only their own account data in the app.
- Users may delete only their own account in the app.
- Staff and superuser management must remain only in Django admin.
- Profile editing must use standard Django form submission and server-side validation rather than JavaScript `PATCH` or AJAX behavior.
- On account deletion, backend logic must:
  - unlink any related `Player`
  - delete the `User`
  - preserve the `Player`
  - log the session out
  - redirect home
  - trigger the goodbye message
- The app must prevent a user from editing another user's data, including direct URL access.
- No business logic may be moved into templates.

## Data Rules

- Editable profile fields in the app:
  - `username`
  - `email`
- Non-editable in this feature:
  - password inside the profile edit form
  - staff and superuser fields
- Email rules:
  - mandatory in registration
  - not unique across users
  - confirmation required via duplicated field
  - compared using normalized trimmed and lowercased values
  - registration may validate the match client-side and must validate it server-side
  - profile edit must validate the match server-side
- Linked `Player` rules:
  - unlink the player before deleting the user
  - keep the player otherwise unchanged and valid
  - allow future relinking to another user
  - leave existing matches, rankings, and tournament history unaffected

## Reuse Rules

- Reuse the current password confirmation JavaScript behavior and structure as much as possible for registration only.
- Do not rely on JavaScript for profile editing or profile email confirmation enforcement.
- Reuse existing templates, views, forms, and message patterns before adding new structures.
- Avoid duplicate validation logic by centralizing normalized email confirmation checks in backend form or view validation for profile editing.

## Acceptance Criteria

1. An authenticated user can edit their own `username`.
2. An authenticated user can edit their own `email`.
3. Registration includes `email` and email confirmation fields.
4. Registration submit remains blocked until both normalized email values match.
5. Profile edit includes email confirmation only when the email is changed, and the backend rejects changed emails whose normalized values do not match.
6. Registration email confirmation shows live Bootstrap valid/invalid feedback while typing.
7. Registration and profile forms display a Spanish warning explaining that email is needed for password recovery and should be accessible by the user.
8. A user cannot edit another user's profile.
9. A user can request deletion only of their own account.
10. Account deletion uses a separate confirmation page.
11. Deleting an account requires explicit confirmation.
12. When a user with a linked player deletes their account:
  - the user is deleted
  - the player is unlinked
  - the player remains valid
  - the user is logged out
  - a goodbye message is shown
  - the app redirects to home
13. Profile editing works without JavaScript-enabled profile submission.
14. No unrelated ranking or player business logic is changed.

## Manual Functional Checks

1. Register a new account with two different emails and verify the form shows invalid feedback and submit stays disabled.
2. Register a new account with emails differing only by spaces or case and verify normalization allows a valid match.
3. Edit the profile `username` without changing the email and verify the form submits successfully without requiring email confirmation.
4. Edit the profile email with a mismatched confirmation and verify the form reloads with Bootstrap validation errors rendered by the server.
5. Attempt to access or edit another user's profile URL directly and verify the action is blocked.
6. Delete a user linked to a player and verify the user is removed, the player remains in the system, the player is no longer linked, the session ends, a goodbye message appears, and the redirect goes to home.

## Test Expectations

- Automated coverage should include:
  - registration rejection or blocking when emails do not match
  - profile update rejection when changed emails do not match
  - successful update of allowed own fields
  - prevention of editing another user's fields
  - own-account deletion unlinking the player while preserving player validity
  - logout and redirect behavior after deletion

## Files Allowed to Change

- registration template files
- profile edit template files
- account deletion confirmation template
- related Django forms
- related Django views
- a small reusable JavaScript file or the existing JavaScript location for registration matching-field validation reuse
- related tests
- URL configuration only if required for the delete flow
- `CHANGELOG.md`

## Files Forbidden to Change

- admin customizations
- ranking or player business logic unrelated to this feature
- unrelated templates, styles, or scripts
- models, unless strictly necessary
