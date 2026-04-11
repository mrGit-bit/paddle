#!/usr/bin/env bash

# ~/paddle/deploy_update.sh

set -euo pipefail

banner() { echo; echo "=== $* ==="; }
notice() {
  printf "\033[33m[notice]\033[0m %s\n" "$*"
}

banner "GIT"
cd ~/paddle
git fetch origin
git status

# Try fast-forward pull, but do not exit on failure.
git pull --ff-only || true

banner "PYTHON DEPENDENCIES"
python -m pip install -r ~/paddle/requirements.txt -q

banner "DJANGO STATIC FILES"
cd ~/paddle/paddle
python manage.py collectstatic --noinput --settings=config.settings.prod

banner "RESTARTING APP SERVICE"
sudo systemctl restart paddle

banner "REMINDERS (MANUAL WHEN NEEDED)"
echo
notice "If git pull --ff-only failed (fast-forward not possible), force sync with:"
notice "cd ~/paddle"
notice "git reset --hard origin/main"
echo
notice "If you changed nginx configuration or certificates, restart nginx:"
notice "sudo systemctl restart nginx"
echo
echo "WELL DONE with: ~/paddle/deploy_update.sh"
