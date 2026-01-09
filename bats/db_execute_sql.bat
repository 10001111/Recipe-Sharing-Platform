@echo off
title Execute SQL on Supabase Database
color 0A

echo ========================================
echo    Execute SQL Query on Supabase
echo ========================================
echo.

cd /d "%~dp0\.."

if "%1"=="" (
    echo Usage: db_execute_sql.bat "SQL QUERY"
    echo.
    echo Examples:
    echo   db_execute_sql.bat "SELECT * FROM users LIMIT 5;"
    echo   db_execute_sql.bat "CREATE TABLE test (id SERIAL PRIMARY KEY);"
    echo.
    pause
    exit /b 1
)

echo Executing SQL query...
echo.

venv\Scripts\python.exe scripts\execute_sql.py "%*"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo    Query executed successfully!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo    Query failed!
    echo ========================================
)

echo.
pause

