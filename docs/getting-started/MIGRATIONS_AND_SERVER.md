# 🚀 Running Migrations and Starting the Server

## ⚠️ Current Issue: Database Connection

**Error:** `could not translate host name "db.rcetefvuniellfuneejg.supabase.co" to address`

**This means:** Your Supabase project is likely **paused** (common on free tier after inactivity).

---

## 🔧 Solution Options

### Option 1: Resume Supabase Project (Recommended)

1. **Go to:** https://app.supabase.com
2. **Check project status** - if it shows "Paused", click "Resume"
3. **Wait 1-2 minutes** for the database to wake up
4. **Then run migrations:**
   ```bash
   python manage.py migrate
   ```

### Option 2: Use SQLite Temporarily (For Testing)

If you want to test the server without Supabase:

1. **Temporarily comment out DB_NAME** in `.env`:
   ```env
   # DB_NAME=postgres
   ```
2. **Django will automatically use SQLite** (local file database)
3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```
4. **Start server:**
   ```bash
   python manage.py runserver
   ```

**Note:** SQLite is fine for development/testing, but use PostgreSQL/Supabase for production!

---

## 📋 Step-by-Step: Running Migrations

### 1. Check Database Connection
```bash
python manage.py check --database default
```

### 2. Create Migrations (if you changed models)
```bash
python manage.py makemigrations
```

### 3. Apply Migrations
```bash
python manage.py migrate
```

**What this does:**
- Creates database tables for your Django apps
- Sets up user authentication tables
- Creates admin interface tables
- Applies all model changes

---

## 🚀 Starting the Development Server

### Basic Command:
```bash
python manage.py runserver
```

### With Custom Port:
```bash
python manage.py runserver 8000
```

### Access Your Site:
- **Homepage:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **API Health Check:** http://127.0.0.1:8000/api/health/

---

## 🎯 What Happens When You Start the Server

1. **Django checks your settings**
2. **Tries to connect to database** (if configured)
3. **Starts web server** on port 8000
4. **Shows you URLs** you can visit
5. **Logs all requests** in the terminal

---

## ⚠️ Common Issues

### Issue 1: Database Connection Error
**Symptom:** `could not translate host name...`

**Solution:** Resume your Supabase project or use SQLite temporarily

### Issue 2: Port Already in Use
**Symptom:** `Error: That port is already in use`

**Solution:** Use a different port:
```bash
python manage.py runserver 8001
```

### Issue 3: Migration Conflicts
**Symptom:** `Conflicting migrations detected`

**Solution:** 
```bash
python manage.py makemigrations --merge
python manage.py migrate
```

---

## ✅ Success Indicators

### When Migrations Work:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, users
Running migrations:
  Applying users.0001_initial... OK
  ...
```

### When Server Starts:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 🎓 Understanding Migrations

**What are migrations?**
- They're like "version control" for your database
- They track changes to your database structure
- They create/modify/delete tables and columns

**Why do we need them?**
- Django models define what your database should look like
- Migrations translate those models into actual database tables
- They ensure everyone's database matches your code

**Example:**
- You create a `UserProfile` model
- Run `makemigrations` → Creates migration file
- Run `migrate` → Creates `users_userprofile` table in database

---

## 📝 Next Steps After Server Starts

1. **Visit homepage:** http://127.0.0.1:8000/
2. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```
3. **Access admin:** http://127.0.0.1:8000/admin/
4. **Test user registration:** http://127.0.0.1:8000/users/register/
5. **Test API:** http://127.0.0.1:8000/api/health/

---

**Ready to test your Recipe Sharing Platform!** 🎉




