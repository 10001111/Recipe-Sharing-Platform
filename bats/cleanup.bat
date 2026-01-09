@echo off
setlocal enabledelayedexpansion

title Recipe Sharing Platform - Cleanup
color 0C

echo ========================================
echo    Cleanup Script
echo ========================================
echo.
echo This will kill all Python processes related to Django.
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

echo.
echo Killing Django/Python processes...
taskkill /F /FI "WINDOWTITLE eq Recipe Sharing Platform*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Django*" >nul 2>&1

echo.
echo Cleaning Python cache files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
for /r . %%f in (*.pyc) do @if exist "%%f" del /q "%%f" 2>nul

echo.
echo Cleanup complete!
echo.
pause

