# RLS (Row Level Security) for Beginners - Simple Explanation

## 🎯 What is RLS?

**RLS = Row Level Security**

**In Simple Terms**: 
- RLS is like a security guard at the database level
- It checks every database query before allowing it
- Makes sure users can only see/edit their own data
- Works even if someone bypasses Django

**Think of it as**: 
- A bouncer at a club checking IDs
- Only lets you see data you're allowed to see
- Extra security layer on top of Django

---

## 🔍 How RLS Works

### Without RLS:
```
User asks: "Show me all recipes"
Database: "Here are ALL recipes" ✅ (even private ones)
```

### With RLS:
```
User asks: "Show me all recipes"
Database: "Let me check... Are you the author? No? Then here are only PUBLISHED recipes" ✅
```

**RLS checks**: "Does this user have permission to see this row?"
- ✅ Yes → Show the row
- ❌ No → Hide the row

---

## 🗄️ Database Requirement

**IMPORTANT**: RLS only works with PostgreSQL!

- ❌ **SQLite**: Does NOT support RLS
- ✅ **PostgreSQL**: Supports RLS
- ✅ **Supabase**: Supports RLS (uses PostgreSQL)

**Your Current Database**: SQLite (doesn't support RLS)

**To Use RLS**: Switch to PostgreSQL/Supabase first

---

## 🔧 What I've Set Up For You

### 1. ✅ RLS Setup Script
**File**: `scripts/setup_rls.py`
- Enables RLS on all tables
- Creates security policies
- Can be run manually

### 2. ✅ Django Management Command
**File**: `apps/api/management/commands/setup_rls.py`
- Easy command: `python manage.py setup_rls`
- Checks if PostgreSQL is being used
- Sets up all RLS policies automatically

### 3. ✅ RLS Middleware
**File**: `apps/api/middleware_rls.py`
- Automatically sets user ID for RLS
- Works with Django authentication
- Already added to your settings

### 4. ✅ SQL Script
**File**: `sql/rls_policies.sql`
- Complete SQL script
- Can be run directly in PostgreSQL
- Documents all policies

---

## 🚀 How to Set Up RLS

### Step 1: Switch to PostgreSQL/Supabase

**If using Supabase** (You already have Supabase configured!):

1. **Check your `.env` file**:
   ```env
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=your_supabase_password
   DB_HOST=db.xxxxx.supabase.co
   DB_PORT=5432
   USE_SQLITE=False
   ```

2. **Make sure Supabase project is active** (not paused)

3. **Test connection**:
   ```bash
   python manage.py check --database default
   ```

### Step 2: Run RLS Setup

**Easy Way** (Recommended):
```bash
python manage.py setup_rls
```

**Alternative Way**:
```bash
python scripts/setup_rls.py
```

### Step 3: Verify It Works

```bash
python scripts/verify_security_features.py
```

---

## 📋 What RLS Policies Were Created

### Users Table
- ✅ Users can see their own profile
- ✅ Users can edit their own profile
- ✅ Everyone can see active user profiles (for recipe authors)

### Recipes Table
- ✅ Everyone can see published recipes
- ✅ Authors can see their own recipes (even unpublished)
- ✅ Only authenticated users can create recipes
- ✅ Authors can edit/delete their own recipes

### Comments Table
- ✅ Everyone can see comments
- ✅ Users can create comments
- ✅ Users can edit/delete their own comments

### Ratings Table
- ✅ Everyone can see ratings
- ✅ Users can create/edit/delete their own ratings

### Favorites Table
- ✅ Users can only see their own favorites
- ✅ Users can create/delete their own favorites

### Meal Plans Table
- ✅ Users can only see their own meal plans
- ✅ Users can create/edit/delete their own meal plans

---

## 🔄 How RLS Works with Django

### The Flow:

1. **User makes request** → Django receives it
2. **RLS Middleware runs** → Sets user ID in database session
3. **Django query runs** → `Recipe.objects.all()`
4. **PostgreSQL checks RLS** → "Can this user see this recipe?"
5. **Result returned** → Only recipes user can see

### Example:

```python
# User requests recipes
user = request.user  # Django user

# RLS middleware sets: app.current_user_id = '123'

# Django query:
recipes = Recipe.objects.filter(author=user)

# PostgreSQL checks RLS:
# - Policy: "Authors can view own recipes"
# - Checks: author_id = '123' AND current_user_id = '123'
# - Result: Returns recipes ✅
```

---

## ⚙️ Current Status

**RLS Setup**: ✅ Ready to use
**Database**: ⚠️ SQLite (needs PostgreSQL for RLS)
**Middleware**: ✅ Enabled
**Policies**: ⚠️ Need to run setup command

**To Enable RLS**:
1. Switch to PostgreSQL/Supabase (if not already)
2. Run: `python manage.py setup_rls`
3. Done! RLS is now active

---

## 🧪 Testing RLS

### Test 1: Check if RLS is Enabled

```bash
python manage.py shell
```

```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT tablename, rowsecurity 
        FROM pg_tables 
        WHERE schemaname = 'public';
    """)
    for table, rls in cursor.fetchall():
        print(f"{table}: RLS {'enabled' if rls else 'disabled'}")
```

### Test 2: Check Policies

```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT tablename, policyname 
        FROM pg_policies 
        WHERE schemaname = 'public';
    """)
    for table, policy in cursor.fetchall():
        print(f"{table}.{policy}")
```

---

## 📚 Files Created

1. ✅ `scripts/setup_rls.py` - RLS setup script
2. ✅ `apps/api/middleware_rls.py` - RLS middleware
3. ✅ `apps/api/management/commands/setup_rls.py` - Management command
4. ✅ `sql/rls_policies.sql` - SQL script
5. ✅ `docs/RLS_SETUP_GUIDE.md` - Setup guide
6. ✅ `docs/RLS_SETUP_COMPLETE.md` - Complete documentation
7. ✅ `docs/RLS_FOR_BEGINNERS.md` - This file

---

## ✅ Summary

**RLS is Ready to Use!**

**What You Have**:
- ✅ All scripts created
- ✅ Middleware configured
- ✅ Policies defined
- ✅ Management command ready

**What You Need**:
- ⚠️ PostgreSQL/Supabase database (currently using SQLite)
- ⚠️ Run setup command: `python manage.py setup_rls`

**Once you switch to PostgreSQL and run the command, RLS will be fully enabled!**

---

## 🎓 Key Points

1. **RLS = Extra Security**: Adds database-level protection
2. **PostgreSQL Only**: Doesn't work with SQLite
3. **Works with Django**: Complements Django security
4. **Automatic**: Middleware handles everything
5. **Optional**: Django security is enough, RLS adds extra layer

---

## 💡 Why Use RLS?

**Benefits**:
- ✅ Extra security if Django is bypassed
- ✅ Database-level protection
- ✅ Defense in depth
- ✅ Prevents unauthorized data access

**When to Use**:
- ✅ Production environments
- ✅ When using PostgreSQL/Supabase
- ✅ When you want extra security
- ✅ When multiple applications access database

**When NOT Needed**:
- ⚠️ Development (Django security is enough)
- ⚠️ Using SQLite (doesn't support RLS)
- ⚠️ Simple applications (Django handles it)

---

## 🚀 Next Steps

1. **Check Database**: Are you using PostgreSQL/Supabase?
2. **If Yes**: Run `python manage.py setup_rls`
3. **If No**: Switch to PostgreSQL/Supabase first
4. **Test**: Verify RLS is working
5. **Monitor**: Check for any issues

---

## 📖 More Information

- **Setup Guide**: `docs/RLS_SETUP_GUIDE.md`
- **Complete Docs**: `docs/RLS_SETUP_COMPLETE.md`
- **SQL Script**: `sql/rls_policies.sql`

**RLS is ready when you are!** 🎉

