# 🔧 Fix Supabase Connection - IPv4 Compatibility Issue

## Problem Identified

Your Supabase connection string shows: **"Not IPv4 compatible"**

This means:
- Your Supabase database hostname resolves to IPv6 only
- Your network/Django is trying to use IPv4
- Connection fails because of this mismatch

## ✅ Solution: Use Session Pooler

Supabase provides a **Session Pooler** that works with IPv4 networks.

### Step 1: Get Session Pooler Connection String

1. In the Supabase modal you have open:
   - Click **"Pooler settings"** button (or go to Settings → Database → Connection Pooling)
   - Select **"Session mode"** (recommended for Django)
   - Copy the connection string

2. The pooler connection string will look like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```
   OR
   ```
   postgresql://postgres:[YOUR-PASSWORD]@[region].pooler.supabase.com:6543/postgres
   ```

### Step 2: Extract the Hostname

From the connection string:
- **Before:** `db.rcetefvuniellfuneejg.supabase.co`
- **After:** `aws-0-us-east-1.pooler.supabase.com` (or similar)

The hostname is the part between `@` and `:6543` (or `:5432`)

### Step 3: Update Your .env File

Open your `.env` file and update:

```env
# Change this line:
DB_HOST=db.rcetefvuniellfuneejg.supabase.co

# To the pooler hostname (example):
DB_HOST=aws-0-us-east-1.pooler.supabase.com

# Also update the port if needed (pooler usually uses 6543):
DB_PORT=6543
```

### Step 4: Test the Connection

Run:
```powershell
.\test_supabase_connection.bat
```

Or manually:
```powershell
.\venv\Scripts\python.exe manage.py check --database default
```

### Step 5: Run Migrations

Once connection works:
```powershell
.\venv\Scripts\python.exe manage.py migrate
```

### Step 6: Start Server

```powershell
.\start_dev.bat
```

---

## Alternative: Direct Connection (If You Have IPv6)

If you want to use the direct connection, you need:
1. IPv6 support on your network, OR
2. Purchase Supabase IPv4 add-on

But **Session Pooler is recommended** and works perfectly for Django!

---

## Quick Reference

**Current (Not Working):**
```
DB_HOST=db.rcetefvuniellfuneejg.supabase.co
DB_PORT=5432
```

**New (Should Work):**
```
DB_HOST=[your-pooler-hostname].pooler.supabase.com
DB_PORT=6543
```

The pooler hostname will be different - get it from Supabase Dashboard → Settings → Database → Connection Pooling → Session mode

