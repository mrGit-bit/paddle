<!-- markdownlint-disable MD051 -->
<!-- markdownlint-disable MD033 -->
# 🏆 Paddle Tennis Hall of Fame

## 📖 Overview

This is a web application built using:

- Django and Django Rest Framework (DRF) in the backend for managing a "Hall of Fame" for a group of paddle tennis players.

- The app features a front-end built with Django templates, JavaScript, and Bootstrap for styling. Users can update match results, view player rankings, get some statistics and player profiles.

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

- Allows registered users to add results for matches (two teams, each with two players) and update results for matches they've played.
- Automatically creates new players if they don't already exist.
- **Implementation**:
  - The `MatchSerializer` includes logic to accept player names, create new players if needed, and validate player duplicates.
  - `perform_create()` in the `MatchViewSet` ensures match creation updates player stats dynamically.
  - The `perform_update()` method resets old match stats before applying new results to ensure correctness.

#### User Management

- When a new user is created linking to an existing player shall be optional. If not linked, the user is added as a new player with stats set to zero, and the player's name is the username. If linked, the user assumes the stats of the player, and the player's name becomes the username.
- **Implementation**:
  - The `UserSerializer` includes a `player_id` field for optional linking with existing non-registered players.
  - The `UserViewSet` ensures users can only update or delete their own profiles (unless the user is an admin).

#### Player Details

- Provides detailed profiles for each player, including stats like wins, matches played, number of matches played, win rate, and losses. Only admin users can update or delete players.
- **Implementation**:
  - The `PlayerSerializer` includes dynamically calculated fields: `matches_played`, `losses`, and `win_rate`.
  - The `PlayerViewSet` restricts modification of player profiles to admin users.

#### Authentication & Permissions

- Non-registered users can only view Hall of Fame rankings and register. Only registered users can add or update match results. A user can only update or delete their own profiles or match results. Admin users can do anything, including creating, updating, and deleting matches,  players and users.
- **Implementation**:
  - DRF's built-in session authentication is used.
  - The `IsAuthenticatedOrReadOnly` permission class allows non-registered users to view player rankings.
  - The `IsAuthenticated` permission class ensures match-related actions are restricted to authenticated users.
- Registered users can login and logout using the provided endpoints.
- **Implementation**:
  - Authenticate users using session-based authentication.
  - The `LoginView` and `LogoutView` endpoints handle user authentication and logout.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🛠️ Technologies Used

- **Backend**: Django Rest Framework (DRF)
  - with `ModelViewSets`, `ModelSerializers` with `SerializerMethodField` and `Routers` for simplicity managing the API.
  - using built-in session authentication provided by DRF.
- **Frontend**:
  - Django Templates,
  - JavaScript,
  - Bootstrap.
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
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── templates/frontend/       # Django templates
│   │   ├── base.html             # Base template with common navigation bar & footer
│   │   ├── register.html         # Template for user registration
│   │   ├── login.html            # Template for user login
│   │   ├── player_details.html   # Template for player details and stats
│   │   ├── user_details.html     # Template for editing user details
│   │   ├── match_results.html    # Template for adding match results
│   │   ├── stats.html            # Template for statistics
│   │   └── hall_of_fame.html     # Template for Hall of Fame
│   ├── static/frontend/          # Static files for the frontend
│   │   ├── css/                  # Stylesheets
│   │   │   └── styles.css
│   │   ├── js/                   # JavaScript files
│   │   │   └── hall_of_fame.js   # JavaScript for interacting with the API
│   │   └── images/               # Images
│   ├── urls.py                   # URL routing for template views
│   └── views.py                  # Views to render templates
├── README.md          # Project documentation
├── requirements.txt   # Dependencies for the project
└── manage.py          # Django entry point
```

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 📡 API Endpoints

### Endpoints for the `games` app

The `games` app manages both players and matches.

`/api/games/players/`:

- `GET` Provides access to the **Hall of Fame** with a ranked list of all players. Open to anyone.
- `POST` Creates a new player. Is Admin only.

`/api/games/players/<id>/`:

- `GET` Provides detailed information about a specific player. Only authenticated users can access it.
- `PUT` & `PATCH` Updates a player's information. Admin only.
- `DELETE` Deletes a player. Admin only.

`/api/games/matches/`:

- `GET` Allows registered users to list all matches
- `POST` Allows registered users to add matches by creating new ones.

`/api/games/matches/<id>/`:

- `GET` Allows registered users to view details of a specific match.
- `PUT` & `PATCH` Allows editing of match details, restricted to authorized users of that match.
- `DELETE` Deletes a match. Restricted to authorized users of that match.

### Endpoints for the `users` app

Manages user registration, login, logout, linking of existing non-registered players, and user profiles management.

`/api/users/`:

- `POST` Allows new users to register. Open to anyone.
- `GET`List of other users' profiles, including stats. For authenticated users.

`/api/users/profile/<id>/`:

- `GET` View a specific user's profile. Authenticated users.
- `PUT` & `PATCH` Update a user's profile. Only the owner of the profile can.
- `DELETE` Delete a user's profile. Only the owner of the profile can.

`/api/users/login/`: `POST` Login endpoint to authenticate users. Open to anyone.

`/api/users/logout/`: `POST` Logout endpoint to log out users. Authenticated users.

### Endpoints for the `api-auth` browsable API

In development, the `api-auth` app provides endpoints for login and logout for the browsable API.

`/api-auth/login/`: Login endpoint for the browsable API.

`/api-auth/logout/`: Logout endpoint for the browsable API.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🚀 Future Enhancements

Starting from the simplest to the more complex:

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
