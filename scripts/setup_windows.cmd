@echo off
setlocal
python -m venv .venv
if errorlevel 1 goto :error
call .venv\Scripts\activate.bat
python -m pip install -r requirements-dev.txt
if errorlevel 1 goto :error
echo.
echo Setup complete. Run: scripts\run_local.cmd
exit /b 0
:error
echo Setup failed. Check that Python 3.11 or newer is installed.
exit /b 1
