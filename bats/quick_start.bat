@echo off
setlocal enabledelayedexpansion

REM Change to the project root directory (one level up from bats folder)
cd /d "%~dp0\.."

REM Get the actual resolved project directory path
for %%I in ("%~dp0\..") do set "PROJECT_DIR=%%~fI"

REM Set variables
set "VENV_PYTHON=!PROJECT_DIR!\venv\Scripts\python.exe"

title Recipe Sharing Platform - Quick Start
color 0B

echo ========================================
echo    Quick Start - Recipe Platform
echo ========================================
echo.

REM Ensure we're in project root
cd /d "!PROJECT_DIR!"

if not exist "!VENV_PYTHON!" (
    echo ERROR: Virtual environment not found!
    echo Please run start.bat or start_dev.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

if not exist manage.py (
    echo ERROR: manage.py not found!
    echo Current directory: !CD!
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat 2>nul

echo.
echo Starting Django development server...
echo Server: http://127.0.0.1:8000
echo.
echo IMPORTANT: Keep this window open while the server is running!
echo To stop: Press Ctrl+C
echo.

cd /d "!PROJECT_DIR!"
"!VENV_PYTHON!" manage.py runserver

REM This line only runs if the server stops
echo.
echo Server stopped.
pause
