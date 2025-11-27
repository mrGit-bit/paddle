# Backlog

This file lists all pending improvements, fixes, and new features planned for future releases of the project. It is public and maintained manually.

Tasks are ordered by **Priority**, calculated as:

`Priority = Importance × Simplicity`

Where:

- `Importance` = ranging from 1 (low importance) to 3 (high importance)  
- `Simplicity` = ranging from 1 (difficult task) to 3 (easy task)

Higher `Priority` numbers (from 1 to 9) indicate tasks that should be done first.

---

## Pending Tasks

Rules:

- Ordered by `priority` (**PRI**) from highest to lowest.
- For tasks with the same `priority`, sorted by `simplicity` (**SIMP**) so easier tasks come first.
- Completed tasks are removed from this list and added to the [CHANGELOG.md](CHANGELOG.md).

| Requirement | IMP. | SIMP. | PRI. |
|------------|------|-------|------|
| To avoid duplicate players and users, replace contextual options in the match form with a dropdown list of player names that also includes a “new player” option | 2 | 2 | 4 |
| Dark mode | 1 | 3 | 3 |
| The “forgot password” link in user details incorrectly points to the login page | 1 | 3 | 3 |
| Make the mobile app installable on the Apple Store | 3 | 1 | 3 |
| “Players” navigation option linked from the ranking table and menu. Searching or linking to a player should show player stats and matches played | 3 | 1 | 3 |
| Email field in the registration form should be duplicated to avoid mistakes; reuse password dynamic check to ensure both emails match | 1 | 2 | 2 |
| DevOps: establish rotation criteria for log files | 1 | 2 | 2 |
| Registration should be limited to real emails using a confirmation link | 1 | 2 | 2 |
| All user profile fields should be editable (not only email). Include the ability to delete a user and unlink from a player (player remains valid) | 2 | 1 | 2 |
| Add a “verify results” option to matches: Verified (True/False), Verified by (User), Verified on (Date) | 2 | 1 | 2 |
| Advanced stats page for additional rankings: more matches played, best win rate (min. 10 matches), hot players (ranking increase), new players | 2 | 1 | 2 |
| Rolling news bar at the top of home page with latest ranking movements (top 10) and/or last matches added | 1 | 1 | 1 |
| New registered players with zero matches should not appear in the ranking; they should be listed separately at the bottom | 1 | 1 | 1 |
| Add a gender field to players | 1 | 1 | 1 |
| Add gender filters to the ranking (all, men, women, mixed). Requires marking match gender and a new gender input in match form | 1 | 1 | 1 |
| Add throttling control to prevent brute force attacks on login and registration | 1 | 1 | 1 |

---

## Design Ideas

No priority assigned yet. These represent potential large-scale or long-term enhancements.

- “Americano” tournament format  
- Video reel at app start  
- Support multiple groups of friends with separate rankings  
- Personalized news feed based on user activity, including AI-generated notifications  
- AI-generated player profile tag based on results  
- Bet mode: AI prediction of match results based on past performance  

---

## Completed Tasks

Leave empty — completed tasks are moved to `CHANGELOG.md`.

---
