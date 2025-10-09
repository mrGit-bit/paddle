# 🚀 Release Process for rankingdepadel.club

This document describes the manual release workflow for the rankingdepadel.club production website.

## Branching model

- **develop** → daily work, features & fixes
- **staging** → pre-production testing
- **main** → stable production code

## Steps

### 1. Prepare the release

- Ensure all feature/fix branches are merged into **develop**.
- Run tests and ensure test coverage over 90%: `pytest frontend/tests/ --cov=frontend.views --cov-report=term-missing`.
- Update `CHANGELOG.md`:
  - Add a new section with today’s date and version.
  - List changes under **Added / Changed / Fixed**.
- Update `README.md` if needed.
- Update version number in `about.html` (hardcoded `vX.Y.Z`).
- Add & Commit changes to **develop**.
- Push changes: `git push`

### 2. Promote to staging

- In GitHub Open PR: `develop ➜ staging`
- Title: `Release X.Y.Z — summary`
- Description:
  - Summary: Key changes
  - Migrations: If any describe / none
  - Risk: Low / medium
- Test plan
- Merge PR.

### 3. Deploy to staging VM

On staging server:

```bash
git fetch origin
git checkout staging
git pull --ff-only
source ~/venv/bin/activate
```

if changes in dependencies:

```bash
pip install -r requirements.txt
```

if changes in static files:

```bash
cd /home/ubuntu/paddle/paddle
PYTHONPATH=/home/ubuntu/paddle DJANGO_SETTINGS_MODULE=paddle.config.settings.prod \
python -m django collectstatic --noinput
```

if changes in migrations:

```bash
cd /home/ubuntu/paddle/paddle
PYTHONPATH=/home/ubuntu/paddle DJANGO_SETTINGS_MODULE=paddle.config.settings.prod \
python manage.py migrate
```

finally, restart services:

```bash
sudo systemctl restart paddle
sudo systemctl reload nginx
```

- Test the app at the staging URL

### 4. Promote to production

- In GitHub Open PR: `staging ➜ main`
- Title: `Release X.Y.Z — summary`
- Description and Test plan: as above
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
git pull --ff-only origin develop
```
