<!-- markdownlint-disable MD051 -->
<!-- markdownlint-disable MD033 -->
# 🏆 Paddle Tennis Hall of Fame

## 📖 Overview

This is a web application built using Django and Django Rest Framework (DRF) in the backend for managing a "Hall of Fame" for a group of paddle tennis players.

The app features a front-end built with Django templates, JavaScript, and Bootstrap for styling. Users can view player rankings, detailed match records, and player profiles.

<a id="index"></a>

### 🔗 Index

- [📖 Overview](#📖-overview)
- [✨ Key Features & Implementation](#✨-key-features--implementation)
- [🛠️ Technologies Used](#🛠️-technologies-used)
- [🕹️ Usage Verification](#🕹️-usage-verification)
- [🗂️ Project Structure](#🗂️-project-structure)
- [📋 App Explanations](#📋-app-explanations)
- [📡 API Endpoints](#📡-api-endpoints)
- [🚀 Future Enhancements](#🚀-future-enhancements)
- [🚀 Installation](#🚀-installation)

---

### ✨ Key Features & Implementation

- **🏅 Hall of Fame Rankings**:
  - *Feature*: Displays a ranked list of paddle tennis players based on the number of matches won.
  - *Implementation*: The `PlayerViewSet` in `views.py` allows viewing players, and their `wins` field is serialized by `PlayerSerializer`. To rank players by the number of wins, the queryset includes ordering by `wins` field.

- **🎮 Match Results**:
  - *Feature*: Registered users can add results for matches,each involving two teams of two players each. New players are created if they didn't exist before the match is created.
  - *Implementation*:
    - The `Match` model contains a `teams` field represented as a JSON dictionary, and the view allows for creation and updating of matches (`MatchViewSet`). Only registered users can create or update match records.
    - The logic for creating new players (when they don't already exist) is into the `MatchSerializer` in the `create` and `update` methods of the serializer. There is also logic here to avoid player duplicates in the same match.
    - A helper function called `extract_players` within the `MatchSerializer` is used for extracting player lists. This function is used in both the `validate`, `create`, and `update` methods.
    - Match statistics are updated via the `perform_create()` and `perform_update()` methods in the `MatchViewSet`, ensuring that the stats for each player are kept current.

- **📋 Player Details**:
  - *Feature*: Registered users can view a detailed profile for each player, including all matches they have played.
  - *Implementation*:
    - The `PlayerViewSet` provides access to the detailed profiles of each player. Player information such as wins, losses, and matches played are serialized and made available.
    - `PlayerSerializer` includes a `matches` field that provides a list of matches involving each player. This is implemented using a `SerializerMethodField` that retrieves related matches for the given player.
  
- **🔒 Authentication**:
  - *Feature*: Only registered users can add or update match results and view player details.
  - *Implementation*:
    - The default permission is set to `IsAuthenticatedOrReadOnly`, which means non-registered users can view basic information such as the Hall of Fame rankings (so `PlayerViewSet` allows read access).
    - The `permission_classes` in `MatchViewSet` is set to `[IsAuthenticated]`, which ensures that only authenticated users can create or update match results.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🛠️ Technologies Used

- **Backend**: Django Rest Framework (DRF)
  - with ModelViewSets, ModelSerializers and Routers for simplicity managing the API.
  - using built-in session authentication provided by DRF.
- **Frontend**:
  - Django Templates,
  - JavaScript,
  - Bootstrap.
- **Database**: SQLite for development and testing purposes.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🕹️ Usage Verification

### ➕ Add Match Results

Users need to be registered to add match results, and they must manually enter player information, which is allowed by the `MatchSerializer`.

### 📜 View Hall of Fame

Anyone (including unauthenticated users) can view player rankings. The Hall of Fame rankings are accessible through the `PlayerViewSet`, which supports read-only access for non-authenticated users.

### 👤 Player Profiles

Registered users can view detailed player information, including match history for each player.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🗂️ Project Structure

```bash
paddle/
├── config/            # Project configuration and settings
├── api/               # API apps
│   ├── games/         # API app for players & matches
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── models.py  # Models for players & matches
│   │   ├── urls.py
│   │   └── tests.py   
│   └── users/         # App for managing registered users
│       ├── serializers.py
│       ├── views.py
│       ├── models.py  # Optional custom user model 
│       ├── urls.py
│       └── tests.py   # Tests for users API
├── frontend/          # Non Django templates and JavaScript
│   ├── js/            # JavaScript files
│   ├── css/           # Stylesheets
│   └── html/          # Static HTML files
├── static/            # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/         # Django HTML templates
│   ├── base.html
│   ├── players/
│   │   ├── list.html
│   │   └── detail.html
│   ├── matches/
│       ├── list.html
│       └── detail.html
│   └── users/
│       ├── login.html
│       ├── register.html
│       └── profile.html
├── requirements.txt   # Dependencies for the project
└── manage.py          # Django entry point
```

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 📋 App Explanations

**`games/`**: The `games` app manages both players and matches.

- **Player-Related**:
  - Players may be registered or non-registered users.
  - A non-registered player can be linked to a new user using the `player_id` provided in the `UserSerializer` (`serializers.py`).
  - If a new user links with a non-registered player, they inherit their stats.
- **Match-Related**: Matches involve two teams of two players each, and the `winning_team` field is used to update player stats accordingly

**`users/`**: Manages user registration, login, logout, linking of existing non-registered players, and user profiles management.

- **User Registration**:
  - The `UserViewSet` allows anyone to create a new user (`permission_classes` = [`AllowAny`]).
  - The `UserSerializer` includes a `player_id` field that allows new users to link with existing non-registered players.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 📡 API Endpoints

`/api/players/`: Provides access to the Hall of Fame (list of all players). The endpoint is open to anyone, which complies with the requirement to allow unauthenticated users to view the Hall of Fame.

`/api/players/<id>/`: Provides detailed information about a specific player. Only authenticated users can access it.

`/api/matches/`: Allows registered users to list matches and create new ones.

`/api/matches/<id>/`: Allows editing of match details, restricted to authorized users.

`/api/users/register/`: Allows new users to register.

`/api/users/login/`: Login endpoint to authenticate users.

`/api/users/profile/`: Allows authenticated users to view a list of other users' profiles, including stats.

`/api/users/profile/<id>/`: Place where users can update their details.

<div style="text-align: right"><a href="#index">Back to Index</a></div>

---

## 🚀 Future Enhancements

- Add a leaderboard filter for date ranges.
- Enable advanced statistics for each player.
- Integrate user profiles with customizable avatars.
- Support live match updates using WebSockets.

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
