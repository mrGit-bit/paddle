# 🚀 Release Process

This document describes the **manual release workflow** for the production website.

## Branching model

- **develop** → daily work, features & fixes
- **staging** → pre-production testing
- **main** → stable production code

## Steps

### 1. Prepare the release

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

- RebuildMobile app if there are:
  - Changes to Capacitor configuration `capacitor.config.ts`: new server.url, new plugin, or app name/id, etc.
  - New native plugins: push notifications, camera, deep links, share intent, etc.
  - Changes to Android/iOS build settings: minSdkVersion, permissions, icon, splash, etc.
  - New Android/iOS app version in Play Store to rebuild with a new version code
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
      url: 'https://staging.rankingdepadel.club/mobiletest/',
      cleartext: false,
      allowNavigation: ['staging.rankingdepadel.club'],
    },

- Commit and push changes:

```bash
git add -all
git commit -m "docs(release): prepare release vX.Y.Z"
git push origin develop
```

### 2. Promote to staging

- In GitHub Open PR: `develop ➜ staging`
- Title: `Release X.Y.Z — summary`
- Merge PR.


### 3. Deploy to staging VM

On staging server:

```bash
git fetch origin
git checkout staging
git pull --ff-only
source ~/venv/bin/activate
```

if .env needs to be modified: `nano .env`

if dependencies changed:

```bash
pip install -r requirements.txt
```

if static files changed:

```bash
cd /home/ubuntu/paddle/paddle
PYTHONPATH=/home/ubuntu/paddle DJANGO_SETTINGS_MODULE=paddle.config.settings.prod \
python -m django collectstatic --noinput
```

if database migrations changed:

```bash
cd /home/ubuntu/paddle/paddle
PYTHONPATH=/home/ubuntu/paddle DJANGO_SETTINGS_MODULE=paddle.config.settings.prod \
python manage.py migrate
```

Finally, restart services:

```bash
sudo systemctl restart paddle
sudo systemctl reload nginx
```

Checks:

- `systemctl status paddle --no-pager` → active (running)
- `sudo nginx -t` → syntax is ok
- Site loads correctly
- Test the app at the staging URL according to the test staging site plan.

### 4. Promote to production

- In GitHub Open PR: `staging ➜ main`
- Title: `Release X.Y.Z — summary`
- Description and test plan: same as above
- Merge PR.

### 5. Deploy to production VM

On production server:

- as above in the staging server

### 6. Tag the release

From Codespaces (on main branch):

```bash
git checkout main
git pull --ff-only
git tag -a vX.Y.Z -m "Release vX.Y.Z — summary"
git push origin vX.Y.Z
```

If you can’t switch to main (pending changes in develop):

```bash
git add .
git commit -m "docs(release): update RELEASE.md and requirements.in"
git push
git checkout main
```

### 7. Rollback (if needed)

On production/staging server:

```bash
git fetch --all --tags
git checkout <previous-good-commit-or-tag> -B main
sudo systemctl restart paddle
sudo systemctl reload nginx
```

### 8. Update IDE branches after production deployment

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

## Quick reference

### Prepare release

`pytest && git add . && git commit -m "docs(release): prepare vX.Y.Z" && git push`

### Merge and deploy

develop → staging → main (via PRs)

On each server:

```bash
git fetch && git checkout <branch> && git pull --ff-only
source ~/venv/bin/activate
python paddle/manage.py collectstatic --noinput --settings=paddle.config.settings.prod
python paddle/manage.py migrate --settings=paddle.config.settings.prod
sudo systemctl restart paddle && sudo systemctl reload nginx
```

### Tag version

`git tag -a vX.Y.Z -m "Release vX.Y.Z" && git push origin vX.Y.Z`

### Update IDE branches

`git checkout develop && git merge origin/main -m "chore: sync develop after vX.Y.Z" && git push`
