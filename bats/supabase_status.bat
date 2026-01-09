@echo off
title Supabase Status
color 0E

echo ========================================
echo    Supabase Status
echo ========================================
echo.

cd /d "%~dp0"

npx supabase status

echo.
pause

