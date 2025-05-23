<!-- markdownlint-disable MD051 -->
<!-- markdownlint-disable MD033 -->

# 🏆 Paddle Tennis Hall of Fame

## 📖 Overview

Paddle Tennis Hall of Fame is a web application designed for groups of friends who play paddle tennis together. It helps them manage their own "Hall of Fame" within their group.

Registered users can track matches played, update match results, view player rankings, and access player statistics.

This web application is built using:

- Django and Django Rest Framework (DRF) for the RESTful API.
- Django templates, JavaScript, and Bootstrap for the frontend.

<a id="index"></a>

### 🔗 Index

- [📖 Overview](#📖-overview)
- [🔗 Index](#🔗-index)
- [✨ Key Features & Implementation](#✨-key-features--implementation)
- [🛠️ Technologies Used](#🛠️-technologies-used)
- [🗂️ Project Structure](#🗂️-project-structure)
- [📡 API Endpoints](#📡-api-endpoints)
- [🌐 Frontend Endpoints & Templates](#🌐-frontend-endpoints--templates)
- [🛠️ JavaScript Functionalities](#🛠️-javascript-functionalities)
- [📑 Pagination](#📑-pagination)
- [🧪 Testing](#🧪-testing)
- [🚀 Future Enhancements](#🚀-future-enhancements)
- [🚀 Installation](#🚀-installation)
- [🤝 Contributing](#🤝-contributing)
- [📄 License](#📄-license)

---

### ✨ Key Features & Implementation

#### Basic Functionalities

Full-stack web application that includes:

- A **RESTful API** built with Django and Django REST Framework (DRF); independently created from,
- a **frontend** developed using Django templates, vanilla JavaScript, and Bootstrap 5.
- Additional user-friendly features have been introduced which include:
  - **Pagination** for easier navigation;
  - **Match filtering** by own matches and all matches;
  - A **badge indicator** for the number of new matches not reviewed in the current session;
  - **Real-time validation** during user registration; and,
  - **Mini Hall of Fame**: personalized ranking section for users not appearing on the current page

The entire application is fully **mobile responsive**, ensuring a consistent experience across different devices and screen sizes.

#### Hall of Fame Rankings

- Displays a ranked list of paddle tennis players based on their number of wins.
- Publicly accessible (no authentication required).
- **Implementation**:
  - The `PlayerViewSet` in `views.py` retrieves players, ordering them by the `ranking_position` field to create the ranking.
  - The `models.py` calculate `matches_played`, `losses`, and `win_rate` as `@property` decorators for read-only fields.

#### Match Results

- Authenticated users can add and update match results.
- Each match consists of two teams, each with two players.
- Team players could be one of three categories: registered, existing non-registered players, and new players.
- Those categories are automatically populated when adding the player´s names.
- When a new match is added, new players are created if they don't exist.
- Users can only add, update, or delete matches in which they are a participant.
- **Implementation**:
  - The `MatchSerializer` handles player name input, creates new players if needed, and prevents duplicate player entries.
  - `perform_create()` in the `MatchViewSet` updates player stats when a match is created.
  - `perform_update()` resets old match stats before applying new results to maintain data integrity.

#### User Management

- Users can register, log in, and manage their profiles.
- During registration, users can link their account to an existing player or create a new one.
- When linking to an existing player, the user takes over the player's stats, and the player's name is changed to the user's username.
- Users can only update their own profiles, unless they are an admin, in which case they can update and delete any profile.
- **Implementation**:
  - The `UserSerializer` includes a `player_id` field for optional linking to an existing player.
  - The `UserViewSet` restricts profile modification to the user's own profile or admins.

#### Player Details

- Provides detailed profiles for each player, including their ranking position, match history and stats such as wins, matches played, win rate, and losses.
- Only admins can update or delete player details.
- **Implementation**:
  - The `PlayerSerializer` uses calculated fields: `matches_played`, `losses`, and `win_rate`.
  - The `PlayerViewSet` restricts player profile modification to admins.

#### Authentication & Permissions

- Unauthenticated users can only:
  - View the Hall of Fame.
  - Register.
  - Log in.
- Authenticated users can:
  - View the Hall of Fame.
  - Add match results.
  - Update or delete their own match results.
  - View and update their editable fields in their own user profile.
  - View own player stats.
- Admins have full access, including creating, updating, and deleting matches, players, and users.
- **Implementation**:
  - DRF's built-in session authentication is used.
  - The `IsAuthenticatedOrReadOnly` permission allows unauthenticated users to view player rankings.
  - The `IsAuthenticated` permission restricts match-related actions to authenticated users.
- Session-based authentication for login and logout.
- **Implementation:**
  - The `LoginView` and `LogoutView` API endpoints handle user authentication and logout.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🛠️ Technologies Used

- **Backend**: Django Rest Framework (DRF)
  - `ModelViewSets`, `ModelSerializers` with `SerializerMethodField`, and `Routers` for simplified API management.
  - Built-in session authentication from DRF.
- **Frontend**:
  - Django Templates.
  - Vanilla JavaScript.
  - Bootstrap 5.
- **Database**: SQLite for development and testing.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🗂️ Project Structure

- Folder structure:

```bash
paddle/
├── config/                 # Project configuration and settings
│   └── settings/           # Different settings for development and production
├── db.sqlite3              # SQLite database
├── fixtures/               # Test data
├── frontend/               # Frontend logic (in views.py), js, styles and html 
│   ├── migrations/         # Migrations for the frontend app
│   ├── static/frontend/    # Static files for the frontend
│     ├── css/              # CSS styles for the frontend
│     └── js/               # JavaScript files for the frontend
│   └── templates/frontend/ # HTML templates for the frontend
├── games/                  # API app for players & matches
│   ├── migrations/         # Migrations for the games app
│   └── tests/              # Tests for games API
├── staticfiles/            # Collected static files 
├── users/                  # API app for user management
│   ├── migrations/         # Migrations for the users app
│   └── tests/              # Tests for users API
├── .coverage               # Test coverage report
├── README.md               # Project documentation
├── requirements.in         # pip-tools dependencies
├── requirements.txt        # Compiled dependencies
└── .env                    # Environment variables
```

- Configuration files:

```bash
├── config/            # Project configuration and settings
│   ├── __init__.py    # Allows notations like config.settings, config.urls, etc.
│   └── settings/      # Different settings for development and production
│     ├── __init__.py  # Allows i.e. from config.settings import dev
│     ├── base.py      # Common settings
│     ├── dev.py       # Development-specific settings
│     └── prod.py      # Production-specific settings│    
│ ├── urls.py
│ └── wsgi.py
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
│   │   ├── js/                   # JavaScript files
│   │   │   ├── editUserProfile.js      # Send a PATCH request to the API for updating user details
│   │   │   ├── matchDeleteHighlight.js # On deletion update match card background dynamically
│   │   │   ├── matchEdit.js            # Update match card and form for editing
│   │   │   ├── passwordValidation.js   # Confirm password match
│   │   │   ├── playerLabelUpdater.js   # Update player labels dynamically on match form
│   │   │   ├── tabPaginationReset.js   # Update pagination dynamically on tab change
│   │   │   └── winningTeamHighlight.js # Update winning team card background
│   ├── templates/frontend/       # Folder containing Django templates
│   │   ├── _match_card.html      # Match history card to be included in match.html
│   │   ├── _pagination.html      # Reusable pagination component
│   │   ├── _user_form.html       # Reusable user form for register.html and user.html
│   │   ├── base.html             # Base template with common navigation bar & footer
│   │   ├── hall_of_fame.html     # Template for Hall of Fame
│   │   ├── hof_user_snippet.html # Template for mini table to be included in hall_of_fame.html
│   │   ├── login.html            # Template for user login
│   │   ├── match.html            # Template for adding and reviewing match results
│   │   ├── register.html         # Template for user registration
│   │   └── user.html             # Template for checking or editing user details
│   ├── __init__.py
│   ├── urls.py                   # URLs frontend configuration
│   └── views.py                  # Views logic to render the templates
```

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

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

## 🌐 Frontend Endpoints & Templates

### 🏗️ Foundation Template

All templates extend a base layout using `{% extends "base.html" %}` where `base.html` provides the site-wide layout, including the common navigation bar and standard footer. It serves as the foundation for all pages, ensuring a consistent look and feel across the site.

The navigation bar is:

- Collapsible on small screens.
- Sticky to the top on scroll.
- Links accessible to unauthenticated users are: Paddle HoF, Register, and Login.
- Links accessible to authenticated users are: Paddle HoF, Matches, User Profile (displaying the _current_ user's name in the navbar), and Logout.
- Matches link should display a badge with the number of _pending_ matches for the current user in that session. By clicking on the badge the user is redirected to the `match.html` page. The badge is only displayed if there are any pending matches.

### 🔗 URLs & Full Page Templates

These are the full-page templates directly mapped to URLs:

| URL                     | Purpose                               | Template Loaded     | Specs                                                                                                                                            |
| ----------------------- | ------------------------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `/`                     | Hall of Fame – ranked list of players | `hall_of_fame.html` | Table with wins, matches played, and rates for each player.                                                                                      |
| `/register/`            | User registration                     | `register.html`     | Dynamic checking of restrictions and load available players to choose from.                                                                      |
| `/login/`               | User login                            | `login.html`        | User & password fields and login button.                                                                                                         |
| `/logout/`              | User logout                           | N/A - View handled  | Logout link with bootstrap icon. _This action is a redirection._                                                                                 |
| `/users/<id>/`          | User details and editing              | `user.html`         | User profile stats and editable fields.                                                                                                          |
| `/matches/`             | Match results and editing             | `match.html`        | Form for adding and editing matches, and match history, filtered only for the user or non filtered for all players. Displays the list of matches using `_match_card.html`. |
| `/matches/<id>/delete/` | Delete match                          | N/A - View handled  | Trash button with bootstrap icon. _This action is a redirection_.                                                                                |

### 📂 Partial & Reusable Templates

These partial templates are reusable components designed to be included in other templates using `{% include %}`:

- `_match_card.html`: Displays match cards to be used in the tabs of the Match History section of `match.html`. Includes teams with color indication for winning team in green background, date played with a "new!" badge indication for _not yet reviewed_ matches by the user in that session, and delete and edit buttons for matches where the user is a participant. The edit button let the user edit his own matches.

- `_user_form.html`: A dynamic form for creating and editing users. Reused in both `register.html` (for new users) and `user.html` (for editing allowed fields of the user profile).

- `_pagination.html`: A reusable template for pagination, used in `hall_of_fame.html` and `match.html`. It shows current page number with indication of total pages,"Rewind", "Fast Forward" and following and previous page number, any of them showed only when available.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🛠️ JavaScript Functionalities

- `passwordValidation.js`: Checks if the password and confirm password fields match, and dynamically displays an error message if they don't. Is used in `register.html`.
- `playerLabelUpdater.js`: The label of the player input field updates dynamically as the user types, based on the input value to distinguish between registered players, existing (but not registered) players, and new players in the form fields of `match.html`.
- `winningTeamHighlight.js`: Dynamically updates the background of the "Team 1" and "Team 2" cards in the form fields of `match.html` based on the selection of the "winning_team" radio button with green background for the winning team.
- `matchDeleteHighlight.js`: Dynamically updates the background of the match card in the form fields of `match.html` to indicate deletion _before sending the DELETE request_.
- `matchEdit.js`: Allows editing of match details in `match.html`. The Edit button is only visible in matches of the match history section where the current user is a participant. By clicking on the edit button in a match card, the following happens:
  - The selected match card to be edited is highlighted.
  - The form in `match.html` is pre-filled with the data of the selected match.
  - The html is focused on the form.
  - The "Add Match" button is changed to "Edit Match". When the user clicks "Edit Match", the endpoint of the API is called by PUT (the API will delete the match and create a new one) .
  - A "Cancel Edit" button is added to the form, which allows canceling the edit and reloads the default `match.html`.
- `editUserProfile.js`: Allows editing of allowed user details in `user.html`. _Only the email field has been flagged as editable so far._ By changing the value on the email field in the user profile, "Cancel Changes" and "Save Changes" buttons are enabled:
  - When the user clicks "Save Changes", the endpoint of the API is called by PATCH.
  - When the user clicks "Cancel Changes", the form is reset to the original values.
- `tabPaginationReset.js` is loaded with match.html for:
  - Showing the correct pagination on initial load based on the active tab;
  - Hiding the inactive tab’s pagination;
  - Resetting pagination to page 1 when switching between tabs.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🔄 Pagination

This application implements pagination to efficiently handle and display large datasets of players and matches. Pagination is applied to the Hall of Fame and Match History views, ensuring a smooth and responsive user experience, even with extensive data.

### Backend Pagination (Django REST Framework)

The backend utilizes Django REST Framework's (DRF) built-in pagination capabilities. This provides a standardized way to paginate API responses.

- **How it Works:** When requesting a paginated endpoint (e.g., `/api/games/players/` or `/api/games/matches/`), the API will return a subset of the data along with metadata about the pagination.
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

## 🧪 Testing

The project comes with a suite of tests for the `games`, `users`, and `frontend` apps. The tests can be run using the `pytest` command from the project's root directory. These tests cover authentication, authorization and model logic. Frontend template rendering tests are left for future development.

The test files follow the naming conventions:

- `games/tests/test_permissions.py`
- `games/tests/test_players.py`
- `games/tests/test_stats.py`
- `users/tests/test_authentication.py`
- `users/tests/test_permissions.py`
- `users/tests/test_register.py`

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🚀 Future Enhancements

This section details the planned improvements for the Paddle Tennis Hall of Fame application, organized by priority and complexity into short-term, medium-term, and long-term goals.

### Short-Term Enhancements (High Priority & Simple)

These are relatively easy to implement and will quickly improve the application's value.

1. **Americano tournament application:**
    - **Description:** Add a feature to allow users to apply to an Americano tournament, arrange matches, add and view match results and at the end of the tournament when all matches are played, displays the final results.
    - **Benefit:** Engage new players in every Americano tournament.
    - **Implementation Details:**
        - Add a new "Americano" menu item to the navigation bar.
        - Create a new API endpoint for the "Americano" tournament.
        - Create a new frontend view for the "Americano" tournament application.
        - Create a new frontend template for the "Americano" tournament application.
        - Add "Americanos played" and "Americanos positions" fields to the `Player` model.
        - Add "Americano stats" in the player details.

2. **Match Confirmation System:**
    - **Description:** Introduce a system for users to confirm their participation in matches.  A "pending confirmation" badge will replace the current "not seen" badge on unconfirmed matches. Users can confirm matches via a new "Confirm" button or by using the existing "Edit" or "Delete" buttons. Each user can only confirm a match once. The navigation bar will display the total number of matches using a badge with that number awaiting confirmation by the current user. The user who created the match is automatically considered to have confirmed it.
    - **Benefit:** Enhances data accuracy and user engagement by requiring verification of match results from all participants.
    - **Implementation Details:**
        - Add a `created_by` field (User ID and name) to the `Match` model to track the match creator.
        - Add a `confirmed_by` field (User IDs and names) to the `Match` model to track confirmations.
        - Automatically add the `created_by` user's ID and user name to the `confirmed_by` list upon match creation.
        - Add the user's ID to the `confirmed_by` list when they edit a match or click the _Confirm_ button.
        - Update the navigation bar badge to show the number of matches pending confirmation for the current user.
        - Use the current _New!_ badge to highlight matches awaiting confirmation of the current user, and display "Confirm," "Edit," and "Delete" buttons in the `_match_card.html` template only in those matches.

3. **User Password Management:**
    - **Description:** Allow users to change or reset their passwords.
    - **Benefit:** Enhances user account security and usability.
    - **Implementation Notes:** Leverage Django's built-in authentication and password reset views, potentially integrating an email service for reset links. The email field in `models.py` should not be left blank, as the reset link will not work if it is.

### Medium-Term Enhancements (Important & Moderately Complex)

These enhancements are more involved but will significantly improve the application's functionality and user experience.

1. **Hall of Fame Background Video:**
    - **Description:** Add a short video or animated loop in the landing page background.
    - **Benefit:** Enhance visual appeal and user engagement.
    - **Implementation Note:** Use a lightweight video format to prevent slowing down page loading. Consider lazy loading or conditional playback for mobile devices.

2. **User Profile Avatars:**
    - **Description:** Integrate randomized avatar images for player profiles.
    - **Benefit:** Adds visual appeal and personalization to user profiles.
    - **Implementation Note:** Utilize an avatar generation API (e.g., `https://avatars.dicebear.com`) or a set of default local images.

3. **Multiple Groups of Friends:**
    - **Description:**  Enhance the application to support multiple, independent groups of friends, each with its own isolated data. Each group will have its own unique Hall of Fame, players, matches, and users, completely separate from other groups. A new landing page will allow visitors to enter a group code to access a specific group's data. Visitors can explore the group's public information only if they know the group code, and later register to become a full user within that group.
    - **Benefit:**  Significantly expands the application's utility by enabling multiple, unrelated groups of friends to use the platform independently. This increases the potential user base and fosters a sense of community within each group. Also enhances security and privacy by isolating data and access controls within each group.
    - **Implementation Details:**
        - **Group Model:**
            - Introduce in the `users` app a new `Group` model to represent each group of friends.
            - `name`: A user-friendly name for the group.
            - `code`: A unique, admin generated code for group access. This code will be used by visitors to access the group's landing page.
        - **Group Association:**
            - Add a `group` foreign key field to the `User`, `Player`, and `Match` models to link them to a specific group.
            - Users, players, and matches will belong to one and only one group.
            - When a new user registers they will be automatically associated with the group where they was visiting.
            - Visitors who know the group code can access the group's landing page to view public information (e.g., the Hall of Fame) without registering.
            - Only authenticated users of that group can create new matches.
            - When a new match is created, it will be automatically associated with the group of the user who created it.
        - **Data Isolation:**
            - Modify API endpoints and database queries to filter data based on the user's associated group.
            - Ensure that users can only access and manipulate data (players, matches, etc.) that belongs to their group.
        - **Landing Page:**
            - Create a new landing page with a form to enter a group code.
            - If the code is valid:
                - Redirect the visitor to the Hall of Fame page for that group.
                - Display in the Navbar indication of the group's name.
                - Provide options for visitors to log in or register to become a user of that group.
                - No need to enter the code again in the same session of that user or visitor for future group access, as it is stored in the session and the landing page will be the HoF for that group.
            - If the code is invalid, display a error message and implement security measures to prevent brute-force attempts to guess group codes.
        - **Group Management:**
            - Only admin users can create, update, delete or change code groups.
        - **Navigation:**
            - Update the navigation bar to display the name of the current group the visitor or user is viewing.            -
        - **Considerations:**
            - **Permissions:** Visitors of that group (not logged in users) shall have the same permissions as current non-authenticated users.

### Long-Term Enhancements (Complex & Strategic)

These enhancements represent major architectural or feature additions that will require significant effort but will transform the application.

1. **Social Authentication:**
    - **Description:** Allow users to sign up and log in using social accounts (Google, Facebook, etc.).
    - **Benefit:** Streamlines the registration process and enhances user convenience.
    - **Implementation Note:** Integrate `django-allauth` to add social authentication options.

2. **Frontend Migration to SPA:**
    - **Description:** Transition the frontend from a Multi-Page Application (MPA) to a Single-Page Application (SPA) using React.
    - **Benefit:** Provides a more dynamic and responsive user experience, improved navigation, and a more modern UI.
    - **Implementation Note:** Use Django REST Framework (DRF) for the backend API and React for the frontend, ensuring a clear separation of concerns.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🚀 Installation

### 📋 Prerequisites

- Python 3.8 or higher: Required to run Django 5.x and supported packages.
- pip (Python package manager): comes pre-installed with Python.
- Git (for cloning the repository)
- virtualenv (recommended, for creating isolated environments)

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

#### 🚀 PythonAnywhere Deployment

- Clone your repo on PythonAnywhere:

```bash
git clone https://github.com/mrGit-bit/paddle.git
cd paddle
```

- Create and activate a virtual environment:

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Create a .env file with your production settings (see above).

- Apply migrations and collect static files:

```bash
python manage.py migrate
python manage.py collectstatic
```

- In your PythonAnywhere Web settings:
  - Set the working directory to `/home/yourusername/paddle`
  - Set the virtualenv path to `/home/yourusername/paddle/venv`
  - Edit the WSGI file to load:

```bash
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
```

- Reload your web app from the PythonAnywhere dashboard.

- Access the app at `https://yourusername.pythonanywhere.com/`

#### Switching Between Environments

The settings module is chosen automatically based on the `.env` variable:

| Mode        | `DJANGO_ENVIRONMENT` | Settings File           |
|-------------|--------------------|-------------------------|
| Development | `dev`                | `config/settings/dev.py`  |
| Production  | `prod`               | `config/settings/prod.py` |

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.
