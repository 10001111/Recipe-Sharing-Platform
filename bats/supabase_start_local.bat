@echo off
title Start Local Supabase
color 0B

echo ========================================
echo    Starting Local Supabase
echo ========================================
echo.

cd /d "%~dp0"

REM Check if Supabase CLI is available
where npx >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: npx not found!
    echo Please install Node.js to use Supabase CLI.
    pause
    exit /b 1
)

npx supabase --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Supabase CLI not found!
    echo Installing Supabase CLI...
    npm install -g supabase
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to install Supabase CLI!
        pause
        exit /b 1
    )
)

echo Starting local Supabase containers...
echo This may take a few minutes on first run...
echo.

npx supabase start

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo    Local Supabase Started!
    echo ========================================
    echo.
    echo Getting connection information...
    npx supabase status
    echo.
    echo To use local Supabase, update your .env file:
    echo   DB_HOST=localhost
    echo   DB_PORT=54322
    echo   DB_NAME=postgres
    echo   DB_USER=postgres
    echo   DB_PASSWORD=(check output above)
    echo.
    echo Supabase Studio: http://localhost:54323
    echo.
) else (
    echo.
    echo ERROR: Failed to start local Supabase!
    echo Make sure Docker is running.
    pause
    exit /b 1
)

pause

