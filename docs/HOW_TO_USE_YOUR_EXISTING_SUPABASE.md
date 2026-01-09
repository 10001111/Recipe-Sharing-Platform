# 🎯 How to Use Your Existing Supabase Project

## ✅ You Already Have Everything!

I can see you have a `.env` file with your Supabase project credentials:
- **Project ID:** `rcetefvuniellfuneejg`
- **Database:** Already configured
- **API Keys:** Already set up

**You don't need to create anything new!** Just use what you have.

---

## 🚀 Simple Steps to Use Your Existing Project

### Step 1: Link Supabase CLI to Your Existing Project

Open PowerShell and run:

```powershell
npx supabase link --project-ref rcetefvuniellfuneejg
```

This connects Supabase CLI to your existing project. You'll be asked to log in if you haven't already.

### Step 2: Fix the IPv4 Connection Issue

Your `.env` currently has:
```
DB_HOST=db.rcetefvuniellfuneejg.supabase.co
DB_PORT=5432
```

**This is IPv6-only and won't work.** You need to use the **Session Pooler** instead.

**Update your `.env` file:**
1. Go to https://app.supabase.com/project/rcetefvuniellfuneejg
2. Go to **Settings → Database → Connection Pooling**
3. Copy the **Session mode** connection string
4. Extract the hostname (the part between `@` and `:6543`)

Update `.env`:
```env
DB_HOST=aws-0-us-east-1.pooler.supabase.com  # Use YOUR pooler hostname
DB_PORT=6543  # Pooler uses port 6543
```

### Step 3: Start Your Project

Just run:
```powershell
.\start.bat
```

That's it! It will use your existing Supabase project.

---

## 🔄 How to Switch Between Projects

If you want to use a different Supabase project:

### Option 1: Update .env File
1. Get credentials from your other Supabase project
2. Update `.env` file with new credentials
3. Run `.\start.bat`

### Option 2: Use Supabase CLI Link
```powershell
# Link to different project
npx supabase link --project-ref YOUR_OTHER_PROJECT_ID

# This updates supabase/.temp/project-ref
# But Django still uses .env file, so update .env too!
```

**Important:** Django reads from `.env` file, so you need to update `.env` even if you link with CLI.

---

## 🗑️ What Batch Files Do You Actually Need?

**You only need ONE file:**
- ✅ `start.bat` - This does everything (cleanup, setup, start)

**Optional (only if you want to use local Supabase):**
- `supabase_start_local.bat` - Start local Supabase (for offline development)
- `supabase_stop_local.bat` - Stop local Supabase

**You can DELETE these (not needed):**
- ❌ `start_dev.bat` - Same as start.bat
- ❌ `quick_start.bat` - Not needed
- ❌ `cleanup.bat` - Already in start.bat
- ❌ `test_supabase_connection.bat` - Not needed
- ❌ `supabase_status.bat` - Can use CLI directly
- ❌ `supabase_link_remote.bat` - Can use CLI directly

---

## 📝 Simple Workflow

**Daily development:**
```powershell
.\start.bat
```

**If you need to check Supabase:**
```powershell
npx supabase status
```

**If you want to pull latest schema from Supabase:**
```powershell
npx supabase db pull
```

**That's it!** No need for multiple batch files.

---

## 🎯 Key Points

1. **Your `.env` file is already correct** - Just need to fix IPv4 issue (use pooler)
2. **Supabase CLI is optional** - Django works fine without it
3. **You only need `start.bat`** - Everything else is optional
4. **To switch projects** - Just update `.env` file with new credentials

---

## ❓ Common Questions

**Q: Do I need Supabase CLI?**
A: No! Django works fine with just `.env` file. CLI is only useful if you want to:
- Run Supabase locally (offline development)
- Pull/push database schema
- Manage migrations

**Q: How do I use my other Supabase project?**
A: Just update `.env` file with that project's credentials. No CLI needed.

**Q: Why so many batch files?**
A: You're right - you only need `start.bat`. The others are optional helpers.

---

## ✅ Quick Fix Right Now

1. **Fix IPv4 issue** - Update `.env` to use Session Pooler (see Step 2 above)
2. **Run:** `.\start.bat`
3. **Done!** Your project will connect to your existing Supabase project.

