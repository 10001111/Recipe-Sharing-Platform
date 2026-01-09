# 🔑 Environment Variables & API Keys Guide

Complete guide to all environment variables and API keys needed for the Recipe Sharing Platform.

## 📋 Required Variables for Database Connection

### 🔴 Critical (Required for Database)

These are **absolutely essential** - your Django app won't connect to the database without them:

#### 1. **SECRET_KEY** 🔐
- **What it is:** Django's secret key for cryptographic operations
- **Where to get it:** Generate it yourself (see below)
- **Required:** YES - Django won't run without it
- **Security:** Keep it secret! Never share or commit to Git

**How to generate:**
```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Example:**
```env
SECRET_KEY=django-insecure-abc123xyz789...very-long-random-string
```

---

#### 2. **DB_NAME** 📊
- **What it is:** Name of your PostgreSQL database
- **Where to get it:** Supabase Settings → Database
- **Required:** YES - for database connection
- **Default value:** Usually `postgres`

**How to find in Supabase:**
1. Go to your Supabase project dashboard
2. Click **Settings** (gear icon) → **Database**
3. Look for "Database name" or check connection string
4. Usually it's `postgres` (default)

**Example:**
```env
DB_NAME=postgres
```

---

#### 3. **DB_USER** 👤
- **What it is:** PostgreSQL database username
- **Where to get it:** Supabase Settings → Database
- **Required:** YES - for database connection
- **Default value:** Usually `postgres`

**How to find in Supabase:**
1. Go to Settings → Database
2. Look for "Database user" or check connection string
3. Usually it's `postgres` (default)

**Example:**
```env
DB_USER=postgres
```

---

#### 4. **DB_PASSWORD** 🔒
- **What it is:** Password for your PostgreSQL database
- **Where to get it:** The password you created when setting up Supabase project
- **Required:** YES - for database connection
- **Security:** Keep it secret! This is your database password

**How to find in Supabase:**
- This is the password you **created** when setting up your Supabase project
- If you forgot it, you can reset it in Supabase Settings → Database → Reset database password

**Example:**
```env
DB_PASSWORD=your-strong-password-here
```

---

#### 5. **DB_HOST** 🌐
- **What it is:** Hostname/URL of your Supabase database server
- **Where to get it:** Supabase Settings → Database
- **Required:** YES - for database connection
- **Format:** `db.xxxxx.supabase.co`

**How to find in Supabase:**
1. Go to Settings → Database
2. Scroll down to "Connection string" or "Connection info"
3. Look for the hostname (starts with `db.` and ends with `.supabase.co`)
4. It looks like: `db.abcdefghijklmnop.supabase.co`

**Example:**
```env
DB_HOST=db.abcdefghijklmnop.supabase.co
```

---

#### 6. **DB_PORT** 🔌
- **What it is:** Port number for PostgreSQL connection
- **Where to get it:** Supabase Settings → Database
- **Required:** YES - for database connection
- **Default value:** `5432` (standard PostgreSQL port)

**How to find in Supabase:**
1. Go to Settings → Database
2. Check connection string or connection info
3. Usually `5432` (default PostgreSQL port)

**Example:**
```env
DB_PORT=5432
```

---

### 🟡 Important (For Future Features)

These are needed for future features but not required for basic database connection:

#### 7. **SUPABASE_URL** 🌍
- **What it is:** Your Supabase project URL
- **Where to get it:** Supabase Settings → API
- **Required:** NO (for now) - but will be needed for Supabase client features
- **Format:** `https://xxxxx.supabase.co`

**How to find in Supabase:**
1. Go to Settings → API
2. Look for "Project URL" or "Reference ID"
3. It's your project's base URL

**Example:**
```env
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
```

---

#### 8. **SUPABASE_ANON_KEY** 🔑
- **What it is:** Anonymous/public API key for Supabase
- **Where to get it:** Supabase Settings → API
- **Required:** NO (for now) - but will be needed for Supabase client features
- **Security:** Can be exposed in frontend code (it's public)
- **Format:** Long string starting with `eyJ...`

**How to find in Supabase:**
1. Go to Settings → API
2. Look for "anon" or "public" key
3. It's a long JWT token starting with `eyJ...`

**Example:**
```env
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYzODk2NzI4MCwiZXhwIjoxOTU0NTQzMjgwfQ.example-signature
```

---

#### 9. **SUPABASE_SERVICE_ROLE_KEY** 🔐
- **What it is:** Service role API key (has admin privileges)
- **Where to get it:** Supabase Settings → API
- **Required:** NO (for now) - but will be needed for admin operations
- **Security:** ⚠️ **KEEP SECRET!** Never expose in frontend - has full database access
- **Format:** Long string starting with `eyJ...`

**How to find in Supabase:**
1. Go to Settings → API
2. Look for "service_role" key
3. It's a long JWT token starting with `eyJ...`
4. ⚠️ **Warning:** This key has admin access - keep it secret!

**Example:**
```env
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNjM4OTY3MjgwLCJleHAiOjE5NTQ1NDMyODB9.example-signature
```

---

### 🟢 Optional (For Development)

#### 10. **DEBUG** 🐛
- **What it is:** Enable/disable Django debug mode
- **Where to get it:** Set it yourself
- **Required:** NO - defaults to `False` (safer)
- **When to use:** Set to `True` for development, `False` for production

**Example:**
```env
DEBUG=True
```

---

#### 11. **ALLOWED_HOSTS** 🌐
- **What it is:** List of allowed hostnames for your Django app
- **Where to get it:** Set it yourself
- **Required:** NO - defaults to `localhost,127.0.0.1`
- **Format:** Comma-separated list

**Example:**
```env
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
```

---

## 📝 Complete .env File Template

Here's what your complete `.env` file should look like:

```env
# ============================================
# DJANGO SETTINGS (Required)
# ============================================
SECRET_KEY=your-generated-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ============================================
# DATABASE CONFIGURATION (Required for DB connection)
# Get these from: Supabase Settings → Database
# ============================================
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-database-password-here
DB_HOST=db.your-project-ref.supabase.co
DB_PORT=5432

# ============================================
# SUPABASE API KEYS (Optional - for future features)
# Get these from: Supabase Settings → API
# ============================================
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

# ============================================
# EMAIL CONFIGURATION (Optional - for later)
# ============================================
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

---

## 🎯 Quick Reference: What You Need Right Now

### Minimum Required (To Start the Project):

```env
SECRET_KEY=your-generated-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=db.xxxxx.supabase.co
DB_PORT=5432
```

### Recommended (For Full Functionality):

Add the Supabase API keys too (even if not using them yet):
```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

---

## 🔍 Where to Find Everything in Supabase

### Step-by-Step Guide:

1. **Go to Supabase Dashboard:**
   - Visit: https://app.supabase.com
   - Log in to your account
   - Select your project

2. **Get Database Credentials:**
   - Click **Settings** (gear icon) in left sidebar
   - Click **Database** in the settings menu
   - Scroll down to find:
     - Connection string (shows host, port, database name)
     - Database password (the one you created)
     - Connection info section

3. **Get API Keys:**
   - Still in Settings, click **API** in the settings menu
   - You'll see:
     - **Project URL** (at the top)
     - **anon public** key (safe to expose)
     - **service_role** key (keep secret!)

---

## ⚠️ Security Best Practices

### 🔴 Never Commit These:
- `.env` file (already in `.gitignore`)
- SECRET_KEY
- DB_PASSWORD
- SUPABASE_SERVICE_ROLE_KEY

### 🟢 Safe to Commit:
- `env.example` file (template without real values)
- Code files
- Documentation

### 🔐 Key Security Rules:

1. **SECRET_KEY:**
   - Generate a unique one for each environment
   - Never reuse between projects
   - If exposed, generate a new one immediately

2. **DB_PASSWORD:**
   - Use a strong password (12+ characters, mixed case, numbers, symbols)
   - Never share it
   - If compromised, reset it in Supabase

3. **SUPABASE_SERVICE_ROLE_KEY:**
   - ⚠️ **Most sensitive** - has admin access
   - Never expose in frontend code
   - Only use in backend/server-side code
   - If exposed, regenerate it in Supabase

4. **SUPABASE_ANON_KEY:**
   - Safe to use in frontend (it's public)
   - Still, don't commit it unnecessarily
   - Can be regenerated if needed

---

## ✅ Verification Checklist

Before starting your project, verify:

- [ ] SECRET_KEY is generated and added
- [ ] DB_NAME is set (usually `postgres`)
- [ ] DB_USER is set (usually `postgres`)
- [ ] DB_PASSWORD is set (your Supabase password)
- [ ] DB_HOST is set (from Supabase)
- [ ] DB_PORT is set (usually `5432`)
- [ ] DEBUG is set (True for development)
- [ ] ALLOWED_HOSTS is set
- [ ] `.env` file is in project root (same folder as `manage.py`)
- [ ] `.env` file is NOT committed to Git (check `git status`)

---

## 🧪 Test Your Configuration

After setting up your `.env` file, test it:

```bash
# Test database connection
python scripts/test_database_connection.py

# Or use Django's check command
python manage.py check --database default

# Or test via API (after starting server)
python manage.py runserver
# Then visit: http://127.0.0.1:8000/api/health/
```

---

## 🆘 Troubleshooting

### Error: "SECRET_KEY not found"
- **Solution:** Make sure `.env` file exists and has SECRET_KEY

### Error: "Database connection failed"
- **Check:** DB_HOST, DB_NAME, DB_USER, DB_PASSWORD are correct
- **Check:** Supabase project is running (not paused)
- **Check:** Network connection

### Error: "Invalid API key"
- **Check:** Copied the full key (they're very long)
- **Check:** No extra spaces or quotes
- **Check:** Using the right key (anon vs service_role)

---

## 📚 Additional Resources

- **Supabase Documentation:** https://supabase.com/docs
- **Django Settings:** https://docs.djangoproject.com/en/4.2/topics/settings/
- **Security Guide:** See [docs/security/SECURITY.md](../security/SECURITY.md)

---

**Last Updated:** Milestone 1.2  
**Next Steps:** Test database connection and run migrations

