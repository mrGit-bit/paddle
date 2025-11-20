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
- Run tests and confirm coverage over 90%, if not develop additional tests:

```bash
cd paddle
pytest frontend/tests/ --cov=frontend.views --cov-report=term-missing
```

- Update `CHANGELOG.md`:
  - Add a new section with today’s date and version.
  - List changes under **Added / Changed / Fixed**.
- Update `README.md` if needed.
- Update version number in `about.html` (hardcoded `vX.Y.Z`).

### 📱 1.2 Prepare the Mobile release

- Rebuild the Mobile app if there are:
  - Changes to Capacitor configuration `capacitor.config.ts`: new server.url, new plugin, or app name/id, etc.
  - New native plugins: push notifications, camera, deep links, share intent, etc.
  - Changes to Android/iOS build settings: minSdkVersion, permissions, icon, splash, etc.
  - New Android/iOS app version in Play Store to rebuild with a new version code

- Before every rebuild bump version code in `/workspaces/paddle/mobile/android/app/build.gradle`

- Generate and download artifacts:

  - build `apk`: is generated for debugging/testing (Appetize.io or sideloading).
  - build `aab`: is the file uploaded to Play Console.

### 👩‍❤️‍💋‍👨 1.3 Common steps

- Commit and push changes:

```bash
git add --all
git commit -m "docs(release): prepare release vX.Y.Z"
git push origin develop
```

## 🚆 2. Promote to staging

- In GitHub Open PR: `develop ➜ staging`
- Title: `Release X.Y.Z — summary`
- Merge PR.


## 🚆 3. Deploy to staging VM

### 🖥️ 3.1 Deploy the Web App to Staging

On staging server:

```bash
git fetch origin
git checkout staging
git pull --ff-only
source ~/venv/bin/activate
```

- if .env needs to be modified: `nano .env`

- if dependencies have been changed:

```bash
pip install -r requirements.txt
```

- if static files have changed:

```bash
cd /home/ubuntu/paddle/paddle
PYTHONPATH=/home/ubuntu/paddle DJANGO_SETTINGS_MODULE=paddle.config.settings.prod \
python -m django collectstatic --noinput
```

- if database migrations have changed:

```bash
cd /home/ubuntu/paddle/paddle
PYTHONPATH=/home/ubuntu/paddle DJANGO_SETTINGS_MODULE=paddle.config.settings.prod \
python manage.py migrate
```

### 📱 3.2 “Test the Mobile App on Staging Backend

When testing CRUD operations with the mobile app, the staging server and staging database needs to be used instead of the production server and production database. This is only for testing staging API calls. It should never be applied on production.


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

- To staging server is password protected, so, to avoid login & password request using the mobile app, temporarily  comment / uncomment in the staging server file `/etc/nginx/sites-available/paddle` the password authentication:

```bash
# auth_basic           "Restricted Area";
# auth_basic_user_file /etc/nginx/.htpasswd;
```

- Don´t forget uncomment `auth_basic` and `auth_basic_user_file` in `/etc/nginx/sites-available/paddle` after mobile app testing. 

### 👩‍❤️‍💋‍👨 3.3 Common actions

Finally, restart services:

```bash
sudo systemctl restart paddle
sudo nginx -t
sudo systemctl reload nginx
```

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


## 🏭 5. Promote Web App to production

- In GitHub Open PR: `staging ➜ main`
- Title: `Release X.Y.Z — summary`
- Description and test plan: same as above
- Merge PR.
- If this release includes mobile changes, follow the Mobile Release Section before promoting to main.

## 🏭 6. Deploy Web App to production VM

On production server:

- as above in the staging server

## 🔖 7. Tag the release

- Repo tags represent the overall codebase release.
- They do not have to match Play Store version.
- Tag version refers to the repository state (web + mobile), not the mobile versionCode.
- The repository tag version is shown in the `about` page of the web app.

🌳 From IDE Codespaces on main branch:

```bash
git checkout main
git pull --ff-only
git tag -a vX.Y.Z -m "Release vX.Y.Z — summary"
git push origin vX.Y.Z
```

If you can’t switch to main because of pending changes in develop, on develop branch:

```bash
git add .
git commit -m "docs(release): update RELEASE.md and requirements.in"
git push
git checkout main
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

