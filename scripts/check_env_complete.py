"""
Check if all required environment variables are set

This script checks your .env file and tells you what's missing.
"""

import os
import sys
from decouple import config

def check_env_variables():
    """Check all environment variables."""
    print("\n" + "="*70)
    print("ENVIRONMENT VARIABLES CHECK")
    print("="*70)
    
    # Required variables
    required = {
        'SECRET_KEY': 'Django secret key (generate with: python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")',
        'DEBUG': 'Debug mode (True for development, False for production)',
        'ALLOWED_HOSTS': 'Allowed hostnames (comma-separated, e.g., localhost,127.0.0.1)',
        'DB_NAME': 'Database name (usually "postgres" for Supabase)',
        'DB_USER': 'Database username (usually "postgres" for Supabase)',
        'DB_PASSWORD': 'Database password (your Supabase database password)',
        'DB_HOST': 'Database hostname (from Supabase Settings → Database)',
        'DB_PORT': 'Database port (usually "5432")',
    }
    
    # Optional but recommended
    optional = {
        'SUPABASE_URL': 'Supabase project URL (for future features)',
        'SUPABASE_ANON_KEY': 'Supabase anonymous API key (for future features)',
        'SUPABASE_SERVICE_ROLE_KEY': 'Supabase service role key (for admin operations)',
        'EMAIL_BACKEND': 'Email backend (django.core.mail.backends.console.EmailBackend for dev)',
    }
    
    print("\nREQUIRED VARIABLES:")
    print("-" * 70)
    missing_required = []
    for var, description in required.items():
        try:
            value = config(var, default=None)
            if value:
                # Hide sensitive values
                if 'PASSWORD' in var or 'SECRET' in var or 'KEY' in var:
                    display_value = f"{value[:10]}..." if len(value) > 10 else "***"
                else:
                    display_value = value
                print(f"  [OK] {var:25} = {display_value}")
            else:
                print(f"  [MISSING] {var:25} = MISSING")
                missing_required.append((var, description))
        except Exception as e:
            print(f"  ❌ {var:25} = ERROR: {str(e)}")
            missing_required.append((var, description))
    
    print("\nOPTIONAL VARIABLES:")
    print("-" * 70)
    missing_optional = []
    for var, description in optional.items():
        try:
            value = config(var, default=None)
            if value:
                if 'KEY' in var:
                    display_value = f"{value[:20]}..." if len(value) > 20 else "***"
                else:
                    display_value = value
                print(f"  [OK] {var:25} = {display_value}")
            else:
                print(f"  [OPTIONAL] {var:25} = NOT SET (optional)")
                missing_optional.append((var, description))
        except Exception:
            print(f"  ⚠️  {var:25} = NOT SET (optional)")
            missing_optional.append((var, description))
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    if missing_required:
        print(f"\n[MISSING] MISSING REQUIRED VARIABLES: {len(missing_required)}")
        for var, desc in missing_required:
            print(f"   - {var}: {desc}")
    else:
        print("\n[OK] All required variables are set!")
    
    if missing_optional:
        print(f"\n[OPTIONAL] OPTIONAL VARIABLES NOT SET: {len(missing_optional)}")
        for var, desc in missing_optional:
            print(f"   - {var}: {desc}")
    else:
        print("\n[OK] All optional variables are set!")
    
    # Database username check
    print("\n" + "="*70)
    print("DATABASE USERNAME VERIFICATION")
    print("="*70)
    db_user = config('DB_USER', default=None)
    if db_user:
        if db_user == 'postgres':
            print(f"\n[OK] DB_USER is correct: '{db_user}'")
            print("   This is the standard PostgreSQL username for Supabase.")
        else:
            print(f"\n[WARNING] DB_USER is '{db_user}'")
            print("   Expected: 'postgres'")
            print("   Supabase uses 'postgres' as the default database username.")
            print("   If you're sure this is correct, you can keep it.")
    else:
        print("\n[MISSING] DB_USER is not set!")
    
    # Database name check
    db_name = config('DB_NAME', default=None)
    if db_name:
        if db_name == 'postgres':
            print(f"\n[OK] DB_NAME is correct: '{db_name}'")
            print("   This is the standard database name for Supabase.")
        else:
            print(f"\n[WARNING] DB_NAME is '{db_name}'")
            print("   Expected: 'postgres'")
            print("   Supabase uses 'postgres' as the default database name.")
    
    print("\n" + "="*70 + "\n")
    
    return len(missing_required) == 0

if __name__ == '__main__':
    success = check_env_variables()
    sys.exit(0 if success else 1)

