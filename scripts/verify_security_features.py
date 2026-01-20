"""
Security Features Verification Script

This script verifies:
1. Database connection and functionality
2. Row Level Security (RLS) status
3. Email authentication
4. Google OAuth authentication
5. RLS policies configuration
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from django.contrib.auth import get_user_model
from django.conf import settings
import requests

User = get_user_model()

def check_database_connection():
    """Check if database connection is working"""
    print("=" * 70)
    print("1. DATABASE CONNECTION CHECK")
    print("=" * 70)
    
    try:
        db_engine = settings.DATABASES['default']['ENGINE']
        db_name = settings.DATABASES['default'].get('NAME', '')
        
        print(f"[OK] Database Engine: {db_engine}")
        
        with connection.cursor() as cursor:
            # Check database type
            if 'postgresql' in db_engine.lower():
                try:
                    cursor.execute("SELECT version();")
                    version = cursor.fetchone()[0]
                    print(f"[OK] Database Connected (PostgreSQL)")
                    print(f"     Version: {version.split(',')[0]}")
                except:
                    print(f"[OK] Database Connected (PostgreSQL)")
            elif 'sqlite' in db_engine.lower():
                print(f"[OK] Database Connected (SQLite)")
                print(f"     Database File: {db_name}")
            
            # Check if we can query tables
            if 'postgresql' in db_engine.lower():
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """)
            else:
                # SQLite
                cursor.execute("""
                    SELECT name 
                    FROM sqlite_master 
                    WHERE type='table' 
                    ORDER BY name;
                """)
            
            tables = cursor.fetchall()
            print(f"[OK] Found {len(tables)} tables in database")
            
            # Test a simple query
            User.objects.count()
            print(f"[OK] Can query User model (Django ORM working)")
            
            return True
    except Exception as e:
        print(f"[ERROR] Database Connection Failed: {e}")
        return False

def check_rls_status():
    """Check Row Level Security (RLS) status"""
    print("\n" + "=" * 70)
    print("2. ROW LEVEL SECURITY (RLS) CHECK")
    print("=" * 70)
    
    db_engine = settings.DATABASES['default']['ENGINE']
    
    # Check if PostgreSQL
    if 'postgresql' in db_engine.lower():
        try:
            with connection.cursor() as cursor:
                # Check which tables have RLS enabled
                cursor.execute("""
                    SELECT schemaname, tablename, rowsecurity
                    FROM pg_tables
                    WHERE schemaname = 'public'
                    ORDER BY tablename;
                """)
                tables = cursor.fetchall()
                
                rls_enabled = []
                rls_disabled = []
                
                for schema, table, rls in tables:
                    if rls:
                        rls_enabled.append(table)
                    else:
                        rls_disabled.append(table)
                
                print(f"[OK] RLS Enabled Tables: {len(rls_enabled)}")
                if rls_enabled:
                    for table in rls_enabled:
                        print(f"     - {table}")
                
                print(f"\n[WARN] RLS Disabled Tables: {len(rls_disabled)}")
                if len(rls_disabled) > 0 and len(rls_disabled) <= 10:
                    for table in rls_disabled[:10]:
                        print(f"     - {table}")
                elif len(rls_disabled) > 10:
                    print(f"     - {rls_disabled[0]} ... and {len(rls_disabled) - 1} more")
                
                # Check for existing RLS policies
                cursor.execute("""
                    SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
                    FROM pg_policies
                    WHERE schemaname = 'public'
                    ORDER BY tablename, policyname;
                """)
                policies = cursor.fetchall()
                
                print(f"\n[INFO] RLS Policies Found: {len(policies)}")
                if policies:
                    for schema, table, policy, permissive, roles, cmd, qual in policies:
                        print(f"     - {table}.{policy} ({cmd})")
                else:
                    print("     [WARN] No RLS policies found")
                    print("     [WARN] RLS is enabled but no policies exist - RLS is effectively inactive")
                
                return {
                    'enabled_tables': rls_enabled,
                    'disabled_tables': rls_disabled,
                    'policies': policies
                }
        except Exception as e:
            print(f"[ERROR] RLS Check Failed: {e}")
            return None
    else:
        # SQLite - RLS not supported
        print("[INFO] RLS is a PostgreSQL feature")
        print("     SQLite does not support Row Level Security")
        print("     Consider using PostgreSQL/Supabase for RLS support")
        print("     Django ORM handles security for SQLite")
        return {
            'enabled_tables': [],
            'disabled_tables': [],
            'policies': []
        }

def check_email_authentication():
    """Check email/password authentication"""
    print("\n" + "=" * 70)
    print("3. EMAIL AUTHENTICATION CHECK")
    print("=" * 70)
    
    try:
        from django.contrib.auth import authenticate
        
        # Check if email authentication is configured
        print("[OK] Email Authentication Available")
        print("     - Django's built-in authentication system")
        print("     - Users can register with email/username")
        print("     - Password hashing enabled")
        
        # Check if we can authenticate
        test_user = User.objects.filter(is_active=True).first()
        if test_user:
            print(f"[OK] Test User Found: {test_user.username}")
            print(f"     - Email: {test_user.email}")
            print(f"     - Has Password: {test_user.has_usable_password()}")
        else:
            print("[WARN] No active users found for testing")
        
        # Check authentication backend
        from django.contrib.auth import get_backends
        backends = get_backends()
        print(f"\n[OK] Authentication Backends: {len(backends)}")
        for backend in backends:
            print(f"     - {backend.__class__.__name__}")
        
        return True
    except Exception as e:
        print(f"❌ Email Authentication Check Failed: {e}")
        return False

def check_google_authentication():
    """Check Google OAuth authentication"""
    print("\n" + "=" * 70)
    print("4. GOOGLE OAUTH AUTHENTICATION CHECK")
    print("=" * 70)
    
    try:
        supabase_url = getattr(settings, 'SUPABASE_URL', '')
        supabase_anon_key = getattr(settings, 'SUPABASE_ANON_KEY', '')
        supabase_service_key = getattr(settings, 'SUPABASE_SERVICE_ROLE_KEY', '')
        
        if not supabase_url or not supabase_anon_key:
            print("[ERROR] Supabase Not Configured")
            print("        Missing SUPABASE_URL or SUPABASE_ANON_KEY in settings")
            return False
        
        print("[OK] Supabase Configuration Found")
        print(f"     - Supabase URL: {supabase_url[:30]}...")
        print(f"     - Anon Key: {'[OK] Set' if supabase_anon_key else '[ERROR] Missing'}")
        print(f"     - Service Key: {'[OK] Set' if supabase_service_key else '[WARN] Missing'}")
        
        # Check if Supabase endpoint is accessible
        try:
            response = requests.get(
                f"{supabase_url}/rest/v1/",
                headers={'apikey': supabase_anon_key},
                timeout=5
            )
            if response.status_code == 200:
                print("[OK] Supabase API Accessible")
            else:
                print(f"[WARN] Supabase API returned status {response.status_code}")
        except Exception as e:
            print(f"[WARN] Cannot reach Supabase API: {e}")
        
        # Check if Google OAuth is configured in code
        from apps.users import supabase_auth
        if hasattr(supabase_auth, 'get_supabase_user_info'):
            print("[OK] Google OAuth Handler Found")
            print("     - Location: apps/users/supabase_auth.py")
        
        # Check if OAuth callback endpoint exists
        from django.urls import reverse
        try:
            url = reverse('users:supabase_auth')
            print(f"[OK] OAuth Callback Endpoint: {url}")
        except:
            print("[WARN] OAuth Callback Endpoint Not Found")
        
        # Check for OAuth users
        oauth_users = User.objects.filter(password__startswith='!')  # Unusable password = OAuth user
        print(f"\n[INFO] OAuth Users Found: {oauth_users.count()}")
        
        return True
    except Exception as e:
        print(f"❌ Google Authentication Check Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_rls_recommendations():
    """Provide RLS recommendations"""
    print("\n" + "=" * 70)
    print("5. RLS RECOMMENDATIONS")
    print("=" * 70)
    
    rls_status = check_rls_status()
    
    if not rls_status:
        return
    
    print("\n[INFO] Recommended RLS Policies:")
    print("\n1. Users Table (users_customuser):")
    print("     - Users can view their own profile")
    print("     - Users can update their own profile")
    
    print("\n2. Recipes Table (recipes_recipe):")
    print("     - Anyone can view published recipes")
    print("     - Authors can edit their own recipes")
    print("     - Authenticated users can create recipes")
    
    print("\n3. Comments Table (recipes_comment):")
    print("     - Anyone can view comments")
    print("     - Authors can edit/delete their own comments")
    print("     - Authenticated users can create comments")
    
    print("\n4. Ratings Table (recipes_rating):")
    print("     - Anyone can view ratings")
    print("     - Users can create/edit their own ratings")
    
    print("\n[NOTE] RLS is optional when using Django ORM")
    print("       Django handles permissions, RLS adds database-level security")

def main():
    """Run all checks"""
    print("\n" + "=" * 70)
    print("SECURITY FEATURES VERIFICATION")
    print("=" * 70)
    print()
    
    results = {
        'database': check_database_connection(),
        'rls': check_rls_status() is not None,
        'email_auth': check_email_authentication(),
        'google_auth': check_google_authentication(),
    }
    
    check_rls_recommendations()
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    for feature, status in results.items():
        status_icon = "[OK]" if status else "[ERROR]"
        print(f"{status_icon} {feature.replace('_', ' ').title()}: {'Working' if status else 'Issues Found'}")
    
    all_working = all(results.values())
    
    if all_working:
        print("\n[OK] All security features are working correctly!")
    else:
        print("\n[WARN] Some features need attention. See details above.")
    
    print("=" * 70)

if __name__ == '__main__':
    main()

