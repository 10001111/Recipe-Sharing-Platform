@echo off
title Test Supabase Connection
color 0B

echo ========================================
echo    Supabase Connection Test
echo ========================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat 2>nul

echo Testing database connection...
echo.

venv\Scripts\python.exe manage.py check --database default

if errorlevel 1 (
    echo.
    echo ========================================
    echo    Connection Failed
    echo ========================================
    echo.
    echo Most likely causes:
    echo 1. Supabase project is PAUSED (most common)
    echo 2. Wrong database password
    echo 3. Network/firewall blocking connection
    echo.
    echo ========================================
    echo    How to Fix
    echo ========================================
    echo.
    echo Step 1: Check Supabase Project Status
    echo ----------------------------------------
    echo 1. Go to: https://app.supabase.com
    echo 2. Log in to your account
    echo 3. Find your project: rcetefvuniellfuneejg
    echo 4. Check if it shows:
    echo    - GREEN/RUNNING = Active (good!)
    echo    - PAUSED/STOPPED = Needs to be resumed
    echo.
    echo If paused:
    echo - Click "Resume" or "Restore" button
    echo - Wait 1-2 minutes for it to start
    echo - Run this test again
    echo.
    echo Step 2: Verify Database Settings
    echo ----------------------------------------
    echo 1. In Supabase Dashboard:
    echo    Settings ^> Database
    echo 2. Check "Connection string" section
    echo 3. Verify DB_HOST matches your .env file
    echo 4. Verify DB_PASSWORD matches your .env file
    echo.
    echo Step 3: Try Connection Pooler (Alternative)
    echo ----------------------------------------
    echo Sometimes connection pooler works better:
    echo 1. Go to: Settings ^> Database ^> Connection Pooling
    echo 2. Use the pooler hostname instead
    echo 3. Update DB_HOST in .env file
    echo.
) else (
    echo.
    echo ========================================
    echo    Connection Successful!
    echo ========================================
    echo.
    echo Your Supabase database is connected!
    echo You can now run migrations and start the server.
    echo.
)

echo.
pause

