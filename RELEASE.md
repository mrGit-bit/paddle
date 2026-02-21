<!-- markdownlint-disable MD025 -->

# 🚀 Release Process

This repository contains:

- A **Django web application**
- A **Capacitor Android mobile app**

Releases may be performed either:

- ✅ With automation (CI + Release Prep workflow)
- 🧾 Fully manually

Both flows are supported and documented below.

---

# 🌳 Branching Model

- 🧰 **develop** → daily development
- 🚊 **staging** → pre-production testing
- 🏭 **main** → production-ready code

All promotions must go through Pull Requests.

---

# 🔐 CI Enforcement (If Enabled)

If CI and branch protection are enabled:

- All PRs into `develop`, `staging`, and `main` must pass:
  - pytest
  - coverage ≥ 90%

If CI is not enforced, manual testing is required before merging.

---

# 1️⃣ Prepare the Release

Two supported modes:

- 🅰️ Automated Preparation (Recommended)
- 🅱️ Manual Preparation

---

# 🅰️ OPTION A — Automated Preparation (Recommended)

Uses GitHub Action: **Release Prep (no-AI)**

## Step A1 — Trigger Workflow

GitHub → Actions → **Release Prep (no-AI)**

Inputs:

- `version`: `X.Y.Z`
- `target_branch`: `develop`

The workflow will:

- Move `## [Unreleased]` → `## [X.Y.Z] - YYYY-MM-DD` in `CHANGELOG.md`
- Update `paddle/config/__init__.py`:

  ```python
  __version__ = "X.Y.Z"
  ```

- Create branch `chore/release-vX.Y.Z`
- Open PR into `develop`

## Step A2 — Review and Merge

- Review CHANGELOG section
- Review version bump
- Ensure CI is green (if enabled)
- Merge PR into `develop`

---

# 🅱️ OPTION B — Manual Preparation

## Step B1 — Run Tests Locally

```bash
cd paddle
pytest frontend/tests/ --cov=frontend.views --cov-report=term-missing
pytest paddle/americano/tests/test_americano_views.py --cov=americano.views --cov-report=term-missing
```

Coverage must be ≥ 90%.

## Step B2 — Update Files Manually

### Update CHANGELOG.md

- Move content under `## [Unreleased]` into `## [X.Y.Z] - YYYY-MM-DD` and leave an empty `## [Unreleased]` section at the top.
  
### Update Version Source

- Edit: `paddle/config/__init__.py`, ensure `__version__` is set to `X.Y.Z`:

### Update Documentation

- `BACKLOG.md`
- `README.md` (if required)

## Step B3 — Commit

```bash
git add --all
git commit -m "version(release): prepare release vX.Y.Z"
git push origin develop
```

---

# 2️⃣ Promote to Staging

Open PR `develop → staging` with title `Release X.Y.Z — short summary`. If CI is enabled: Wait for green checks before merging and merge PR.

---

# 3️⃣ Deploy to Staging

Two methods supported.

---

## 🅰️ Semi-Automated Deploy

From local machine:

```bash
ssh staging-update
```

If fast-forward fails:

```bash
cd ~/paddle
git reset --hard origin/staging
```

If migrations pending:

```bash
cd ~/paddle/paddle
python manage.py migrate --settings=config.settings.prod
```

If nginx config changed:

```bash
sudo systemctl restart nginx
```

---

## 🅱️ Manual Deploy

```bash
git fetch origin
git checkout staging
git pull --ff-only
source ~/venv/bin/activate
```

If dependencies changed:

```bash
pip install -r requirements.txt
```

If static files changed:

```bash
python manage.py collectstatic --noinput
```

If migrations changed:

```bash
python manage.py migrate --noinput
```

Restart services:

```bash
sudo systemctl restart paddle
sudo nginx -t
sudo systemctl reload nginx
```

---

# 4️⃣ Test on Staging

Minimum checklist:

- Login/logout
- Rankings page loads
- Match creation/edit
- Static assets
- About page shows correct version

---

# 5️⃣ Promote to Production

Open PR:

```bash
staging → main
```

Wait for CI if enforced.

Merge PR.

---

# 6️⃣ Deploy to Production

## Semi-Automated

```bash
ssh prod-update
```

## Manual

Same steps as staging, but on production server.

---

# 7️⃣ Tag the Release

## Install release scripts (one-time)

Scripts live in:

```bash
scripts/
```

Make them executable:

```bash
chmod +x scripts/tag_release.sh \
  scripts/backmerge_main_to_develop.sh
```

## A) Automated (scripts)

```bash
./scripts/tag_release.sh X.Y.Z "Release vX.Y.Z"
```

## B) Manual (CLI commands)

```bash
git checkout main
git fetch origin
git pull --ff-only
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

---

# 8️⃣ Mobile App Release (Independent Flow)

Rebuild only if:

- Capacitor config changed
- Native plugins changed
- Play Store version bump required

Update:

```bash
mobile/android/app/build.gradle
```

Bump:

- `versionCode`
- `versionName`

Artifacts:

- `.apk` → testing
- `.aab` → Play Console upload

Upload `.aab` manually to Play Console.

---

# 9️⃣ Rollback (Web Only)

On server:

```bash
git fetch --all --tags
git checkout <previous-tag> -B main
sudo systemctl restart paddle
sudo systemctl reload nginx
```

---

# 🔁 Update IDE Branches After Production Deployment

## A) Automated (scripts)

```bash
./scripts/backmerge_main_to_develop.sh X.Y.Z
```

## B) Manual (CLI commands)

```bash
git checkout develop
git fetch origin
git pull --ff-only origin develop
git merge origin/main \
  -m "merge(release): backmerge main into develop after vX.Y.Z"
git push origin develop
```

---

# 🔎 Version Source of Truth

Application version is defined exclusively in:

```bash
paddle/config/__init__.py
```

```python
__version__ = "X.Y.Z"
```

Rules:

- `CHANGELOG.md` is documentation only.
- `## [Unreleased]` must remain permanently.
- The About page reads from `config.__version__`.
- Never derive runtime version from CHANGELOG.

---

# 🧠 Automation Philosophy

- Version is defined in one place.
- CHANGELOG documents releases.
- All promotions occur via PR.
- CI blocks broken merges (if enabled).
- Deployment may remain manual for safety.
