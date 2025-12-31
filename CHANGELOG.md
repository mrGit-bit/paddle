<!-- markdownlint-disable MD024 -->
# Changelog

All notable changes to this project will be documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Since v1.0.4 the project is two products in one repo in GitHub: a Web app and an Android app. To avoid duplication, the repo is versioned as a whole, so the changelog should reflect changes in:

- Web app (Django)
- Android app (Capacitor → Play Store)
- API (Django Rest Framework)
- DevOps: anything that supports running and delivering the web or mobile apps.

Every change should belong to one of the following categories: `added`, `changed`, `updated`, `upgraded`, `improved`, `removed` or `fixed`.

## [1.1.0] – 2025-12-30

Tournament management new functionality added.

### Web

- Added a tournament management new functionality:
  - Create tournaments with configurable number of players.
  - Support for registered and non-registered players (auto-creation on submit).  
  - Unlimited number of rounds, created on demand.
  - Per-round match management:
    - Player assignment per team and per match using dropdowns.
    - Editable court number per match (purely cosmetic).
    - Match score input per team.
  - Americano standings table:
    - Wins, points for, points against, and computed point difference.
    - Automatic recomputation after every save (new or edit match edits) or round deletion.
    - Rankings support ties (“1224” style), and tied rows are visually grouped.
  - Permissions model:
    - Tournament visible to everyone.
    - Only logged-in participants, staff and creator can edit rounds and results.
    - Only creators or staff can delete tournaments.
    - Round and tournament deletion with confirmation always.  
  - New Americano navigation menu in navbar:
    - Ongoing tournaments marked with a badge.
    - Finished tournaments listed chronologically.
    - Single entry point to create a new tournament marked with a badge.

- Changed the menu layout to allow anyone to see the matches menu. Anonymous users will be redirected to the login page.

### Mobile

### DevOps

## [1.0.6] – 2025-12-08

Fixed problem of lenghty time loading of the logo image in the navbar.

### Web

- Fixed loading of logo image in the navbar that was blocking the app because it was too big. It is done by resizing and changing the old 1024x1045 to a 96x96 WebP format with a fallback to png format.
- Changed the "forgot password” in user details (incorrectly pointing to the login page) to "change password” (now points to the password reset page `password_reset_form.html`).

### Mobile

### DevOps

- Added `deploy_update.sh` script to automate deployment updates of the staging and production servers.

## [1.0.5] – 2025-11-30

Added logo in base.html, fixed overlapping in android 15 and improved static files with versioned files.

### Web

- Improved base.html:
  - Added the logo image to the navbar, resizing the log and the text for screens less than 360px (iPhone 4/5/SE and Galaxy S9+).
  - Fixed size of the group name in the hall of fame view to avoid truncation in above mentioned devices.
  - Fixed several inconsistencies in the navbar links distribution leading to incorrect right alignment in the desktop view.
  - Added a link for the footer: Clicking anywhere in the footer redirects to the home page. No underlined text or color change for this link.

### Mobile

- Fixed overlapping issue deactivating the edge-to-edge by default of Android 15.

### DevOps

- Added versioned collected static files (with hashed filenames) for serving with NGINX to avoid cache issues with these files and fetch always the latest version.

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
