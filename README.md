# 🏆 Paddle Tennis Hall of Fame

## 📖 Overview

This is a web application built using Django and Django Rest Framework (DRF) for managing a "Hall of Fame" for paddle tennis players. The app features a front-end built with Django templates and JavaScript, enabling users to view player rankings and detailed match records.

### ✨ Key Features

- **🏅 Hall of Fame Rankings**:
  - Displays a ranked list of paddle tennis players based on the number of matches won.
- **🎮 Match Results**:
  - Registered users can add results for matches (2 vs. 2 format).
  - Matches can include non-registered players by entering their names manually.
- **📋 Player Details**:
  - View a detailed profile for each player, including all matches they’ve played.
- **🔒 Authentication**:
  - Only registered users can add or update match results.

---

## 🛠️ Technologies Used

- **Backend**: Django Rest Framework (DRF)
- **Frontend**: Django Templates, JavaScript
- **Database**: SQLite (for development)
- **Authentication**: DRF session authentication

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

## 📡 API Endpoints

- **🏅 Player Rankings**: `/api/players/`
- **👤 Player Profile**: `/api/players/<id>/`
- **🎮 Match Results**: `/api/matches/`
- **🎮 Match Deatils**: `/api/matches/<id>`

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

1. Register to watch player details.
2. Click on a player’s name in the Hall of Fame to view their profile.
3. The profile displays all matches involving the player and some personal data.

---

## 🗂️ Project Structure

```
paddle/
├── config/            # Project configuration and settings
├── api/               # API apps
│   ├── players/       # API app for player-related endpoints
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── tests.py   # Tests for players API
│   └── matches/       # API app for match-related endpoints
│       ├── serializers.py
│       ├── views.py
│       ├── models.py
│       ├── urls.py
│       └── tests.py   # Tests for matches API
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
├── requirements.txt   # Dependencies for the project
└── manage.py          # Django entry point
```

---

## 🚀 Future Enhancements

- Add a leaderboard filter for date ranges.
- Enable advanced statistics for each player.
- Integrate user profiles with customizable avatars.
- Support live match updates using WebSockets.

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

