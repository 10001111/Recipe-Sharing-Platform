# Backend Start Guide

## Quick Start

### Option 1: Using Batch File (Easiest)
```bash
start_dev.bat
```
This will:
- Activate virtual environment
- Install dependencies if needed
- Run migrations
- Start Django server on port 8000

### Option 2: Manual Start

#### Step 1: Activate Virtual Environment
```bash
# Windows PowerShell
venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat
```

#### Step 2: Install Dependencies (if not already installed)
```bash
pip install -r requirements.txt
```

#### Step 3: Run Migrations
```bash
python manage.py migrate
```

#### Step 4: Start Development Server
```bash
python manage.py runserver
```

The backend will be available at: **http://127.0.0.1:8000**

## Troubleshooting

### Virtual Environment Not Found
If you get "venv not found":
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Port 8000 Already in Use
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Or use a different port
python manage.py runserver 8001
```

### Missing Environment Variables
Create a `.env` file in the project root (copy from `env.example`):
```bash
copy env.example .env
```

Then edit `.env` and add your configuration values.

### Database Errors
If you get database errors:
```bash
python manage.py migrate
```

### Import Errors
If you get "Module not found" errors:
```bash
pip install -r requirements.txt
```

## Verify Backend is Running

1. Open browser: http://127.0.0.1:8000
2. You should see Django welcome page or API root
3. Check API: http://127.0.0.1:8000/api/
4. Check health: http://127.0.0.1:8000/api/health/

## Common Commands

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8000

# Run on all interfaces
python manage.py runserver 0.0.0.0:8000

# Check for issues
python manage.py check
```

