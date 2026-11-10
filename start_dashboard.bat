@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
title FleetPulse AI - Intelligent Fleet Dispatcher

echo ==============================================================================
echo   FleetPulse AI -- Autonomous Multi-Objective Fleet Dispatcher
echo   Authors: V Naga Adithya (23BCE9062) ^& M Karthik (23BCE9659)
echo ==============================================================================
echo.

echo [1/3] Detecting Python environment...
set "PY_CMD="

:: Check standard python
python --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=python"
    goto :python_found
)

:: Check Python launcher py
py --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py"
    goto :python_found
)

:: Check Anaconda installation
if exist "%USERPROFILE%\anaconda3\python.exe" (
    set "PY_CMD=%USERPROFILE%\anaconda3\python.exe"
    goto :python_found
)

:: Check default Python 3.12 path
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    goto :python_found
)

:python_found
if not defined PY_CMD (
    echo [ERROR] Python not detected in PATH or standard installation folders.
    echo Please install Python 3.10+ and make sure it is added to your PATH.
    echo.
    pause
    exit /b 1
)

echo        Found: !PY_CMD!
echo.

echo [2/3] Checking port 8501 and freeing stale processes...
for /f "tokens=5" %%p in ('netstat -aon ^| findstr ":8501" ^| findstr "LISTENING"') do (
    echo        Terminating stale process on port 8501 [PID %%p]...
    taskkill /f /pid %%p >nul 2>&1
)
echo.

echo [3/3] Verifying dependencies...
!PY_CMD! -c "import streamlit, plotly, pandas, numpy" >nul 2>&1
if errorlevel 1 (
    echo        Installing required packages from requirements.txt...
    !PY_CMD! -m pip install -r requirements.txt
)
echo        Dependencies verified.
echo.

echo ==============================================================================
echo   STARTING FLEETPULSE DASHBOARD TELEMETRY CENTER
echo   URL: http://localhost:8501
echo.
echo   - Your default browser will open automatically.
echo   - If it does not, visit: http://localhost:8501
echo   - To stop the server, press Ctrl+C in this terminal.
echo ==============================================================================
echo.

!PY_CMD! -m streamlit run app.py --server.port 8501

echo.
echo Dashboard session closed.
pause
