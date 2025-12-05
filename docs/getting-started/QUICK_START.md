# ⚡ Quick Start - Complete Milestone 1.1

This is a quick reference to complete the remaining steps of Milestone 1.1.

## 🚀 Final Steps (25-30 minutes)

### Step 1: Create `.env` File (2 minutes)

```bash
# Windows
copy env.example .env

# Mac/Linux
cp env.example .env
```

### Step 2: Generate SECRET_KEY (1 minute)

```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and add it to your `.env` file:
```env
SECRET_KEY=paste-generated-key-here
```

### Step 3: Set Up Supabase (15-20 minutes)

1. Go to https://supabase.com and sign up
2. Create a new project:
   - Name: `recipe-sharing-platform`
   - Set a strong database password (save it!)
   - Choose your region
3. Wait 2-3 minutes for project setup
4. Get your credentials:
   - Go to Settings → Database
   - Note: Host, Database name, User, Port
   - Use the password you created
5. Get API keys:
   - Go to Settings → API
   - Copy: Project URL, anon key, service_role key

### Step 4: Configure `.env` File (5 minutes)

Edit `.env` and fill in:

```env
SECRET_KEY=your-generated-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (from Supabase Settings → Database)
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-supabase-password
DB_HOST=db.xxxxx.supabase.co
DB_PORT=5432

# Supabase API (from Supabase Settings → API)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

### Step 5: Test Database Connection (1 minute)

```bash
python manage.py check --database default
```

Should return: "System check identified no issues"

### Step 6: Run Migrations (1 minute)

```bash
python manage.py migrate
```

### Step 7: Create Superuser (1 minute)

```bash
python manage.py createsuperuser
```

Enter username, email, and password when prompted.

### Step 8: Start Development Server (1 minute)

```bash
python manage.py runserver
```

Visit:
- Main site: http://127.0.0.1:8000
- Admin panel: http://127.0.0.1:8000/admin

## ✅ Verification Checklist

- [ ] `.env` file created
- [ ] SECRET_KEY generated and added
- [ ] Supabase account created
- [ ] Supabase project created
- [ ] Database credentials added to `.env`
- [ ] Database connection test passes
- [ ] Migrations run successfully
- [ ] Superuser created
- [ ] Development server runs
- [ ] Can access http://127.0.0.1:8000
- [ ] Can log into admin panel

## 🎉 You're Done!

Once all checkboxes are checked, **Milestone 1.1 is complete!**

---

**Need detailed instructions?** See [SETUP_GUIDE.md](SETUP_GUIDE.md)

