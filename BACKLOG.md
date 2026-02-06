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
| ------------ | ------ | ------- | ------ |
| After a reasonable expiry time (2 weeks for instance) the results are automatically approved and the match could be no longer deleted | 2 | 3 | 6 |
| Limit the time when a match can be added (same as the expiry time, 2 weeks for instance) | 2 | 3 | 6 |
| Add gender in players created in the tournament form | 2 | 2 | 4 |
| Add a favicon.ico | 1 | 3 | 3 |
| Update about.html to compute also the number of matches played by gender | 1 | 3 | 3 |
| The success message after creating a match should include changes in the rankings for the match creator (global ranking and by gender) and changes in rate for those rankings | 2 | 3 | 6 |
| Make player names clickable → profile page | 3 | 1 | 3 |
| Add a new button for the creator of the tournament and for the admin to close the tournament and move it to state "finalizado" even in the same day of the tournament day. Creator/admin could also reopen the tournament for editing during the same day of the tournament. | 1 | 2 | 2 |
| Dark mode | 1 | 2 | 2 |
| Email field in the registration form should be duplicated to avoid mistakes; reuse password dynamic check to ensure both emails match | 1 | 2 | 2 |
| DevOps: establish rotation criteria for log files | 1 | 2 | 2 |
| All user profile fields should be editable (not only email). Include the ability to delete a user and unlink from a player (player remains valid) | 2 | 1 | 2 |
| Advanced stats page for additional rankings: teams with more matches played, best win rate (min. 10 matches), hot players (ranking increase), new players | 2 | 1 | 2 |
| Rolling news bar at the top of home page with latest ranking movements (top 10) and/or last matches added | 2 | 1 | 2 |
| Add throttling control to prevent brute force attacks on login and registration | 1 | 1 | 1 |

---

## Design Ideas

No priority assigned yet. These represent potential large-scale or long-term enhancements.

- Video reel at app start  
- Support multiple groups of friends with separate rankings  
- Personalized news feed based on user activity, including AI-generated notifications  
- AI-generated player profile tag based on results  
- Bet mode: AI prediction of match results based on past performance  

---

## Completed Tasks

Leave empty — completed tasks are moved to `CHANGELOG.md`.

---
