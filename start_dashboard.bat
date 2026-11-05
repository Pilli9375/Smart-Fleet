@echo off
cd /d "%~dp0"
echo Launching FleetPulse AI Dashboard...
python -m streamlit run app.py
pause
