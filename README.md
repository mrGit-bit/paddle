<!-- markdownlint-disable MD051 -->
<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD060 -->
<!-- markdownlint-disable MD024 -->

# 🏆 Paddle Tennis Hall of Fame

<a id="overview"></a>

## 📖 Overview

Paddle Tennis Hall of Fame is a web application designed for groups of friends who play paddle tennis together. It helps them manage their own "Hall of Fame" within their group. It is also available as an Android mobile app that loads the same web experience through a WebView.

Registered users can track matches played, update match results, view player rankings, and access player statistics.

In addition, the web app includes a tournament management module to create and manage round-based friendly competitions, with live standings and per-round match entry.

This application is built using:

- Django and Django Rest Framework (DRF) for the RESTful API.
- Django templates, JavaScript, and Bootstrap for the web frontend.
- Capacitor + Android (WebView-based shell) for the mobile app distributed via Google Play using Android App Bundles (AAB).

The project is two products in the same repo in GitHub:

- Web app (Django)
- Android app (Capacitor → Play Store)

<a id="index"></a>

### 🔗 Index

- [📖 Overview](#overview)
- [✨ Key Features & Implementation](#key-features)
- [🛠️ Technologies Used](#technologies)
- [🗂️ Project Structure](#project-structure)
- [📡 API Endpoints](#api-endpoints)
- [🌐 Frontend Endpoints & Templates](#frontend-endpoints)
- [🛠️ JavaScript Functionalities](#javascript)
- [📑 Pagination](#pagination)
- [📱 Android Mobile App](#android-app)
- [📱 iOS Mobile App](#ios-app)
- [🧪 Testing](#testing)
- [🚀 Installation](#installation)
- [🤝 Contributing](#contributing)
- [📄 License](#license)

---

<a id="key-features"></a>

### ✨ Key Features & Implementation

#### Basic Functionalities

Full-stack web application that includes:

- A **RESTful API** built with Django and Django REST Framework (DRF); independently created from,
- a **frontend** app developed using Django templates & views, vanilla JavaScript, and Bootstrap 5.
- Additional user-friendly features have been introduced which include:
  - **Pagination** for easier navigation;
  - **Match filtering** by own matches and all matches;
  - A **badge indicator** for the number of new matches not reviewed in the current session;
  - **Real-time validation** during user registration; and,
  - **Public player pages** with selector and per-player profile (`/players/` and `/players/<id>/`);
  - **Clickable ranking rows** that open player profiles;
  - **Mini Hall of Fame**: personalized ranking section for users not appearing on the current page
  - Player gender is stored in `Player.gender` and match scope is stored in `Match.match_gender_type` (derived automatically via `compute_gender_type()`).
  - The last selected ranking scope is persisted (session-based) and used after match creation redirects.

The entire application is fully **mobile responsive**, ensuring a consistent experience across different devices and screen sizes, even in smaller screens,.

#### Hall of Fame Rankings

- Displays a ranked list of paddle tennis players.
- Publicly accessible (no authentication required).
- Supports:
  - scoped rankings: **Todos**, **Masculinos**, **Femeninos**, **Mixtos**
  - competition ranking with ties (“1224” style), showing the rank number only for the first row in each tie group
  - an “unranked” table (players with 0 matches in the selected scope) shown only on the last page
  - clickable rows to navigate directly to public player profile pages

- **Implementation**:
  - Frontend app: a single `ranking_view()` renders all ranking scopes (including `"all"`), with `hall_of_fame_view()` acting as a thin wrapper to preserve URL names.
  - Ranking computation is centralized in `frontend/services/ranking.py` (`compute_ranking(scope)`).
  - Templates (`hall_of_fame.html`, `hof_user_snippet.html`) always render `display_*` fields for consistency across scopes and ties.
  - Navigation between scopes is done via Bootstrap 5 nav-tabs (links, no JS state).
  - `rowLink.js` enables row-level navigation to player profile pages with minimal JavaScript.

#### Match Results

- Each match consists of two teams, each with two players.
- Authenticated users can add and delete match results in which they are a participant.
- Matches are **not editable**. Disputes are handled by **delete + re-create**.
- Player selection uses a dropdown:
  - existing registered players
  - existing unregistered players
  - new player creation directly from the match form (“Nuevo jugador / Nueva jugadora”), including gender

- **Implementation**:
  - Frontend app: `match_view()` in `frontend/views.py` handles match creation and deletion using PRG (Post-Redirect-Get) and Django messages.
  - On creation, new players are created if they don’t exist (case-insensitive).
  - Deletion is handled via normal POST form submission (`action=delete`) to preserve consistent messaging and navigation.

#### Tournaments Management

- **Permissions**:
  - Public access: Any user (authenticated or anonymous) can view tournaments and results.
  - Creation and editing: Only authenticated users can create a new tournament.
  - Only tournament participants, staff, and the creator can edit rounds and match assignments while the tournament is open (until and including the tournament day).
  - Only the tournament creator or staff can delete the tournament.
- Tournament **creation**: Users can select registered/existing players and also add new players (one per line). New players are automatically created in the database if they do not exist (case-insensitive uniqueness enforced).
- **Rounds**:  
  - Any number of rounds can be created (no limit based on courts).
  - Matches store court number and team scores.
  - Results can be saved partially: a round can include matches without completed scores.
- **Standings**:
  - Wins: +1 per win.
  -Points accounting: points_for, points_against, and derived points_diff = points_for - points_against.
  - Standings are recomputed from scratch after edits, ensuring no double-counting.
  - Rankings support ties (“1224” style), and tied rows are visually grouped.
- **Implementation** of App `americano`:
  - **Views**:
    - `americano_new`: create tournament (including new player creation) and auto-create Round 1.
    - `americano_detail`: render standings + rounds table; edit capabilities depend on can_edit.
    - `americano_assign_round`: persist court, team assignments, and optional scores; triggers standings recomputation.
    - `americano_new_round`: creates new empty rounds.
    - `americano_delete_round`: deletes a round (with renumbering). `americano_delete_tournament`: deletes the tournament (creator or staff only).
  - **Data model**: `AmericanoTournament`, `AmericanoRound`, `AmericanoMatch` and `AmericanoPlayerStats`.
  - **UI**: Integrated into the global navbar under Americanos with ongoing and finished tournaments.

#### User Management

- Users can register, log in, and manage their profiles.
- During registration, users can link their account to an existing player or create a new one.
- During registration, users must select a gender (M/F).
- When linking to an existing unregistered player, the user can set/update that player's gender during registration (admin remains the authoritative channel for later changes).
- When linking to an existing player, the user takes over the player's stats, and the player's name is changed to the user's username.
- Users can only update their own profiles, unless they are an admin, in which case they can update and delete any profile.
- **Implementation**:
  - API:
    - The `UserSerializer` includes a `player_id` field for optional linking to an existing player.
    - The `UserViewSet` restricts profile modification to the user's own profile or admins.
  - Frontend app: The `UserView` in `views.py` handles user registration, login, and logout.

#### Player Details

- Provides public player pages:
  - `/players/`: player selector.
  - `/players/<id>/`: detailed profile with match history and scoped stats.
- Player profile scoped stats preserve tie-aware ranking display:
  - ranking tables keep compact ties (“1224” style);
  - player profile shows numeric rank when needed for clarity.
- Only admins can update or delete player details.
- **Implementation**:
  - API:
    - The `PlayerSerializer` uses calculated fields: `matches_played`, `losses`, and `win_rate`.
    - The `PlayerViewSet` restricts player profile modification to admins.
  - Frontend app:
    - `players_view()` renders the public players selector page.
    - `player_detail_view()` renders profile stats + paginated match history and builds scope-aware return links to the right ranking page and pagination.
    - `get_player_stats` returns `wins`, `matches`, `win_rate` and `ranking_position`.

#### Authentication & Permissions

- Unauthenticated users can only:
  - View the Hall of Fame, public players pages and about page.
  - Register.
  - Log in.
- Authenticated users can:
  - View the same of non authenticated users.
  - View & add match results.
  - Update or delete their own match results.
  - View and update their editable fields in their own user profile.
  - View own player stats.
- Admins have full access, including creating, updating, and deleting matches, players, and users. Admin users have also links to the staging site and django admin panel.
- **Americano tournaments**:
  - Everyone can view tournaments and standings.
  - Only authenticated users can create tournaments.
  - Only tournament participants can edit rounds while open.
  - Only creator or staff can delete the tournament.

- **Implementation**:
  - API:
    - DRF's built-in session authentication is used.
    - The `IsAuthenticatedOrReadOnly` permission allows unauthenticated users to view player rankings.
    - The `IsAuthenticated` permission restricts match-related actions to authenticated users.
  - Session-based authentication for login and logout.
  - The `LoginView` and `LogoutView` API endpoints handle user authentication and logout.
  - Frontend app: The `LoginView` and `LogoutView` in `views.py` handle user authentication and logout. Extensive use of decorators to handle different authentication states.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

<a id="technologies"></a>

## 🛠️ Technologies Used

- **Backend**: Django Rest Framework (DRF)
  - `ModelViewSets`, `ModelSerializers` with `SerializerMethodField`, and `Routers` for simplified API management.
  - Built-in session authentication from DRF.
- **Frontend Web**:
  - Django Templates & Views.
  - Vanilla JavaScript.
  - Bootstrap 5.
- **Mobile App**:  
  - Capacitor (Android), using a WebView shell that loads the live web app.
  - Android App Bundles (AAB) built via GitHub Actions and distributed through Google Play (internal testing track).
- **Database**:
  - SQLite for development.
  - Oracle autonomous databases (two independent ADBs) for staging and production.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

<a id="project-structure"></a>

## 🗂️ Project Structure

- Folder structure:

```bash
/workspaces/paddle/
├── mobile/                   # Capacitor project for the Android mobile app
│   ├── android/              # Native Android project (Gradle)
│   ├── resources/            # Source assets (icon, splash) for Capacitor
│   ├── capacitor.config.ts   # Capacitor configuration (server.url, appId, etc.)
│   └── package.json          # Node dependencies for the mobile shell
├── paddle/                   # Django project
│ ├── americano/              # Americano tournaments (frontend views + models)
│ │   ├── migrations/         # Migrations for americano app
│ │   └── tests/              # Tests for americano views and standings
│ ├── config/                 # Project configuration and settings
│ │   └── settings/           # Different settings for development and production
│ ├── db.sqlite3              # SQLite database
│ ├── fixtures/               # Test data
│ ├── frontend/               # Frontend logic (in views.py), js, styles and html 
│ │   ├── migrations/         # Migrations for the frontend app
│ │   ├── static/frontend/    # Static files for the frontend
│ │   │   ├── css/            # CSS styles for the frontend
│ │   │   └── js/             # JavaScript files for the frontend
│ │   └── templates/frontend/ # HTML templates for the frontend
│ ├── games/                  # API app for players & matches
│ │   ├── migrations/         # Migrations for the games app
│ │   └── tests/              # Tests for games API
│ ├── staticfiles/            # Collected static files 
│ └── users/                  # API app for user management
│     ├── migrations/         # Migrations for the users app
│     └── tests/              # Tests for users API
├── .coverage               # Test coverage report
├── README.md               # Project documentation
├── requirements.in         # pip-tools dependencies
├── requirements.txt        # Compiled dependencies
└── .env                    # Environment variables
```

- Tests folders and files:

```bash
├── fixtures/          # Test data
├── games/             # API app for players & matches
│   └── tests/         # Tests for games API
├── users/             # API app for user management
│   └── tests/         # Tests for users API
```

- API Apps:

```bash
├── games/             # API app for players & matches
│   ├── serializers.py
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── tests/         # Tests for games API
├── users/             # API app for user management
│   ├── serializers.py
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── tests/         # Tests for users API
```

- Frontend apps and files:

```bash
├── frontend/                     # Frontend logic (in views.py), js, styles and html templates
│   ├── static/frontend/          # Static files for the frontend in development
│   │   ├── css/                  # Stylesheets
│   │   │   └── styles.css        # Custom styles for the frontend overriding Bootstrap styles
│   │   ├── favicon.ico           # Browser favicon
│   │   ├── img/                  # Images
│   │   │   ├── ios-share.svg
│   │   │   ├── logo_96.png
│   │   │   ├── logo_96.webp
│   │   │   ├── logo_180.png
│   │   │   ├── logo_192.png
│   │   │   ├── logo_512.png
│   │   │   └── logo_1024.png
│   │   └── js/                   # JavaScript files
│   │       ├── americano_new_players_remaining.js # Update remaining players counter in Americano creation
│   │       ├── editUserProfile.js      # Send a PATCH request to the API for updating user details
│   │       ├── ios-install.js          # Controls iOS PWA install banner behavior
│   │       ├── matchDeleteHighlight.js # On deletion update match card background dynamically
│   │       ├── passwordValidation.js   # Confirm password match
│   │       ├── playerLabelUpdater.js   # Update player labels dynamically on match form
│   │       ├── rowLink.js              # Make ranking rows clickable to open player pages
│   │       ├── tabPaginationReset.js   # Update pagination dynamically on tab change
│   │       └── winningTeamHighlight.js # Update winning team card background
│   │   └── manifest.json         # Web App Manifest (PWA metadata)
│   ├── templates/frontend/       # Folder containing Django templates
│   │   ├── _match_card.html      # Match history card to be included in match.html
│   │   ├── _pagination.html      # Reusable pagination component
│   │   ├── _player_select.html   # Reusable player selector component
│   │   ├── _user_form.html       # Reusable user form for register.html and user.html
│   │   ├── about.html            # Template for About page
│   │   ├── americano/            # Americano templates
│   │   │   ├── americano_detail.html
│   │   │   ├── americano_list.html
│   │   │   └── americano_new.html
│   │   ├── base.html             # Base template with common navigation bar & footer
│   │   ├── hall_of_fame.html     # Template for Hall of Fame
│   │   ├── hof_user_snippet.html # Template for mini table to be included in hall_of_fame.html
│   │   ├── login.html            # Template for user login
│   │   ├── match.html            # Template for adding and reviewing match results
│   │   ├── pass_reset/           # Password reset flow templates and email texts
│   │   ├── player_detail.html    # Public player profile page
│   │   ├── players.html          # Public player selector page
│   │   ├── register.html         # Template for user registration
│   │   └── user.html             # Template for checking or editing user details
│   ├── __init__.py
│   ├── urls.py                   # URLs frontend configuration
│   └── views.py                  # Views logic to render the templates
```

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

<a id="api-endpoints"></a>

## 📡 API Endpoints

All API endpoints follow the [RESTful API design](https://restfulapi.net/) principles and use standard HTTP methods (GET, POST, PUT, PATCH, DELETE). The API uses standard HTTP status codes to indicate success or failure. Errors will be returned as a `400 Bad Request` or a `404 Not Found` with an error message in the response body.

### Endpoints for the `games` app

The `games` app manages both players and matches.

`/api/games/players/`:

- `GET`: Provides access to the **Hall of Fame** with a ranked list of all players. Publicly accessible.
- `POST`: Creates a new player. Admin-only.

`/api/games/players/<id>/`:

- `GET`: Provides detailed information about a specific player. Only authenticated users can access it.
- `PUT` & `PATCH`: Updates a player's information. Admin-only.
- `DELETE`: Deletes a player. Admin-only.

`/api/games/matches/?player=<player_name>`:

- `GET`: Returns all matches, or filtering matches by a specific player. Allows authenticated users viewing match history and display the form for adding match results:
  - When there is no query parameter, all matches are shown ordered by date.
  - When query parameter is specified, only matches played by the `player_name` are shown ordered by date.

`/api/games/matches/`:

- `POST`: Allows authenticated users to add matches, creating new players if needed. The user must be one of the match participants.

`/api/games/matches/<id>/`:

- `PUT` & `PATCH`: Allows authenticated match participants to edit match details.
- `DELETE`: Deletes a match. Restricted to authenticated match participants.

`/api/games/players/player_names/`:

- `GET`: Returns a JSON dictionary with a list of registered users (players already linked to a User account) and a list of non-registered players, both with their ID and name. Results are sorted alphabetically. Publicly accessible. This endpoint is used:
  - During user registration: to provide a list of non-registered players to choose from;
  - When introducing new match results: to differentiate between registered players, existing non-registered players and new players.

### Endpoints for the `users` app

Manages user registration, login, logout, linking of existing non-registered players during user registration, and user profiles management.

`/api/users/`:

- `POST`: Allows new users to register. Publicly accessible. Checks if the username already exists.

`/api/users/<id>/`:

- `GET`: Returns the authenticated user's own profile. Only the authenticated user, owner of the profile or an admin can access it.
- `PATCH`: Updates a user's profile. Only the authenticated user, owner of the profile or an admin can modify it.
- `DELETE`: Deletes a user's profile. Only an admin can perform this action.

### Endpoints for the `api-auth` browsable API

In development, the `api-auth` app provides endpoints for login and logout when using the browsable API.

`/api-auth/login/`: Login endpoint for the browsable API.

`/api-auth/logout/`: Logout endpoint for the browsable API.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

<a id="frontend-endpoints"></a>

## 🌐 Frontend Endpoints & Templates

### 🏗️ Foundation Template

All templates extend a base layout using `{% extends "base.html" %}` where `base.html` provides the site-wide layout, including the common navigation bar and standard footer. It serves as the foundation for all pages, ensuring a consistent look and feel across the site.

The navigation bar is:

- Collapsible on small screens.
- Sticky to the top on scroll.
- Links accessible to unauthenticated users are: Paddle HoF, Register, Login and About.
- Links accessible to authenticated users are: Paddle HoF, Matches, User Profile (displaying the _current_ user's name in the navbar), About, and Logout.
- Matches link should display a badge with the number of _pending_ matches for the current user in that session. By clicking on the badge the user is redirected to the `match.html` page. The badge is only displayed if there are any pending matches.

### 🔗 URLs & Full Page Templates

These are the full-page templates directly mapped to URLs:

| URL                     | Purpose                               | Template Loaded     | Specs                                                                                                                                            |
| ----------------------- | ------------------------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `/` | Hall of Fame – ranking (Todos los partidos) | `hall_of_fame.html` | Ranking table + scoped nav-tabs + ties (“1224” style) + unranked players table on last page. |
| `/ranking/male/`   | Ranking – Partidos masculinos | `hall_of_fame.html` | Scoped ranking (male matches only). |
| `/ranking/female/` | Ranking – Partidos femeninos  | `hall_of_fame.html` | Scoped ranking (female matches only). |
| `/ranking/mixed/`  | Ranking – Partidos mixtos     | `hall_of_fame.html` | Scoped ranking (mixed matches only). |
| `/players/` | Public player selector | `players.html` | Public page to select a player and open profile. |
| `/players/<id>/` | Public player profile | `player_detail.html` | Scoped stats + match history + scope-aware return links to ranking and page. |
| `/register/`            | User registration                     | `register.html`     | Dynamic checking of restrictions and load available players to choose from.                                                                      |
| `/login/`               | User login                            | `login.html`        | User & password fields and login button.                                                                                                         |
| `/logout/`              | User logout                           | N/A - View handled  | Logout link with bootstrap icon. _This action is a redirection._                                                                                 |
| `/users/<id>/`          | User details and editing              | `user.html`         | User profile stats and editable fields.                                                                                                          |
| `/matches/` | Match results | `match.html` | Add match + match history (My Matches / All). Note: To edit: delete + re-create. |
| `/about/`               | About                                 | `about.html`        | About page with version from `.env` `APP_VERSION` (fallback `—`). |
| `/americano/`                         | Americano tournaments list      | `americano_list.html`   | Shows ongoing and finished tournaments. Public.                                                                |
| `/americano/nuevo/`                   | Create new Americano tournament | `americano_new.html`    | Only authenticated users can create. Supports selecting existing players + adding new players (created in DB). |
| `/americano/<id>/`                    | Americano tournament detail     | `americano_detail.html` | Standings + rounds. Public read access; participants can edit while tournament is open.                        |
| `/americano/<id>/nueva-ronda/`        | Create new round                | N/A - View handled      | Adds an empty round. Only participants while open.                                                             |
| `/americano/round/<round_id>/assign/` | Save round assignment/results   | N/A - View handled      | Saves court, players and optional scores; recomputes standings. Only participants while open.                  |
| `/americano/round/<round_id>/delete/` | Delete round                    | N/A - View handled      | Deletes a round and renumbers remaining rounds. Only participants while open.                                  |
| `/americano/delete/<id>/`             | Delete tournament               | N/A - View handled      | Only creator or staff. Deletes tournament, rounds, and stats.                                                  |

### 📂 Partial & Reusable Templates

These partial templates are reusable components designed to be included in other templates using `{% include %}`:

- `_match_card.html`: Displays match cards to be used in the tabs of the Match History section of `match.html`. Includes teams with color indication for winning team in green background, date played with a "new!" badge indication for _not yet reviewed_ matches by the user in that session, and delete and edit buttons for matches where the user is a participant. The edit button let the user edit his own matches.

- `_user_form.html`: A dynamic form for creating and editing users. Reused in both `register.html` (for new users) and `user.html` (for editing allowed fields of the user profile).

- `_pagination.html`: A reusable template for pagination, used in `hall_of_fame.html` and `match.html`. It shows current page number with indication of total pages,"Rewind", "Fast Forward" and following and previous page number, any of them showed only when available.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

<a id="javascript"></a>

## 🛠️ JavaScript Functionalities

- `passwordValidation.js`: Checks if the password and confirm password fields match, and dynamically displays an error message if they don't. Is used in `register.html`.
- `playerLabelUpdater.js`: Provides real-time hints when typing a “new player” name in the match form (registered/existing/new), to prevent duplicates and confusion.
- `rowLink.js`: Makes ranking rows clickable to open public player profile pages.
- `winningTeamHighlight.js`: Dynamically updates the background of the "Team 1" and "Team 2" cards in the form fields of `match.html` based on the selection of the "winning_team" radio button with green background for the winning team.
- `matchDeleteHighlight.js`: Highlights the match card before showing a confirm dialog and submitting the delete POST form (PRG + Django messages).
- `editUserProfile.js`: Allows editing of allowed user details in `user.html`. _Only the email field has been flagged as editable so far._ By changing the value on the email field in the user profile, "Cancel Changes" and "Save Changes" buttons are enabled:
  - When the user clicks "Save Changes", the endpoint of the API is called by PATCH.
  - When the user clicks "Cancel Changes", the form is reset to the original values.
- `tabPaginationReset.js` is loaded with match.html for:
  - Showing the correct pagination on initial load based on the active tab;
  - Hiding the inactive tab’s pagination;
  - Resetting pagination to page 1 when switching between tabs.
- `americano_new_players_remaining.js`: Used in `americano_new.html` template. Updates the “Jugadores restantes” indicator in real time during tournament creation based on selected registered players and manually entered new players.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

<a id="pagination"></a>

## 🔄 Pagination

This application implements pagination to efficiently handle and display large datasets of players and matches. Pagination is applied to the Hall of Fame and Match History views, ensuring a smooth and responsive user experience, even with extensive data.

### Backend Pagination (Django REST Framework)

The backend utilizes Django REST Framework's (DRF) built-in pagination capabilities. This provides a standardized way to paginate API responses.

- **How it Works:** When requesting a paginated endpoint (e.g., `/api/games/players/` or `/api/games/matches/`), the API will return a subset of the data along with metadata about the pagination.
- **Deterministic Order:** Player pagination uses an ordered queryset before paginating to keep stable page contents.
- **Query Parameter:** To navigate through pages, use the `?page=<page_number>` query parameter in your request. For example, `/api/games/players/?page=2` will retrieve the second page of players.
- **Response Structure:** The API response for paginated endpoints includes:
  - `count`: The total number of items available.
  - `next`: The URL for the next page of results (or `null` if there is no next page).
  - `previous`: The URL for the previous page of results (or `null` if there is no previous page).
  - `results`: An array containing the data for the current page.
- **Page Size:** The default page size is set to 12 items per page in the `settings.py` file (`PAGE_SIZE = 12`). This specific size was chosen because the `_match_card.html` template displays match cards in a grid layout with three columns on larger screens. Using a multiple of three ensures that rows are always filled completely.

### Frontend Pagination (Bootstrap 5)

The frontend leverages Bootstrap 5's pagination component to provide a user-friendly interface for navigating through paginated data.

- **How it Works:** The frontend dynamically generates pagination links based on the `next`, `previous`, `count`, and `current_page` fields provided by the frontend view. These links allow users to navigate between pages of data of 12 items per page maximum.
- **Implementation:** The pagination component `_pagination.html` is loaded in:
  - `hall_of_fame.html` for player ranking pages of 12 players; and,
  - `match.html` with two independent pagination subset for _My Matches_ and _All Matches_ tabs. Pagination is displayed only for the active tab, and hidden for the inactive one. A dedicated JavaScript file (`tabPaginationReset.js`) is used to reset the pagination to the first page when a new tab is selected, hiding the pagination for the inactive tab and updating the URL hash accordingly.
- **User Experience:** The pagination component seamlessly integrates with the application's design, allowing users to easily navigate between pages of maximum 12 players or matches. It displays the current page number, number of total pages and provides links to previous and next pages (if available). Also full rewind or fast forward to the first or last page are available when needed.
- **Dynamic Rendering:** The pagination component is dynamically rendered based on the data received from the API, ensuring that the correct number of pages and relevant navigation links are displayed.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

<a id="android-app"></a>

## 📱 Android Mobile App

An Android mobile app is available, built with Capacitor and implemented as a WebView-based native wrapper that loads the same web application used in desktop and mobile browsers.

### How it works

- The app does not duplicate business logic; it simply wraps the existing web frontend.
- It consists of:
  - An native Android shell (APK/AAB)
  - An embedded WebView managed by Capacitor
- The WebView loads the live web application from:
  - Staging (`https://staging.rankingdepadel.club`)
  - Production (`https://rankingdepadel.club`)
- Session-based authentication and cookies are reused exactly as in the browser version.
- UI and behavior remain consistent with the web app, while native Android-specific behavior (fonts, system UI, edge-to-edge handling) is handled at the wrapper level.

### Distribution

- The app is built as an **Android App Bundle (AAB)** using a GitHub Actions workflow.
- Signed AABs are uploaded to **Google Play Console** and distributed via the **Internal Testing** track.
- Testers install and update the app through the Play Store like any standard Android application.

> Note: The native Android project (Capacitor configuration and Android build files) lives in the mobile/ folder within this repository.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

<a id="ios-app"></a>

## 📱 iOS Mobile App

An iOS mobile app experience is available via a Progressive Web App (PWA), allowing iPhone and iPad users to install and run the application without using the App Store.

### How it works

- The iOS app is delivered as a Progressive Web App (PWA) built directly from the existing web application.
- No native iOS wrapper or App Store distribution is used.
- Users install the app using Safari via:
  - Safari → Share → Add to Home Screen
- Once installed, the app:
  - Runs in standalone full-screen mode
  - Uses the same UI, routes, and backend as the web and Android versions
  - Reuses session-based authentication and cookies exactly as in the browser
- Updates are delivered instantly on every web deployment (no app updates required).
- Native capabilities are limited by iOS PWA constraints:
  - No native plugins (camera, biometrics, etc.)
  - Background execution and system integrations are more restricted than in the Android app

### Distribution

- The app is not distributed via the App Store.
- Installation is performed directly by the user from the browser.
- This approach avoids Apple Developer Program requirements and macOS/Xcode dependencies.

> Note: This PWA-based iOS app provides an app-like experience while keeping maintenance and operational complexity minimal.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

<a id="testing"></a>

## 🧪 Testing

The project comes with a suite of tests for the API (`games` and `users`), and `frontend` apps.

### Test files

- `frontend/tests/test_login.py`
- `frontend/tests/test_password_reset.py`
- `frontend/tests/test_players_stats.py`
- `frontend/tests/test_ranking_redirect.py`
- `frontend/tests/test_ranking_ties.py`
- `frontend/tests/test_views_coverage_extra.py`
- `frontend/tests/test_views.py`
- `americano/tests/test_americano_views.py`
- `games/tests/test_permissions.py`
- `games/tests/test_players.py`
- `games/tests/test_stats.py`
- `users/tests/test_authentication.py`
- `users/tests/test_permissions.py`
- `users/tests/test_register.py`

### Test coverage

Ensure first that all tests pass with:

```bash
pytest -q
```

and then that more than 90% of frontend and americano code is covered by tests using:

```bash
pytest /workspaces/paddle/paddle/frontend/tests/ --cov=frontend.views --cov-report=term-missing
pytest /workspaces/paddle/paddle/americano/tests/test_americano_views.py --cov=americano.views --cov-report=term-missing
```

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

<a id="installation"></a>

## 🚀 Installation

### 📋 Prerequisites

- Python 3.8 or higher: Required to run Django 5.x and supported packages.
- pip (Python package manager): comes pre-installed with Python.
- Git (for cloning the repository)
- virtualenv (recommended, for creating isolated environments)

> These installation steps refer to the **web application** (Django).  
> The Android mobile app is built via a separate Capacitor project in the `mobile/` folder and distributed through Google Play (internal testing). Local building of the mobile app requires Android tooling and is not covered in this section.

For testing, development and configuration you may also need:

- `pytest` and `pytest-django` (for running tests)
- `coverage` (for generating test coverage reports)
- `django-extensions` (for additional Django commands)
- `python-decouple` (for managing environment variables)
- `pip-tools` (for managing requirements)

### 🏗️ Steps

- Clone the repository:
  - `git clone https://github.com/mrGit-bit/paddle`
  - `cd paddle`

- Create and activate a virtual environment:
  - `python -m venv venv`
  - `source venv/bin/activate` (For Windows: `venv\Scripts\activate`)

- Install dependencies:
  - `pip install -r requirements.txt`

### ⚙️ Environment Configuration

This project uses `python-decouple` to manage environment variables from a `.env` file.  
The app dynamically loads either development or production settings based on the value of `DJANGO_ENVIRONMENT`.

#### 1. Setup your `.env` file

Copy the example file to create your actual configuration:

```bash
cp .env.example .env
```

Then edit .env with the values for your local or production environment.

#### 2. Set the environment variables

| Variable               | Description                                  | Example                      |
| ---------------------- | -------------------------------------------- | ---------------------------- |
| `DJANGO_ENVIRONMENT`   | Which settings to load: `dev` or `prod`      | `dev`                        |
| `SECRET_KEY`           | Django secret key                            | `django-insecure-...`        |
| `DEBUG`                | Toggle debug mode (`True` or `False`)        | `True`                       |
| `ALLOWED_HOSTS`        | Comma-separated list of allowed hostnames    | `127.0.0.1,localhost`        |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated list of trusted CSRF origins | `http://127.0.0.1:8000`      |
| `SITE_URL`             | Full URL to the app                          | `http://127.0.0.1:8000/`     |
| `BASE_API_URL`         | Root URL of the backend API                  | `http://127.0.0.1:8000/api/` |

#### 3. 🔁 Switch between environments

You can switch between development and production by changing just one line in your .`env` file:

```bash
DJANGO_ENVIRONMENT=dev   # for local development
DJANGO_ENVIRONMENT=prod  # for production (e.g., PythonAnywhere)
```

#### 4. Settings architecture

The Django settings are split across multiple files for better separation of development and production configurations:

```bash
config/
└── settings/
    ├── __init__.py    # Loads either dev.py or prod.py based on DJANGO_ENVIRONMENT
    ├── base.py        # Shared settings for all environments
    ├── dev.py         # Development-only settings
    └── prod.py        # Production-only settings
```

`base.py` contains all settings common to both environments: apps, middleware, templates, DRF config, etc.

`dev.py` and `prod.py` import from `base.py` and override or extend as needed (e.g., databases, debug, host permissions).

`__init__.py` automatically determines which file to load based on the DJANGO_ENVIRONMENT variable defined in your .env file.

#### 🧪 Local Development

- Apply migrations:
   `python manage.py migrate`

- Create a Django superuser:
   `python manage.py createsuperuser`

- Run the development server:

```bash
cd paddle
python manage.py runserver
```

- Access the app at: `http://localhost:8000/`

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

<a id="contributing"></a>

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Make your changes.
4. Commit your changes: `git commit -m 'Add feature'`.
5. Run tests ensuring coverage over 90%.
6. Push to the branch: `git push origin feature-name`.
7. Open a pull request from the branch `feature-name` to `develop`.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

<a id="license"></a>

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.
