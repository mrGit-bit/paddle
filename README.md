<!-- markdownlint-disable MD051 -->
<!-- markdownlint-disable MD033 -->
# 🏆 Paddle Tennis Hall of Fame

## 📖 Overview

Paddle Tennis Hall of Fame is a web application that allows users to manage a "Hall of Fame" for a group of friends playing paddle tennis in their tennis club.

Registered users can keep track of matches played, update their match results, view player rankings and get some player stats.

This is a web application built using:

- Django and Django Rest Framework (DRF) to build a RESTful API.

- Django templates for the HTML pages, JavaScript for interactivity in those pages, and Bootstrap for styling.

<a id="index"></a>

### 🔗 Index

- [📖 Overview](#📖-overview)
- [✨ Key Features & Implementation](#✨-key-features--implementation)
- [🛠️ Technologies Used](#🛠️-technologies-used)
- [🗂️ Project Structure](#🗂️-project-structure)
- [📡 API Endpoints](#📡-api-endpoints)
- [🚀 Future Enhancements](#🚀-future-enhancements)
- [🚀 Installation](#🚀-installation)

---

### ✨ Key Features & Implementation

#### Hall of Fame Rankings

- Displays a ranked list of paddle tennis players based on the number of matches won.
- Accessible to anyone (unauthenticated users).
- **Implementation**:
  - The `PlayerViewSet` in `views.py` enables viewing players. Player ranking is achieved by ordering the queryset by the `wins` field.
  - The `PlayerSerializer` uses `SerializerMethodField` to calculate dynamic fields like `matches_played`, `losses`, and `win_rate`.

#### Match Results

- Allows registered users to add results for matches (two teams, each with two players) and update results for matches they've played:
  - When adding a new match, players are created if they don't already exist.
  - When creating, updating or deleting a match, the user should be one of the participants of the match.
- **Implementation**:
  - The `MatchSerializer` includes logic to accept player names, create new players if needed, and avoid player duplicates.
  - `perform_create()` in the `MatchViewSet` ensures match creation updates player stats dynamically.
  - The `perform_update()` method resets old match stats before applying new results to ensure correctness.

#### User Management

- Allows users to register, login and check & modify its own profile:
  - When a new user is being created, the user can choose to link with an existing player.
  - When not linked to any player, the user is added as a new player with stats set to zero, and the player's name will be the username.
  - If player is linked, the user assumes the stats of the player, and the player's name is changed to be the username.
  - Users can only update or delete their own profiles (unless the user is an admin).
- **Implementation**:
  - The `UserSerializer` includes a `player_id` field for the above mentioned optional linking with an existing non-registered player.
  - The `UserViewSet` ensures users can only update or delete their own profiles (unless the user is an admin).

#### Player Details

- Provides detailed profiles for each player, including a list of matches played and player stats like wins, matches played, number of matches played, win rate, and losses. Only admin users can update or delete players details.
- **Implementation**:
  - The `PlayerSerializer` includes dynamically calculated fields: `matches_played`, `losses`, and `win_rate`.
  - The `PlayerViewSet` restricts modification of player profiles to admin users.

#### Authentication & Permissions

- Non-registered users can only view:
  - Hall of Fame;
  - register; and,
  - login.  

- Registered users can also:
  - add match results;
  - update or delete their own match results;
  - review and update their own profile;
  - view player stats.
  
- Admin users can do anything, including creating, updating, and deleting matches, players and users.

- **Implementation**:
  - DRF's built-in session authentication is used.
  - The `IsAuthenticatedOrReadOnly` permission class allows non-registered users to view player rankings.
  - The `IsAuthenticated` permission class ensures match-related actions are restricted to authenticated users.
- Registered users can login and logout using the provided endpoints.
- **Implementation**:
  - Authenticate users using session-based authentication.
  - The `LoginView` and `LogoutView` API endpoints handle user authentication and logout.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🛠️ Technologies Used

- **Backend**: Django Rest Framework (DRF)
  - with `ModelViewSets`, `ModelSerializers` with `SerializerMethodField` and `Routers` for simplicity managing the API.
  - using built-in session authentication provided by DRF.
- **Frontend**:
  - Django Templates,
  - JavaScript,
  - Bootstrap 5.
- **Database**: SQLite for development and testing purposes.

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

All API endpoints follow the [RESTful API design](https://restfulapi.net/) principles.

### Endpoints for the `games` app

The `games` app manages both players and matches.

`/api/games/players/`:

- `GET` Provides access to the **Hall of Fame** with a ranked list of all players. Open to anyone.
- `POST` Creates a new player. Is Admin only.

`/api/games/players/<id>/`:

- `GET` Provides detailed information about a specific player. Only authenticated users can access it.
- `PUT` & `PATCH` Updates a player's information. Admin only.
- `DELETE` Deletes a player. Admin only.

`/api/games/matches/?player=<player_name>`:

- `GET` All matches, or filtering matches by a specific player. Allows registered users viewing match history and display the form for adding match results:
  - When there is no query parameter, all matches are shown ordered by date.
  - When query parameter is specified, only matches played by the player_name are shown ordered by date.

`/api/games/matches/`:

- `POST` Allows registered users to add matches by creating new ones. Also players are created if they don't already exist. The user should be one of the participants of the match.

`/api/games/matches/<id>/`:

- `PUT` & `PATCH` Allows editing of match details. This is restricted to match participants.
- `DELETE` Deletes a match. Restricted to match participants.

`/api/games/players/player_names/`

- `GET` Custom endpoint to return a JSON dictionary with a list of registered users (players linked to a User account) and a list of non-registered players both with their ID and name. Results are sorted alphabetically. Open to anyone and will be used:
  - during user registration: to provide a list of non registered players to choose from;
  - and when introducing new match results: to differentiate between registered players and new players.

### Endpoints for the `users` app

Manages user registration, login, logout, linking of existing non-registered players, and user profiles management.

`/api/users/`:

- `POST` Allows new users to register. Open to anyone. Check if username already exists.

`/api/users/<id>/`:

- `GET` View the user's own profile. Only the owner of the profile can.
- `PUT` & `PATCH` Update a user's profile. Only the owner of the profile can.
- `DELETE` Delete a user's profile. Only the owner of the admin can.

### Endpoints for the `api-auth` browsable API

In development, the `api-auth` app provides endpoints for login and logout for the browsable API.

`/api-auth/login/`: Login endpoint for the browsable API.

`/api-auth/logout/`: Logout endpoint for the browsable API.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🌐 Frontend Endpoints & Templates

### 🏗️ Foundation Template

All templates extend a base layout using `{% extends "base.html" %}` where:

- `base.html`: Provides the site-wide layout, including the common navigation bar and standard footer. It serves as the foundation for all pages, ensuring a consistent look and feel across the site.

### 🔗 URLs & Full Page Templates

These are the full-page templates directly mapped to URLs:

|URL| Purpose|Template Loaded|
|---|---|---|
|`/` | Hall of Fame – ranked list of players |`hall_of_fame.html`|
|`/register/` | User registration |`register.html`|
|`/login/` | User login |`login.html`|
|`/logout/` | User logout |N/A - View handled|
|`/users/<id>/` | User details and editing |`user.html`|
|`/matches/` | Match results and editing |`match.html`|
|`/matches/<id>/delete/` | Delete match |N/A - View handled|

### 📂 Partial & Reusable Templates

These partial templates are reusable components designed to be included in full templates using `{% include %}`:

- `_match_card.html`: Displays a match card used in the tabs of Match History section of `match.html`.
  
- `_user_form.html`:A dynamic form for creating and editing users.
Reused in both `register.html` (for new users) and `user.html` (for editing profiles).

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🛠️ JavaScript functionalities

- `passwordValidation.js`: checks if the password and confirm password fields match, and displays dynamically an error message if they don't. Is used in `register.html`.
- `playerLabelUpdater.js`: the label of the player input field updates dynamically as the user types, based on the input value to distinguish between registered players, existing players, and new players in the form fields of `match.html`.
- `winningTeamHighlight.js`: dynamically updates the background of the "Team 1" and "Team 2" cards in the form fields of `match.html` based on the selection of the "winning_team" radio button.
- `matchDeleteHighlight.js`: dynamically updates the background of the match card in the form fields of `match.html` when the delete button is pressed.
- `matchEdit.js`: allows editing of match details in `match.html`. By clicking on the edit button in a match card in the match history (the Edit button is only visible in matches where the current user is a participant):
  - the selected match card to be edited is highlighted;
  - the form in match.html is pre-filled with the data of the match;
  - the html is focused on the form;
  - the "Add Match" button is changed to "Edit Match". When the user clicks "Edit Match", the endpoint of the API is called by PUT;
  - a "Cancel Edit" button is added to the form, which allows canceling the edit and reloads  the default match.html.
- `editUserProfile.js`: allows editing of allowed user details in `user.html`. Only the email field is editable. By changing the value on the email field in the user profile, "Cancel Changes" and "Save Changes" buttons are enabled:
  - When the user clicks "Save Changes", the endpoint of the API is called by PATCH.
  - When the user clicks "Cancel Changes", the form is reset to the original values.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🧪 Testing

The project comes with a suite of tests for the `games`, `users` and `frontend` apps. The tests can be run using the `pytest` command.

These are the files for testing:

- `games/tests/test_permissions.py`
- `games/tests/test_players.py`
- `games/tests/test_stats.py`
- `users/tests/test_authentication.py`
- `users/tests/test_permissions.py`
- `users/tests/test_register.py`
- `frontend/test_frontend.py`

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🚀 Future Enhancements

Starting from the simplest to the more complex features:

### **Match model**

- Modify the match model in `games/models.py` to support the new fields: `created_at`, `updated_at` and `created_by`.

### **User Management**

- **Allow New Users to Link with More Than One Non-Registered Player**:
  - Users can link their accounts with multiple non-registered players' assuming their stats by adding their outcomes, allowing seamless integration of historical data.
  - **Implementation Note**: Modify the player model and user registration workflow to support multiple link to several players.

- **Allow Users to Change/Reset Their Passwords**:
  - Provide options for users to update their passwords or initiate a reset if they forget.
  - **Implementation Note**: Use Django's built-in authentication and password reset views, with an email service to send reset links.

### **Security**

- **Allow Social Authentication (Google, Facebook, etc.)**:
  - Let users sign up or log in using third-party authentication services.
  - **Implementation Note**: Integrate `django-allauth` to add social authentication options.

### **Frontend Enhancements**

- **Move the Frontend from MPA (Multi-Page Application) to SPA (Single-Page Application) with React**:
  - Transition the frontend to React for a more dynamic user experience, improved navigation, and more modern UI interactions.
  - **Implementation Note**: Use Django Rest Framework (DRF) to provide a backend API and React for the frontend, ensuring the separation of concerns.

### **User Experience**

- **Integrate User Profiles with Randomized Images for Player Avatars**:
  - Assign randomized avatar images to players for a more personalized and visually engaging profile.
  - **Implementation Note**: Use an avatar generation API (e.g., `https://avatars.dicebear.com`) or a default set of local images to choose from in case the API is not available.

- **Add a Reel Video in the Background of the Hall of Fame Loading Page**:
  - Include a short video or animated loop in the Hall of Fame page background to enhance visual appeal.
  - **Implementation Note**: Use a lightweight video format to prevent slowing down page loading. Consider lazy loading or conditional playback for mobile devices.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🚀 Installation

### 📋 Prerequisites

1. Python 3.8 or higher
2. pip (Python package manager)
3. pytest (for running tests)

### 🏗️ Steps

1. Clone the repository:  
   `git clone https://github.com/your-repo/paddle.git`  
   `cd paddle`

2. Create and activate a virtual environment:  
   `python -m venv venv`  
   `source venv/bin/activate` (For Windows: `venv\Scripts\activate`)

3. Install dependencies:  
   `pip install -r requirements.txt`

4. Configure the database in `settings.py`:  
   - Update the `DATABASES` setting with your PostgreSQL credentials or use the default SQLite for development.

5. Apply migrations:  
   `python manage.py migrate`

6. Create a superuser:  
   `python manage.py createsuperuser`

7. Run the development server:  
   `python manage.py runserver`

8. Access the app at:  
   `http://127.0.0.1:8000/`

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

---

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.
