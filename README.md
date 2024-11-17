# 🏆 Paddle Tennis Hall of Fame

## 📖 Overview

This is a web application built using Django and Django Rest Framework (DRF) for managing a "Hall of Fame" for paddle tennis players. 

The app features a front-end built with Django templates and JavaScript. Users can view player rankings, detailed match records, and player profiles.

### ✨ Key Features

- **🏅 Hall of Fame Rankings**:
  - Displays a ranked list of paddle tennis players based on the number of matches won.
- **🎮 Match Results**:
  - Registered users can add results for matches.
  - Matches are between two teams of two players each.
  - Matches can include non-registered players by entering their names manually.
- **📋 Player Details**:
  - View a detailed profile for each player, including all matches they’ve played.
- **🔒 Authentication**:
  - Only registered users can:
   - add or update match results;
   - view player details.

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

---

## 🕹️ Usage

### ➕ Add Match Results

1. Log in as a registered user.
2. Navigate to the "Add Match" page.
3. Enter match details, including player names (pick from registered users or introduce unregistered).
4. Submit the form to update rankings.

### 📜 View Hall of Fame

1. Visit the "Hall of Fame" page.
2. Browse through the ranked list of players.

### 👤 Player Profiles

1. Register to view player details.
2. Click on a player’s name in the Hall of Fame to view their profile.
3. The profile displays all matches involving the player and some personal data.

---

## 🗂️ Project Structure

```
paddle/
├── config/            # Project configuration and settings
├── api/               # API apps
│   ├── games/          # API app for players & matches
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

---

## 📋 App Explanations

1. **`games/`**:
   - Manages players and matches
   - For players:
     - Players functionalities are player data, rankings, and profiles.
     - Players may or may not be associated with registered users.   
     - Stores player information.
     - Provide APIs for player rankings and profiles.
    - For matches:
     - Manages match-related functionality, including match creation and retrieval.
     - Matches involve 2 vs. 2 players, and winners contribute to player rankings.   
     - Store match details, including teams, date, and winners.
     - Provide APIs for match results and details.

2. **`users/`**:
   - Manages user registration, login, logout and profile management.
   - Registered users are the same than registered players.
   - Registered players are allowed to:
     - Add or update match results;
     - Add non registered players when adding or updating a match;
     - Check other users details
   - Non registered players can:
     - Check the hall of fame;
     - Become registered players using user registration;     

---

## 📡 API Endpoints

|**🏅 Player Rankings**| `/api/players/`| Retrieves a list of all players ranked by the number of matches won.

- **👤 Player Profile**: `/api/players/<id>/`
  - Retrieves details about a specific player, including their match history.

- **🎮 Match Results**: `/api/matches/`
  - Allows registered users to create and retrieve match results.

- **📄 Match Details**: `/api/matches/<id>/`
  - Retrieves details about a specific match, including the players and the winning team.

- **🔒 User Registration**: `/api/users/register/`
  - Allows new users to register.

- **🔒 User Login**: `/api/users/login/`
  - Allows users to log in and authenticate.

- **👤 User Profile**: `/api/users/profile/`
  - Retrieves details about the logged-in user.


---

## 🚀 Future Enhancements

- Add a leaderboard filter for date ranges.
- Enable advanced statistics for each player.
- Integrate user profiles with customizable avatars.
- Support live match updates using WebSockets.

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

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.  
2. Create a feature branch: `git checkout -b feature-name`.  
3. Commit your changes: `git commit -m 'Add feature'`.  
4. Push to the branch: `git push origin feature-name`.  
5. Open a pull request.

---

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

