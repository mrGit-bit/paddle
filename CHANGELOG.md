<!-- markdownlint-disable MD024 -->
# Changelog

All notable changes to this project will be documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Since v1.0.4 the project is two products in one repo in GitHub: a Web app and an Android app. To avoid duplication, the repo is versioned as a whole, so the changelog should reflect changes in:

- Web app (Django)
- Android app (Capacitor → Play Store)
- API (Django Rest Framework)
- DevOps: anything that supports running and delivering the web or mobile apps (deployment, infrastructure, automation, CI/CD, server configuration, environment variables and secrets, system dependencies, build pipelines, Android workflow, monitoring/logging, reverse proxies (nginx), runtime configuration or databases configuration.

Every change should belong to one of the following categories: added, changed, updated, upgraded, removed or fixed.

## [1.0.4] – 2025-11-20

### Web

### Mobile

- Added Android app in Google Play Store for close testing

### DevOps

- Updated GitHub Actions workflow for AAB signing
- Added PLAY_STORE_KEYSTORE_* secrets to GitHub Actions
- Upgraded Java version in GitHub Actions from 17 to 21 for Android builds.
- Updated Android SDK to API 35 in the GitHub pipeline.
- Added nginx staging bypass for mobile testing

## [1.0.3] – 2025-10-23

### Added

- Password reset feature added using Django's built-in views and styled like the register template form.
- Password reset emails are sent using Brevo SMTP to the user´s registered email.

### Changed

- Login template styles updated to match register template styles.

### Fixed

- Autocomplete attribute fixed in login and register input templates forms to adapt autofilling.
- Autocapitalize, autocorrect and spellcheck attributes fixed in login and register input templates forms to avoid autocorrections in mobile browsers.

---

## [1.0.2] – 2025-10-09

### Added

- Admin users now see two additional navigation links in the navbar: one to the staging site and one to the Django admin site.
- New template for the about page, including app stadistics, version number and contact email.
- In the registration form, the required fields are now marked with an asterisk.

### Changed

- Version number removed from the footer.
- Updated README.md.

---

## [1.0.1] – 2025-10-02

### Added

- Added the possibility of login using the email.
- Login using username or email is now case insensitive.
- Increased test coverage to over 90%.

### Changed

- Updated UI texts in JS files to Spanish.

### Fixed

- Player name comparison (to avoid creating matches with repeated players) is now case-insensitive.
- Label update in match form fields is now case-insensitive.
- In the registering form, when checking if the user name already exists, the comparison is now case-insensitive and performed not only on users, like before, but also for existing players names. If either exists, registration is blocked.

---

## [1.0.0] – 2025-09-25

### Added

- Version number added to the footer.

### Changed

- Spanish UI for all frontend templates (user-visible text localized to **es-ES**).
- Improved presentation on very small devices (≤ 400px) to enhance readability and tap targets.
