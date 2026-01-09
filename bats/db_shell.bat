@echo off
title Supabase Database Interactive Shell
color 0A

echo ========================================
echo    Supabase Database Interactive Shell
echo ========================================
echo.

cd /d "%~dp0\.."

echo Starting interactive database shell...
echo.

venv\Scripts\python.exe scripts\db_shell.py

pause

