@echo off
cd /d "%~dp0"
title FleetPulse AI Telemetry Center

:: Free port 8501 if previously occupied
for /f "tokens=5" %%p in ('netstat -aon ^| findstr ":8501" ^| findstr "LISTENING"') do taskkill /f /pid %%p >nul 2>&1

echo ============================================================
echo   FleetPulse AI -- Autonomous Fleet Dispatcher
echo   Launching Command Center at http://localhost:8501 ...
echo ============================================================
echo.

python -m streamlit run app.py --server.port 8501

echo.
echo Dashboard session closed.
pause
