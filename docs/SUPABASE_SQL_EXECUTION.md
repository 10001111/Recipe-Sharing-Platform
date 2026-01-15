# 🔧 Supabase SQL Execution Guide

## Overview

You now have multiple ways to execute SQL queries directly on your Supabase database:

1. **Direct PostgreSQL connection** (psycopg2) - Recommended for SQL execution
2. **Supabase Python client** - For REST API operations
3. **Django ORM** - For application-level database operations

---

## ✅ Installed Packages

The following packages are installed and ready to use:

- ✅ `supabase>=2.0.0` - Official Supabase Python client
- ✅ `psycopg2-binary>=2.9.0` - PostgreSQL adapter for direct SQL execution
- ✅ `PyJWT>=2.8.0` - JWT token handling

---

## 🚀 Quick Start

### Method 1: Simple Query Script (Recommended)

**File:** `scripts/supabase_query.py`

```bash
# Execute a SELECT query
python scripts/supabase_query.py "SELECT * FROM users_customuser LIMIT 5;"

# Count records
python scripts/supabase_query.py "SELECT COUNT(*) FROM recipes_recipe;"

# Check user permissions
python scripts/supabase_query.py "SELECT username, email, is_superuser FROM users_customuser;"
```

**Output:**
```
[OK] Query executed successfully. Returned 1 row(s).

username | email              | is_superuser
-------------------------------------------------------
pa381187 | pa381187@gmail.com | True
```

---

### Method 2: Full-Featured SQL Script

**File:** `scripts/execute_sql.py`

```bash
# Execute a query
python scripts/execute_sql.py "SELECT * FROM users_customuser;"

# Execute from file
python scripts/execute_sql.py --file queries/my_query.sql

# Interactive mode
python scripts/execute_sql.py --interactive

# Output as JSON
python scripts/execute_sql.py "SELECT * FROM users_customuser;" --json
```

**Features:**
- ✅ Interactive mode
- ✅ File execution
- ✅ JSON output
- ✅ Transaction control
- ✅ Error handling

---

### Method 3: Using Python Directly

**File:** `scripts/db_execute.py`

```python
from scripts.db_execute import execute_sql

# Execute and get results
results, count = execute_sql("SELECT * FROM users_customuser LIMIT 5;")

# Execute without results (INSERT/UPDATE/DELETE)
_, count = execute_sql("UPDATE users_customuser SET is_active = True;", fetch_results=False)
```

---

## 📋 Common SQL Queries

### Check Users

```sql
-- List all users
SELECT username, email, is_superuser, is_staff, is_active 
FROM users_customuser;

-- Count users
SELECT COUNT(*) as total_users FROM users_customuser;

-- Check user roles (Django Groups)
SELECT u.username, u.email, g.name as role
FROM users_customuser u
LEFT JOIN auth_user_groups ug ON u.id = ug.user_id
LEFT JOIN auth_group g ON ug.group_id = g.id;
```

### Check Recipes

```sql
-- List all recipes
SELECT id, title, author_id, created_at 
FROM recipes_recipe 
ORDER BY created_at DESC 
LIMIT 10;

-- Count recipes by author
SELECT u.username, COUNT(r.id) as recipe_count
FROM users_customuser u
LEFT JOIN recipes_recipe r ON u.id = r.author_id
GROUP BY u.id, u.username;
```

### Check Database Schema

```sql
-- List all tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;

-- Check table structure
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'users_customuser'
ORDER BY ordinal_position;
```

### Check RLS Policies (if enabled)

```sql
-- List all RLS policies
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, policyname;
```

---

## 🔐 Security Notes

### Using Service Role Key

When executing SQL queries, you're connecting directly to PostgreSQL using:
- **DB_USER**: `postgres` (or your database user)
- **DB_PASSWORD**: Your database password
- **Service Role Key**: Used for Supabase API operations

**Important:**
- ✅ Direct SQL execution bypasses Row Level Security (RLS)
- ✅ Use with caution - you have full database access
- ✅ Service role key should NEVER be exposed in frontend code
- ✅ Keep `.env` file secure and never commit it to Git

---

## 🛠️ Troubleshooting

### Connection Errors

**Error:** `could not translate host name`

**Solution:**
1. Check if your Supabase project is paused (free tier pauses after inactivity)
2. Resume project at https://app.supabase.com
3. Verify `.env` file has correct `DB_HOST` and `DB_PORT`

**Error:** `password authentication failed`

**Solution:**
1. Verify `DB_PASSWORD` in `.env` matches your Supabase database password
2. Get password from: Supabase Dashboard → Settings → Database → Database password

**Error:** `relation does not exist`

**Solution:**
- Django table names use format: `app_model` (e.g., `users_customuser`, `recipes_recipe`)
- Check actual table names: `SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';`

---

## 📚 Additional Resources

### Django Table Names

Django automatically creates table names from your models:
- `CustomUser` → `users_customuser`
- `Recipe` → `recipes_recipe`
- `UserProfile` → `users_userprofile`
- `Category` → `recipes_category`

### Useful Scripts

- `scripts/supabase_query.py` - Simple query execution
- `scripts/execute_sql.py` - Full-featured SQL execution
- `scripts/db_execute.py` - Python API for SQL execution
- `scripts/db_shell.py` - Interactive database shell

### Supabase Documentation

- [Supabase Python Client](https://supabase.com/docs/reference/python/introduction)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

---

## 💡 Tips

1. **Always test queries** in interactive mode first
2. **Use transactions** for multiple related queries
3. **Backup data** before running DELETE or UPDATE queries
4. **Use LIMIT** when exploring large tables
5. **Check Django migrations** to understand table structure

---

## Example: Check Current Setup

```bash
# Check users
python scripts/supabase_query.py "SELECT username, email, is_superuser FROM users_customuser;"

# Check roles
python scripts/supabase_query.py "SELECT name FROM auth_group;"

# Check user-role assignments
python scripts/supabase_query.py "SELECT u.username, g.name as role FROM users_customuser u LEFT JOIN auth_user_groups ug ON u.id = ug.user_id LEFT JOIN auth_group g ON ug.group_id = g.id;"
```

---

**Ready to execute SQL queries!** 🚀

