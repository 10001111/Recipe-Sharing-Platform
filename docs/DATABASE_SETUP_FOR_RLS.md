# Database Setup for RLS - Step by Step

## 🎯 Goal: Set Up PostgreSQL/Supabase for RLS

This guide will help you switch from SQLite to PostgreSQL/Supabase so you can use RLS.

---

## 📋 Prerequisites

- ✅ Supabase account (you already have one!)
- ✅ Supabase project created
- ✅ `.env` file in project root

---

## 🔧 Step-by-Step Setup

### Step 1: Get Supabase Database Credentials

1. **Go to Supabase Dashboard**
   - Visit: https://app.supabase.com
   - Login to your account
   - Select your project

2. **Get Database Settings**
   - Click **Settings** (gear icon) in sidebar
   - Click **Database** in settings menu
   - You'll see connection details

3. **Copy These Values**:
   ```
   Host: db.xxxxx.supabase.co
   Database name: postgres (usually)
   Port: 5432 (usually)
   User: postgres (usually)
   Password: [Your Supabase password]
   ```

---

### Step 2: Update `.env` File

**Location**: `.env` file in project root (same folder as `manage.py`)

**Add/Update These Lines**:

```env
# Database Configuration for PostgreSQL/Supabase
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_supabase_password_here
DB_HOST=db.xxxxx.supabase.co
DB_PORT=5432

# IMPORTANT: Set this to False to use PostgreSQL
USE_SQLITE=False
```

**Replace**:
- `your_supabase_password_here` → Your actual Supabase password
- `db.xxxxx.supabase.co` → Your actual Supabase host

---

### Step 3: Verify Connection

**Test if connection works**:

```bash
python manage.py check --database default
```

**Expected Output**:
```
System check identified no issues (0 silenced).
```

**If you get errors**:
- Check your `.env` file values
- Make sure Supabase project is active (not paused)
- Verify password is correct

---

### Step 4: Run Migrations

**Apply database migrations**:

```bash
python manage.py migrate
```

**This will**:
- Create all tables in PostgreSQL
- Set up database structure
- Keep your existing data (if any)

---

### Step 5: Set Up RLS

**Now you can enable RLS**:

```bash
python manage.py setup_rls
```

**Expected Output**:
```
=== RLS Setup for Django ===

[OK] PostgreSQL detected - RLS can be enabled
[OK] Enabled RLS on users_customuser
[OK] Enabled RLS on recipes_recipe
...
[OK] RLS setup completed successfully!
```

---

## ✅ Verification

**Check if RLS is enabled**:

```bash
python scripts/verify_security_features.py
```

**You should see**:
```
[OK] Database: Working
[OK] RLS: Working
[OK] Email Auth: Working
[OK] Google Auth: Working
```

---

## 🐛 Troubleshooting

### Error: "Could not connect to database"

**Solutions**:
1. Check Supabase project is active (not paused)
2. Verify `.env` file values are correct
3. Check internet connection
4. Try restarting Supabase project

### Error: "ModuleNotFoundError: rest_framework_simplejwt"

**Solution**:
```bash
# Activate venv
.\venv\Scripts\Activate.ps1

# Install package
pip install djangorestframework-simplejwt
```

### Error: "RLS only works with PostgreSQL!"

**This is normal** - You're still using SQLite. Follow steps above to switch to PostgreSQL.

---

## 📝 Example `.env` File

**Complete example** (replace with your values):

```env
# Django Secret Key
SECRET_KEY=your-secret-key-here

# Debug Mode
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (PostgreSQL/Supabase)
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_actual_password
DB_HOST=db.rcetefvuniellfuneejg.supabase.co
DB_PORT=5432
USE_SQLITE=False

# Supabase Configuration
SUPABASE_URL=https://rcetefvuniellfuneejg.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

---

## 🎯 Summary

**To Enable RLS**:

1. ✅ Get Supabase database credentials
2. ✅ Update `.env` file with PostgreSQL settings
3. ✅ Set `USE_SQLITE=False`
4. ✅ Run `python manage.py migrate`
5. ✅ Run `python manage.py setup_rls`
6. ✅ Done!

**RLS is now enabled and protecting your database!** 🎉

---

## 💡 Important Notes

- **Backup First**: Always backup before switching databases
- **Test Connection**: Verify connection before running migrations
- **Keep SQLite**: SQLite is fine for development, PostgreSQL for production
- **RLS is Optional**: Django security is enough, RLS adds extra layer

---

## 🆘 Need Help?

If you encounter issues:
1. Check `.env` file values
2. Verify Supabase project is active
3. Test connection: `python manage.py check --database default`
4. Check error messages carefully

**Most common issue**: Supabase project is paused - resume it in dashboard!

