@echo off
title FleetPulse AI - Hybrid Fuzzy-NSGA-II Fleet Dispatcher
color 0B

echo ==============================================================================
echo   FleetPulse AI: Hybrid Fuzzy-NSGA-II Intelligent Fleet Dispatcher
echo ==============================================================================
echo.

:: 1. Verify Python Installation
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
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

:: 2. Prompt or auto-install requirements if needed
echo [2/3] Checking dependencies...
python -c "import streamlit, plotly, pandas, numpy, matplotlib" >nul 2>&1
if errorlevel 1 (
    echo Dependencies missing. Installing from requirements.txt...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        color 0C
        echo [ERROR] Failed to install dependencies. Please run 'pip install -r requirements.txt' manually.
        pause
        exit /b 1
    )
) else (
    echo All required packages (Streamlit, Plotly, Pandas, NumPy, Matplotlib) are installed.
)
echo.

:: 3. Launch Streamlit Application
echo [3/3] Starting FleetPulse AI Web Dashboard...
echo.
echo Application will open in your default browser at: http://localhost:8501
echo To stop the application, press Ctrl+C in this window.
echo ==============================================================================
echo.

python -m streamlit run app.py

if errorlevel 1 (
    streamlit run app.py
)

pause
