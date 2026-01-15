"""
Tests for User Models and Relationships

This test suite verifies:
1. CustomUser model functionality
2. UserProfile model and OneToOne relationship
3. User-Recipe relationships
4. Profile signal creation
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .models import UserProfile

User = get_user_model()


class CustomUserModelTest(TestCase):
    """Test CustomUser model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
    
    def test_user_creation(self):
        """Test user can be created"""
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
    
    def test_user_str(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), "testuser")
    
    def test_user_unique_email(self):
        """Test email must be unique"""
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="anotheruser",
                email="test@example.com",
                password="testpass123"
            )
    
    def test_user_authentication(self):
        """Test user can authenticate"""
        from django.contrib.auth import authenticate
        authenticated_user = authenticate(
            username="testuser",
            password="testpass123"
        )
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user, self.user)


class UserProfileModelTest(TestCase):
    """Test UserProfile model and OneToOne relationship"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        # Profile should be created automatically by signal
        self.profile = UserProfile.objects.get(user=self.user)
    
    def test_profile_auto_creation(self):
        """Test profile is automatically created when user is created"""
        self.assertIsNotNone(self.profile)
        self.assertEqual(self.profile.user, self.user)
    
    def test_profile_one_to_one_relationship(self):
        """Test User-Profile OneToOne relationship"""
        # User can access profile via related_name
        self.assertEqual(self.user.profile, self.profile)
        # Profile belongs to user
        self.assertEqual(self.profile.user, self.user)
    
    def test_profile_creation(self):
        """Test profile can be created"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.dietary_preferences, 'none')
        self.assertEqual(self.profile.bio, '')
    
    def test_profile_str(self):
        """Test profile string representation"""
        expected = f"{self.user.username}'s Profile"
        self.assertEqual(str(self.profile), expected)
    
    def test_profile_unique_user(self):
        """Test one profile per user"""
        with self.assertRaises(IntegrityError):
            UserProfile.objects.create(user=self.user)
    
    def test_profile_cascade_delete(self):
        """Test profile is deleted when user is deleted"""
        profile_id = self.profile.id
        self.user.delete()
        self.assertFalse(UserProfile.objects.filter(id=profile_id).exists())
    
    def test_profile_dietary_preferences(self):
        """Test dietary preferences choices"""
        self.profile.dietary_preferences = 'vegan'
        self.profile.save()
        self.assertEqual(self.profile.dietary_preferences, 'vegan')
        
        # Test invalid choice (should still work, but not ideal)
        self.profile.dietary_preferences = 'invalid'
        self.profile.save()
        self.assertEqual(self.profile.dietary_preferences, 'invalid')


class UserRecipeRelationshipTest(TestCase):
    """Test User-Recipe relationships"""
    
    def setUp(self):
        """Set up test data"""
        from apps.recipes.models import Recipe, Category
        
        self.user = User.objects.create_user(
            username="chef",
            email="chef@example.com",
            password="testpass123"
        )
        self.category = Category.objects.create(
            name="Dinner",
            slug="dinner"
        )
        self.recipe1 = Recipe.objects.create(
            title="Recipe 1",
            description="Test",
            instructions="Test",
            author=self.user,
            category=self.category
        )
        self.recipe2 = Recipe.objects.create(
            title="Recipe 2",
            description="Test",
            instructions="Test",
            author=self.user,
            category=self.category
        )
    
    def test_user_recipes_relationship(self):
        """Test User-Recipe ForeignKey relationship"""
        # User can access recipes via related_name
        recipes = self.user.recipes.all()
        self.assertEqual(recipes.count(), 2)
        self.assertIn(self.recipe1, recipes)
        self.assertIn(self.recipe2, recipes)
    
    def test_user_ratings_relationship(self):
        """Test User-Rating relationship"""
        from apps.recipes.models import Rating
        
        rating = Rating.objects.create(
            recipe=self.recipe1,
            user=self.user,
            stars=5
        )
        
        # User can access ratings via related_name
        self.assertIn(rating, self.user.recipe_ratings.all())
    
    def test_user_comments_relationship(self):
        """Test User-Comment relationship"""
        from apps.recipes.models import Comment
        
        comment = Comment.objects.create(
            recipe=self.recipe1,
            user=self.user,
            text="Great recipe!"
        )
        
        # User can access comments via related_name
        self.assertIn(comment, self.user.recipe_comments.all())
    
    def test_user_favorites_relationship(self):
        """Test User-Favorite relationship"""
        from apps.recipes.models import Favorite
        
        favorite = Favorite.objects.create(
            recipe=self.recipe1,
            user=self.user
        )
        
        # User can access favorites via related_name
        self.assertIn(favorite, self.user.favorite_recipes.all())
