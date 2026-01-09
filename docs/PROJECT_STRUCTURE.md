# 📁 Project Structure

## 🗂️ File Organization

### Root Directory
- `start.bat` - Main launcher (runs `bats/start.bat`)
- `manage.py` - Django management script
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (not in git)
- `env.example` - Environment variables template

### 📂 bats/ - Batch Scripts
All batch files are organized here:
- `start.bat` - Main script (cleanup, setup, start server)
- `start_dev.bat` - Alternative start script
- `quick_start.bat` - Quick start (assumes setup done)
- `cleanup.bat` - Cleanup script
- `supabase_start_local.bat` - Start local Supabase
- `supabase_stop_local.bat` - Stop local Supabase
- `supabase_status.bat` - Check Supabase status
- `supabase_link_remote.bat` - Link to remote Supabase
- `test_supabase_connection.bat` - Test Supabase connection
- `test_steps.bat` - Test script

### 📂 docs/ - Documentation
All markdown documentation files:
- `README.md` - Main documentation
- `STRUCTURE.md` - Project structure
- `HOW_TO_USE_YOUR_EXISTING_SUPABASE.md` - Supabase guide
- `SUPABASE_CLI_GUIDE.md` - Supabase CLI guide
- `FIX_SUPABASE_CONNECTION.md` - Connection troubleshooting
- `HOW_TO_USE_BATCH_FILES.md` - Batch files guide
- `SUPABASE_CONNECTION_STATUS.md` - Connection status
- `getting-started/` - Getting started guides
- `development/` - Development docs
- `security/` - Security docs

## 🚀 Quick Start

Just run from project root:
```powershell
.\start.bat
```

This will automatically:
1. Clean up old processes
2. Set up virtual environment
3. Install dependencies
4. Run migrations
5. Start the server

## 📝 Notes

- All batch files are in `bats/` folder
- All documentation is in `docs/` folder
- The root `start.bat` is a launcher that calls `bats/start.bat`
- You can run batch files directly from `bats/` folder if needed

