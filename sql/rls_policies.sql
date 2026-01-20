-- Row Level Security (RLS) Policies for Recipe Sharing Platform
-- 
-- IMPORTANT: This only works with PostgreSQL/Supabase!
-- Run this script after enabling RLS on tables.
--
-- Usage:
--   psql -d your_database -f sql/rls_policies.sql
--   OR
--   python manage.py setup_rls

-- ============================================================================
-- 1. ENABLE RLS ON TABLES
-- ============================================================================

ALTER TABLE users_customuser ENABLE ROW LEVEL SECURITY;
ALTER TABLE recipes_recipe ENABLE ROW LEVEL SECURITY;
ALTER TABLE recipes_comment ENABLE ROW LEVEL SECURITY;
ALTER TABLE recipes_rating ENABLE ROW LEVEL SECURITY;
ALTER TABLE recipes_favorite ENABLE ROW LEVEL SECURITY;
ALTER TABLE recipes_mealplan ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- 2. USERS TABLE POLICIES
-- ============================================================================

-- Policy: Users can view their own profile
CREATE POLICY IF NOT EXISTS "Users can view own profile"
ON users_customuser
FOR SELECT
USING (id::text = current_setting('app.current_user_id', true));

-- Policy: Users can update their own profile
CREATE POLICY IF NOT EXISTS "Users can update own profile"
ON users_customuser
FOR UPDATE
USING (id::text = current_setting('app.current_user_id', true));

-- Policy: Public can view active user profiles (for recipe authors)
CREATE POLICY IF NOT EXISTS "Public can view active user profiles"
ON users_customuser
FOR SELECT
USING (is_active = true);

-- ============================================================================
-- 3. RECIPES TABLE POLICIES
-- ============================================================================

-- Policy: Anyone can view published recipes
CREATE POLICY IF NOT EXISTS "Public can view published recipes"
ON recipes_recipe
FOR SELECT
USING (is_published = true);

-- Policy: Authors can view their own recipes (even if unpublished)
CREATE POLICY IF NOT EXISTS "Authors can view own recipes"
ON recipes_recipe
FOR SELECT
USING (author_id::text = current_setting('app.current_user_id', true));

-- Policy: Authenticated users can create recipes
CREATE POLICY IF NOT EXISTS "Authenticated users can create recipes"
ON recipes_recipe
FOR INSERT
WITH CHECK (current_setting('app.current_user_id', true) IS NOT NULL);

-- Policy: Authors can update their own recipes
CREATE POLICY IF NOT EXISTS "Authors can update own recipes"
ON recipes_recipe
FOR UPDATE
USING (author_id::text = current_setting('app.current_user_id', true));

-- Policy: Authors can delete their own recipes
CREATE POLICY IF NOT EXISTS "Authors can delete own recipes"
ON recipes_recipe
FOR DELETE
USING (author_id::text = current_setting('app.current_user_id', true));

-- ============================================================================
-- 4. COMMENTS TABLE POLICIES
-- ============================================================================

-- Policy: Anyone can view comments
CREATE POLICY IF NOT EXISTS "Public can view comments"
ON recipes_comment
FOR SELECT
USING (true);

-- Policy: Authenticated users can create comments
CREATE POLICY IF NOT EXISTS "Authenticated users can create comments"
ON recipes_comment
FOR INSERT
WITH CHECK (user_id::text = current_setting('app.current_user_id', true));

-- Policy: Authors can update their own comments
CREATE POLICY IF NOT EXISTS "Authors can update own comments"
ON recipes_comment
FOR UPDATE
USING (user_id::text = current_setting('app.current_user_id', true));

-- Policy: Authors can delete their own comments
CREATE POLICY IF NOT EXISTS "Authors can delete own comments"
ON recipes_comment
FOR DELETE
USING (user_id::text = current_setting('app.current_user_id', true));

-- ============================================================================
-- 5. RATINGS TABLE POLICIES
-- ============================================================================

-- Policy: Anyone can view ratings
CREATE POLICY IF NOT EXISTS "Public can view ratings"
ON recipes_rating
FOR SELECT
USING (true);

-- Policy: Users can create their own ratings
CREATE POLICY IF NOT EXISTS "Users can create own ratings"
ON recipes_rating
FOR INSERT
WITH CHECK (user_id::text = current_setting('app.current_user_id', true));

-- Policy: Users can update their own ratings
CREATE POLICY IF NOT EXISTS "Users can update own ratings"
ON recipes_rating
FOR UPDATE
USING (user_id::text = current_setting('app.current_user_id', true));

-- Policy: Users can delete their own ratings
CREATE POLICY IF NOT EXISTS "Users can delete own ratings"
ON recipes_rating
FOR DELETE
USING (user_id::text = current_setting('app.current_user_id', true));

-- ============================================================================
-- 6. FAVORITES TABLE POLICIES
-- ============================================================================

-- Policy: Users can view their own favorites
CREATE POLICY IF NOT EXISTS "Users can view own favorites"
ON recipes_favorite
FOR SELECT
USING (user_id::text = current_setting('app.current_user_id', true));

-- Policy: Users can create their own favorites
CREATE POLICY IF NOT EXISTS "Users can create own favorites"
ON recipes_favorite
FOR INSERT
WITH CHECK (user_id::text = current_setting('app.current_user_id', true));

-- Policy: Users can delete their own favorites
CREATE POLICY IF NOT EXISTS "Users can delete own favorites"
ON recipes_favorite
FOR DELETE
USING (user_id::text = current_setting('app.current_user_id', true));

-- ============================================================================
-- 7. MEAL PLANS TABLE POLICIES
-- ============================================================================

-- Policy: Users can view their own meal plans
CREATE POLICY IF NOT EXISTS "Users can view own meal plans"
ON recipes_mealplan
FOR SELECT
USING (user_id::text = current_setting('app.current_user_id', true));

-- Policy: Users can create their own meal plans
CREATE POLICY IF NOT EXISTS "Users can create own meal plans"
ON recipes_mealplan
FOR INSERT
WITH CHECK (user_id::text = current_setting('app.current_user_id', true));

-- Policy: Users can update their own meal plans
CREATE POLICY IF NOT EXISTS "Users can update own meal plans"
ON recipes_mealplan
FOR UPDATE
USING (user_id::text = current_setting('app.current_user_id', true));

-- Policy: Users can delete their own meal plans
CREATE POLICY IF NOT EXISTS "Users can delete own meal plans"
ON recipes_mealplan
FOR DELETE
USING (user_id::text = current_setting('app.current_user_id', true));

-- ============================================================================
-- VERIFICATION
-- ============================================================================

-- Check which tables have RLS enabled
SELECT 
    schemaname, 
    tablename, 
    rowsecurity as rls_enabled
FROM pg_tables
WHERE schemaname = 'public'
    AND tablename IN (
        'users_customuser',
        'recipes_recipe',
        'recipes_comment',
        'recipes_rating',
        'recipes_favorite',
        'recipes_mealplan'
    )
ORDER BY tablename;

-- Check existing policies
SELECT 
    schemaname,
    tablename,
    policyname,
    cmd as operation,
    qual as using_expression
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, policyname;

