@echo off
title Execute SQL File on Supabase Database
color 0A

echo ========================================
echo    Execute SQL File on Supabase
echo ========================================
echo.

cd /d "%~dp0\.."

if "%1"=="" (
    echo Usage: db_execute_file.bat "path\to\file.sql"
    echo.
    pause
    exit /b 1
)

echo Executing SQL file: %1
echo.

venv\Scripts\python.exe scripts\execute_sql.py --file "%1"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo    File executed successfully!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo    File execution failed!
    echo ========================================
)

echo.
pause

