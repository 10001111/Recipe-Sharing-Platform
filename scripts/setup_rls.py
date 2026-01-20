"""
RLS (Row Level Security) Setup Script for Django

This script enables RLS on PostgreSQL tables and creates security policies.

IMPORTANT: This only works with PostgreSQL/Supabase, not SQLite!
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def check_database_type():
    """Check if using PostgreSQL"""
    db_engine = settings.DATABASES['default']['ENGINE']
    is_postgresql = 'postgresql' in db_engine.lower()
    
    print("=" * 70)
    print("RLS SETUP - DATABASE CHECK")
    print("=" * 70)
    print(f"Database Engine: {db_engine}")
    
    if not is_postgresql:
        print("\n[ERROR] RLS only works with PostgreSQL!")
        print("        Current database: SQLite")
        print("        Please switch to PostgreSQL/Supabase first.")
        print("\nSee docs/RLS_SETUP_GUIDE.md for instructions.")
        return False
    
    print("[OK] PostgreSQL detected - RLS can be enabled")
    return True


def enable_rls_on_table(table_name):
    """Enable RLS on a specific table"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""
                ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;
            """)
            print(f"[OK] Enabled RLS on {table_name}")
            return True
    except Exception as e:
        print(f"[WARN] Could not enable RLS on {table_name}: {e}")
        return False


def create_user_policies():
    """Create RLS policies for users table"""
    print("\n" + "=" * 70)
    print("CREATING USER POLICIES")
    print("=" * 70)
    
    policies = []
    
    # Policy 1: Users can view their own profile
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Users can view own profile"
        ON users_customuser
        FOR SELECT
        USING (id::text = current_setting('app.current_user_id', true));
    """)
    
    # Policy 2: Users can update their own profile
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Users can update own profile"
        ON users_customuser
        FOR UPDATE
        USING (id::text = current_setting('app.current_user_id', true));
    """)
    
    # Policy 3: Public can view user profiles (for recipe authors)
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Public can view user profiles"
        ON users_customuser
        FOR SELECT
        USING (is_active = true);
    """)
    
    return execute_policies(policies, "users_customuser")


def create_recipe_policies():
    """Create RLS policies for recipes table"""
    print("\n" + "=" * 70)
    print("CREATING RECIPE POLICIES")
    print("=" * 70)
    
    policies = []
    
    # Policy 1: Anyone can view published recipes
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Public can view published recipes"
        ON recipes_recipe
        FOR SELECT
        USING (is_published = true);
    """)
    
    # Policy 2: Authors can view their own recipes (even if unpublished)
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Authors can view own recipes"
        ON recipes_recipe
        FOR SELECT
        USING (author_id::text = current_setting('app.current_user_id', true));
    """)
    
    # Policy 3: Authenticated users can create recipes
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Authenticated users can create recipes"
        ON recipes_recipe
        FOR INSERT
        WITH CHECK (current_setting('app.current_user_id', true) IS NOT NULL);
    """)
    
    # Policy 4: Authors can update their own recipes
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Authors can update own recipes"
        ON recipes_recipe
        FOR UPDATE
        USING (author_id::text = current_setting('app.current_user_id', true));
    """)
    
    # Policy 5: Authors can delete their own recipes
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Authors can delete own recipes"
        ON recipes_recipe
        FOR DELETE
        USING (author_id::text = current_setting('app.current_user_id', true));
    """)
    
    return execute_policies(policies, "recipes_recipe")


def create_comment_policies():
    """Create RLS policies for comments table"""
    print("\n" + "=" * 70)
    print("CREATING COMMENT POLICIES")
    print("=" * 70)
    
    policies = []
    
    # Policy 1: Anyone can view comments
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Public can view comments"
        ON recipes_comment
        FOR SELECT
        USING (true);
    """)
    
    # Policy 2: Authenticated users can create comments
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Authenticated users can create comments"
        ON recipes_comment
        FOR INSERT
        WITH CHECK (user_id::text = current_setting('app.current_user_id', true));
    """)
    
    # Policy 3: Authors can update their own comments
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Authors can update own comments"
        ON recipes_comment
        FOR UPDATE
        USING (user_id::text = current_setting('app.current_user_id', true));
    """)
    
    # Policy 4: Authors can delete their own comments
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Authors can delete own comments"
        ON recipes_comment
        FOR DELETE
        USING (user_id::text = current_setting('app.current_user_id', true));
    """)
    
    return execute_policies(policies, "recipes_comment")


def create_rating_policies():
    """Create RLS policies for ratings table"""
    print("\n" + "=" * 70)
    print("CREATING RATING POLICIES")
    print("=" * 70)
    
    policies = []
    
    # Policy 1: Anyone can view ratings
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Public can view ratings"
        ON recipes_rating
        FOR SELECT
        USING (true);
    """)
    
    # Policy 2: Users can create their own ratings
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Users can create own ratings"
        ON recipes_rating
        FOR INSERT
        WITH CHECK (user_id::text = current_setting('app.current_user_id', true));
    """)
    
    # Policy 3: Users can update their own ratings
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Users can update own ratings"
        ON recipes_rating
        FOR UPDATE
        USING (user_id::text = current_setting('app.current_user_id', true));
    """)
    
    # Policy 4: Users can delete their own ratings
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Users can delete own ratings"
        ON recipes_rating
        FOR DELETE
        USING (user_id::text = current_setting('app.current_user_id', true));
    """)
    
    return execute_policies(policies, "recipes_rating")


def create_favorite_policies():
    """Create RLS policies for favorites table"""
    print("\n" + "=" * 70)
    print("CREATING FAVORITE POLICIES")
    print("=" * 70)
    
    policies = []
    
    # Policy 1: Users can view their own favorites
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Users can view own favorites"
        ON recipes_favorite
        FOR SELECT
        USING (user_id::text = current_setting('app.current_user_id', true));
    """)
    
    # Policy 2: Users can create their own favorites
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Users can create own favorites"
        ON recipes_favorite
        FOR INSERT
        WITH CHECK (user_id::text = current_setting('app.current_user_id', true));
    """)
    
    # Policy 3: Users can delete their own favorites
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Users can delete own favorites"
        ON recipes_favorite
        FOR DELETE
        USING (user_id::text = current_setting('app.current_user_id', true));
    """)
    
    return execute_policies(policies, "recipes_favorite")


def create_mealplan_policies():
    """Create RLS policies for meal plans table"""
    print("\n" + "=" * 70)
    print("CREATING MEAL PLAN POLICIES")
    print("=" * 70)
    
    policies = []
    
    # Policy 1: Users can view their own meal plans
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Users can view own meal plans"
        ON recipes_mealplan
        FOR SELECT
        USING (user_id::text = current_setting('app.current_user_id', true));
    """)
    
    # Policy 2: Users can create their own meal plans
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Users can create own meal plans"
        ON recipes_mealplan
        FOR INSERT
        WITH CHECK (user_id::text = current_setting('app.current_user_id', true));
    """)
    
    # Policy 3: Users can update their own meal plans
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Users can update own meal plans"
        ON recipes_mealplan
        FOR UPDATE
        USING (user_id::text = current_setting('app.current_user_id', true));
    """)
    
    # Policy 4: Users can delete their own meal plans
    policies.append("""
        CREATE POLICY IF NOT EXISTS "Users can delete own meal plans"
        ON recipes_mealplan
        FOR DELETE
        USING (user_id::text = current_setting('app.current_user_id', true));
    """)
    
    return execute_policies(policies, "recipes_mealplan")


def execute_policies(policies, table_name):
    """Execute a list of RLS policies"""
    success_count = 0
    error_count = 0
    
    try:
        with connection.cursor() as cursor:
            for policy_sql in policies:
                try:
                    cursor.execute(policy_sql)
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    error_msg = str(e)
                    # Check if policy already exists (not a real error)
                    if 'already exists' in error_msg.lower():
                        print(f"[INFO] Policy already exists (skipping)")
                        success_count += 1
                        error_count -= 1
                    else:
                        print(f"[WARN] Policy creation failed: {error_msg[:100]}")
            
            connection.commit()
            
            print(f"\n[INFO] Policies for {table_name}:")
            print(f"       Success: {success_count}")
            if error_count > 0:
                print(f"       Errors: {error_count}")
            
            return success_count > 0
    except Exception as e:
        print(f"[ERROR] Failed to create policies: {e}")
        return False


def setup_rls():
    """Main function to set up RLS"""
    print("\n" + "=" * 70)
    print("RLS SETUP FOR DJANGO")
    print("=" * 70)
    print()
    
    # Check database type
    if not check_database_type():
        return False
    
    print("\n" + "=" * 70)
    print("ENABLING RLS ON TABLES")
    print("=" * 70)
    
    # Enable RLS on all tables
    tables = [
        'users_customuser',
        'recipes_recipe',
        'recipes_comment',
        'recipes_rating',
        'recipes_favorite',
        'recipes_mealplan',
    ]
    
    enabled_tables = []
    for table in tables:
        if enable_rls_on_table(table):
            enabled_tables.append(table)
    
    print(f"\n[INFO] RLS enabled on {len(enabled_tables)} tables")
    
    # Create policies
    print("\n" + "=" * 70)
    print("CREATING RLS POLICIES")
    print("=" * 70)
    
    results = {
        'users': create_user_policies(),
        'recipes': create_recipe_policies(),
        'comments': create_comment_policies(),
        'ratings': create_rating_policies(),
        'favorites': create_favorite_policies(),
        'mealplans': create_mealplan_policies(),
    }
    
    # Summary
    print("\n" + "=" * 70)
    print("RLS SETUP SUMMARY")
    print("=" * 70)
    
    for table, success in results.items():
        status = "[OK]" if success else "[ERROR]"
        print(f"{status} {table.title()} policies: {'Created' if success else 'Failed'}")
    
    all_success = all(results.values())
    
    if all_success:
        print("\n[OK] RLS setup completed successfully!")
        print("\n[NOTE] RLS policies use 'app.current_user_id' setting.")
        print("       You'll need to set this in Django views using:")
        print("       connection.cursor().execute(\"SET app.current_user_id = %s\", [user_id])")
    else:
        print("\n[WARN] Some policies failed. Check errors above.")
    
    return all_success


if __name__ == '__main__':
    setup_rls()

