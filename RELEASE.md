# 🚀 Release Process

This repository contains both the Django web application and the Capacitor Android mobile app.

This document describes how to perform releases for:

- the web app (staging → production), and
- the mobile app (build → Play Console internal testing → production)

Both release flows are independent and can be executed separately.

## 🌳 Git Branching model

- 🧰 **develop** → daily work, features & fixes. Usually worked in the IDE.
- 🚊 **staging** → pre-production testing. Deployed in a staging server with a staging database.
- 🏭 **main** → stable production code

## 🧰 1. Prepare the release

### 🖥️ 1.1 Prepare the Web App release

- Ensure all feature/fix branches are merged into **develop**.
- Run tests and confirm coverage over 90%, if under that rate develop additional tests.

```bash
cd paddle
pytest frontend/tests/ --cov=frontend.views --cov-report=term-missing
pytest /workspaces/paddle/paddle/americano/tests/test_americano_views.py --cov=americano.views --cov-report=term-missing
```

- Update:
  - `BACKLOG.md`: remove implemented functionalities from the backlog in the current release version
  - `CHANGELOG.md`: rename [Unreleased] to a new version number `vX.Y.Z`. Also add a summary of the release under the new version number.
  - `README.md`: amended to reflect the current v1.3.0 behavior in the documentation itself (without copying release notes)
- Ensure `CHANGELOG.md` is updated correctly (`## [Unreleased]` during development, then promote to `## [X.Y.Z] - YYYY-MM-DD` on release).

### 📱 1.2 Prepare the Mobile release (only if necessary)

- Rebuild the Mobile app if there are:
  - Changes to Capacitor configuration `capacitor.config.ts`: new server.url, new plugin, or app name/id, etc.
  - New native plugins: push notifications, camera, deep links, share intent, etc.
  - Changes to Android/iOS build settings: minSdkVersion, permissions, icon, splash, etc.
  - New Android/iOS app version in Play Store to rebuild with a new version code

- Before every rebuild bump version code in `/workspaces/paddle/mobile/android/app/build.gradle`

- Generate and download artifacts:

  - build `apk`: is generated for debugging/testing (Appetize.io or side loading).
  - build `aab`: is the file uploaded to Play Console.

### 👩‍❤️‍💋‍👨 1.3 Final preparation steps

- Commit and push changes:

```bash
git add --all
git commit -m "version(release): prepare release vX.Y.Z"
git push origin develop
```

## 🚆 2. Promote to staging

- In GitHub Open PR: `develop ➜ staging`
- Title: `Release X.Y.Z — summary` where summary is the short description of the release contained in the CHANGELOG.md
- Merge PR.

## 🚆 3. Deploy to staging VM

### 🖥️ 3.1 Deploy the Web App to Staging

Deployment could be done semi-automatically (with the `staging-update` command) or manually.

> Notes:
>
> - if .env needs to be modified remember to do: `nano .env`
> - If the staging database has been stopped due to inactivity do not forget to restart it in the console panel.

#### Semi-automated deploy

Automated deploy to staging server could be achieved with ```ssh staging-update``` command in windows local terminal.

If ```git pull --ff-only``` fails (because fast-forwarding is not possible), force sync with:

```bash
cd ~/paddle
git reset --hard origin/main
```

If Django models have changed and migrations are pending, run:

```bash
cd ~/paddle/paddle
python manage.py migrate --settings=config.settings.prod
```

If nginx has changed (changes in the configuration or in certificates), restart nginx: ```sudo systemctl restart nginx```

#### Manual deploy

```bash
git fetch origin
git checkout staging
git pull --ff-only
source ~/venv/bin/activate
```

- if dependencies have been changed:

```bash
pip install -r requirements.txt
```

- if static files have changed:

```bash
(venv) ubuntu@staging:~/paddle/paddle$ python manage.py collectstatic --noinput
```

Note: use the `--clear` option to remove old static files.

- if database migrations have changed:

```bash
(venv) ubuntu@staging:~/paddle/paddle$ python manage.py migrate --noinput
```

Finally, restart services:

```bash
sudo systemctl restart paddle
sudo nginx -t
sudo systemctl reload nginx
```

### 📱 3.2 Test the Mobile App on Staging Backend

Only if Android has been bundled and if CRUD operations with the mobile app are required, the staging backend needs to be used.

- Replace in `/workspaces/paddle/mobile/capacitor.config.ts` the production build:
  
  ```bash
  server: {
     url: 'https://rankingdepadel.club',
     cleartext: false,
     allowNavigation: ['rankingdepadel.club', 'www.rankingdepadel.club'],
   },
  ```
  
  with the staging build:

    ```bash
    server: {
      url: 'https://staging.rankingdepadel.club',
      cleartext: false,
      allowNavigation: ['staging.rankingdepadel.club'],
    },
    ```

- Because the staging server is password protected, to avoid login & password request using the mobile app, temporarily  comment / uncomment in the staging server file `/etc/nginx/sites-available/paddle` the password authentication following lines:

```bash
# auth_basic           "Restricted Area";
# auth_basic_user_file /etc/nginx/.htpasswd;
```

- Don´t forget uncomment `auth_basic` and `auth_basic_user_file` in `/etc/nginx/sites-available/paddle` after mobile app testing.

>Note: Before moving to production, make a plan for manual testing of functionalities.

## 📱 4. Mobile App release

- The mobile release does not require deploys to servers.
- Instead, the new release has to be built (automatically with GitHub Actions) and uploaded to Play Store as an aab artifact.

### Switch back to production from staging if needed

- If you tested the mobile app against the staging backend, remember to switch capacitor.config.ts back to the production server.url, commit the change, bump versionCode, and rebuild the final AAB for Play Store.

### How to bump `versionCode` and `versionName`

- Bump `versionCode` and `versionName` in `/workspaces/paddle/mobile/android/app/build.gradle`
- Google Play does not accept AAB uploads unless `versionCode` is strictly higher than any previous upload.
- `versionName` is the version number that is shown to users in the Play Store.

### How to build (GitHub Actions)  

- `.apk` and `.aab` are automatically built by GitHub Actions.
- Never commit signing keys (`upload-keystore.jks`, `.jks.base64`) to GitHub repository.The GitHub Action automatically injects them via GitHub secrets.

### How to upload to Play Console

- In Play Console, choose `New release` upload the `.aab` artifact.
- Play Store only accepts `.aab`. The `.apk` is optional and used for local or emulator testing.

### Instructions for internal testers

- Enroll: open this link on your phone and be signed in with your tester Google account: `https://play.google.com/apps/testing/club.rankingdepadel.app`

- Update: use the direct link: `https://play.google.com/store/apps/details?id=club.rankingdepadel.app`. When the update is ready, the button will show `Update`.

- Verify: On your phone, long-press `app icon` → `App info`. Scroll to the App version and It should show the new version.

## 🏭 5. Promote Web App to production in GitHub repository

- In GitHub Open PR: `staging ➜ main`
- Title: `Release X.Y.Z — summary`
- Description and test plan: same as above
- Merge PR.
- If this release includes mobile changes, follow the Mobile Release Section before promoting to main.

## 🏭 6. Deploy Web App to production VM

To deploy the web app to production VM make the same changes as in the staging replacing ```ssh staging-update``` with ```ssh prod-update```.

if you find an error requesting to stash or merge conflicts, use `git reset --hard origin/main`.

## 🔖 7. Tag the release

>Note: The repository tag version is shown in the `about` page of the web app (don´t forget to update!).

🌳 From IDE Codespaces on main branch:

If you can’t switch to main because of pending changes in develop, on `develop` branch:

```bash
git add .
git commit -m "docs(release): update RELEASE.md and requirements.in"
git push
git checkout main
```

Then update the `main` branch and tag the release:

```bash
git checkout main
git pull --ff-only
git tag -a vX.Y.Z -m "Release vX.Y.Z — summary"
git push origin vX.Y.Z
```

To check current history of commits and tags:

```bash
git fetch --tags
git log --decorate --simplify-by-decoration --oneline
git log --oneline --graph -n 5
git show --stat
```

## 🔙 8. Rollback if needed (Web App only)

On production/staging server:

```bash
git fetch --all --tags
git checkout <previous-good-commit-or-tag> -B main
sudo systemctl restart paddle
sudo systemctl reload nginx
```

## 📆 9. Update IDE branches after production deployment

In Codespaces IDE:

- Fetch all branches: `` git fetch --all --prune ``

- Update develop:

```bash
git checkout develop
git status         # should be clean
git fetch origin

# Merge main into develop (creates a merge commit if needed)
git merge origin/main -m "chore(branches): back-merge main into develop after vX.Y.Z release"

# If conflicts appear: fix files -> git add <fixed> -> git commit

# Push updated develop
git push
```
