# Row Level Security (RLS) Setup Guide for Django

## 📚 What is RLS?

**Row Level Security (RLS)** is a PostgreSQL feature that adds database-level security. It ensures that users can only access rows they're allowed to see, even if they bypass Django.

**Think of it as**: A security guard at the database level that checks every query before allowing it.

---

## ⚠️ Important Prerequisites

### Database Requirement

**RLS only works with PostgreSQL/Supabase!**

- ❌ **SQLite**: Does NOT support RLS
- ✅ **PostgreSQL**: Supports RLS
- ✅ **Supabase**: Supports RLS (uses PostgreSQL)

**Current Status**: You're using SQLite, so you'll need to switch to PostgreSQL/Supabase first.

---

## 🔄 Step 1: Switch to PostgreSQL/Supabase (If Needed)

### Option A: Use Supabase (Recommended)

1. **Get Supabase Credentials**:
   - Go to https://app.supabase.com
   - Select your project
   - Go to Settings → Database
   - Copy connection details

2. **Update `.env` file**:
   ```env
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=db.xxxxx.supabase.co
   DB_PORT=5432
   USE_SQLITE=False
   ```

3. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

### Option B: Use Local PostgreSQL

1. **Install PostgreSQL** (if not installed)
2. **Create Database**:
   ```bash
   createdb recipe_sharing
   ```
3. **Update `.env` file**:
   ```env
   DB_NAME=recipe_sharing
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   USE_SQLITE=False
   ```

---

## 🔒 Step 2: Enable RLS on Tables

RLS needs to be enabled on each table you want to protect.

### Tables to Protect

1. **Users Table** (`users_customuser`)
2. **Recipes Table** (`recipes_recipe`)
3. **Comments Table** (`recipes_comment`)
4. **Ratings Table** (`recipes_rating`)
5. **Favorites Table** (`recipes_favorite`)
6. **Meal Plans Table** (`recipes_mealplan`)

---

## 📋 Step 3: Create RLS Policies

RLS policies define WHO can access WHAT data.

### Policy Types

- **SELECT**: Who can read data
- **INSERT**: Who can create data
- **UPDATE**: Who can modify data
- **DELETE**: Who can remove data

---

## 🛠️ Implementation

I'll create:
1. SQL script to enable RLS
2. SQL script to create policies
3. Django management command to set up RLS
4. Verification script

---

## 🎯 RLS Policies We'll Create

### 1. Users Table
- Users can view their own profile
- Users can update their own profile
- Admins can view all profiles

### 2. Recipes Table
- Anyone can view published recipes
- Authors can edit/delete their own recipes
- Authenticated users can create recipes

### 3. Comments Table
- Anyone can view comments
- Authors can edit/delete their own comments
- Authenticated users can create comments

### 4. Ratings Table
- Anyone can view ratings
- Users can create/edit their own ratings
- Users can delete their own ratings

### 5. Favorites Table
- Users can view their own favorites
- Users can create/delete their own favorites

### 6. Meal Plans Table
- Users can view their own meal plans
- Users can create/edit/delete their own meal plans

---

## ⚙️ How RLS Works with Django

**Important**: RLS works alongside Django, not instead of it!

**Two Layers of Security**:
1. **Django Layer** (Primary): Checks permissions in views
2. **RLS Layer** (Secondary): Database-level protection

**Benefits**:
- ✅ Extra security if Django is bypassed
- ✅ Protection against SQL injection
- ✅ Database-level access control
- ✅ Defense in depth

---

## 📝 Next Steps

After switching to PostgreSQL/Supabase, I'll:
1. Create SQL scripts to enable RLS
2. Create RLS policies for all tables
3. Create Django management command
4. Test RLS policies
5. Document everything

---

## ⚠️ Important Notes

1. **RLS requires PostgreSQL** - SQLite won't work
2. **RLS works with Supabase Auth** - May need adjustments for Django auth
3. **Test thoroughly** - RLS can block legitimate queries if misconfigured
4. **Backup first** - Always backup before making database changes

---

## 🔍 Current Status

**Database**: SQLite (needs to switch to PostgreSQL for RLS)
**RLS Status**: Not enabled (requires PostgreSQL)
**Next Step**: Switch to PostgreSQL/Supabase, then enable RLS

