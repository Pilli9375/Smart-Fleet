@echo off
cd /d "%~dp0"
title FleetPulse AI Telemetry Center

:: Release port 8501 if previously occupied
for /f "tokens=5" %%p in ('netstat -aon ^| findstr ":8501" ^| findstr "LISTENING"') do taskkill /f /pid %%p >nul 2>&1

echo ============================================================
echo   FleetPulse AI -- Multi-Objective Fleet Dispatcher
echo   Launching Dashboard on http://127.0.0.1:8501 ...
echo ============================================================
echo.

python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501

echo.
echo Dashboard session closed.
pause
