@echo off
REM Simple start script - kills existing processes and starts servers
REM Run with elevated permissions for port access

REM Check for admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

cd /d "%~dp0"

REM Kill processes on port 8000 (Django backend)
echo Killing processes on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

REM Kill processes on port 3000 (Frontend - if exists)
echo Killing processes on port 3000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

timeout /t 1 /nobreak >nul

REM Start Django backend on port 8000
echo Starting Django backend on port 8000...
start "Django Backend" /HIGH venv\Scripts\python.exe manage.py runserver 8000

REM Wait for Django to start
timeout /t 3 /nobreak >nul

REM Start Next.js frontend on port 3000
echo Starting Next.js frontend on port 3000...
cd frontend
if not exist node_modules (
    echo Installing frontend dependencies (this may take a few minutes)...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install frontend dependencies
        echo Make sure Node.js and npm are installed
        echo Run: node --version and npm --version to verify
        cd ..
        pause
        exit /b 1
    )
)
echo Starting Next.js development server...
start "Next.js Frontend" /HIGH cmd /k "npm run dev"
cd ..

echo.
echo Backend running on http://127.0.0.1:8000
echo Frontend running on http://127.0.0.1:3000
echo.
echo Press any key to stop servers (close windows manually)

pause
