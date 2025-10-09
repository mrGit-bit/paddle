# Changelog

All notable changes to this project will be documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
<!-- markdownlint-disable MD024 -->

## [1.0.2] – 2025-10-09

### Added

- Admin users now see two additional navigation links in the navbar: one to the staging site and one to the Django admin site.
- New template for the about page, including app stadistics, version number and contact email.
- In the registration form, the required fields are now marked with an asterisk. 

### Changed

- Version number removed from the footer.
- Updated README.md.

### Fixed

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
