"""
Quick script to help diagnose Supabase connection issues.
This will guide you through checking your Supabase project status.
"""

print("\n" + "="*70)
print("SUPABASE CONNECTION DIAGNOSIS")
print("="*70)

print("\n📋 Step 1: Check Your Supabase Project Status")
print("-" * 70)
print("1. Go to: https://app.supabase.com")
print("2. Log in to your account")
print("3. Find your project")
print("4. Check if it shows:")
print("   ✅ GREEN/RUNNING - Project is active")
print("   ⏸️  PAUSED/STOPPED - Project needs to be resumed")
print("\n💡 Free tier projects pause after 7 days of inactivity!")

print("\n📋 Step 2: Get the Correct Database Hostname")
print("-" * 70)
print("1. In Supabase Dashboard, go to: Settings → Database")
print("2. Scroll down to 'Connection string' or 'Connection info'")
print("3. Look for a string like:")
print("   postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres")
print("4. The part after '@' and before ':5432' is your DB_HOST")
print("   Example: db.xxxxx.supabase.co")

print("\n📋 Step 3: Alternative - Use Connection Pooler")
print("-" * 70)
print("Sometimes connection pooler works better:")
print("1. Go to: Settings → Database → Connection Pooling")
print("2. Look for 'Connection string' under Session or Transaction mode")
print("3. Use that hostname instead")

print("\n📋 Step 4: Update Your .env File")
print("-" * 70)
print("1. Open your .env file")
print("2. Update DB_HOST with the correct value from Step 2 or 3")
print("3. Save the file")

print("\n📋 Step 5: Test the Connection")
print("-" * 70)
print("Run this command:")
print("  .\\venv\\Scripts\\python.exe manage.py check --database default")
print("\nIf successful, you'll see:")
print("  System check identified no issues (0 silenced).")

print("\n" + "="*70)
print("Common Issues:")
print("="*70)
print("❌ Project is paused → Resume it in Supabase dashboard")
print("❌ Wrong hostname → Get correct one from Settings → Database")
print("❌ Network issues → Check your internet connection")
print("="*70 + "\n")

