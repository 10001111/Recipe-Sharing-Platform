# Database Setup Guide

## Issue: Database Connection Error

If you're seeing errors like:
```
could not translate host name "postgresql://..." to address
```

This means your `.env` file has an incorrect `DB_HOST` configuration.

## Solution Options

### Option 1: Use SQLite for Local Development (Recommended)

For local development and testing, SQLite is simpler and doesn't require a database server.

**In your `.env` file, comment out or remove these lines:**
```env
# DB_NAME=postgres
# DB_USER=postgres
# DB_PASSWORD=your_password
# DB_HOST=your_host
# DB_PORT=5432
```

Django will automatically use SQLite (`db.sqlite3`) when `DB_NAME` is not set.

### Option 2: Fix PostgreSQL Configuration

If you want to use PostgreSQL/Supabase, your `.env` file should have:

```env
# Database Configuration
DB_NAME=postgres
DB_USER=postgres.rcetefvuniellfuneejg
DB_PASSWORD=your_password_here
DB_HOST=aws-0-us-west-2.pooler.supabase.com
DB_PORT=5432
```

**Important:** 
- `DB_HOST` should be **just the hostname**, not a full connection URL
- Do NOT include `postgresql://` or `postgres://` in `DB_HOST`
- Do NOT include username/password in `DB_HOST`

### Option 3: Parse Connection String (Automatic Fix)

The settings.py file now automatically detects if `DB_HOST` contains a full connection URL and extracts just the hostname. However, it's better to fix your `.env` file directly.

## Example .env File for SQLite (Local Development)

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite - no configuration needed)
# Leave DB_NAME unset to use SQLite

# Supabase (for OAuth)
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

## Example .env File for PostgreSQL/Supabase

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL/Supabase)
DB_NAME=postgres
DB_USER=postgres.rcetefvuniellfuneejg
DB_PASSWORD=your_password_here
DB_HOST=aws-0-us-west-2.pooler.supabase.com
DB_PORT=5432

# Supabase (for OAuth)
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

## Verifying Database Configuration

After fixing your `.env` file:

```bash
# Check Django configuration
python manage.py check

# Run migrations
python manage.py migrate

# Load sample data
python manage.py load_sample_data
```

## Troubleshooting

### Error: "could not translate host name"
- **Cause**: `DB_HOST` contains a full connection URL instead of just hostname
- **Fix**: Extract just the hostname from your connection string

### Error: "connection refused" or "timeout"
- **Cause**: Database server is not accessible
- **Fix**: Check your network connection or use SQLite for local development

### Error: "authentication failed"
- **Cause**: Wrong username/password in `.env`
- **Fix**: Verify your database credentials

### Want to Force SQLite?
- Simply remove or comment out `DB_NAME` in your `.env` file
- Django will automatically use SQLite

