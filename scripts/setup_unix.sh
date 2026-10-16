#!/usr/bin/env sh
set -eu
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
printf '\nSetup complete. Run: ./scripts/run_local.sh\n'
