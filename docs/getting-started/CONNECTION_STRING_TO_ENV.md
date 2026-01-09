# 🔄 Converting Connection String to .env Variables

## Quick Reference Guide

### Supabase Connection String Format:
```
postgresql://postgres:[YOUR-PASSWORD]@db.rcetefvuniellfuneejg.supabase.co:5432/postgres
```

### How to Extract Each Part:

```
postgresql://postgres:[YOUR-PASSWORD]@db.rcetefvuniellfuneejg.supabase.co:5432/postgres
│          │        │                  │                                    │    │
│          │        │                  │                                    │    └─ DB_NAME
│          │        │                  │                                    └────── DB_PORT
│          │        │                  └─────────────────────────────────────────── DB_HOST
│          │        └──────────────────────────────────────────────────────────── DB_PASSWORD
│          └──────────────────────────────────────────────────────────────────── DB_USER
└────────────────────────────────────────────────────────────────────────────── (ignore)
```

---

## Step-by-Step Extraction

### 1. Username (DB_USER)
- **Location:** After `postgresql://` and before `:`
- **From string:** `postgres`
- **In .env:** `DB_USER=postgres`

### 2. Password (DB_PASSWORD)
- **Location:** After `:` and before `@`
- **From string:** `[YOUR-PASSWORD]` (replace with actual password)
- **In .env:** `DB_PASSWORD=your-actual-password`

### 3. Hostname (DB_HOST)
- **Location:** After `@` and before `:5432`
- **From string:** `db.rcetefvuniellfuneejg.supabase.co`
- **In .env:** `DB_HOST=db.rcetefvuniellfuneejg.supabase.co`

### 4. Port (DB_PORT)
- **Location:** After hostname `:` and before `/postgres`
- **From string:** `5432`
- **In .env:** `DB_PORT=5432`

### 5. Database Name (DB_NAME)
- **Location:** After the last `/`
- **From string:** `postgres`
- **In .env:** `DB_NAME=postgres`

---

## Example Conversion

### Input (Connection String):
```
postgresql://postgres:mypassword123@db.rcetefvuniellfuneejg.supabase.co:5432/postgres
```

### Output (.env file):
```env
DB_USER=postgres
DB_PASSWORD=mypassword123
DB_HOST=db.rcetefvuniellfuneejg.supabase.co
DB_PORT=5432
DB_NAME=postgres
```

---

## Your Current .env Configuration

Based on your connection string, your `.env` should have:

```env
DB_USER=postgres
DB_PASSWORD=supa1234!"#$
DB_HOST=db.rcetefvuniellfuneejg.supabase.co
DB_PORT=5432
DB_NAME=postgres
```

**✅ This looks correct!** The hostname matches what Supabase shows.

---

## If Using Connection Pooler

If you switch to connection pooler, the hostname will be different:

**Pooler Connection String:**
```
postgresql://postgres:password@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

**Updated .env:**
```env
DB_HOST=aws-0-us-east-1.pooler.supabase.com
```

**Everything else stays the same!**

---

## Quick Test

After updating your `.env` file:

```bash
python manage.py check --database default
```

**Expected result:**
```
System check identified no issues (0 silenced).
```

**If you get an error:** See troubleshooting section in SUPABASE_CONNECTION_EXPLAINED.md

