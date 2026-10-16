#!/usr/bin/env sh
set -eu
if [ -x .venv/bin/python ]; then
  exec .venv/bin/python -m uvicorn services.api.civicshift.main:app --host 127.0.0.1 --port 8000
fi
exec python3 -m uvicorn services.api.civicshift.main:app --host 127.0.0.1 --port 8000
