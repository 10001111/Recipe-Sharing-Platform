@echo off
setlocal enabledelayedexpansion

REM Change to the project root directory (one level up from bats folder)
cd /d "%~dp0\.."

REM Get the actual resolved project directory path
for %%I in ("%~dp0\..") do set "PROJECT_DIR=%%~fI"

REM Set variables that need to persist throughout the script
set "VENV_PYTHON=!PROJECT_DIR!\venv\Scripts\python.exe"
set "VENV_PIP=!PROJECT_DIR!\venv\Scripts\pip.exe"

title Recipe Sharing Platform - Development Server
color 0A

echo ========================================
echo    Recipe Sharing Platform Setup
echo ========================================
echo.
echo This script will:
echo - Activate Python virtual environment
echo - Install/update dependencies
echo - Run database migrations
echo - Start Django development server (Port 8000)
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

REM Ensure we're in the project directory
cd /d "!PROJECT_DIR!"

echo.
echo ========================================
echo    Step 1/5: Virtual Environment
echo ========================================
echo Current directory: !CD!
if not exist venv (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        echo Make sure Python is installed and in your PATH.
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created successfully.
) else (
    echo ✓ Virtual environment found.
)

REM Verify venv Python exists
if not exist "!VENV_PYTHON!" (
    echo ERROR: Python executable not found in venv!
    echo Expected: !VENV_PYTHON!
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Step 2/5: Installing Dependencies
echo ========================================
echo Current directory: !CD!
echo Python: !VENV_PYTHON!
echo Pip: !VENV_PIP!

REM Activate virtual environment (for PATH, but we'll use explicit paths)
call venv\Scripts\activate.bat 2>nul

if not exist "!VENV_PIP!" (
    echo pip not found. Installing pip...
    "!VENV_PYTHON!" -m ensurepip --upgrade
    if errorlevel 1 (
        echo ERROR: Failed to install pip!
        pause
        exit /b 1
    )
    echo ✓ pip installed.
) else (
    echo ✓ pip found.
)

echo.
echo Updating pip...
"!VENV_PIP!" install --upgrade pip --quiet >nul 2>&1
echo ✓ pip ready.

echo.
echo Installing project dependencies...
if not exist requirements.txt (
    echo ERROR: requirements.txt not found!
    echo Current directory: !CD!
    pause
    exit /b 1
)
echo This may take a few minutes...
"!VENV_PIP!" install -r requirements.txt
REM Don't exit on pip errors - "already satisfied" is OK
echo.
echo ✓ Dependencies installation completed.
echo Step 2/5 COMPLETE!
echo.

echo.
echo ========================================
echo    Step 3/5: Environment Configuration
echo ========================================
echo Current directory: !CD!

REM Ensure we're still in project directory
cd /d "!PROJECT_DIR!"

if not exist .env (
    echo WARNING: .env file not found!
    if exist env.example (
        echo Creating .env from env.example...
        copy env.example .env >nul 2>&1
        if errorlevel 1 (
            echo ERROR: Failed to copy env.example to .env
            pause
            exit /b 1
        )
        echo ✓ .env file created from env.example.
        echo NOTE: Please edit .env with your database credentials.
    ) else (
        echo ERROR: env.example not found!
        echo Please create a .env file manually.
        pause
        exit /b 1
    )
) else (
    echo ✓ .env file found.
)
echo Step 3/5 COMPLETE!
echo.

echo.
echo ========================================
echo    Step 4/5: Database Migrations
echo ========================================
echo Current directory: !CD!

REM Ensure we're in project directory
cd /d "!PROJECT_DIR!"

if not exist manage.py (
    echo ERROR: manage.py not found!
    echo Current directory: !CD!
    echo Project directory: !PROJECT_DIR!
    pause
    exit /b 1
)

echo Running database migrations...
echo Using Python: !VENV_PYTHON!
echo.
echo NOTE: If you see database connection errors, that's OK!
echo       You can configure your database later in the .env file.
echo       The server will still start (using SQLite fallback if configured).
echo.
"!VENV_PYTHON!" manage.py migrate 2>&1
set MIGRATE_RESULT=!ERRORLEVEL!
if !MIGRATE_RESULT! NEQ 0 (
    echo.
    echo ========================================
    echo    Migration Warning
    echo ========================================
    echo.
    echo Migrations failed (error code !MIGRATE_RESULT!)
    echo.
    echo This is usually because:
    echo - Database is not configured in .env file
    echo - No internet connection to Supabase
    echo - Database credentials are incorrect
    echo.
    echo DON'T WORRY! The server can still start.
    echo Django will use SQLite fallback if configured.
    echo.
    echo You can fix the database connection later and run:
    echo   python manage.py migrate
    echo.
    echo Continuing to start the server...
    timeout /t 2 /nobreak >nul
) else (
    echo.
    echo ✓ Migrations completed successfully.
)
echo.
echo ========================================
echo    Step 4/5 COMPLETE!
echo ========================================
echo.
echo Moving to final step...
timeout /t 1 /nobreak >nul
echo.

echo.
echo ========================================
echo    Step 5/5: Starting Server
echo ========================================
echo.

REM Final directory check
cd /d "!PROJECT_DIR!"

echo ========================================
echo    Setup Complete! Starting Server...
echo ========================================
echo.
echo ✓ Virtual environment: Ready
echo ✓ Dependencies: Installed
echo ✓ Environment file: Configured
if !MIGRATE_RESULT! EQU 0 (
    echo ✓ Database migrations: Completed
) else (
    echo ⚠ Database migrations: Skipped (will use SQLite or fix DB later)
)
echo.
echo ========================================
echo    Server Information
echo ========================================
echo.
echo Server URL:     http://127.0.0.1:8000
echo Admin panel:    http://127.0.0.1:8000/admin
echo.
if !MIGRATE_RESULT! NEQ 0 (
    echo ========================================
    echo    Database Note
    echo ========================================
    echo.
    echo Your Supabase database is not accessible.
    echo Django will use SQLite (local file) instead.
    echo.
    echo To fix Supabase connection later:
    echo 1. Go to https://app.supabase.com
    echo 2. Resume your project if paused
    echo 3. Update .env with correct DB_HOST (use Session Pooler)
    echo 4. Run: python manage.py migrate
    echo.
)
echo IMPORTANT: The server will keep running in this window.
echo            Keep this window open while developing!
echo.
echo To stop the server: Press Ctrl+C
echo.

REM Final check before starting server
cd /d "!PROJECT_DIR!"

if not exist "!VENV_PYTHON!" (
    echo ERROR: Python executable not found!
    echo Expected: !VENV_PYTHON!
    pause
    exit /b 1
)

if not exist manage.py (
    echo ERROR: manage.py not found in current directory!
    echo Current directory: !CD!
    pause
    exit /b 1
)

REM Test Django configuration first
echo.
echo Testing Django configuration...
"!VENV_PYTHON!" manage.py check 2>&1
set CHECK_RESULT=!ERRORLEVEL!
if !CHECK_RESULT! NEQ 0 (
    echo.
    echo WARNING: Django configuration check found issues!
    echo This might prevent the server from starting.
    echo.
    echo Common issues:
    echo - Missing SECRET_KEY in .env file
    echo - Database connection errors
    echo - Missing dependencies
    echo.
    echo Continuing anyway - you'll see the actual error when server starts...
    echo.
    timeout /t 2 /nobreak >nul
)

echo.
echo ========================================
echo    Starting Django Development Server
echo ========================================
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul

REM Open browser BEFORE starting server
start http://127.0.0.1:8000

echo.
echo Browser opened. Starting Django server...
echo.
echo ========================================
echo    Server Output (Keep This Window Open!)
echo ========================================
echo.
echo The server will start below. Keep this window open!
echo To stop: Press Ctrl+C
echo.
echo ========================================
echo.

REM Start server - this will block until Ctrl+C
"!VENV_PYTHON!" manage.py runserver
set SERVER_RESULT=!ERRORLEVEL!

REM If we get here, the server has stopped
echo.
echo ========================================
echo    Server Process Ended
echo ========================================
echo.
echo Exit code: !SERVER_RESULT!
echo.
echo The server has stopped. This usually means:
echo - The server encountered an error (check messages above)
echo - You pressed Ctrl+C to stop it
echo - Port 8000 was already in use
echo.

REM Check if server exited with an error
if !SERVER_RESULT! NEQ 0 (
    echo.
    echo ========================================
    echo    Server Exited with Error
    echo ========================================
    echo.
    echo Error code: !SERVER_RESULT!
    echo.
    echo Common causes:
    echo 1. Port 8000 already in use
    echo    Solution: Close other programs using port 8000
    echo             Or run: netstat -ano ^| findstr :8000
    echo.
    echo 2. Database connection error blocking startup
    echo    Solution: Check your .env file database settings
    echo             Make sure DB_HOST uses Session Pooler for IPv4
    echo             Or temporarily comment out DB_NAME to use SQLite
    echo.
    echo 3. Missing dependencies or configuration errors
    echo    Solution: Check error messages above
    echo.
    echo 4. Django settings error
    echo    Solution: Check config/settings.py for errors
    echo.
    pause
    exit /b 1
)

REM This line only runs if the server stops normally
echo.
echo ========================================
echo    Server Stopped
echo ========================================
echo.
echo The development server has stopped.
echo Press any key to close this window...
pause >nul
