<!-- markdownlint-disable MD024 -->

# Changelog

All notable changes to this repo are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
The repo version covers the web app, mobile wrapper, and release/devops work.
Use stable domain prefixes within release bullets when a section mixes work
types, for example `UI/UX`, `Governance`, `Release`, `Backend`, `Data`,
`Mobile`, `Tests`, or `Docs`.

## [Unreleased]

- `UI/UX`: Added pair-ranking medals to the medallero so top pairs, parejas
  catastróficas, and highlighted catastrophic pairs award medals to both
  players without mixing the pairs scope into individual ranking batches.
- `UI/UX`: Moved the player-detail `Pulsa para detalles` helper into the
  `Estadísticas` heading row and formatted ranking pills as `1 / 75%` without
  brackets.
- `UI/UX`: Linked medallero cards to the selected player's scope-specific
  ranking page and kept the player-detail medal cards clickable to the same
  destination.
- `UI/UX`: Limited player-detail `Contendientes` nemesis and victim cards to
  opponents with at least five shared matches before applying the existing
  head-to-head efficiency thresholds.
- `UI/UX`: Added a player-detail `Medallas` section before statistics, reusing
  medallero cards with the selected player's medal card expanded by default
  and collapsible on click.
- `UI/UX`: Converted player-detail statistics cards into a Bootstrap accordion
  with compact header summaries, collapsed defaults, and truncation-safe pills.
- `Governance`: Added the `$context-budget-review` skill for low-context
  governance and workflow reviews, with a 40% warning threshold and 60%
  conversation budget, and compacted the Django view audit skill to defer
  checklist and report details to references.
- `Governance`: Added the `$debug` skill and Codex routing entry for
  repeatable bug reproduction, hypothesis testing, fixes, and regression
  coverage.
- `Release`: Clarified that release requests only authorize deployment through
  staging, and that production promotion must wait for explicit approval after
  staging manual checks or the documented staging-approval resume command.
- `Release`: Added release-session context guidance to summarize polling,
  deploy logs, validation output, and diffs instead of filling the conversation
  with full command streams; `/clear` remains an optional post-cycle
  suggestion.

## [1.10.1] - 2026-05-07

- `Dependencies`: Updated vulnerable Python and mobile npm dependencies reported
  by Dependabot, kept patched minimum Python dependency floors in
  `requirements.in`, and removed unused PostgreSQL, WhiteNoise, and
  `dj-database-url` packages while retaining Gunicorn for staging and
  production.
- `Governance`: Resolved repository-governance audit findings by tightening
  router wording, consolidating backlog and release ownership, removing the
  obsolete Codex release-prep workflow, and loosening active spec execution
  notes.
- `Governance`: Added the `$write-a-skill` skill for adapting and maintaining
  repository-local Codex skills with concise metadata, progressive disclosure,
  and validation guidance.
- `Release`: Updated release automation to fall back from required PR checks
  to visible PR checks when branch protection reports no required checks, and
  made release back-merges independent of local GPG signing keys.
- `Release`: Moved release-prep changelog editing into a tested helper that
  preserves Markdown spacing between generated version headers and bullets.

## [1.10.0] - 2026-05-06

- `UI/UX`: Added a public `Medallero` navbar page with backend-owned medal
  assignment, compact collapsed player rows, medal summary icons, and expanded
  three-column medal cards.
- `Governance`: Added Medallero presentation and since-last-merge code audit
  reports for the completed development cycle.
- `Governance`: Added the `$test-design` skill to steer tests toward
  behavior, accessibility, structure, and style contracts instead of brittle
  implementation or incidental-copy assertions.
- `Governance`: Added concise Markdown guidance for Codex-created docs and
  skills.
- `Governance`: Added the `$sdd-grill-me` planning skill for SDD-specific
  plan pressure-tests before specs or implementation.
- `Governance`: Updated cycle-closure reports to suggest `/clear` after a
  completed cycle.
- `Governance`: Reorganized ChatGPT and Codex governance into lightweight
  router documents backed by workflow skills for progressive context
  disclosure.
- `Backend`: Made Americano new-round creation POST-only and protected the
  empty-tournament action with a CSRF form.
- `Backend`: Kept match update side effects transactional so invalid updates
  preserve existing player links and rankings.
- `Performance`: Batched player-detail ranking scope computation and reduced
  new-match badge lookups to ID-only queries.

## [1.9.4] - 2026-04-26

- `UI/UX`: Tightened player-detail `Contendientes` cards to require a strict
  head-to-head rate above 60% and updated the visible labels to the shorter
  `Némesis` and `Víctimas` threshold wording.

## [1.9.3] - 2026-04-22

- `Governance`: Aligned template presentation audits with the repository audit
  lifecycle and clarified routing between focused, Django view, and governance
  markdown audits.
- `UI/UX`: Prevented inactive player-detail efficiency selector cards from
  activating or changing visible trend rows.
- `UI/UX`: Added player-detail Contendientes cards with individual
  head-to-head nemesis and victim ratios plus disabled no-data wheels.

## [1.9.2] - 2026-04-21

- `UI/UX`: Reworked player detail statistics into a grouped `Estadísticas`
  area with shadowed insight cards for rankings, recent form, partners, and
  rival pairs.
- `UI/UX`: Improved player detail insight cards with scoped ranking-efficiency
  legends, centered wheels, compact partner/rival names, cumulative recent-form
  charting, qualitative balance labels, and number-first trend labels for
  small screens.
- `Governance`: Added template presentation audit guidance and tightened UI
  and release-consolidation rules so shared styles, cascade effects, and final
  release summaries stay reviewable.

## [1.9.1] - 2026-04-16

- `UI/UX`: Reworked player detail statistics with scoped efficiency wheels,
  recent-trend cards, ranking progress bars, and clearer partner-frequency
  versus partner-efficiency displays.
- `UI/UX`: Added partner efficiency cards with compact win/match records and
  kept authenticated users defaulted to their own linked player detail.
- `UI/UX`: Cleaned ranking sort icons on small screens and simplified anonymous
  player selector labels.
- `Governance`: Tightened ChatGPT pre-spec handoffs, ignored pre-spec storage,
  closure commits, and instruction duplication checks.
- `Docs`: Added the Django development server helper prompt.

## [1.9.0] - 2026-04-07

### Changed

- `Data`: Added group ownership for players, matches, and Americano
  tournaments, migrated legacy records into `club moraleja`, and preserved
  global case-insensitive player-name uniqueness.
- `UI/UX`: Scoped authenticated rankings, matches, players, pair rankings, and
  tournaments to the user's group while preserving anonymous aggregate browsing
  through the public `Hall of Fame`.
- `UI/UX`: Updated registration to require a group choice, support group
  creation or joining, validate email/group errors consistently, and add a
  `crea un grupo` Hall of Fame CTA.
- `Release`: Hardened release automation with required local validation,
  staging/production migrations, version checks, tracked deploy steps, and
  environment-specific manual checks.
- `Governance`: Simplified SDD to one approved active-work spec, consolidated
  shipped specs into compact release records, clarified loose-spec lifecycle
  states, and required sequential closure steps.
- `Docs`: Added the multi-group and Hall of Fame rollout manual checklist.

## [1.8.1] - 2026-04-01

### Changed

- `UI/UX`: `Parejas del siglo` y `Parejas catastróficas` now require at least
  5 matches instead of 3 before a pair is eligible for the rate-based tables.

## [1.8.0] - 2026-04-01

### Changed

- `UI/UX`: Added a public `Parejas` navbar page with top pair rankings by
  victories plus best and worst win-rate tables for pairs with at least 3
  matches, reusing the ranking-table visual style with both player names shown
  on separate lines in one cell.
- `Release`: Release automation now verifies the requested app version on staging and
  production after each remote deploy, and the tracked SSH update-command
  template now terminates cleanly instead of dropping into an interactive
  shell.
- `Governance`: Governance now caps `docs/PROJECT_INSTRUCTIONS.md` with an explicit
  character budget and moves overflow detail to higher-context docs so the file
  remains loadable in ChatGPT Project instructions.
- `Governance`: Changelog entries now use stable domain prefixes so mixed
  releases stay easier to scan.

### Fixed

- `Backend`: Registration now allows linking an existing unregistered player
  when the submitted username matches that selected player's current name, and
  duplicate-name rejections now show the correct username guidance instead of
  falling through to the email-mismatch path.

## [1.7.0] - 2026-03-31

### Changed

- Release docs and governance now treat
  `python scripts/release_orchestrator.py <version>` as the primary release
  entrypoint, with `/prompts:release <version>` documented only as an optional
  wrapper.
- Governance now lets clearly minor doc/governance/repository-guidance changes
  use the reduced-process path without an extra confirmation turn.
- Governance now treats direct user closure commands such as `close cycle` or
  `close specification` as immediate authorization to stage, commit, and push
  without an extra confirmation turn.
- Release consolidation governance now also requires reviewing the release
  changelog section and keeping it as a simple, light summary of shipped
  changes.
- Loose non-release specs/plans now default to `Release tag: unreleased`; the
  release flow now consolidates only loose files explicitly marked with the
  shipped `vX.Y.Z`.
- Folded non-shipped `1.6.0` history into `1.6.1` and cleared the remaining
  loose historical spec/plan files.
- Reduced Markdown verbosity across governance docs, active specs/plans,
  consolidated release files, and recent changelog entries.
- Match entry and deletion now use a 30-day window: results older than 30 days
  are treated as automatically approved, cannot be deleted, and cannot be
  added retroactively.
- Governance now requires explicitly evaluating `/review` and `audit` on
  non-trivial work and stating why a checkpoint is skipped.
- Governance now requires review/audit findings to be limited to medium/high
  severity and to be explicitly accepted for action or discarded by the user
  before implementation continues.
- Ranking pages now support page-local sorting by position, wins, matches, and
  win rate without changing canonical ranking or pagination behavior.
- Player detail pages now show the top 3 habitual partners, ordered by matches
  together using the existing partner tie-break rules.
- Governance now makes `/plan` more question-heavy by default after exploration
  for non-trivial planning work.
- README now aligns its reduced-process guidance with the higher-authority
  governance docs.

## [1.6.1] - 2026-03-27

### Added

- `/prompts:release` orchestration and its checked-in prompt contract.
- `governance-markdown-auditor` plus repository audit export support.

### Changed

- Release operations now use repo-local SSH assets and clearer Codespaces `gh`
  auth guidance.
- `RELEASE.md` now documents the command-driven flow, fallback scripts, and
  `/prompts:release <version>` syntax.
- Governance now treats `/review` and `audit` as explicit workflow tools,
  allows the reduced-process path for narrow doc work, and requires live
  verification for external-tool assumptions.
- Governance ownership is tighter: compact authority split, closure-owned
  backlog reconciliation, explicit spec/plan tracking metadata, and rollover of
  non-shipped releases into the next shipped release.

### Fixed

- `/prompts:release` now handles SSH key permissions, `gh` auth fallback,
  workflow-run matching, no-check PRs, partial failure reporting, and
  release-tag consolidation more reliably.
- The release-orchestrator pytest suite now uses `config.test_settings` by
  default.

## [1.5.0] - 2026-03-16

### Changed

- Updated governance and repository guidance so active development continues using one spec file and one plan file per SDD, while completed released deployments are consolidated only after a successful tagged release back-merge from `main` to `develop`, and the first Codex task after that back-merge must perform any pending consolidation before new SDD work starts.
- Tightened post-release consolidation governance so already-consolidated released deployments cannot leave released per-SDD spec/plan files behind as loose files outside the applicable release-level consolidated files.
- Added post-release consolidated deployment spec/plan files for traced released batches and removed the superseded per-SDD markdown files they now replace.
- Updated governance workflow so Codex may suggest spec-focused pre-audits and scoped post-implementation audits only when needed, and must state the reason whenever suggesting either audit.
- Updated governance so Codex must also briefly explain when a spec-focused pre-audit or post-implementation audit is not needed, not only when one is suggested.
- Clarified governance so closing a development cycle requires processing all remaining requested-work changes until `git status --short` is clean after staging, committing, and pushing.
- Hardened account forms so registration and profile updates reject case-insensitive duplicate emails while preserving the current username-or-email login flow.
- Removed the inactive PATCH-based profile-edit helper and its unused legacy JavaScript path, keeping `frontend.views` aligned with the active server-rendered profile flow.
- Added focused auth regressions and query-count visibility tests for registration, profile, and authenticated match-list flows.
- Added inline Bootstrap eye-icon password visibility controls to auth-form password fields on login, registration, and password reset screens.

### Fixed

- Reduced duplicate query work in registration, profile stats rendering, and authenticated match-list loading by reusing the registration queryset, computing player stats once per request path, and eager-loading related match players for the paginated lists.

## [1.4.1] - 2026-03-14

### Changed

- Refreshed `README.md` so it reflects the latest documented project state and serves as a practical repository guide for Codex CLI agents.
- Updated governance in `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md` so Markdown line-length findings (`MD013`) are non-blocking and long lines should not be wrapped only for line-length linting.
- Updated governance in `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md` so contributors check `README.md` when repository context is needed and keep it updated when README-covered guidance or project context changes.

### Fixed

- Fixed `.github/workflows/release.yml` release tagging on GitHub Actions by configuring a valid Git identity and validating that `paddle/config/__init__.py` matches the latest released version in `CHANGELOG.md` before extracting release notes.

## [1.4.0] - 2026-03-12

### Changed

- Simplified `docs/PROJECT_INSTRUCTIONS.md` to fit ChatGPT Project instruction size constraints while preserving the same governance rules and synchronized version metadata with `AGENTS.md`.
- Clarified in `docs/PROJECT_INSTRUCTIONS.md` that it must remain under 8000 characters and updated `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md` so handoff now asks whether to continue developing before any commit/push/closure step.
- Updated `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md` so recommended commit messages must summarize the full accumulated uncommitted change set since the last commit, rephrased when multiple development steps are grouped into one commit.
- Reworked account management so profile editing uses standard Django form submissions for `username` and `email`, registration requires confirmed email with live matching feedback, and account deletion happens through a dedicated confirmation page that unlinks any related `Player` before deleting the user.
- Clarified in `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md` that deprecated API or DRF constraints must be enforced centrally in governance and should not be repeated in feature specs unless a task directly touches that deprecated surface.

### Fixed

- Fixed `.github/workflows/release.yml` release-notes extraction by replacing reserved `awk` variable usage that caused GitHub Actions parser errors.

### Changed

- Updated `.github/workflows/release.yml` to derive release version/tag from `paddle/config/__init__.py` (`__version__`) instead of changelog header parsing.
- Updated `RELEASE.md` to document CI jobs in the release flow and clarify when `scripts/tag_release.sh` and `scripts/backmerge_main_to_develop.sh` are manual fallback tools.

## [1.3.1] - 2026-03-09

### Fixed

- Fixed `.github/workflows/release.yml` release-notes extraction by replacing reserved `awk` variable usage that caused GitHub Actions parser errors.
- Updated about-page version test to assert the configured version label dynamically instead of a hardcoded release number.
- Fixed `release-prep-no-ai` workflow commit staging so release PRs include both `CHANGELOG.md` and `paddle/config/__init__.py` version bump changes.

### Changed

- Updated release PR template to align checklist and CI gates with `.github/workflows/ci.yml` and `.github/workflows/release-prep-no-ai.yml`.
- Configured Codespaces/Web VS Code workspace port settings so port `8000` defaults to public visibility on load.
- Updated `release-prep-no-ai.yml` to build PR bodies from `.github/PULL_REQUEST_TEMPLATE/release.md` and inject the corresponding `CHANGELOG.md` release section as the summary.
- Updated governance instructions in `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md` to require an explicit post-commit-message question about staging changes, committing, and pushing to the remote branch.
- Refactored `frontend.views` into internal domain modules (`view_modules`) while keeping `frontend.views` as a compatibility facade with unchanged route behavior.
- Updated governance flow to enforce mandatory stop-and-review gates immediately after spec creation and plan creation.
- Strengthened Markdown governance rules to require markdownlint-compliant authoring/checklist for every new or modified Markdown file.
- Aligned ranking source of truth by sharing one canonical ranking policy between persisted `Player.ranking_position` and frontend ranking computation (same ordering, tie keys, and competition-style positions), with zero-match players persisted as unranked (`0`).
- Harmonized frontend player-participation match queries by centralizing shared queryset construction across matches, players, and new-match detection helpers (behavior preserved).
- Hardened pytest database safety by using tracked `config.settings.dev` in pytest and adding a fail-fast guard that aborts test runs if they target development `db.sqlite3`.
- Updated Americano tournament creation to capture gender for newly added non-registered players (male/female inputs) and persist it on player creation.

### Added

- Added player insights on `/players/<id>/` with trend (últimos 5/10/total), most frequent partner, and top 3 most frequent rival pairs.
- Added governance synchronization rules requiring version/date updates in `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` on every Project Instructions change.

### Removed

- Removed deprecated Django REST Framework API surface:
  - URL endpoints: `/api/games/`, `/api/users/`, `/api-auth/`
  - API-specific modules and API-only tests in `games` and `users`
  - DRF runtime/settings/dependency wiring no longer used by the supported web product

## [1.3.0] - 2026-02-20

### Added

- Added `favicon.ico`.
- Added public player pages:
  - `/players/` (player selector)
  - `/players/<id>/` (player profile with scoped stats and match history).
- Added clickable ranking rows to open player profiles using minimal JavaScript (`rowLink.js`).
- Added scope-aware return navigation from player profile back to the corresponding ranking page and pagination position.

### Fixed

- Fixed inconsistent pagination by ensuring `Player` queryset is ordered before paginating.
- Fixed player profile stats display for tied rankings:
  - Ranking pages keep compact tie display (only first in group shows position).
  - Player profile now shows numeric position when needed for clarity.
- Fixed navbar “Ranking” link to return to the last visited ranking scope instead of always defaulting to “Todos”.

### Changed

- About page version label is derived from `CHANGELOG.md` (`Unreleased` or latest release).

## [1.2.1] - 2026-02-02

### Mobile

- Added iOS Progressive Web App (PWA) support:
  - Web App Manifest and iOS-specific meta tags.
  - Proper Home Screen icons for iPhone.
  - Safari-only install guidance banner explaining how to add the app to the Home Screen in `base.html`.

## [1.2.0] - 2026-01-24

- Added scoped gender-based rankings.
- Improved UX/UI across multiple views and features.

### Web

- Added:
  - scoped rankings: `all` ("Todos los partidos"), `male` ("Partidos masculinos"), `female` ("Partidos femeninos") and `mixed` ("Partidos mixtos").
  - schema fields: `Player.gender` and `Match.match_gender_type` (both temporary nullables).
  - gender field to registration form: gender required; linking existing unregistered player sets/updates gender.
  - `compute_gender_type()` function to automatically set `match_gender_type`.
  - Bootstrap 5 nav-tabs on the ranking page header, visible to all; for navigation between every type of ranking.
  - unranked players table (players with zero matches) at the bottom of the ranking tables in the last page. Scoped by gender and labeled accordingly.
  
- Improved:
  - Admin experience: enhanced Player/Match admin lists, filters, and bulk actions.

- General UX/UI consistency:  
  - Unified message positioning and tone.
  - Added persistence for the last selected ranking scope.
  - Enhanced `playerLabelUpdater.js` with real-time hints when creating a new player from the match form.
  
- Changed:
  - match entry form: replaced datalist with a dropdown select for player selection and creation of players with gender.
  
- Updated:
  - legacy players gender in the database (manually set) .
  
- Removed
  - the edit option from matches played (disputes are handled by delete + re-create)
  - the edit button from the UI, the edit JS and any edit-mode logic.
  -`matchEdit.js` as it is no longer used.
  - Persist last selected ranking scope.

- Improved:
  - Keep only one real ranking view function `ranking_view` while keeping `hall_of_fame_view` as a thin wrapper just to preserve URL names across templates and tests.
  - Moved ranking calculation to an external service file (`services/ranking.py`).

## [1.1.1] - 2026-01-01

Fixes and UI/UX improvements in the tournament management module for small devices (Galaxy S5/S8, iPhone 4/5/SE).

### Web

- Fixed standings table truncation on small screens (e.g., negative values in the points difference column) on the tournament detail page.
- Changed standings columns: replaced `points_for` and `points_against` with a new `matches_played` column (counting completed matches with valid results) to reduce horizontal space and improve readability.
- Fixed rounds table truncation on small screens (e.g., "Guardar" button and court selector "nº") by adjusting column width proportions.
- Improved rounds table result layout so both team scores are visually grouped in the center of the row for better alignment and readability.
- Improved round workflow UX: the **“Nueva ronda”** action now also saves the current round results (same effect as “Guardar”), allowing users to naturally continue to the next round after completing match results.
- Unified visual emphasis of save actions by styling all match-saving buttons as primary actions, improving clarity of the expected user interaction.

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

Fixed problem of lengthy time loading of the logo image in the navbar.

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

- Autocomplete attribute fixed in login and register input templates forms to adapt auto filling.
- Autocapitalize, autocorrect and spellcheck attributes fixed in login and register input templates forms to avoid auto corrections in mobile browsers.

---

## [1.0.2] – 2025-10-09

### Added

- Admin users now see two additional navigation links in the navbar: one to the staging site and one to the Django admin site.
- New template for the about page, including app statistics, version number and contact email.
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
