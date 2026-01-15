"""
Script to clean up users and their associated data

This script will:
1. Show data associated with each user
2. Delete all users except pa381187@gmail.com
3. Delete all data associated with deleted users
4. Make pa381187@gmail.com a superuser
"""

import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.recipes.models import Recipe, Comment, Rating, Favorite
from apps.users.models import UserProfile

User = get_user_model()

def main():
    print("=" * 70)
    print("USER CLEANUP SCRIPT")
    print("=" * 70)
    
    # Find the user to keep
    try:
        user_to_keep = User.objects.get(email='pa381187@gmail.com')
        print(f"\n[OK] Found user to keep: {user_to_keep.username} ({user_to_keep.email})")
    except User.DoesNotExist:
        print("\n[ERROR] User pa381187@gmail.com not found!")
        return
    
    # Show data associated with each user
    print("\n" + "=" * 70)
    print("DATA ASSOCIATED WITH USERS:")
    print("=" * 70)
    
    users_to_delete = []
    for user in User.objects.all():
        recipes_count = Recipe.objects.filter(author=user).count()
        comments_count = Comment.objects.filter(user=user).count()
        ratings_count = Rating.objects.filter(user=user).count()
        favorites_count = Favorite.objects.filter(user=user).count()
        
        print(f"\n{user.username} ({user.email}):")
        print(f"  - Recipes: {recipes_count}")
        print(f"  - Comments: {comments_count}")
        print(f"  - Ratings: {ratings_count}")
        print(f"  - Favorites: {favorites_count}")
        print(f"  - Superuser: {user.is_superuser}")
        print(f"  - Staff: {user.is_staff}")
        
        if user.email != 'pa381187@gmail.com':
            users_to_delete.append(user)
    
    if not users_to_delete:
        print("\n[OK] No users to delete!")
        return
    
    # Confirm deletion
    print("\n" + "=" * 70)
    print("USERS TO DELETE:")
    print("=" * 70)
    for user in users_to_delete:
        print(f"  - {user.username} ({user.email})")
    
    print("\n" + "=" * 70)
    print("DELETING USERS AND THEIR DATA...")
    print("=" * 70)
    
    # Delete users (CASCADE will handle related data)
    deleted_count = 0
    for user in users_to_delete:
        username = user.username
        email = user.email
        
        # Count data before deletion
        recipes_count = Recipe.objects.filter(author=user).count()
        comments_count = Comment.objects.filter(user=user).count()
        ratings_count = Rating.objects.filter(user=user).count()
        favorites_count = Favorite.objects.filter(user=user).count()
        
        # Delete user (CASCADE will delete related data)
        user.delete()
        deleted_count += 1
        
        print(f"\n[OK] Deleted {username} ({email}):")
        print(f"  - Removed {recipes_count} recipes")
        print(f"  - Removed {comments_count} comments")
        print(f"  - Removed {ratings_count} ratings")
        print(f"  - Removed {favorites_count} favorites")
    
    print(f"\n[OK] Deleted {deleted_count} user(s)")
    
    # Make pa381187@gmail.com a superuser
    print("\n" + "=" * 70)
    print("UPDATING pa381187@gmail.com TO SUPERUSER...")
    print("=" * 70)
    
    user_to_keep.is_superuser = True
    user_to_keep.is_staff = True
    user_to_keep.save()
    
    print(f"\n[OK] Updated {user_to_keep.username} ({user_to_keep.email}):")
    print(f"  - Superuser: {user_to_keep.is_superuser}")
    print(f"  - Staff: {user_to_keep.is_staff}")
    
    # Final summary
    print("\n" + "=" * 70)
    print("FINAL STATUS:")
    print("=" * 70)
    remaining_users = User.objects.all()
    print(f"\nRemaining users: {remaining_users.count()}")
    for user in remaining_users:
        print(f"  - {user.username} ({user.email}) - Superuser: {user.is_superuser}")
    
    print("\n[OK] Cleanup complete!")

if __name__ == '__main__':
    main()

