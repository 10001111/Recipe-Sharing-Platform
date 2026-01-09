"""
Test script for user workflow: registration, login, logout, delete account

This script helps verify that user authentication and account management work correctly.
"""

import os
import sys
import django

# Setup Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group
from apps.users.models import UserProfile

User = get_user_model()


def create_test_user(username='testuser', email='test@example.com', password='testpass123'):
    """Create a test user"""
    print(f"\n{'='*70}")
    print("Creating Test User")
    print(f"{'='*70}")
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists. Deleting...")
        User.objects.filter(username=username).delete()
    
    # Create user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    
    print(f"[OK] Created user: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  ID: {user.id}")
    print(f"  Is Active: {user.is_active}")
    print(f"  Date Joined: {user.date_joined}")
    
    # Check if profile was created
    if hasattr(user, 'profile'):
        print(f"  Profile: [OK] Created")
        print(f"    Bio: {user.profile.bio or '(empty)'}")
        print(f"    Dietary Preferences: {user.profile.dietary_preferences}")
    else:
        print(f"  Profile: [ERROR] Not found")
    
    # Check roles
    user_groups = list(user.groups.values_list('name', flat=True))
    if user_groups:
        print(f"  Roles: {', '.join(user_groups)}")
    else:
        print(f"  Roles: (none - default 'user' role should be assigned)")
    
    return user


def test_authentication(username='testuser', password='testpass123'):
    """Test user authentication"""
    print(f"\n{'='*70}")
    print("Testing Authentication")
    print(f"{'='*70}")
    
    user = authenticate(username=username, password=password)
    if user:
        print(f"[OK] Authentication successful for '{username}'")
        print(f"  User ID: {user.id}")
        print(f"  Is Active: {user.is_active}")
        return True
    else:
        print(f"[ERROR] Authentication failed for '{username}'")
        return False


def test_user_info(username='testuser'):
    """Display user information"""
    print(f"\n{'='*70}")
    print("User Information")
    print(f"{'='*70}")
    
    try:
        user = User.objects.get(username=username)
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"ID: {user.id}")
        print(f"Is Active: {user.is_active}")
        print(f"Is Staff: {user.is_staff}")
        print(f"Is Superuser: {user.is_superuser}")
        print(f"Date Joined: {user.date_joined}")
        
        # Profile info
        if hasattr(user, 'profile'):
            profile = user.profile
            print(f"\nProfile:")
            print(f"  Bio: {profile.bio or '(empty)'}")
            print(f"  Dietary Preferences: {profile.dietary_preferences}")
            print(f"  Created At: {profile.created_at}")
        
        # Roles
        groups = list(user.groups.values_list('name', flat=True))
        if groups:
            print(f"\nRoles: {', '.join(groups)}")
        else:
            print(f"\nRoles: (none)")
        
        return user
    except User.DoesNotExist:
        print(f"[ERROR] User '{username}' not found")
        return None


def delete_test_user(username='testuser'):
    """Delete test user"""
    print(f"\n{'='*70}")
    print("Deleting Test User")
    print(f"{'='*70}")
    
    try:
        user = User.objects.get(username=username)
        user_id = user.id
        user.delete()
        print(f"[OK] User '{username}' (ID: {user_id}) deleted successfully")
        
        # Verify deletion
        if not User.objects.filter(username=username).exists():
            print(f"[OK] Deletion verified - user no longer exists")
        else:
            print(f"[WARNING] User still exists after deletion")
        
        return True
    except User.DoesNotExist:
        print(f"[ERROR] User '{username}' not found")
        return False


def main():
    """Main test workflow"""
    print("\n" + "="*70)
    print("USER WORKFLOW TEST")
    print("="*70)
    print("\nThis script will:")
    print("1. Create a test user")
    print("2. Test authentication")
    print("3. Display user information")
    print("4. Optionally delete the user")
    print("\n" + "="*70)
    
    username = 'testuser'
    email = 'test@example.com'
    password = 'testpass123'
    
    # Step 1: Create user
    user = create_test_user(username, email, password)
    
    # Step 2: Test authentication
    auth_success = test_authentication(username, password)
    
    # Step 3: Display user info
    test_user_info(username)
    
    # Step 4: Ask about deletion
    print(f"\n{'='*70}")
    print("Next Steps")
    print(f"{'='*70}")
    print(f"\nTest user created: {username}")
    print(f"Password: {password}")
    print(f"\nTo test in the browser:")
    print(f"1. Go to http://127.0.0.1:8000/users/login/")
    print(f"2. Login with username: {username}, password: {password}")
    print(f"3. Test logout functionality")
    print(f"4. Test delete account functionality")
    print(f"\nTo delete this test user via script, run:")
    print(f"  python scripts/test_user_workflow.py --delete")
    
    # Check for delete flag
    if '--delete' in sys.argv:
        delete_test_user(username)


if __name__ == '__main__':
    main()

