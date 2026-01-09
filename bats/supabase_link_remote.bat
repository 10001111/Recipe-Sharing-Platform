@echo off
title Link to Remote Supabase Project
color 0A

echo ========================================
echo    Link to Remote Supabase Project
echo ========================================
echo.
echo This will link your local project to your remote Supabase project.
echo You need your project reference ID (found in Supabase dashboard URL).
echo.
echo Example: https://app.supabase.com/project/rcetefvuniellfuneejg
echo          Project ID: rcetefvuniellfuneejg
echo.
pause

cd /d "%~dp0"

echo.
echo Checking if you're logged in...
npx supabase login --help >nul 2>&1

echo.
echo If not logged in, you'll be prompted to authenticate.
echo.
pause

echo.
echo Linking to remote project...
echo Enter your project reference ID when prompted:
echo.

npx supabase link --project-ref

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo    Successfully Linked!
    echo ========================================
    echo.
    echo Your local project is now linked to remote Supabase.
    echo You can now use:
    echo   - supabase db pull (pull schema from remote)
    echo   - supabase db push (push migrations to remote)
    echo.
) else (
    echo.
    echo ERROR: Failed to link project!
    echo Make sure you're logged in and have the correct project ID.
)

echo.
pause

