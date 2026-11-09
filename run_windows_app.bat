@echo off
setlocal
cd /d "%~dp0"
echo [P03-P2] Starting job-skill analysis UI...
where uv >nul 2>nul
if errorlevel 1 (
  echo [FAIL] uv is missing. Please install uv first.
  goto :fail
)
uv sync --locked --python 3.12
if errorlevel 1 goto :fail
echo [INFO] The local page should open in your browser.
echo [INFO] If it does not, open http://127.0.0.1:8501
echo [INFO] Press Ctrl+C to stop the local server.
uv run --no-sync streamlit run streamlit_app.py --server.address=127.0.0.1 --server.port=8501 --browser.gatherUsageStats=false
if errorlevel 1 goto :fail
exit /b 0
:fail
echo [FAIL] Startup stopped. Send this output to the W01 window.
pause
exit /b 1
