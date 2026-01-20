# RLS Setup Complete - Implementation Guide

## ✅ What Was Created

I've set up everything you need for Row Level Security (RLS) in Django:

### 1. **RLS Setup Script** (`scripts/setup_rls.py`)
- Enables RLS on all tables
- Creates security policies
- Can be run manually or via management command

### 2. **Django Management Command** (`apps/api/management/commands/setup_rls.py`)
- Easy command: `python manage.py setup_rls`
- Checks database type
- Sets up all RLS policies

### 3. **RLS Middleware** (`apps/api/middleware_rls.py`)
- Automatically sets user ID for RLS policies
- Works with Django authentication
- Already added to `MIDDLEWARE` in settings

### 4. **SQL Script** (`sql/rls_policies.sql`)
- Complete SQL script for manual setup
- Can be run directly in PostgreSQL
- Documents all policies

### 5. **Documentation**
- `docs/RLS_SETUP_GUIDE.md` - Setup instructions
- `docs/RLS_SETUP_COMPLETE.md` - This file

---

## ⚠️ IMPORTANT: Database Requirement

**RLS only works with PostgreSQL/Supabase!**

**Current Status**: You're using SQLite, which doesn't support RLS.

**To Use RLS**:
1. Switch to PostgreSQL/Supabase database
2. Run `python manage.py setup_rls`
3. RLS will be enabled automatically

---

## 🚀 How to Set Up RLS

### Step 1: Switch to PostgreSQL/Supabase

**If using Supabase** (Recommended):
1. Get your Supabase database credentials
2. Update `.env` file:
   ```env
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=your_supabase_password
   DB_HOST=db.xxxxx.supabase.co
   DB_PORT=5432
   USE_SQLITE=False
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```

**If using Local PostgreSQL**:
1. Install PostgreSQL
2. Create database: `createdb recipe_sharing`
3. Update `.env` file with PostgreSQL credentials
4. Run migrations

### Step 2: Run RLS Setup

**Option A: Using Management Command** (Recommended)
```bash
python manage.py setup_rls
```

**Option B: Using Python Script**
```bash
python scripts/setup_rls.py
```

**Option C: Using SQL Script**
```bash
psql -d your_database -f sql/rls_policies.sql
```

### Step 3: Verify RLS is Working

```bash
python scripts/verify_security_features.py
```

---

## 🔒 What RLS Policies Were Created

### Users Table (`users_customuser`)
- ✅ Users can view their own profile
- ✅ Users can update their own profile
- ✅ Public can view active user profiles

### Recipes Table (`recipes_recipe`)
- ✅ Anyone can view published recipes
- ✅ Authors can view their own recipes (even unpublished)
- ✅ Authenticated users can create recipes
- ✅ Authors can update/delete their own recipes

### Comments Table (`recipes_comment`)
- ✅ Anyone can view comments
- ✅ Authenticated users can create comments
- ✅ Authors can update/delete their own comments

### Ratings Table (`recipes_rating`)
- ✅ Anyone can view ratings
- ✅ Users can create/update/delete their own ratings

### Favorites Table (`recipes_favorite`)
- ✅ Users can view/create/delete their own favorites

### Meal Plans Table (`recipes_mealplan`)
- ✅ Users can view/create/update/delete their own meal plans

---

## 🔧 How RLS Works with Django

### The Flow:

1. **User makes request** → Django middleware runs
2. **RLS Middleware** → Sets `app.current_user_id` in PostgreSQL session
3. **Django ORM query** → PostgreSQL checks RLS policies
4. **RLS Policy** → Checks if user has permission
5. **Result** → Returns only allowed rows

### Example:

```python
# User requests their recipes
user = request.user  # Django user object

# RLS middleware sets: app.current_user_id = '123'

# Django query:
recipes = Recipe.objects.filter(author=user)

# PostgreSQL checks RLS:
# - Policy: "Authors can view own recipes"
# - Checks: author_id = '123' AND current_user_id = '123'
# - Result: Returns recipes ✅
```

---

## 📋 RLS Middleware

**Already Added**: `apps.api.middleware_rls.RLSAuthMiddleware`

**What it does**:
- Sets `app.current_user_id` for authenticated users
- Clears it after request
- Only works with PostgreSQL (skips for SQLite)

**Location**: `config/settings.py` → `MIDDLEWARE` list

---

## 🧪 Testing RLS

### Test 1: Verify RLS is Enabled

```bash
python manage.py shell
```

```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT tablename, rowsecurity 
        FROM pg_tables 
        WHERE schemaname = 'public' 
        AND tablename LIKE 'recipes_%';
    """)
    for table, rls in cursor.fetchall():
        print(f"{table}: RLS {'enabled' if rls else 'disabled'}")
```

### Test 2: Check Policies

```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT tablename, policyname, cmd 
        FROM pg_policies 
        WHERE schemaname = 'public';
    """)
    for table, policy, cmd in cursor.fetchall():
        print(f"{table}.{policy} ({cmd})")
```

### Test 3: Test User Access

```python
from django.contrib.auth import get_user_model
from apps.recipes.models import Recipe

User = get_user_model()
user = User.objects.first()

# Set user ID for RLS
with connection.cursor() as cursor:
    cursor.execute("SET app.current_user_id = %s", [str(user.id)])

# Query recipes
recipes = Recipe.objects.all()
print(f"User {user.username} can see {recipes.count()} recipes")
```

---

## ⚙️ Configuration

### Current Setup

**Middleware**: ✅ Enabled (`RLSAuthMiddleware`)
**Policies**: ⚠️ Need to run setup script
**Database**: ⚠️ Need PostgreSQL/Supabase

### To Enable RLS:

1. **Switch to PostgreSQL** (if using SQLite)
2. **Run setup command**: `python manage.py setup_rls`
3. **Verify**: Check that policies are created
4. **Test**: Make sure queries still work

---

## 🎯 Next Steps

1. **Switch to PostgreSQL/Supabase** (if not already)
2. **Run RLS setup**: `python manage.py setup_rls`
3. **Test your application**: Make sure everything still works
4. **Monitor**: Check for any RLS-related errors

---

## 📚 Files Created

1. `scripts/setup_rls.py` - RLS setup script
2. `apps/api/middleware_rls.py` - RLS middleware
3. `apps/api/management/commands/setup_rls.py` - Management command
4. `sql/rls_policies.sql` - SQL script
5. `docs/RLS_SETUP_GUIDE.md` - Setup guide
6. `docs/RLS_SETUP_COMPLETE.md` - This file

---

## ✅ Summary

**RLS Setup is Ready!**

- ✅ All scripts created
- ✅ Middleware configured
- ✅ Policies defined
- ⚠️ Need PostgreSQL/Supabase database
- ⚠️ Need to run setup command

**Once you switch to PostgreSQL and run the setup command, RLS will be fully enabled!**

