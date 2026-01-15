# Quick Fix: Use SQLite for Local Development

## The Problem
You're getting database connection errors because PostgreSQL/Supabase credentials are incorrect or the database is not accessible.

## The Solution
**Use SQLite for local development** - it's simpler, faster, and doesn't require a database server!

## Quick Steps

### Option 1: Use the Script (Easiest)
```bash
# Run the helper script
scripts\use_sqlite.bat
```

This will automatically comment out your PostgreSQL configuration.

### Option 2: Manual Fix

1. **Open your `.env` file**

2. **Comment out or remove these lines:**
   ```env
   # DB_NAME=postgres
   # DB_USER=postgres.rcetefvuniellfuneejg
   # DB_PASSWORD=your_password
   # DB_HOST=aws-0-us-west-2.pooler.supabase.com
   # DB_PORT=5432
   ```

3. **Save the file**

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Load sample data:**
   ```bash
   python manage.py load_sample_data
   ```

## What Happens?

- Django will automatically create `db.sqlite3` in your project root
- All migrations will run against SQLite
- Sample data will load successfully
- No database server needed!

## Your .env File Should Look Like:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database - Using SQLite (no configuration needed)
# DB_NAME=postgres  <-- Commented out
# DB_USER=...
# DB_PASSWORD=...
# DB_HOST=...
# DB_PORT=...

# Supabase (for OAuth)
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

## After Switching to SQLite

```bash
# 1. Run migrations
python manage.py migrate

# 2. Load sample data
python manage.py load_sample_data

# 3. Create superuser (optional)
python manage.py createsuperuser

# 4. Start server
python manage.py runserver 8000
```

## Why SQLite?

- ✅ No setup required
- ✅ No database server needed
- ✅ Perfect for local development
- ✅ Fast and reliable
- ✅ Easy to backup (just copy `db.sqlite3`)

## When to Use PostgreSQL?

- Production deployment
- When you need advanced PostgreSQL features
- When working with a team that shares a database
- When you have proper database credentials configured

For now, **SQLite is perfect for local development!**

