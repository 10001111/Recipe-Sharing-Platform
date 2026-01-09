"""
Database Connection Test Script

This script tests the database connection to verify that Django can connect
to the PostgreSQL database (Supabase) successfully.

Usage:
    python scripts/test_database_connection.py
    OR
    python manage.py shell < scripts/test_database_connection.py
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from django.conf import settings


def test_database_connection():
    """Test the database connection."""
    print("\n" + "="*70)
    print("DATABASE CONNECTION TEST")
    print("="*70)
    
    try:
        # Get database configuration
        db_config = settings.DATABASES['default']
        print(f"\n📊 Database Configuration:")
        print(f"   Engine: {db_config.get('ENGINE', 'N/A')}")
        print(f"   Name: {db_config.get('NAME', 'N/A')}")
        print(f"   User: {db_config.get('USER', 'N/A')}")
        print(f"   Host: {db_config.get('HOST', 'N/A')}")
        print(f"   Port: {db_config.get('PORT', 'N/A')}")
        
        # Test connection
        print(f"\n🔌 Testing connection...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"   ✅ Connection successful!")
            print(f"   PostgreSQL version: {version[0]}")
        
        # Test database name
        print(f"\n📋 Database Information:")
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()
            print(f"   Current database: {db_name[0]}")
        
        # Test if we can query
        print(f"\n✅ Database connection test PASSED!")
        print("="*70 + "\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Database connection test FAILED!")
        print(f"   Error: {str(e)}")
        print("\n💡 Troubleshooting:")
        print("   1. Check your .env file has correct database credentials")
        print("   2. Verify your Supabase project is running")
        print("   3. Check your network connection")
        print("   4. Ensure database password is correct")
        print("="*70 + "\n")
        return False


if __name__ == '__main__':
    success = test_database_connection()
    sys.exit(0 if success else 1)
