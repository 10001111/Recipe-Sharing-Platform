@echo off
title Stop Local Supabase
color 0C

echo ========================================
echo    Stopping Local Supabase
echo ========================================
echo.

cd /d "%~dp0"

npx supabase stop

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Local Supabase stopped successfully!
) else (
    echo.
    echo WARNING: Supabase may not have been running.
)

echo.
pause

