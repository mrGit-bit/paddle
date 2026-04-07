# Spec 038 Manual Checklist

Use this sheet to validate the multi-group and Hall of Fame changes from
`specs/038-multi-group-support-with-hall-of-fame.md`.

## How To Use

- Set `Status` to `Pending`, `Passed`, `Failed`, `Improve`, or `N/A`.
- Use `Notes` for findings, URLs, accounts used, screenshots, or blockers.
- Keep the rows as the source of truth while testing.

## Anonymous Hall Of Fame

| Check | Status | Notes |
| --- | --- | --- |
| Log out and open `/`; confirm the page title/header shows `Hall of Fame`. | Passed | |
| Confirm rankings load without errors for anonymous users. | Passed | |
| Confirm `Inicia sesión`, `regístrate`, and `crea un grupo` are visible. | Passed | |
| Confirm `regístrate` opens `/register/`. | Passed | |
| Confirm `crea un grupo` also opens `/register/` and preselects the create-group path. | Passed | |

## Registration UI

| Check | Status | Notes |
| --- | --- | --- |
| Open `/register/` and confirm the `Grupo/club` control is near the end of the form. | Passed | |
| Confirm existing clubs are listed before the create option. | Passed | |
| Confirm the create option is labeled `➕ Crear nuevo grupo/club`. | Passed | |
| Confirm there are no visible join/create radio buttons. | Passed | |
| With no club selected, confirm the existing-player selector is hidden. | Passed | |
| Select an existing club and confirm the existing-player selector appears. | Passed | |
| Select `➕ Crear nuevo grupo/club` and confirm the new-group-name field appears. | Passed | |
| While typing in `Contraseña` and `Confirma tu contraseña`, confirm field height stays stable. | Passed | |
| Confirm the eye icons stay vertically centered while typing and while validation feedback appears. | Passed | |
| Confirm validation icons do not overlap the eye icons. | Passed | |
| Email checks for an appropriate email format are in place. | Passed | Invalid email formats are rejected before registration completes. |

## Existing-Player Filtering

| Check | Status | Notes |
| --- | --- | --- |
| Create or use at least two clubs with different unlinked players. | Passed | |
| Select club A in `/register/` and confirm only unlinked players from club A appear. | Passed | |
| Switch to club B and confirm the selector refreshes to only club B players. | Passed | |
| Confirm club A players are no longer shown after switching to club B. | Passed | |

## Join Existing Club

| Check | Status | Notes |
| --- | --- | --- |
| Register a new user by selecting an existing club and no existing player. | Passed | |
| Confirm account creation succeeds and the user is logged in. | Passed | |
| Confirm the main page shows that club name, not `Hall of Fame`. | Passed | |
| Confirm the created player belongs to the selected club. | Passed | |

## Claim Existing Player

| Check | Status | Notes |
| --- | --- | --- |
| Register a user by selecting an existing club and choosing an unlinked player from that club. | Passed | |
| Confirm the user is linked to that existing player. | Passed | |
| Confirm the player is no longer available for later registrations. | Passed | |
| If username renaming is still intended, confirm the player name matches the username after linking. | Passed | |

## Create New Club

| Check | Status | Notes |
| --- | --- | --- |
| Open `/register/?create_group=1` or use `crea un grupo`. | Passed | |
| Confirm the create option is selected in `Grupo/club`. | Passed | |
| Enter a new club name and complete registration. | Passed | |
| Confirm the club is created and the user is logged in. | Passed | |
| Confirm the main page shows the new club name. | Passed | |

## Registration Validation

| Check | Status | Notes |
| --- | --- | --- |
| Submit with no `Grupo/club` selection and confirm validation blocks submission. | Passed | Registration now requires an explicit `Grupo/club` selection and no longer falls back to `club moraleja`. |
| Select create-club and submit without a club name; confirm validation appears. | Passed | Validation appears and the register button recovers correctly after correcting the input. |
| Try creating a club with an existing name; confirm duplicate-name validation appears. | Passed | Duplicate-name validation appears and the form remains usable after correction. |
| Attempt to submit a player from another club and confirm the backend rejects it. | Passed | |

## Group-Scoped Rankings And Matches

| Check | Status | Notes |
| --- | --- | --- |
| Log in as a user from club A and confirm `/` only shows club A ranking data. | Passed | |
| Create a match in club A and confirm rankings/stats update for club A. | Passed | |
| Log in as a user from club B and confirm club A’s new match is not visible there. | Passed | |
| Confirm club B rankings were not affected by club A activity. | Passed | |

## Players And Pair Rankings

| Check | Status | Notes |
| --- | --- | --- |
| Logged in as club A, open `/players/` and confirm only club A players appear. | Passed | |
| Open a player detail page and confirm ranking rows, history, and insights are scoped to club A. | Passed | |
| Logged in as club A, open `/ranking/pairs/` and confirm only club A pair data is shown. | Passed | |
| Log out and confirm `/players/` and `/ranking/pairs/` show aggregate Hall of Fame data. | Passed | |

## Americano

| Check | Status | Notes |
| --- | --- | --- |
| Logged in as club A, create an Americano tournament and confirm only club A players can be selected. | Passed | |
| Confirm the tournament appears in club A views/navigation. | Passed | |
| Log in as club B and confirm the club A tournament does not appear in club B scoped views. | Passed | |
| Log out and confirm aggregate public Americano browsing still works. | Passed | |

## Legacy And Migration Sanity

| Check | Status | Notes |
| --- | --- | --- |
| Confirm pre-existing legacy data appears under `club moraleja`. | Passed | |
| If a migrated legacy user exists, log in and confirm the main page shows `club moraleja`. | Passed | |
| Restart the dev server after migrations and confirm `/`, `/register/`, `/matches/`, `/players/`, and `/americano/` load without schema errors. | Passed | |
