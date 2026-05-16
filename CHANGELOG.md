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

- `Governance`: Added a repository harness map, local harness check command,
  active spec validation, CI harness gates, and release dry-run validation.
- `Governance`: Added source-of-truth, fallback disclosure, explicit-target,
  conflict-handling, and configured-linter guidance to router and
  skill-authoring docs.
- `Governance`: Added `$prd-to-specs` to break phased PRDs into approved
  vertical-slice implementation specs.
- `Governance`: Clarified that `$prd-to-specs` outputs are implemented through
  the normal single-spec SDD gate.

## [1.10.3] - 2026-05-11

- `UI/UX`: Restored Bootstrap accordion icons, compacted player-detail ranking
  pills, and linked pair medals to the `Parejas` ranking page.
- `Backend`: Made Americano round assignment validate before transactional
  persistence and reduced detail-page query work.
- `Release`: Streamlined release orchestration with local prep, deterministic
  promotion checks, validation skip controls, next-patch derivation, and
  consolidation guards.
- `Governance`: Clarified Markdown lint handling and changelog style so entries
  stay category-grouped, outcome-focused, and concise.
- `Governance`: Added `$phased-prd` for persistent PRDs that split complex
  work into later approved implementation phase specs.

## [1.10.2] - 2026-05-10

- `UI/UX`: Expanded medallero coverage to pair rankings, kept medal ribbons and
  collapsed strips visually stable, and linked medal cards to the relevant
  ranking scope.
- `UI/UX`: Reworked player detail with a `Medallas` section, collapsible
  statistics cards, compact ranking pills, and stricter `Contendientes`
  eligibility.
- `Governance`: Added `$context-budget-review` and `$debug`, tightened routing
  and CSS/test guidance, and reduced high-volume audit context.
- `Release`: Clarified staging-only release authorization, production approval,
  and compact release-session reporting.
- `Tests`: Updated medallero and player-detail assertions to check durable
  structure instead of brittle copy or markup details.

## [1.10.1] - 2026-05-07

- `Dependencies`: Patched vulnerable Python and mobile npm dependencies,
  tightened Python dependency floors, and removed unused runtime packages.
- `Governance`: Resolved governance audit findings, added `$write-a-skill`, and
  simplified active spec execution guidance.
- `Release`: Hardened release automation for visible-check fallbacks, GPG-free
  back-merges, and tested changelog release-prep spacing.

## [1.10.0] - 2026-05-06

- `UI/UX`: Added the public `Medallero` page with backend-owned medal
  assignment, compact player rows, summary icons, and expanded medal cards.
- `Backend`: Hardened Americano mutations with POST-only new-round creation,
  CSRF-protected empty-tournament actions, and transactional match updates.
- `Performance`: Reduced player-detail ranking and new-match badge query work.
- `Governance`: Added presentation and code audit reports, `$test-design`, and
  `$sdd-grill-me`; compacted docs and reorganized ChatGPT/Codex governance
  around router files plus workflow skills.

## [1.9.4] - 2026-04-26

- `UI/UX`: Tightened player-detail `Contendientes` thresholds and shortened the
  visible `Némesis` and `Víctimas` labels.

## [1.9.3] - 2026-04-22

- `UI/UX`: Added player-detail `Contendientes` cards and prevented inactive
  efficiency selector cards from changing visible trend rows.
- `Governance`: Aligned template presentation audits with the repository audit
  lifecycle and clarified audit routing.

## [1.9.2] - 2026-04-21

- `UI/UX`: Reworked player-detail statistics into grouped insight cards with
  clearer ranking, trend, partner, and rival-pair visuals across screen sizes.
- `Governance`: Added template presentation audit guidance and tightened UI and
  release-summary review rules.

## [1.9.1] - 2026-04-16

- `UI/UX`: Added scoped efficiency wheels, recent trends, ranking progress,
  partner efficiency cards, cleaner mobile ranking icons, and default linked
  player detail for authenticated users.
- `Governance`: Tightened ChatGPT pre-spec handoffs, ignored pre-spec storage,
  closure commits, and instruction duplication checks.
- `Docs`: Added the Django development server helper prompt.

## [1.9.0] - 2026-04-07

- `Data`: Added group ownership for players, matches, and Americano
  tournaments, migrated legacy data into `club moraleja`, and preserved global
  player-name uniqueness.
- `UI/UX`: Scoped authenticated rankings, matches, players, pairs, tournaments,
  and registration to groups while keeping anonymous aggregate browsing through
  the public `Hall of Fame`.
- `Release`: Hardened deployment automation with local validation, migrations,
  version checks, tracked deploy steps, and manual environment checks.
- `Governance`: Simplified SDD to one approved active-work spec, consolidated
  shipped specs into release records, clarified loose-spec lifecycle states,
  and required sequential closure steps.
- `Docs`: Added the multi-group and Hall of Fame rollout checklist.

## [1.8.1] - 2026-04-01

- `UI/UX`: Raised `Parejas del siglo` and `Parejas catastróficas` eligibility
  from 3 to 5 shared matches.

## [1.8.0] - 2026-04-01

- `UI/UX`: Added the public `Parejas` page with pair wins and best/worst
  win-rate tables using the ranking-table visual style.
- `Backend`: Fixed registration linking for existing unregistered players when
  the submitted username matches the selected player.
- `Release`: Added staging and production version verification after deploys
  and fixed the tracked SSH update command flow.
- `Governance`: Added a Project Instructions character budget and stable
  changelog domain prefixes.

## [1.7.0] - 2026-03-31

- `UI/UX`: Added ranking-page local sorting, top habitual partners on player
  detail, and a 30-day window for match entry and deletion.
- `Governance`: Made release orchestration command-first, expanded reduced
  process and closure authorization rules, tightened review/audit checkpoints,
  and compacted Markdown across specs, plans, release records, and changelog
  entries.
- `Release`: Consolidated historical release/spec records and limited release
  consolidation to files explicitly tagged with the shipped version.

## [1.6.1] - 2026-03-27

- `Release`: Added `/prompts:release`, repo-local SSH release assets, clearer
  `gh` auth guidance, and more reliable release orchestration around SSH,
  checks, failures, and release-tag consolidation.
- `Governance`: Added `governance-markdown-auditor`, tightened ownership and
  audit routing, allowed reduced process for narrow docs, and required live
  verification for external-tool assumptions.
- `Tests`: Pointed the release-orchestrator pytest suite at
  `config.test_settings` by default.

## [1.5.0] - 2026-03-16

- `UI/UX`: Added Bootstrap password visibility controls to auth forms.
- `Backend`: Hardened account email uniqueness, removed inactive profile-edit
  API code, and reduced duplicate query work in auth and match-list flows.
- `Governance`: Consolidated released SDD specs/plans after tagged releases,
  tightened post-release cleanup, and clarified audit and closure expectations.
- `Tests`: Added auth regression coverage and query-count visibility for
  registration, profile, and authenticated match-list flows.

## [1.4.1] - 2026-03-14

- `Docs`: Refreshed `README.md` as the practical repository guide for Codex CLI
  agents.
- `Governance`: Marked Markdown `MD013` as non-blocking and required README
  updates when README-covered guidance changes.
- `Release`: Fixed release tagging by configuring Git identity and validating
  the changelog/config version match before extracting release notes.

## [1.4.0] - 2026-03-12

- `UI/UX`: Reworked account management with standard Django forms, confirmed
  registration email feedback, and a dedicated account deletion flow.
- `Release`: Fixed release-notes extraction, derived release tags from
  `__version__`, and documented CI jobs plus manual fallback scripts.
- `Governance`: Compressed Project Instructions, synchronized version metadata,
  refined commit/closure handoff rules, and centralized deprecated API/DRF
  constraints.

## [1.3.1] - 2026-03-09

- `UI/UX`: Added player insights for trends, frequent partners, and frequent
  rival pairs; captured gender when creating Americano players.
- `Backend`: Shared canonical ranking policy, centralized player-participation
  match queries, and removed the deprecated DRF API surface.
- `Release`: Fixed release prep, PR body generation, release notes extraction,
  and workspace port settings.
- `Governance`: Added mandatory spec/plan stop gates, Markdown compliance
  rules, and instruction version/date synchronization.
- `Tests`: Made the about-page version assertion dynamic and added fail-fast
  protection against running pytest on the development SQLite database.

## [1.3.0] - 2026-02-20

- `UI/UX`: Added public player pages, clickable ranking rows, scope-aware
  return navigation, consistent pagination, and clearer tied-ranking display.
- `Backend`: Derived the about-page version label from `CHANGELOG.md`.
- `Branding`: Added `favicon.ico`.

## [1.2.1] - 2026-02-02

- `Mobile`: Added iOS PWA support with manifest metadata, Home Screen icons,
  and Safari install guidance.

## [1.2.0] - 2026-01-24

- `UI/UX`: Added gender-scoped rankings, ranking tabs, unranked player tables,
  last-scope persistence, improved player creation hints, and cleaner match
  entry without edit-mode flows.
- `Backend`: Added player and match gender fields, automatic match gender
  computation, migrated legacy player gender data, and moved ranking
  calculation into `services/ranking.py`.
- `Admin`: Improved Player and Match admin lists, filters, and bulk actions.

## [1.1.1] - 2026-01-01

- `UI/UX`: Improved Americano tournament usability on very small devices with
  tighter standings/round layouts, clearer score grouping, and primary save
  actions.
- `Backend`: Made `Nueva ronda` save current round results before creating the
  next round.

## [1.1.0] - 2025-12-30

- `UI/UX`: Added Americano tournament navigation, public tournament viewing,
  participant/staff/creator editing permissions, and confirmation flows for
  deletion.
- `Backend`: Added configurable Americano tournaments with registered and
  unregistered players, unlimited rounds, per-round match management, and
  automatic standings recomputation.
- `UI/UX`: Made the matches menu visible to everyone, with anonymous users
  redirected to login.

## [1.0.6] - 2025-12-08

- `UI/UX`: Optimized the navbar logo with a small WebP/PNG fallback and fixed
  the account password link to use the password reset flow.
- `DevOps`: Added `deploy_update.sh` for staging and production updates.

## [1.0.5] - 2025-11-30

- `UI/UX`: Added the navbar logo, improved very-small-screen navbar/group-name
  layout, fixed desktop navbar alignment, and made the footer link home.
- `Mobile`: Disabled Android 15 edge-to-edge overlap by default.
- `DevOps`: Added versioned collected static files for NGINX cache busting.

## [1.0.4] - 2025-11-20

- `Mobile`: Added the Android app to Google Play Store closed testing.
- `DevOps`: Updated Android release CI for AAB signing, Play Store secrets,
  Java 21, Android SDK API 35, and staging bypass support for mobile testing.

## [1.0.3] - 2025-10-23

- `UI/UX`: Added password reset with Brevo SMTP email delivery and aligned
  login styling with registration.
- `Mobile`: Fixed login and registration form autocomplete, autocapitalize,
  autocorrect, and spellcheck behavior.

## [1.0.2] - 2025-10-09

- `UI/UX`: Added admin navbar links, an about page with app stats/version/contact
  details, required-field markers on registration, and removed the footer
  version number.
- `Docs`: Updated `README.md`.

## [1.0.1] - 2025-10-02

- `Auth`: Added case-insensitive username/email login and case-insensitive
  registration checks across users and player names.
- `UI/UX`: Updated JavaScript UI text to Spanish and fixed case-insensitive
  match-form label updates.
- `Tests`: Increased coverage above 90%.

## [1.0.0] - 2025-09-25

- `UI/UX`: Localized frontend templates to Spanish and improved readability and
  tap targets on very small devices.
- `Release`: Added the version number to the footer.
