# 📋 How to Use the Batch Files

## Quick Guide

### Option 1: Quick Start (Recommended for Daily Use)
**When:** You've already set up the project before

1. **Double-click** `quick_start.bat` OR
2. **Right-click** → "Run as administrator" (if needed)
3. Wait for the server to start
4. Your browser will open automatically at `http://127.0.0.1:8000`

**What it does:** Just starts the server (fast - 2 seconds)

---

### Option 2: Full Development Setup
**When:** First time, or after pulling new changes

1. **Double-click** `start_dev.bat` OR
2. **Right-click** → "Run as administrator" (if needed)
3. Press any key when prompted
4. Wait for setup to complete (30-60 seconds)
5. Your browser will open automatically

**What it does:** 
- Checks virtual environment
- Installs/updates packages
- Checks .env file
- Runs database migrations
- Starts server

---

### Option 3: Cleanup
**When:** Server won't stop, or you want to clean up

1. **Double-click** `cleanup.bat`
2. Press any key to confirm
3. It will kill stuck processes and clean cache files

---

## Using from Command Line (PowerShell)

You can also run them from PowerShell:

```powershell
# Quick start
.\quick_start.bat

# Full setup
.\start_dev.bat

# Cleanup
.\cleanup.bat
```

---

## Troubleshooting

### "Virtual environment not found"
→ Run `start_dev.bat` first to create it

### "Port 8000 already in use"
→ Run `cleanup.bat` to kill stuck processes

### "Module not found" errors
→ Run `start_dev.bat` to reinstall dependencies

### Script won't run
→ Right-click → "Run as administrator"

---

## What Happens When Server Starts?

- **Main site:** http://127.0.0.1:8000
- **Admin panel:** http://127.0.0.1:8000/admin
- **To stop:** Press `Ctrl+C` in the terminal window

