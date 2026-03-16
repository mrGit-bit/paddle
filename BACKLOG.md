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
| After a reasonable expiry time (1 month for instance) the results are automatically approved and the match could be no longer deleted. Limit to the same time frame (1 month) the time when a match can be added | 2 | 3 | 6 |
| In every ranking page give the ability to order by win rate and by number of matches played. The default order should be by position and the order by position shpuld be restored after every page change, just ordering the players present on the consulted page. Add also a small bootstrap icon near the column headers of mathces and win rate to change the order in the page between ascending and descending. | 2 | 2 | 4 |
| In player details, the table for "pareja habitual" should have three rows for the most usual 3 partners instead of only one, ordered by more matches together | 2 | 3 | 6 |
| Add a new button for the creator of the tournament and for the admin to close the tournament and move it to state "finalizado" even in the same day of the tournament day. Creator/admin could also reopen the tournament for editing during the same day of the tournament. | 1 | 2 | 2 |
| DevOps: establish rotation criteria for log files | 1 | 2 | 2 |
| Advanced stats page for additional rankings: teams with more matches played, best win rate (min. 10 matches), hot players (ranking increase), new players | 2 | 1 | 2 |
| Rolling news bar at the top of home page with latest ranking movements (top 10) and/or last matches added | 2 | 1 | 2 |
| Add rate limits to prevent brute force attacks on login and registration | 1 | 1 | 1 |

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
