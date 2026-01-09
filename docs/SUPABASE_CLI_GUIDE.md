# 🚀 Supabase CLI Integration Guide

This project now integrates with **Supabase CLI** for better database management!

## 📋 What is Supabase CLI?

Supabase CLI allows you to:
- **Run Supabase locally** (no internet needed!)
- **Manage database migrations** easily
- **Sync with remote Supabase** projects
- **Test database changes** before deploying

---

## 🛠️ Available Commands

### Quick Commands (Batch Files)

| File | What It Does |
|------|-------------|
| `supabase_start_local.bat` | Start local Supabase containers |
| `supabase_stop_local.bat` | Stop local Supabase containers |
| `supabase_status.bat` | Check Supabase status |
| `supabase_link_remote.bat` | Link to remote Supabase project |

### Direct CLI Commands

```powershell
# Start local Supabase
npx supabase start

# Stop local Supabase
npx supabase stop

# Check status
npx supabase status

# Link to remote project
npx supabase link --project-ref YOUR_PROJECT_ID

# Pull schema from remote
npx supabase db pull

# Push migrations to remote
npx supabase db push

# Create a new migration
npx supabase migration new migration_name

# Reset local database
npx supabase db reset
```

---

## 🎯 Two Ways to Use Supabase

### Option 1: Local Supabase (Recommended for Development)

**Benefits:**
- ✅ Works offline
- ✅ Fast (no network latency)
- ✅ Free (no usage limits)
- ✅ Safe (won't affect production)

**Setup:**
1. Run `supabase_start_local.bat`
2. Update your `.env` file:
   ```env
   DB_HOST=localhost
   DB_PORT=54322
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=(check output from start command)
   ```
3. Run `start.bat` - it will automatically use local Supabase!

### Option 2: Remote Supabase (Production/Cloud)

**Benefits:**
- ✅ Accessible from anywhere
- ✅ Real production environment
- ✅ Can share with team

**Setup:**
1. Use your existing `.env` with remote Supabase credentials
2. Make sure your Supabase project is **not paused**
3. Use **Session Pooler** for IPv4 compatibility:
   ```env
   DB_HOST=aws-0-us-east-1.pooler.supabase.com
   DB_PORT=6543
   ```

---

## 🔄 How `start.bat` Works with Supabase CLI

The updated `start.bat` file now:

1. **Checks for Supabase CLI** - Detects if you have it installed
2. **Detects local vs remote** - Checks your `.env` file
3. **Starts local Supabase** - If using local, starts containers automatically
4. **Uses correct connection** - Connects to local or remote based on config

---

## 📝 Common Workflows

### Workflow 1: Local Development

```powershell
# 1. Start local Supabase
.\supabase_start_local.bat

# 2. Update .env to use local Supabase
# (DB_HOST=localhost, DB_PORT=54322)

# 3. Start Django project
.\start.bat
```

### Workflow 2: Sync with Remote

```powershell
# 1. Link to remote project
.\supabase_link_remote.bat

# 2. Pull latest schema from remote
npx supabase db pull

# 3. Start Django (will use remote)
.\start.bat
```

### Workflow 3: Create Database Migrations

```powershell
# 1. Make changes to Django models
# (edit models.py files)

# 2. Create Django migration
.\venv\Scripts\python manage.py makemigrations

# 3. Create Supabase migration (optional)
npx supabase migration new add_new_table

# 4. Apply migrations
.\venv\Scripts\python manage.py migrate
```

---

## 🎓 Key Concepts

### Local Supabase vs Remote Supabase

**Local Supabase:**
- Runs in Docker containers on your computer
- Port: `54322` (different from remote `5432`)
- Host: `localhost`
- Password: Generated when you start (check `supabase status`)

**Remote Supabase:**
- Runs on Supabase cloud servers
- Port: `5432` or `6543` (pooler)
- Host: `db.xxxxx.supabase.co` or pooler hostname
- Password: Your Supabase project password

### When to Use Which?

- **Local:** Daily development, testing, offline work
- **Remote:** Production, team collaboration, deployment

---

## 🐛 Troubleshooting

### "Supabase CLI not found"
```powershell
# Install Supabase CLI globally
npm install -g supabase
```

### "Docker not running"
- Install Docker Desktop: https://www.docker.com/products/docker-desktop
- Start Docker Desktop
- Try `supabase_start_local.bat` again

### "Port already in use"
```powershell
# Stop local Supabase
.\supabase_stop_local.bat

# Or check what's using the port
netstat -ano | findstr :54322
```

### "Cannot connect to local Supabase"
1. Check if Supabase is running: `.\supabase_status.bat`
2. Verify `.env` has correct local settings
3. Check Docker is running

---

## 📚 Learn More

- **Supabase CLI Docs:** https://supabase.com/docs/guides/cli
- **Local Development:** https://supabase.com/docs/guides/cli/local-development
- **Database Migrations:** https://supabase.com/docs/guides/cli/managing-environments

---

## ✅ Quick Reference

| Task | Command |
|------|---------|
| Start local Supabase | `.\supabase_start_local.bat` |
| Stop local Supabase | `.\supabase_stop_local.bat` |
| Check status | `.\supabase_status.bat` |
| Link to remote | `.\supabase_link_remote.bat` |
| Start Django project | `.\start.bat` |

---

**Happy coding! 🚀**

