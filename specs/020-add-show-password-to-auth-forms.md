# Spec 020: Add Show Password Control to Auth Forms

## Functional Goal

Add a visible show/hide password control to all auth-form password inputs so users can reveal or hide the entered value while logging in, registering, or setting a new password through the reset flow, using an inline Bootstrap icon inside each password field instead of a separate text link/button below the field.

## Scope

### In

- Add a show/hide control for the login password field.
- Add a show/hide control for the registration password and confirm-password fields.
- Add a show/hide control for the password reset new-password and confirm-password fields.
- Implement the behavior with shared frontend code that supports multiple password fields on the same page.
- Keep UI text in Spanish.
- Preserve existing client-side validation and password-confirmation behavior.
- Add or update the smallest relevant tests covering rendered auth templates and password-field toggle hooks.
- Update `CHANGELOG.md` under `## [Unreleased]`.

### Out

- Profile-edit flows that do not currently expose editable password fields.
- Backend authentication logic, password validation rules, or password-reset token handling.
- Broad auth redesign, CSS refactors, or icon-system introduction.
- Changes to non-auth forms or non-password inputs.

## UI/UX Requirements

- Each affected password input must expose a visible inline control inside the field area to toggle visibility.
- The control must use Bootstrap icons to reflect the current state instead of visible text labels.
- Toggling visibility must not clear the field value, break focus handling, or interfere with form submission.
- The implementation must work when a page contains more than one password field.
- Existing form layout should remain substantially unchanged aside from the inline icon control.
- The control must remain accessible through appropriate labels or assistive text even though the visible UI uses icons.

## Backend/Frontend Requirements

- Use shared vanilla JavaScript rather than duplicating per-template toggle logic.
- Keep templates presentation-only; do not add business logic to templates.
- Reuse existing auth templates, Bootstrap icon support already loaded in `base.html`, and existing frontend script-loading patterns where practical.
- Keep the existing password confirmation/validation script compatible with the new visibility toggle behavior.

## Data Rules

- Password input `name`, `id`, and autocomplete attributes must remain unchanged so current form processing continues to work.
- Existing validation messages and required-field behavior must remain intact.

## Reuse Rules

- Prefer one reusable password-visibility script for all affected auth templates.
- Reuse existing auth template structure instead of introducing new partials unless needed to avoid repeated markup.
- Reuse current frontend testing patterns in `paddle/frontend/tests/`.

## Acceptance Criteria

1. The login page renders a visible show/hide control for the password field.
2. The registration form renders visible show/hide controls for both password fields.
3. The password reset confirm page renders visible show/hide controls for both new-password fields when the reset link is valid.
4. The control toggles the associated input between hidden and visible states without changing the entered value.
5. The control icon updates between hidden and visible states to reflect the current visibility state.
6. Existing auth flows and password-confirmation behavior continue to work without regression.
7. `CHANGELOG.md` includes an `Unreleased` entry matching the new auth-form password visibility behavior.

## Manual Functional Checks

1. Open the login page, type a password, and confirm the inline eye icon reveals the text and toggles back to hide it again.
2. Open the registration page, use the inline icon controls on both password fields, and confirm the values remain intact while the form still enforces matching passwords.
3. Submit the registration form with mismatched passwords after toggling visibility and confirm the existing mismatch validation still appears.
4. Open a valid password reset link, toggle visibility on both new-password fields through the inline icons, and confirm the reset form still submits successfully with matching values.
5. Verify the affected pages still render correctly on mobile-width and desktop-width layouts after the inline icon control is added.

## Files Allowed to Change

- `specs/020-add-show-password-to-auth-forms.md`
- `plans/*.md`
- `CHANGELOG.md`
- `paddle/frontend/templates/frontend/login.html`
- `paddle/frontend/templates/frontend/_user_form.html`
- `paddle/frontend/templates/frontend/pass_reset/password_reset_confirm.html`
- `paddle/frontend/static/frontend/js/*.js`
- `paddle/frontend/tests/test_auth.py`
- `paddle/frontend/tests/test_password_reset.py`
- Additional targeted frontend auth tests if needed within `paddle/frontend/tests/`

## Files Forbidden to Change

- `paddle/frontend/forms.py`
- `paddle/frontend/view_modules/**`
- `paddle/config/**`
- `mobile/**`
- `.github/workflows/**`
- Database migrations
- Deprecated API/DRF files
