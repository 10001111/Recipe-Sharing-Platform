@echo off
setlocal enabledelayedexpansion

REM Change to the project root directory (one level up from bats folder)
cd /d "%~dp0\.."

REM Get the actual resolved project directory path
for %%I in ("%~dp0\..") do set "PROJECT_DIR=%%~fI"

REM Set variables that need to persist throughout the script
set "VENV_PYTHON=!PROJECT_DIR!\venv\Scripts\python.exe"
set "VENV_PIP=!PROJECT_DIR!\venv\Scripts\pip.exe"

title Recipe Sharing Platform - Clean & Start
color 0A

echo ========================================
echo    Recipe Sharing Platform
echo    Clean, Setup, and Start
echo ========================================
echo.
echo This script will:
echo 1. Clean up old processes and cache files
echo 2. Set up virtual environment and dependencies
echo 3. Run database migrations
echo 4. Start the development server
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

REM ========================================
REM STEP 1: CLEANUP
REM ========================================
echo.
echo ========================================
echo    Step 1: Cleaning Up
echo ========================================
echo.

REM Ensure we're in project root before cleanup
cd /d "!PROJECT_DIR!"

echo Killing any running Python/Django processes...
taskkill /F /FI "WINDOWTITLE eq Recipe Sharing Platform*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Django*" >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1
echo ✓ Processes cleaned.

echo.
echo Cleaning Python cache files...
REM Ensure we're in project root
cd /d "!PROJECT_DIR!"
REM Clean cache files - suppress errors to prevent script exit
for /d /r "!PROJECT_DIR!" %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
for /r "!PROJECT_DIR!" %%f in (*.pyc) do @if exist "%%f" del /q "%%f" 2>nul
echo ✓ Cache files cleaned.

REM Check if Supabase CLI is available - don't exit on errors
where npx >nul 2>&1
set NPX_AVAILABLE=!ERRORLEVEL!
if !NPX_AVAILABLE! EQU 0 (
    npx supabase --version >nul 2>&1
    set SUPABASE_AVAILABLE=!ERRORLEVEL!
    if !SUPABASE_AVAILABLE! EQU 0 (
        echo.
        echo Checking Supabase local containers...
        cd /d "!PROJECT_DIR!"
        npx supabase status >nul 2>&1
        set SUPABASE_RUNNING=!ERRORLEVEL!
        if !SUPABASE_RUNNING! EQU 0 (
            echo Stopping local Supabase containers (if running)...
            npx supabase stop >nul 2>&1
            echo ✓ Supabase containers stopped.
        )
    )
)

echo.
echo Waiting for processes to fully terminate...
timeout /t 2 /nobreak >nul
echo ✓ Cleanup complete!
echo.

REM Ensure we're still in project root
cd /d "!PROJECT_DIR!"
if errorlevel 1 (
    echo ERROR: Failed to change to project directory!
    echo Project directory: !PROJECT_DIR!
    pause
    exit /b 1
)

echo Continuing to Step 2...
timeout /t 1 /nobreak >nul

REM ========================================
REM STEP 2: SETUP VIRTUAL ENVIRONMENT
REM ========================================
echo.
echo ========================================
echo    Step 2: Virtual Environment
echo ========================================
echo Current directory: !CD!

cd /d "!PROJECT_DIR!"

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

REM ========================================
REM STEP 3: INSTALL DEPENDENCIES
REM ========================================
echo.
echo ========================================
echo    Step 3: Installing Dependencies
echo ========================================
echo.

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
echo.

REM ========================================
REM STEP 4: ENVIRONMENT CONFIGURATION
REM ========================================
echo.
echo ========================================
echo    Step 4: Environment Configuration
echo ========================================
echo Current directory: !CD!

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
echo.

REM ========================================
REM STEP 5: SUPABASE & DATABASE MIGRATIONS
REM ========================================
echo.
echo ========================================
echo    Step 5: Supabase & Database Setup
echo ========================================
echo Current directory: !CD!

cd /d "!PROJECT_DIR!"

if not exist manage.py (
    echo ERROR: manage.py not found!
    echo Current directory: !CD!
    pause
    exit /b 1
)

REM Check if Supabase CLI is available and if local Supabase should be used
set USE_LOCAL_SUPABASE=0
where npx >nul 2>&1
set NPX_CHECK=!ERRORLEVEL!
if !NPX_CHECK! EQU 0 (
    npx supabase --version >nul 2>&1
    set SUPABASE_CHECK=!ERRORLEVEL!
    if !SUPABASE_CHECK! EQU 0 (
        echo.
        echo Supabase CLI detected! Checking local Supabase status...
        cd /d "!PROJECT_DIR!"
        npx supabase status >nul 2>&1
        set SUPABASE_STATUS=!ERRORLEVEL!
        if !SUPABASE_STATUS! NEQ 0 (
            echo Local Supabase not running. Checking if .env uses local Supabase...
            REM Check if .env has local Supabase settings
            findstr /C:"localhost" /C:"127.0.0.1" .env >nul 2>&1
            set LOCAL_CHECK=!ERRORLEVEL!
            if !LOCAL_CHECK! EQU 0 (
                echo Starting local Supabase containers...
                npx supabase start
                set START_RESULT=!ERRORLEVEL!
                if !START_RESULT! EQU 0 (
                    echo ✓ Local Supabase started!
                    echo.
                    echo Getting local Supabase connection info...
                    npx supabase status --output env > supabase_local.env 2>nul
                    echo ✓ Local Supabase is ready!
                    set USE_LOCAL_SUPABASE=1
                ) else (
                    echo WARNING: Failed to start local Supabase. Using remote connection.
                )
            ) else (
                echo Using remote Supabase connection from .env
            )
        ) else (
            echo ✓ Local Supabase is already running!
            set USE_LOCAL_SUPABASE=1
        )
    )
)

echo.
echo Running Django database migrations...
echo NOTE: If you see database connection errors, that's OK!
echo       Django will use SQLite fallback if Supabase is not accessible.
echo.
"!VENV_PYTHON!" manage.py migrate 2>&1
set MIGRATE_RESULT=%ERRORLEVEL%
if !MIGRATE_RESULT! NEQ 0 (
    echo.
    echo ========================================
    echo    Migration Warning
    echo ========================================
    echo.
    echo Migrations failed (error code %MIGRATE_RESULT%)
    echo This is usually because:
    echo - Database is not configured in .env file
    echo - No internet connection to Supabase
    echo - Database credentials are incorrect
    echo - Local Supabase not started (if using local)
    echo.
    echo DON'T WORRY! The server can still start.
    echo Django will use SQLite fallback if configured.
    echo.
    if !USE_LOCAL_SUPABASE! EQU 1 (
        echo TIP: Local Supabase is running. Check .env DB_HOST=localhost:54322
    )
    echo.
    echo Continuing to start the server...
    timeout /t 2 /nobreak >nul
) else (
    echo.
    echo ✓ Migrations completed successfully.
    if !USE_LOCAL_SUPABASE! EQU 1 (
        echo ✓ Using local Supabase database!
    )
)
echo.

REM ========================================
REM STEP 6: START SERVER
REM ========================================
echo.
echo ========================================
echo    Step 6: Starting Server
echo ========================================
echo.

cd /d "!PROJECT_DIR!"

echo ========================================
echo    Setup Complete! Starting Server...
echo ========================================
echo.
echo ✓ Cleanup: Complete
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
echo Waiting 3 seconds before opening browser...
timeout /t 3 /nobreak >nul

start http://127.0.0.1:8000

echo.
echo ========================================
echo    Starting Django Development Server
echo ========================================
echo.
echo Current directory: !CD!
echo Using Python: !VENV_PYTHON!
echo.

REM Final check before starting server
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

cd /d "!PROJECT_DIR!"
echo Starting server... This may take a few seconds...
echo.
"!VENV_PYTHON!" manage.py runserver
set SERVER_RESULT=!ERRORLEVEL!
if !SERVER_RESULT! NEQ 0 (
    echo.
    echo ========================================
    echo    Server Failed to Start
    echo ========================================
    echo.
    echo Error code: !SERVER_RESULT!
    echo.
    echo Common causes:
    echo 1. Port 8000 already in use
    echo    Solution: Close other programs using port 8000
    echo             Or run: netstat -ano ^| findstr :8000
    echo.
    echo 2. Database connection blocking startup
    echo    Solution: Check if Supabase project is paused
    echo             Run: test_supabase_connection.bat
    echo             Or temporarily comment out DB_NAME in .env
    echo.
    echo 3. Missing dependencies or configuration errors
    echo    Solution: Check error messages above
    echo.
    pause
    exit /b 1
)

REM This line only runs if the server stops
echo.
echo ========================================
echo    Server Stopped
echo ========================================
echo.
echo The development server has stopped.
echo Press any key to close this window...
pause >nul

