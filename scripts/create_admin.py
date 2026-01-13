"""
Script to create a superuser for Django admin

Usage:
    python scripts/create_admin.py
"""

import os
import sys
import django

# Setup Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()


def create_admin_user():
    """Create or update admin user"""
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin123'
    
    try:
        user = User.objects.get(username=username)
        print(f"User '{username}' already exists.")
        print("Updating to superuser...")
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.set_password(password)
        user.save()
        print(f"[OK] Updated user '{username}' to superuser")
    except User.DoesNotExist:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"[OK] Created superuser: {username}")
    
    print(f"\nAdmin credentials:")
    print(f"  Username: {username}")
    print(f"  Password: {password}")
    print(f"\nAccess admin at: http://127.0.0.1:8000/admin/")


if __name__ == '__main__':
    create_admin_user()

