@echo off
setlocal
cd /d "%~dp0"
title FleetPulse AI - Hybrid Fuzzy-NSGA-II Fleet Dispatcher

echo ==============================================================================
echo   FleetPulse AI: Hybrid Fuzzy-NSGA-II Intelligent Fleet Dispatcher
echo ==============================================================================
echo.

:: 1. Verify Python Installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python was not found in your system PATH.
    echo Please install Python 3.9 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [1/3] Python detected:
python --version
echo.

:: 2. Check dependencies
echo [2/3] Checking dependencies...
python -c "import streamlit, plotly, pandas, numpy, matplotlib" >nul 2>&1
if errorlevel 1 (
    echo Some dependencies are missing. Installing from requirements.txt...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies.
        echo Please run 'pip install -r requirements.txt' manually.
        echo.
        pause
        exit /b 1
    )
) else (
    echo All required packages are already installed.
)
echo.

:: 3. Launch Streamlit Application
echo [3/3] Starting FleetPulse AI Web Dashboard...
echo.
echo Application will open in your default browser at: http://localhost:8501
echo To stop the application, press Ctrl+C in this terminal window.
echo ==============================================================================
echo.

python -m streamlit run app.py

if errorlevel 1 (
    streamlit run app.py
)

pause
