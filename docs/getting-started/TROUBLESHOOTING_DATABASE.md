# 🔧 Troubleshooting Database Connection Issues

## Understanding the Error

### What Happened?

You got this error:
```
could not translate host name "db.rcetefvuniellfuneejg.supabase.co" to address: Name or service not known
```

### What Does This Mean? (In Simple Terms)

Think of it like trying to call someone on the phone, but the phone number doesn't exist or can't be found.

**What Django is trying to do:**
1. Django reads your `.env` file
2. It sees `DB_HOST=db.rcetefvuniellfuneejg.supabase.co`
3. It tries to "look up" this address on the internet (like looking up a phone number)
4. The internet says: "I don't know this address!" ❌

**Why this happens:**
- The hostname might be incorrect
- Your Supabase project might be paused
- Network/DNS issues
- The project might not be fully set up yet

---

## 🔍 Step-by-Step Diagnosis

### Step 1: Check Your Supabase Project Status

1. **Go to Supabase Dashboard:**
   - Visit: https://app.supabase.com
   - Log in to your account
   - Find your project: `rcetefvuniellfuneejg`

2. **Check Project Status:**
   - Is the project **green/running**? ✅
   - Or is it **paused/stopped**? ⏸️

   **If paused:** Click "Resume" or "Restore" to start it

### Step 2: Get the Correct Database Host

The hostname format might be wrong. Let's get the correct one:

1. **In Supabase Dashboard:**
   - Go to **Settings** (gear icon) → **Database**
   - Scroll down to **"Connection string"** or **"Connection info"**

2. **Look for the connection string:**
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```
   
   The part after `@` and before `:5432` is your **DB_HOST**

3. **Common formats:**
   - ✅ `db.xxxxx.supabase.co` (direct connection)
   - ✅ `aws-0-us-east-1.pooler.supabase.com` (connection pooler)
   - ✅ `xxxxx.supabase.co` (sometimes without `db.` prefix)

### Step 3: Verify Your Project is Active

**Check if your project is running:**
- Go to your Supabase project dashboard
- Look for status indicators
- If it says "Paused" or "Stopped", you need to resume it

**Free tier projects can pause after inactivity!**

---

## 🛠️ How to Fix It

### Fix Option 1: Get the Correct Hostname from Supabase

1. **Go to Supabase Dashboard**
2. **Settings → Database**
3. **Find "Connection string"** or "Connection pooling"
4. **Copy the hostname** from the connection string
5. **Update your `.env` file:**

```env
DB_HOST=the-correct-hostname-from-supabase
```

### Fix Option 2: Check Connection Pooling

Supabase offers two connection methods:

**Direct Connection:**
```
DB_HOST=db.xxxxx.supabase.co
```

**Connection Pooler (Recommended for production):**
```
DB_HOST=aws-0-us-east-1.pooler.supabase.com
```

**To find your pooler:**
- Settings → Database → Connection Pooling
- Look for "Connection string" under "Session mode" or "Transaction mode"

### Fix Option 3: Verify Project is Active

1. Go to Supabase dashboard
2. Check your project status
3. If paused, click "Resume" or "Restore"
4. Wait 1-2 minutes for it to start
5. Try connecting again

---

## 🧪 Testing the Fix

After updating your `.env` file:

```bash
# Test database connection
.\venv\Scripts\python.exe manage.py check --database default

# Or use the test script
.\venv\Scripts\python.exe scripts/test_database_connection.py
```

**Expected result:**
```
System check identified no issues (0 silenced).
```

---

## 📋 Common Issues & Solutions

### Issue 1: "Name or service not known"
**Cause:** Hostname is incorrect or project is paused  
**Solution:** Get correct hostname from Supabase Settings → Database

### Issue 2: "Connection refused"
**Cause:** Project is paused or not active  
**Solution:** Resume your Supabase project

### Issue 3: "Authentication failed"
**Cause:** Wrong password  
**Solution:** Check `DB_PASSWORD` in `.env` matches your Supabase password

### Issue 4: "Connection timeout"
**Cause:** Network/firewall issues  
**Solution:** Check internet connection, try again later

---

## 🎯 Quick Checklist

Before running `python manage.py migrate`, verify:

- [ ] Supabase project is **active/running** (not paused)
- [ ] `DB_HOST` in `.env` matches Supabase Settings → Database
- [ ] `DB_PASSWORD` is correct
- [ ] `DB_NAME` is `postgres` (usually)
- [ ] `DB_USER` is `postgres` (usually)
- [ ] `DB_PORT` is `5432`
- [ ] Internet connection is working

---

## 💡 Pro Tips

1. **Free Tier Projects:** Can pause after 7 days of inactivity
2. **Connection Pooler:** More reliable for production, use if available
3. **Test First:** Always test connection before running migrations
4. **Keep Project Active:** Use your Supabase project regularly to prevent pausing

---

## 🆘 Still Having Issues?

1. **Double-check Supabase Dashboard:**
   - Is project active?
   - What does Settings → Database show?

2. **Try Connection Pooler:**
   - Sometimes more reliable
   - Settings → Database → Connection Pooling

3. **Verify Network:**
   - Can you access https://app.supabase.com?
   - Is your internet working?

4. **Check Supabase Status:**
   - Visit: https://status.supabase.com
   - See if there are any outages

---

**Remember:** This is a common issue! Usually it's just a matter of getting the correct hostname or resuming your project. 🚀

