@echo off
cd /d "%~dp0"
title FleetPulse AI Autonomous Telemetry Dashboard

echo ==============================================================================
echo   FleetPulse AI -- Autonomous Multi-Objective Fleet Dispatcher
echo ==============================================================================
echo.
echo [1/3] Checking environment and releasing stale port 8501...

:: Clean up any orphaned background process listening on port 8501
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8501" ^| findstr "LISTENING"') do (
    echo Terminating stale process on port 8501 (PID: %%a)...
    taskkill /F /PID %%a >nul 2>&1
)

echo [2/3] Verifying Streamlit dependencies...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [NOTICE] Streamlit not detected. Installing required packages...
    pip install -r requirements.txt
)

echo [3/3] Launching Command Center on http://localhost:8501 ...
echo.

:: Launch with WebSocket and CORS compatibility flags to prevent skeleton loading hangs
python -m streamlit run app.py --server.port 8501 --server.enableCORS false --server.enableXsrfProtection false --browser.serverAddress localhost

if errorlevel 1 (
    echo.
    echo [NOTICE] Port 8501 busy. Launching on fallback port 8502...
    python -m streamlit run app.py --server.port 8502 --server.enableCORS false --server.enableXsrfProtection false --browser.serverAddress localhost
)

echo.
echo Dashboard session closed.
pause
