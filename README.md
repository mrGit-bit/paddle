<!-- markdownlint-disable MD051 -->
<!-- markdownlint-disable MD033 -->

# 🏆 Paddle Tennis Hall of Fame

## 📖 Overview

Paddle Tennis Hall of Fame is a web application designed for groups of friends who play paddle tennis together. It helps them manage their own "Hall of Fame" within their tennis club.

Registered users can track matches played, update match results, view player rankings, and access player statistics.

This web application is built using:

- Django and Django Rest Framework (DRF) for the RESTful API.
- Django templates, JavaScript, and Bootstrap for the frontend.

<a id="index"></a>

### 🔗 Index

- [📖 Overview](#📖-overview)
- [✨ Key Features & Implementation](#✨-key-features--implementation)
- [🛠️ Technologies Used](#🛠️-technologies-used)
- [🗂️ Project Structure](#🗂️-project-structure)
- [📡 API Endpoints](#📡-api-endpoints)
- [🌐 Frontend Endpoints & Templates](#🌐-frontend-endpoints--templates)
- [🛠️ JavaScript Functionalities](#🛠️-javascript-functionalities)
- [🧪 Testing](#🧪-testing)
- [🚀 Future Enhancements](#🚀-future-enhancements)
- [🚀 Installation](#🚀-installation)
- [🤝 Contributing](#🤝-contributing)
- [📄 License](#📄-license)

---

### ✨ Key Features & Implementation

#### Hall of Fame Rankings

- Displays a ranked list of paddle tennis players based on their number of wins.
- Publicly accessible (no authentication required).
- **Implementation**:
  - The `PlayerViewSet` in `views.py` retrieves players, ordering them by the `wins` field to create the ranking.
  - The `PlayerSerializer` uses `SerializerMethodField` to dynamically calculate `matches_played`, `losses`, and `win_rate`.

#### Match Results

- Authenticated users can add and update match results.
- Each match consists of two teams, each with two players.
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
- Users can only update or delete their own profiles, unless they are an admin.
- **Implementation**:
  - The `UserSerializer` includes a `player_id` field for optional linking to an existing player.
  - The `UserViewSet` restricts profile modification to the user's own profile or admins.

#### Player Details

- Provides detailed profiles for each player, including their match history and stats such as wins, matches played, win rate, and losses.
- Only admins can update or delete player details.
- **Implementation**:
  - The `PlayerSerializer` uses calculated fields: `matches_played`, `losses`, and `win_rate`.
  - The `PlayerViewSet` restricts player profile modification to admins.

#### Authentication & Permissions

- Unauthenticated users can only:
  - View the Hall of Fame.
  - Register.
  - Log in.
- Authenticated users can also:
  - Add match results.
  - Update or delete their own match results.
  - View and update their profile.
  - View player stats.
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
  - JavaScript.
  - Bootstrap 5.
- **Database**: SQLite for development and testing.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🗂️ Project Structure

```bash
paddle/
├── config/            # Project configuration and settings
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
├── frontend/          # Frontend logic and templates
│   ├── static/frontend/          # Static files for the frontend
│   │   ├── css/                  # Stylesheets
│   │   │   └── styles.css        # Custom styles for the frontend overriding Bootstrap styles
│   │   ├── js/                   # JavaScript files
│   │   │   ├── editUserProfile.js      # Send a PATCH request for updating user details
│   │   │   ├── matchDeleteHighlight.js # On deletion update match card background dynamically
│   │   │   ├── matchEdit.js            # Update match card and form dynamically
│   │   │   ├── passwordValidation.js   # Confirm password match
│   │   │   ├── playerLabelUpdater.js   # Update player labels dynamically on match form
│   │   │   └── winningTeamHighlight.js # Update winning team card dynamically on match form
│   ├── templates/frontend/       # Django templates
│   │   ├── _match_card.html      # Match history card to be included in match.html
│   │   ├── _user_form.html       # Reusable user form for register.html and user.html
│   │   ├── base.html             # Base template with common navigation bar & footer
│   │   ├── hall_of_fame.html     # Template for Hall of Fame
│   │   ├── login.html            # Template for user login
│   │   ├── match.html            # Template for adding and reviewing match results
│   │   ├── register.html         # Template for user registration
│   │   └── user.html             # Template for checking or editing user details
│   │   └── images/               # Images
│   ├── __init__.py
│   ├── test_frontend.py          # Tests for frontend
│   ├── urls.py                   # URL routing for template views
│   └── views.py                  # Views to render the templates
├── README.md          # Project documentation
├── requirements.txt   # Dependencies for the project
└── manage.py          # Django entry point
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

- `GET`: Returns a JSON dictionary with a list of registered users (players linked to a User account) and a list of non-registered players, both with their ID and name. Results are sorted alphabetically. Publicly accessible. Will be used:
  - During user registration: to provide a list of non-registered players to choose from;
  - When introducing new match results: to differentiate between registered players and new players.

### Endpoints for the `users` app

Manages user registration, login, logout, linking of existing non-registered players, and user profiles management.

`/api/users/`:

- `POST`: Allows new users to register. Publicly accessible. Checks if the username already exists.

`/api/users/<id>/`:

- `GET`: Returns the authenticated user's own profile. Only the authenticated user, owner of the profile or an admin can access it.
- `PATCH`: Updates a user's profile. Only the authenticated user, owner of the profile or an admin can modify it.
- `DELETE`: Deletes a user's profile. Only an admin can perform this action.

### Endpoints for the `api-auth` browsable API

In development, the `api-auth` app provides endpoints for login and logout for the browsable API.

`/api-auth/login/`: Login endpoint for the browsable API.

`/api-auth/logout/`: Logout endpoint for the browsable API.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🌐 Frontend Endpoints & Templates

### 🏗️ Foundation Template

All templates extend a base layout using `{% extends "base.html" %}` where:

- `base.html`: Provides the site-wide layout, including the common navigation bar and standard footer. It serves as the foundation for all pages, ensuring a consistent look and feel across the site. The navigation bar is:
  - Collapsible on small screens.
  - Sticky on scroll.
  - Links accessible to unauthenticated users: Paddle HoF, Register, and Login.
  - Links accessible to authenticated users: Paddle HoF, Matches, User Profile (displaying the _current_ user's name), and Logout.
  - Matches should display a badge with the number of _pending_ matches for the current user in that session. By clicking on the badge the user is redirected to the `match.html` page. The badge is only displayed if there are any pending matches. The matches in the dropdown are ordered by date.

### 🔗 URLs & Full Page Templates

These are the full-page templates directly mapped to URLs:

| URL                     | Purpose                               | Template Loaded     | Specs                                                                                                                                            |
| ----------------------- | ------------------------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `/`                     | Hall of Fame – ranked list of players | `hall_of_fame.html` | Table with wins, matches played, and rates for each player.                                                                                      |
| `/register/`            | User registration                     | `register.html`     | Dynamic checking of restrictions and load available players to choose from.                                                                      |
| `/login/`               | User login                            | `login.html`        | User & password fields and login button.                                                                                                         |
| `/logout/`              | User logout                           | N/A - View handled  | Logout link with bootstrap icon. _This action is a redirection._                                                                                 |
| `/users/<id>/`          | User details and editing              | `user.html`         | User profile stats and editable fields.                                                                                                          |
| `/matches/`             | Match results and editing             | `match.html`        | Form for adding and editing matches and match history, both for the user and all matches. Displays the list of matches using `_match_card.html`. |
| `/matches/<id>/delete/` | Delete match                          | N/A - View handled  | Trash button with bootstrap icon. _This action is a redirection_.                                                                                |

### 📂 Partial & Reusable Templates

These partial templates are reusable components designed to be included in full templates using `{% include %}`:

- `_match_card.html`: Displays a match card used in the tabs of the Match History section of `match.html`. With color indication for winning team in green background, date played with a badge indication for _not yet reviewed_ matches by the user in that session, and delete and edit buttons for matches where the user is a participant. The edit button let the user edit his own matches.

- `_user_form.html`: A dynamic form for creating and editing users. Reused in both `register.html` (for new users) and `user.html` (for editing profiles).

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🛠️ JavaScript Functionalities

- `passwordValidation.js`: Checks if the password and confirm password fields match, and dynamically displays an error message if they don't. Is used in `register.html`.
- `playerLabelUpdater.js`: The label of the player input field updates dynamically as the user types, based on the input value to distinguish between registered players, existing players, and new players in the form fields of `match.html`.
- `winningTeamHighlight.js`: Dynamically updates the background of the "Team 1" and "Team 2" cards in the form fields of `match.html` based on the selection of the "winning_team" radio button.
- `matchDeleteHighlight.js`: Dynamically updates the background of the match card in the form fields of `match.html` to indicate deletion _before sending the DELETE request_.
- `matchEdit.js`: Allows editing of match details in `match.html`. The Edit button is only visible in matches of the match history section where the current user is a participant. By clicking on the edit button in a match card, the following happens:
  - The selected match card to be edited is highlighted.
  - The form in `match.html` is pre-filled with the data of the selected match.
  - The html is focused on the form.
  - The "Add Match" button is changed to "Edit Match". When the user clicks "Edit Match", the endpoint of the API is called by PUT.
  - A "Cancel Edit" button is added to the form, which allows canceling the edit and reloads the default `match.html`.
- `editUserProfile.js`: Allows editing of allowed user details in `user.html`. _Only the email field is editable._ By changing the value on the email field in the user profile, "Cancel Changes" and "Save Changes" buttons are enabled:
  - When the user clicks "Save Changes", the endpoint of the API is called by PATCH.
  - When the user clicks "Cancel Changes", the form is reset to the original values.

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

- **How it Works:** The frontend dynamically generates pagination links based on the `next` and `previous` URLs provided in the API response.
- **Implementation:** The pagination component is implemented in the `hall_of_fame.html` and `match.html` templates. The same component is reused in both templates.
- **User Experience:** The pagination component seamlessly integrates with the application's design, allowing users to easily navigate between pages of players or matches. It displays the current page number and provides links to the previous and next pages, if available.
- **Dynamic Rendering:** The pagination component is dynamically rendered based on the data received from the API, ensuring that the correct number of pages and navigation links are displayed.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.
