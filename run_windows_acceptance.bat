@echo off
setlocal
cd /d "%~dp0"
echo [P03-P2] Windows acceptance checks
where uv >nul 2>nul
if errorlevel 1 (
  echo [FAIL] uv not found. Please install uv before continuing.
  goto :fail
)
echo [STEP 1] Syncing project-local .venv with Python 3.12...
uv sync --locked --python 3.12
if errorlevel 1 goto :fail
echo [STEP 2] Running P02, P03, integration and UI tests...
uv run --no-sync python -m unittest discover -s tests -v
if errorlevel 1 goto :fail
echo [STEP 3] Running the bundled CSV demonstration...
uv run --no-sync python demo.py
if errorlevel 1 goto :fail
echo [STEP 4] Checking real Streamlit app execution and server startup...
uv run --no-sync python smoke_test_streamlit.py
if errorlevel 1 goto :fail
echo [PASS] All automated Windows acceptance checks passed.
echo [INFO] Open run_windows_app.bat to verify the real browser experience.
pause
exit /b 0
:fail
echo [FAIL] Acceptance checks stopped. Please send the log to the W01 window.
pause
exit /b 1
