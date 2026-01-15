@echo off
REM Script to switch to SQLite for local development
REM This comments out PostgreSQL database configuration in .env file

echo.
echo ========================================
echo Switching to SQLite for Local Development
echo ========================================
echo.

if not exist .env (
    echo ERROR: .env file not found!
    echo Please create a .env file first.
    pause
    exit /b 1
)

echo Backing up .env to .env.backup...
copy .env .env.backup >nul

echo.
echo Commenting out PostgreSQL database configuration...
echo.

REM Use PowerShell to comment out DB_* lines
powershell -Command "(Get-Content .env) | ForEach-Object { if ($_ -match '^\s*DB_(NAME|USER|PASSWORD|HOST|PORT)\s*=') { '# ' + $_ } else { $_ } } | Set-Content .env.tmp"

REM Replace original file
move /Y .env.tmp .env >nul

echo Done! Your .env file has been updated.
echo.
echo Django will now use SQLite (db.sqlite3) for local development.
echo.
echo To restore PostgreSQL configuration later, uncomment the DB_* lines in .env
echo or restore from .env.backup
echo.
pause

