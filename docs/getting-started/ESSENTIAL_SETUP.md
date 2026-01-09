# 🚀 Essential Setup Guide - Getting Started

Quick reference for essential things you need to know before starting the project.

## ✅ Prerequisites Checklist

Before you begin, make sure you have:

- [x] Python 3.9+ installed
- [x] Virtual environment activated
- [x] Dependencies installed (`pip install -r requirements.txt`)
- [x] Supabase account created
- [x] Supabase project created
- [x] `.env` file created and configured

---

## 🔑 Essential API Keys & Credentials

### Required for Database Connection:

1. **SECRET_KEY** - Django secret key (generate yourself)
2. **DB_NAME** - Database name (usually `postgres`)
3. **DB_USER** - Database user (usually `postgres`)
4. **DB_PASSWORD** - Your Supabase database password
5. **DB_HOST** - Your Supabase database host
6. **DB_PORT** - Database port (usually `5432`)

### Optional (For Future Features):

7. **SUPABASE_URL** - Your Supabase project URL
8. **SUPABASE_ANON_KEY** - Public API key
9. **SUPABASE_SERVICE_ROLE_KEY** - Admin API key (keep secret!)

**📖 Detailed Guide:** See [ENV_VARIABLES_GUIDE.md](ENV_VARIABLES_GUIDE.md)

---

## 🎯 Quick Start Steps

### 1. Generate SECRET_KEY

```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and add to `.env`:
```env
SECRET_KEY=paste-generated-key-here
```

### 2. Get Supabase Database Credentials

1. Go to https://app.supabase.com
2. Select your project
3. Go to **Settings** → **Database**
4. Copy:
   - Host (looks like `db.xxxxx.supabase.co`)
   - Database name (usually `postgres`)
   - User (usually `postgres`)
   - Port (usually `5432`)
   - Password (the one you created)

### 3. Get Supabase API Keys (Optional)

1. Still in Settings, go to **API**
2. Copy:
   - Project URL
   - anon public key
   - service_role key

### 4. Configure `.env` File

Edit your `.env` file with all credentials. See `env.example` for template.

### 5. Test Database Connection

```bash
python scripts/test_database_connection.py
```

Should show: ✅ Connection successful!

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Start Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## ⚠️ Essential Security Rules

1. **Never commit `.env` file** - It's already in `.gitignore`
2. **Keep SECRET_KEY secret** - Never share it
3. **Keep DB_PASSWORD secret** - Never share it
4. **Keep SUPABASE_SERVICE_ROLE_KEY secret** - Has admin access
5. **SUPABASE_ANON_KEY is safe** - Can be used in frontend (it's public)

---

## 🧪 Testing Your Setup

### Test Database Connection:
```bash
python scripts/test_database_connection.py
```

### Test Django Configuration:
```bash
python manage.py check
```

### Test API Endpoints:
```bash
# Start server
python manage.py runserver

# In another terminal or browser:
curl http://127.0.0.1:8000/api/
curl http://127.0.0.1:8000/api/health/
```

---

## 📁 Project Structure Overview

```
Recipe-Sharing-Platform/
├── config/          # Django project settings
├── apps/            # Your Django apps
│   ├── recipes/     # Recipe management
│   ├── users/       # User management
│   └── api/         # REST API endpoints
├── static/          # CSS, JS, images
├── media/           # User uploads
├── templates/       # HTML templates
├── scripts/         # Helper scripts
├── docs/            # Documentation
├── .env             # Your secrets (not in Git!)
├── manage.py        # Django management
└── requirements.txt # Dependencies
```

---

## 🎓 Key Concepts to Understand

### Virtual Environment
- Isolates your project's Python packages
- Always activate before working: `.\venv\Scripts\Activate.ps1` (Windows)

### Environment Variables (.env)
- Stores sensitive configuration
- Never committed to Git
- Loaded by Django automatically

### Django Apps
- Modular components of your project
- Each app handles a specific feature
- We have: recipes, users, api

### Database Connection
- Uses PostgreSQL via Supabase
- Credentials stored in `.env`
- Falls back to SQLite if not configured

---

## 🆘 Common Issues & Solutions

### "SECRET_KEY not found"
- **Fix:** Add SECRET_KEY to `.env` file

### "Database connection failed"
- **Fix:** Check DB credentials in `.env`
- **Fix:** Verify Supabase project is running

### "Module not found"
- **Fix:** Activate virtual environment
- **Fix:** Run `pip install -r requirements.txt`

---

## 📚 Next Steps

1. ✅ Complete `.env` configuration
2. ✅ Test database connection
3. ✅ Run migrations
4. ✅ Create superuser
5. ✅ Start development server
6. 🚀 Move to Milestone 1.3: Database Models

---

## 📖 Additional Resources

- **Environment Variables:** [ENV_VARIABLES_GUIDE.md](ENV_VARIABLES_GUIDE.md)
- **Setup Guide:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Security:** [../security/SECURITY.md](../security/SECURITY.md)
- **Quick Start:** [QUICK_START.md](QUICK_START.md)

---

**Ready to start?** Follow the Quick Start Steps above! 🚀

