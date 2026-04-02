# Backlog

This file lists pending improvements, fixes, and new features planned for
future releases. It is public and maintained manually.

Tasks are ordered by **Priority**, calculated as:

`Priority = Importance × Simplicity`

Where:

- `Importance` ranges from 1 (low) to 3 (high)
- `Simplicity` ranges from 1 (difficult) to 3 (easy)

Higher `Priority` numbers indicate work that should be considered first.

## Pending Tasks

Rules:

- Order tasks by `priority` (**PRI**) from highest to lowest.
- For equal `priority`, sort by `simplicity` (**SIMP**) so easier work comes
  first.
- Before closing a development cycle, reconcile any completed backlog items
  that belong to the requested scope: remove them from this list and ensure the
  implemented result is reflected in [CHANGELOG.md](CHANGELOG.md).
- This reconciliation is owned by development-cycle closure, not by
  `python scripts/release_orchestrator.py <version>` unless the release
  workflow explicitly says otherwise.

| Requirement | IMP. | SIMP. | PRI. |
| --- | --- | --- | --- |
| Add a new button for the creator of the tournament and for the admin to close the tournament and move it to state "finalizado" even in the same day of the tournament day. Creator/admin could also reopen the tournament for editing during the same day of the tournament. | 1 | 2 | 2 |
| DevOps: establish rotation criteria for log files | 1 | 2 | 2 |
| Advanced stats page for additional rankings: teams with more matches played, best win rate (min. 10 matches), hot players (ranking increase), new players | 2 | 1 | 2 |
| Rolling news bar at the top of home page with latest ranking movements (top 10) and/or last matches added | 2 | 1 | 2 |
| Add rate limits to prevent brute force attacks on login and registration | 1 | 1 | 1 |

## Design Ideas

No priority assigned yet. These represent potential large-scale or long-term
enhancements.

- Video reel at app start
- Personalized news feed based on user activity, including AI-generated notifications po
- AI-generated player profile tag based on results
- Bet mode: AI prediction of match results based on past performance

## Completed Tasks

Leave empty. Completed tasks are removed during closure or release
reconciliation and reflected in `CHANGELOG.md`.
