"""
Comprehensive Supabase Connection Test

This script tests all aspects of your Supabase connection:
1. Environment variables configuration
2. Database connection
3. API keys validation
4. Project consistency

Usage:
    python scripts/comprehensive_connection_test.py
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from decouple import config
from django.db import connection
from django.conf import settings
import base64
import json


def decode_jwt_payload(token):
    """Decode JWT token payload."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        payload = parts[1]
        padding = 4 - len(payload) % 4
        if padding:
            payload += '=' * padding
        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    except Exception:
        return None


def test_environment_variables():
    """Test 1: Check environment variables."""
    print("\n" + "="*70)
    print("TEST 1: Environment Variables Configuration")
    print("="*70)
    
    results = {
        'SECRET_KEY': False,
        'DB_NAME': False,
        'DB_USER': False,
        'DB_PASSWORD': False,
        'DB_HOST': False,
        'DB_PORT': False,
        'SUPABASE_URL': False,
        'SUPABASE_ANON_KEY': False,
        'SUPABASE_SERVICE_ROLE_KEY': False,
    }
    
    try:
        secret_key = config('SECRET_KEY')
        results['SECRET_KEY'] = bool(secret_key)
        print(f"  SECRET_KEY: {'✅ Set' if results['SECRET_KEY'] else '❌ Missing'}")
    except Exception:
        print(f"  SECRET_KEY: ❌ Missing")
    
    try:
        db_name = config('DB_NAME')
        results['DB_NAME'] = bool(db_name)
        print(f"  DB_NAME: {'✅ ' + db_name if results['DB_NAME'] else '❌ Missing'}")
    except Exception:
        print(f"  DB_NAME: ❌ Missing")
    
    try:
        db_user = config('DB_USER')
        results['DB_USER'] = bool(db_user)
        print(f"  DB_USER: {'✅ ' + db_user if results['DB_USER'] else '❌ Missing'}")
    except Exception:
        print(f"  DB_USER: ❌ Missing")
    
    try:
        db_password = config('DB_PASSWORD')
        results['DB_PASSWORD'] = bool(db_password)
        print(f"  DB_PASSWORD: {'✅ Set (hidden)' if results['DB_PASSWORD'] else '❌ Missing'}")
    except Exception:
        print(f"  DB_PASSWORD: ❌ Missing")
    
    try:
        db_host = config('DB_HOST')
        results['DB_HOST'] = bool(db_host)
        print(f"  DB_HOST: {'✅ ' + db_host if results['DB_HOST'] else '❌ Missing'}")
    except Exception:
        print(f"  DB_HOST: ❌ Missing")
    
    try:
        db_port = config('DB_PORT', default='5432')
        results['DB_PORT'] = bool(db_port)
        print(f"  DB_PORT: {'✅ ' + str(db_port) if results['DB_PORT'] else '❌ Missing'}")
    except Exception:
        print(f"  DB_PORT: ❌ Missing")
    
    try:
        supabase_url = config('SUPABASE_URL')
        results['SUPABASE_URL'] = bool(supabase_url)
        print(f"  SUPABASE_URL: {'✅ ' + supabase_url if results['SUPABASE_URL'] else '❌ Missing'}")
    except Exception:
        print(f"  SUPABASE_URL: ❌ Missing")
    
    try:
        anon_key = config('SUPABASE_ANON_KEY')
        results['SUPABASE_ANON_KEY'] = bool(anon_key)
        print(f"  SUPABASE_ANON_KEY: {'✅ Set' if results['SUPABASE_ANON_KEY'] else '❌ Missing'}")
    except Exception:
        print(f"  SUPABASE_ANON_KEY: ❌ Missing")
    
    try:
        service_key = config('SUPABASE_SERVICE_ROLE_KEY')
        results['SUPABASE_SERVICE_ROLE_KEY'] = bool(service_key)
        print(f"  SUPABASE_SERVICE_ROLE_KEY: {'✅ Set' if results['SUPABASE_SERVICE_ROLE_KEY'] else '❌ Missing'}")
    except Exception:
        print(f"  SUPABASE_SERVICE_ROLE_KEY: ❌ Missing")
    
    all_set = all(results.values())
    print(f"\n  Status: {'✅ All variables set' if all_set else '❌ Some variables missing'}")
    return all_set, results


def test_api_keys():
    """Test 2: Validate API keys."""
    print("\n" + "="*70)
    print("TEST 2: Supabase API Keys Validation")
    print("="*70)
    
    try:
        supabase_url = config('SUPABASE_URL')
        anon_key = config('SUPABASE_ANON_KEY')
        service_key = config('SUPABASE_SERVICE_ROLE_KEY')
        
        # Extract project ID from URL
        project_id = supabase_url.split('.')[0].replace('https://', '') if supabase_url else None
        
        print(f"  Project ID: {project_id}")
        
        # Validate ANON key
        if anon_key:
            anon_payload = decode_jwt_payload(anon_key)
            if anon_payload:
                anon_role = anon_payload.get('role')
                anon_ref = anon_payload.get('ref')
                print(f"  ANON_KEY:")
                print(f"    Role: {anon_role} {'✅' if anon_role == 'anon' else '❌'}")
                print(f"    Project ID: {anon_ref} {'✅' if anon_ref == project_id else '❌'}")
            else:
                print(f"  ANON_KEY: ❌ Invalid JWT format")
        else:
            print(f"  ANON_KEY: ❌ Not set")
        
        # Validate SERVICE_ROLE key
        if service_key:
            if service_key.startswith('eyJ'):
                service_payload = decode_jwt_payload(service_key)
                if service_payload:
                    service_role = service_payload.get('role')
                    service_ref = service_payload.get('ref')
                    print(f"  SERVICE_ROLE_KEY:")
                    print(f"    Role: {service_role} {'✅' if service_role == 'service_role' else '❌'}")
                    print(f"    Project ID: {service_ref} {'✅' if service_ref == project_id else '❌'}")
                else:
                    print(f"  SERVICE_ROLE_KEY: ❌ Invalid JWT format")
            else:
                print(f"  SERVICE_ROLE_KEY: ⚠️  Not a JWT token (might be old format)")
        else:
            print(f"  SERVICE_ROLE_KEY: ❌ Not set")
        
        return True
    except Exception as e:
        print(f"  ❌ Error validating keys: {str(e)}")
        return False


def test_database_connection():
    """Test 3: Test actual database connection."""
    print("\n" + "="*70)
    print("TEST 3: Database Connection Test")
    print("="*70)
    
    try:
        db_config = settings.DATABASES['default']
        print(f"  Database Engine: {db_config.get('ENGINE')}")
        print(f"  Database Name: {db_config.get('NAME')}")
        print(f"  Database User: {db_config.get('USER')}")
        print(f"  Database Host: {db_config.get('HOST')}")
        print(f"  Database Port: {db_config.get('PORT')}")
        
        print(f"\n  Attempting connection...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"  ✅ Connection successful!")
            print(f"  PostgreSQL Version: {version[0][:80]}...")
            
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()
            print(f"  Current Database: {db_name[0]}")
            
            cursor.execute("SELECT current_user;")
            db_user = cursor.fetchone()
            print(f"  Current User: {db_user[0]}")
            
            return True
    except Exception as e:
        error_msg = str(e)
        print(f"  ❌ Connection failed!")
        print(f"  Error: {error_msg}")
        
        if "could not translate host name" in error_msg:
            print(f"\n  💡 This means:")
            print(f"     - The hostname cannot be found")
            print(f"     - Your Supabase project might be PAUSED")
            print(f"     - Or the hostname is incorrect")
            print(f"\n  🔧 To fix:")
            print(f"     1. Go to https://app.supabase.com")
            print(f"     2. Check if your project is paused")
            print(f"     3. If paused, click 'Resume'")
            print(f"     4. Get correct hostname from Settings → Database")
        
        return False


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("COMPREHENSIVE SUPABASE CONNECTION TEST")
    print("="*70)
    
    results = {}
    
    # Test 1: Environment Variables
    env_ok, env_results = test_environment_variables()
    results['environment'] = env_ok
    
    # Test 2: API Keys
    keys_ok = test_api_keys()
    results['api_keys'] = keys_ok
    
    # Test 3: Database Connection
    db_ok = test_database_connection()
    results['database'] = db_ok
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"  Environment Variables: {'✅ PASS' if results['environment'] else '❌ FAIL'}")
    print(f"  API Keys Validation: {'✅ PASS' if results['api_keys'] else '❌ FAIL'}")
    print(f"  Database Connection: {'✅ PASS' if results['database'] else '❌ FAIL'}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ ALL TESTS PASSED - Supabase is properly connected!")
    else:
        print("⚠️  SOME TESTS FAILED - See details above")
        if not results['database']:
            print("\n🔧 ACTION REQUIRED:")
            print("   Fix the database connection issue to proceed")
    print("="*70 + "\n")
    
    return all_passed


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

