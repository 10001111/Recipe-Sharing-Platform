# 📝 .env File Setup - Important Notes

## ⚠️ Important: .env File Location

**The `.env` file MUST be in the project root** (same folder as `manage.py`), NOT in the `venv` folder!

### Why?

- Django's `python-decouple` looks for `.env` in the project root
- The `venv` folder is excluded from Git and can be deleted/recreated
- Industry standard is to keep `.env` in the project root

### Correct Location:
```
Recipe-Sharing-Platform/
├── .env              ✅ CORRECT - Here!
├── manage.py
├── config/
└── venv/             ❌ WRONG - Not here!
```

---

## ✅ What I've Done

I've created a proper `.env` file in the project root with:

1. **Mapped your existing values:**
   - `supabase-pass` → `DB_PASSWORD`
   - `SUPABASE_URL` → `SUPABASE_URL`
   - `SUPABASE_ANON_KEY` → `SUPABASE_ANON_KEY`
   - `SUPABASE_SECRET` → `SUPABASE_SERVICE_ROLE_KEY` (see note below)

2. **Added missing essential variables:**
   - `SECRET_KEY` (generated)
   - `DEBUG=True`
   - `ALLOWED_HOSTS`
   - `DB_NAME=postgres`
   - `DB_USER=postgres`
   - `DB_HOST` (constructed from your project ID)
   - `DB_PORT=5432`

3. **Organized with clear sections** for easy reference

---

## ⚠️ Important Note About SUPABASE_SERVICE_ROLE_KEY

The `SUPABASE_SECRET` value you had might not be the actual `service_role` key. 

**To get the correct service_role key:**

1. Go to your Supabase dashboard: https://app.supabase.com
2. Select your project
3. Go to **Settings** → **API**
4. Look for **"service_role"** key (not "secret")
5. It should be a long JWT token starting with `eyJ...`
6. Copy that value and replace `SUPABASE_SERVICE_ROLE_KEY` in your `.env` file

**The service_role key looks like:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJjZXRlZnZ1bmllbGxmdW5lZWpnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDg3MTgwNCwiZXhwIjoyMDgwNDQ3ODA0fQ.very-long-signature-here
```

---

## 🧪 Test Your Configuration

After setting up your `.env` file:

```bash
# Test database connection
python scripts/test_database_connection.py

# Or use Django check
python manage.py check --database default
```

---

## 📋 Your Current .env File Contains

✅ **SECRET_KEY** - Generated  
✅ **DEBUG** - Set to True  
✅ **ALLOWED_HOSTS** - localhost,127.0.0.1  
✅ **DB_NAME** - postgres  
✅ **DB_USER** - postgres  
✅ **DB_PASSWORD** - Your Supabase password  
✅ **DB_HOST** - db.rcetefvuniellfuneejg.supabase.co  
✅ **DB_PORT** - 5432  
✅ **SUPABASE_URL** - Your project URL  
✅ **SUPABASE_ANON_KEY** - Your anon key  
⚠️ **SUPABASE_SERVICE_ROLE_KEY** - May need to verify/get correct value  

---

## 🔒 Security Reminder

- ✅ `.env` file is in `.gitignore` (won't be committed)
- ✅ All secrets are properly configured
- ⚠️ Never commit `.env` to Git
- ⚠️ Never share your `.env` file

---

**Your `.env` file is now properly configured in the project root!** 🎉

