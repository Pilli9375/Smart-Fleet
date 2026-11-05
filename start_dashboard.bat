@echo off
cd /d "%~dp0"
title FleetPulse AI Dashboard

echo ==============================================================================
echo   Launching FleetPulse AI Streamlit Dashboard...
echo ==============================================================================
echo.

python -m streamlit run app.py

if errorlevel 1 (
    echo.
    echo If port 8501 is busy, launching on alternative port 8502...
    python -m streamlit run app.py --server.port 8502
)

pause
