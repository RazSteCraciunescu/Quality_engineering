@echo off
setlocal
if exist .venv\Scripts\python.exe (
  .venv\Scripts\python.exe -m uvicorn services.api.civicshift.main:app --host 127.0.0.1 --port 8000
) else (
  python -m uvicorn services.api.civicshift.main:app --host 127.0.0.1 --port 8000
)
if errorlevel 1 pause
