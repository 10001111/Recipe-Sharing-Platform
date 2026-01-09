"""
Environment Variables Verification Script

This script verifies that all environment variables are correctly configured
and validates the Supabase API keys.

Usage:
    python scripts/verify_env_config.py
"""

import os
import sys
import django
import base64
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from decouple import config
from django.db import connection


def decode_jwt_payload(token):
    """Decode JWT token payload."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        payload = parts[1]
        # Add padding if needed
        padding = 4 - len(payload) % 4
        if padding:
            payload += '=' * padding
        
        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    except Exception as e:
        return None


def verify_supabase_keys():
    """Verify Supabase API keys."""
    print("\n" + "="*70)
    print("SUPABASE API KEYS VERIFICATION")
    print("="*70)
    
    # Get keys
    anon_key = config('SUPABASE_ANON_KEY', default=None)
    service_role_key = config('SUPABASE_SERVICE_ROLE_KEY', default=None)
    supabase_url = config('SUPABASE_URL', default=None)
    project_id = supabase_url.split('.')[0].replace('https://', '') if supabase_url else None
    
    print(f"\n📋 Configuration:")
    print(f"   Project ID: {project_id}")
    print(f"   Supabase URL: {supabase_url}")
    
    # Verify ANON key
    print(f"\n🔑 ANON KEY Verification:")
    if anon_key:
        anon_payload = decode_jwt_payload(anon_key)
        if anon_payload:
            print(f"   ✅ Valid JWT token")
            print(f"   Role: {anon_payload.get('role')}")
            print(f"   Project ID (ref): {anon_payload.get('ref')}")
            print(f"   Matches project: {'✅ YES' if anon_payload.get('ref') == project_id else '❌ NO'}")
            if anon_payload.get('role') != 'anon':
                print(f"   ⚠️  WARNING: Expected role 'anon', got '{anon_payload.get('role')}'")
        else:
            print(f"   ❌ Invalid JWT token format")
    else:
        print(f"   ⚠️  ANON_KEY not found")
    
    # Verify SERVICE_ROLE key
    print(f"\n🔐 SERVICE_ROLE KEY Verification:")
    if service_role_key:
        # Check if it's a JWT token (starts with eyJ)
        if service_role_key.startswith('eyJ'):
            service_payload = decode_jwt_payload(service_role_key)
            if service_payload:
                print(f"   ✅ Valid JWT token")
                print(f"   Role: {service_payload.get('role')}")
                print(f"   Project ID (ref): {service_payload.get('ref')}")
                print(f"   Matches project: {'✅ YES' if service_payload.get('ref') == project_id else '❌ NO'}")
                if service_payload.get('role') != 'service_role':
                    print(f"   ⚠️  WARNING: Expected role 'service_role', got '{service_payload.get('role')}'")
                else:
                    print(f"   ✅ Correct role: service_role")
            else:
                print(f"   ❌ Invalid JWT token format")
        else:
            print(f"   ⚠️  WARNING: Service role key doesn't look like a JWT token")
            print(f"   Expected format: eyJ... (JWT token)")
            print(f"   Current format: {service_role_key[:30]}...")
            print(f"   This might be an old format. Get the service_role key from Supabase Settings → API")
    else:
        print(f"   ⚠️  SERVICE_ROLE_KEY not found")
    
    return True


def verify_database_config():
    """Verify database configuration."""
    print("\n" + "="*70)
    print("DATABASE CONFIGURATION VERIFICATION")
    print("="*70)
    
    db_name = config('DB_NAME', default=None)
    db_user = config('DB_USER', default=None)
    db_password = config('DB_PASSWORD', default=None)
    db_host = config('DB_HOST', default=None)
    db_port = config('DB_PORT', default='5432')
    
    print(f"\n📊 Database Settings:")
    print(f"   Name: {db_name}")
    print(f"   User: {db_user}")
    print(f"   Host: {db_host}")
    print(f"   Port: {db_port}")
    print(f"   Password: {'✅ Set' if db_password else '❌ Missing'}")
    
    # Extract project ID from host
    if db_host:
        host_project_id = db_host.replace('db.', '').replace('.supabase.co', '')
        print(f"   Project ID from host: {host_project_id}")
    
    # Test connection
    print(f"\n🔌 Testing database connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"   ✅ Connection successful!")
            print(f"   PostgreSQL version: {version[0][:50]}...")
            
            cursor.execute("SELECT current_database();")
            db_name_check = cursor.fetchone()
            print(f"   Current database: {db_name_check[0]}")
    except Exception as e:
        print(f"   ❌ Connection failed: {str(e)}")
        return False
    
    return True


def verify_django_settings():
    """Verify Django settings."""
    print("\n" + "="*70)
    print("DJANGO SETTINGS VERIFICATION")
    print("="*70)
    
    secret_key = config('SECRET_KEY', default=None)
    debug = config('DEBUG', default=False, cast=bool)
    allowed_hosts = config('ALLOWED_HOSTS', default='localhost,127.0.0.1')
    
    print(f"\n⚙️  Django Settings:")
    print(f"   SECRET_KEY: {'✅ Set' if secret_key else '❌ Missing'}")
    print(f"   DEBUG: {debug}")
    print(f"   ALLOWED_HOSTS: {allowed_hosts}")
    
    if not secret_key:
        print(f"   ⚠️  WARNING: SECRET_KEY is required!")
        return False
    
    return True


def main():
    """Main verification function."""
    print("\n" + "="*70)
    print("ENVIRONMENT VARIABLES VERIFICATION")
    print("="*70)
    
    all_ok = True
    
    # Verify Django settings
    if not verify_django_settings():
        all_ok = False
    
    # Verify database configuration
    if not verify_database_config():
        all_ok = False
    
    # Verify Supabase keys
    verify_supabase_keys()
    
    # Summary
    print("\n" + "="*70)
    if all_ok:
        print("✅ VERIFICATION COMPLETE - All checks passed!")
    else:
        print("⚠️  VERIFICATION COMPLETE - Some issues found (see above)")
    print("="*70 + "\n")
    
    return all_ok


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

