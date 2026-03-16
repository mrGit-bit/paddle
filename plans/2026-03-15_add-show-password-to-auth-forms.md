# Add Inline Password Toggle Icons to Auth Forms

## Context

- The approved scope is defined in `specs/020-add-show-password-to-auth-forms.md`.
- Password inputs currently appear in the login template, the shared registration form partial, and the password reset confirm template.
- The frontend already uses shared vanilla JavaScript for registration field validation, so the password-visibility behavior should follow the same pattern and remain compatible with the existing confirmation logic.
- `CHANGELOG.md` must be updated under `## [Unreleased]` as part of the implementation.

## Spec Reference

- `specs/020-add-show-password-to-auth-forms.md`

## Objectives

- Add a visible inline Bootstrap-icon show/hide control to every auth-form password input in scope.
- Use one shared reusable frontend script that supports single-password and multi-password pages.
- Preserve current auth flow behavior, form validation, field identifiers, and password confirmation handling.
- Add the smallest relevant regression tests for the rendered icon-toggle hooks and changelog entry.

## Scope

### In

- Update login, registration, and password reset confirm templates to render an inline password-visibility icon control for each in-scope password input.
- Add shared JavaScript to attach toggle behavior via reusable DOM hooks.
- Ensure the existing registration password confirmation script still works with the toggle behavior.
- Add or update focused Django template-response tests for login, registration, and password reset confirm pages.
- Update `CHANGELOG.md`.

### Out

- Backend auth logic, forms, validators, or view modules.
- Password fields outside the approved auth flows.
- Broad layout changes beyond the inline icon integration.
- Mobile wrapper changes.

## Risks

- Bootstrap floating-label markup can be sensitive to inline controls placed inside the field area.
  - Mitigation: use a compact wrapper pattern with positioning classes so labels and validation feedback remain intact.
- Shared JS can accidentally target non-auth password fields if the selectors are too broad.
  - Mitigation: bind behavior only through explicit template-added data attributes.
- Existing registration validation could regress if toggling changes field identity or DOM assumptions.
  - Mitigation: keep existing `id` and `name` attributes unchanged and avoid altering the confirmation script contract.
- Icon-only controls can lose accessibility if the visible state has no accessible name.
  - Mitigation: keep `aria-label`, `aria-pressed`, and a stable control button element for each field.

## Files Allowed to Change

- `CHANGELOG.md`
- `paddle/frontend/templates/frontend/login.html`
- `paddle/frontend/templates/frontend/_user_form.html`
- `paddle/frontend/templates/frontend/pass_reset/password_reset_confirm.html`
- `paddle/frontend/static/frontend/js/*.js`
- `paddle/frontend/tests/test_auth.py`
- `paddle/frontend/tests/test_password_reset.py`
- `plans/2026-03-15_add-show-password-to-auth-forms.md`

## Files Forbidden to Change

- `paddle/frontend/forms.py`
- `paddle/frontend/view_modules/**`
- `paddle/config/**`
- `mobile/**`
- `.github/workflows/**`
- Database migrations

## Proposed Changes (Step-by-Step by File)

- `paddle/frontend/templates/frontend/login.html`
  - Change: replace the current below-field text button with an inline positioned icon button inside the password field container, using Bootstrap icon markup and stable data attributes linking the control to the input.
  - Why: login currently has a single handwritten password field and needs the shared toggle hook.
  - Notes: preserve current label, validation feedback, and autocomplete attributes while adding enough right-side spacing so the icon does not overlap typed text.

- `paddle/frontend/templates/frontend/_user_form.html`
  - Change: replace the current below-field text buttons with the same inline positioned icon control pattern for the registration password and confirm-password inputs rendered by the shared form partial.
  - Why: registration is the only page with two password inputs using form widgets and existing client-side matching logic.
  - Notes: keep the current `password` and `confirm_password` IDs unchanged so `passwordValidation.js` continues to work, and ensure both fields can toggle independently.

- `paddle/frontend/templates/frontend/pass_reset/password_reset_confirm.html`
  - Change: replace the current below-field text buttons with the inline positioned icon control pattern on both reset password inputs when `validlink` is true.
  - Why: password reset is in scope and uses handwritten password inputs similar to login.
  - Notes: invalid-link rendering should remain unchanged.

- `paddle/frontend/static/frontend/js/passwordToggle.js`
  - Change: keep one shared vanilla-JS script that finds explicit toggle hooks, flips each associated input between `password` and `text`, swaps the Bootstrap icon class/state for each button, updates the accessibility label, and keeps behavior independent per field.
  - Why: one dedicated script is the simplest reusable implementation across the three templates.
  - Notes: initialize on `DOMContentLoaded`, no global dependencies, and no changes to field values.

- `paddle/frontend/templates/frontend/register.html`
  - Change: include the new password-toggle script alongside the existing validation script if this page does not already load scripts via the shared base.
  - Why: registration must load both the toggle logic and the current password confirmation logic.
  - Notes: if the new script is instead loaded from a broader template already used by all affected pages, keep inclusion centralized and avoid duplication.

- `paddle/frontend/templates/frontend/base.html` or another existing shared script-loading template
  - Change: load the new password-toggle script from the narrowest shared template that covers all affected pages without impacting unrelated pages unnecessarily.
  - Why: login and password reset confirm also need the script.
  - Notes: choose the minimal existing inclusion point discovered during implementation; do not introduce speculative frontend infrastructure.

- `paddle/frontend/tests/test_auth.py`
  - Change: add or update response-content assertions for login and registration pages so the rendered password inputs expose the agreed inline icon toggle hooks and accessibility attributes.
  - Why: this provides focused regression coverage for the affected auth pages.
  - Notes: keep assertions resilient to minor formatting differences by checking for stable data attributes, icon markers, and accessible labels rather than exact whitespace.

- `paddle/frontend/tests/test_password_reset.py`
  - Change: add assertions that the valid password reset confirm page renders both inline icon password visibility controls while the invalid-link path remains unaffected.
  - Why: this covers the third auth flow in scope.
  - Notes: keep the existing password reset flow test and extend it rather than duplicating setup.

- `CHANGELOG.md`
  - Change: update the existing `## [Unreleased]` bullet so it accurately describes inline icon password visibility controls on auth forms.
  - Why: changelog discipline is mandatory for behavior changes.
  - Notes: keep the wording aligned with the shipped behavior only.

## Plan Steps (Execution Order)

- [ ] Step 1: Replace the current below-field text toggle buttons with a reusable inline icon-toggle markup pattern in the three in-scope auth templates while preserving existing field IDs, labels, and validation messaging.
- [ ] Step 2: Implement and load a shared vanilla-JS password toggle script for the affected pages only.
- [ ] Step 3: Update targeted auth/password reset tests to assert the rendered inline icon controls and unaffected invalid-link path.
- [ ] Step 4: Update `CHANGELOG.md` under `## [Unreleased]` so the entry matches the inline icon behavior.
- [ ] Step 5: Run the smallest relevant pytest scope and verify the changed Markdown files meet repository markdown rules.

## Acceptance Criteria (Testable)

- [ ] AC1: Login renders a visible inline Bootstrap-icon password toggle for the password field.
- [ ] AC2: Registration renders visible inline Bootstrap-icon password toggles for both password fields without breaking current password-match validation.
- [ ] AC3: Password reset confirm renders visible inline Bootstrap-icon password toggles for both password fields only when the link is valid.
- [ ] AC4: The shared script toggles each associated field independently between hidden and visible states and updates the icon state plus accessibility label accordingly.
- [ ] AC5: Existing field IDs, names, autocomplete attributes, and validation messages remain compatible with current auth flows.
- [ ] AC6: `CHANGELOG.md` contains an accurate `Unreleased` entry for this UX change.

## Validation Commands

- `pytest paddle/frontend/tests/test_auth.py paddle/frontend/tests/test_password_reset.py`

## Manual Functional Checks

1. Visit `/login/`, enter a password, and confirm the inline eye icon reveals the value and toggles back to hide it again.
2. Visit `/register/`, toggle both password fields independently through their inline icons, and confirm the values stay intact.
3. Submit `/register/` with mismatched passwords after toggling visibility and confirm the existing mismatch validation still appears.
4. Open a valid password reset link, toggle both new-password fields through the inline icons, and confirm a matching-password submission still succeeds.
5. Open an invalid or expired password reset link and confirm no password-toggle controls are rendered because the password form is not shown.

## Execution Log

- 2026-03-15 21:51 — Spec created.
- 2026-03-15 21:52 — Spec approved.
- 2026-03-15 21:52 — Plan created.
- 2026-03-15 22:06 — Spec updated for inline Bootstrap-icon password toggles.
- 2026-03-15 22:06 — Revised plan created for inline Bootstrap-icon password toggles.

## Post-Mortem / Improvements

- Expected to be none for this localized frontend change.
