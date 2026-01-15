"""
Tests for Recipe Models and Relationships

This test suite verifies:
1. Model creation and basic functionality
2. All model relationships (ForeignKeys, ManyToMany, OneToOne)
3. Model methods and properties
4. Constraints and validations
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import (
    Category, Ingredient, Recipe, RecipeIngredient,
    Rating, Comment, Favorite
)

User = get_user_model()


class CategoryModelTest(TestCase):
    """Test Category model"""
    
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(
            name="Breakfast",
            slug="breakfast",
            description="Morning meals"
        )
    
    def test_category_creation(self):
        """Test category can be created"""
        self.assertEqual(self.category.name, "Breakfast")
        self.assertEqual(self.category.slug, "breakfast")
        self.assertTrue(isinstance(self.category, Category))
    
    def test_category_str(self):
        """Test category string representation"""
        self.assertEqual(str(self.category), "Breakfast")
    
    def test_category_unique_name(self):
        """Test category name must be unique"""
        with self.assertRaises(IntegrityError):
            Category.objects.create(
                name="Breakfast",
                slug="breakfast-2"
            )


class IngredientModelTest(TestCase):
    """Test Ingredient model"""
    
    def setUp(self):
        """Set up test data"""
        self.ingredient = Ingredient.objects.create(name="Flour")
    
    def test_ingredient_creation(self):
        """Test ingredient can be created"""
        self.assertEqual(self.ingredient.name, "Flour")
        self.assertTrue(isinstance(self.ingredient, Ingredient))
    
    def test_ingredient_str(self):
        """Test ingredient string representation"""
        self.assertEqual(str(self.ingredient), "Flour")


class RecipeModelTest(TestCase):
    """Test Recipe model and relationships"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testchef",
            email="test@example.com",
            password="testpass123"
        )
        self.category = Category.objects.create(
            name="Dinner",
            slug="dinner"
        )
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            description="A test recipe",
            instructions="Do this, then that",
            prep_time=10,
            cook_time=20,
            author=self.user,
            category=self.category
        )
    
    def test_recipe_creation(self):
        """Test recipe can be created"""
        self.assertEqual(self.recipe.title, "Test Recipe")
        self.assertEqual(self.recipe.author, self.user)
        self.assertEqual(self.recipe.category, self.category)
        self.assertTrue(isinstance(self.recipe, Recipe))
    
    def test_recipe_author_relationship(self):
        """Test Recipe-Author ForeignKey relationship"""
        # Recipe belongs to user
        self.assertEqual(self.recipe.author, self.user)
        # User can access recipes via related_name
        self.assertIn(self.recipe, self.user.recipes.all())
    
    def test_recipe_category_relationship(self):
        """Test Recipe-Category ForeignKey relationship"""
        # Recipe belongs to category
        self.assertEqual(self.recipe.category, self.category)
        # Category can access recipes via related_name
        self.assertIn(self.recipe, self.category.recipes.all())
    
    def test_recipe_total_time_property(self):
        """Test total_time property"""
        self.assertEqual(self.recipe.total_time, 30)
    
    def test_recipe_view_count(self):
        """Test view count increment"""
        initial_count = self.recipe.view_count
        self.recipe.increment_view_count()
        self.assertEqual(self.recipe.view_count, initial_count + 1)
    
    def test_recipe_cascade_delete_author(self):
        """Test recipe is deleted when author is deleted"""
        recipe_id = self.recipe.id
        self.user.delete()
        self.assertFalse(Recipe.objects.filter(id=recipe_id).exists())
    
    def test_recipe_set_null_category(self):
        """Test recipe category is set to NULL when category is deleted"""
        category_id = self.category.id
        self.category.delete()
        self.recipe.refresh_from_db()
        self.assertIsNone(self.recipe.category)


class RecipeIngredientModelTest(TestCase):
    """Test RecipeIngredient through model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testchef",
            email="test@example.com",
            password="testpass123"
        )
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Test",
            instructions="Test",
            author=self.user
        )
        self.ingredient = Ingredient.objects.create(name="Flour")
        self.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=2.5,
            unit="cups"
        )
    
    def test_recipe_ingredient_creation(self):
        """Test RecipeIngredient can be created"""
        self.assertEqual(self.recipe_ingredient.recipe, self.recipe)
        self.assertEqual(self.recipe_ingredient.ingredient, self.ingredient)
        self.assertEqual(float(self.recipe_ingredient.quantity), 2.5)
    
    def test_recipe_ingredient_relationship(self):
        """Test Recipe-Ingredient ManyToMany relationship"""
        # Recipe can access ingredients
        self.assertIn(self.ingredient, self.recipe.ingredients.all())
        # Ingredient can access recipes
        self.assertIn(self.recipe, self.ingredient.recipes.all())
    
    def test_recipe_ingredient_unique_together(self):
        """Test unique_together constraint"""
        with self.assertRaises(IntegrityError):
            RecipeIngredient.objects.create(
                recipe=self.recipe,
                ingredient=self.ingredient,
                quantity=1.0,
                unit="cup"
            )
    
    def test_recipe_ingredient_str(self):
        """Test RecipeIngredient string representation"""
        expected = "2.5 cups Flour"
        self.assertEqual(str(self.recipe_ingredient), expected)


class RatingModelTest(TestCase):
    """Test Rating model and relationships"""
    
    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="testpass123"
        )
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Test",
            instructions="Test",
            author=self.user1
        )
        self.rating = Rating.objects.create(
            recipe=self.recipe,
            user=self.user2,
            stars=5,
            review_text="Great recipe!"
        )
    
    def test_rating_creation(self):
        """Test rating can be created"""
        self.assertEqual(self.rating.recipe, self.recipe)
        self.assertEqual(self.rating.user, self.user2)
        self.assertEqual(self.rating.stars, 5)
    
    def test_rating_recipe_relationship(self):
        """Test Rating-Recipe ForeignKey relationship"""
        # Rating belongs to recipe
        self.assertEqual(self.rating.recipe, self.recipe)
        # Recipe can access ratings via related_name
        self.assertIn(self.rating, self.recipe.ratings.all())
    
    def test_rating_user_relationship(self):
        """Test Rating-User ForeignKey relationship"""
        # Rating belongs to user
        self.assertEqual(self.rating.user, self.user2)
        # User can access ratings via related_name
        self.assertIn(self.rating, self.user2.recipe_ratings.all())
    
    def test_rating_unique_together(self):
        """Test one rating per user per recipe"""
        with self.assertRaises(IntegrityError):
            Rating.objects.create(
                recipe=self.recipe,
                user=self.user2,
                stars=4
            )
    
    def test_recipe_average_rating_property(self):
        """Test recipe average_rating property"""
        # Create another rating
        Rating.objects.create(
            recipe=self.recipe,
            user=self.user1,
            stars=4
        )
        # Average should be (5 + 4) / 2 = 4.5
        self.assertEqual(self.recipe.average_rating, 4.5)
    
    def test_recipe_rating_count_property(self):
        """Test recipe rating_count property"""
        initial_count = self.recipe.rating_count
        Rating.objects.create(
            recipe=self.recipe,
            user=self.user1,
            stars=4
        )
        self.assertEqual(self.recipe.rating_count, initial_count + 1)
    
    def test_rating_cascade_delete_recipe(self):
        """Test rating is deleted when recipe is deleted"""
        rating_id = self.rating.id
        self.recipe.delete()
        self.assertFalse(Rating.objects.filter(id=rating_id).exists())
    
    def test_rating_cascade_delete_user(self):
        """Test rating is deleted when user is deleted"""
        rating_id = self.rating.id
        self.user2.delete()
        self.assertFalse(Rating.objects.filter(id=rating_id).exists())


class CommentModelTest(TestCase):
    """Test Comment model and relationships"""
    
    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username="author",
            email="author@example.com",
            password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="commenter",
            email="commenter@example.com",
            password="testpass123"
        )
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Test",
            instructions="Test",
            author=self.user1
        )
        self.comment = Comment.objects.create(
            recipe=self.recipe,
            user=self.user2,
            text="This is a great recipe!"
        )
    
    def test_comment_creation(self):
        """Test comment can be created"""
        self.assertEqual(self.comment.recipe, self.recipe)
        self.assertEqual(self.comment.user, self.user2)
        self.assertEqual(self.comment.text, "This is a great recipe!")
    
    def test_comment_recipe_relationship(self):
        """Test Comment-Recipe ForeignKey relationship"""
        # Comment belongs to recipe
        self.assertEqual(self.comment.recipe, self.recipe)
        # Recipe can access comments via related_name
        self.assertIn(self.comment, self.recipe.comments.all())
    
    def test_comment_user_relationship(self):
        """Test Comment-User ForeignKey relationship"""
        # Comment belongs to user
        self.assertEqual(self.comment.user, self.user2)
        # User can access comments via related_name
        self.assertIn(self.comment, self.user2.recipe_comments.all())
    
    def test_comment_cascade_delete_recipe(self):
        """Test comment is deleted when recipe is deleted"""
        comment_id = self.comment.id
        self.recipe.delete()
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())
    
    def test_comment_cascade_delete_user(self):
        """Test comment is deleted when user is deleted"""
        comment_id = self.comment.id
        self.user2.delete()
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())


class FavoriteModelTest(TestCase):
    """Test Favorite model and relationships"""
    
    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username="author",
            email="author@example.com",
            password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="fan",
            email="fan@example.com",
            password="testpass123"
        )
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Test",
            instructions="Test",
            author=self.user1
        )
        self.favorite = Favorite.objects.create(
            recipe=self.recipe,
            user=self.user2
        )
    
    def test_favorite_creation(self):
        """Test favorite can be created"""
        self.assertEqual(self.favorite.recipe, self.recipe)
        self.assertEqual(self.favorite.user, self.user2)
    
    def test_favorite_recipe_relationship(self):
        """Test Favorite-Recipe ForeignKey relationship"""
        # Favorite belongs to recipe
        self.assertEqual(self.favorite.recipe, self.recipe)
        # Recipe can access favorites via related_name
        self.assertIn(self.favorite, self.recipe.favorites.all())
    
    def test_favorite_user_relationship(self):
        """Test Favorite-User ForeignKey relationship"""
        # Favorite belongs to user
        self.assertEqual(self.favorite.user, self.user2)
        # User can access favorites via related_name
        self.assertIn(self.favorite, self.user2.favorite_recipes.all())
    
    def test_favorite_unique_together(self):
        """Test one favorite per user per recipe"""
        with self.assertRaises(IntegrityError):
            Favorite.objects.create(
                recipe=self.recipe,
                user=self.user2
            )
    
    def test_favorite_cascade_delete_recipe(self):
        """Test favorite is deleted when recipe is deleted"""
        favorite_id = self.favorite.id
        self.recipe.delete()
        self.assertFalse(Favorite.objects.filter(id=favorite_id).exists())
    
    def test_favorite_cascade_delete_user(self):
        """Test favorite is deleted when user is deleted"""
        favorite_id = self.favorite.id
        self.user2.delete()
        self.assertFalse(Favorite.objects.filter(id=favorite_id).exists())


class ModelRelationshipsIntegrationTest(TestCase):
    """Integration tests for all model relationships"""
    
    def setUp(self):
        """Set up comprehensive test data"""
        # Create users
        self.user1 = User.objects.create_user(
            username="chef1",
            email="chef1@example.com",
            password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="chef2",
            email="chef2@example.com",
            password="testpass123"
        )
        
        # Create category
        self.category = Category.objects.create(
            name="Dessert",
            slug="dessert"
        )
        
        # Create recipe
        self.recipe = Recipe.objects.create(
            title="Chocolate Cake",
            description="Delicious chocolate cake",
            instructions="Mix and bake",
            prep_time=20,
            cook_time=30,
            author=self.user1,
            category=self.category
        )
        
        # Create ingredients
        self.flour = Ingredient.objects.create(name="Flour")
        self.sugar = Ingredient.objects.create(name="Sugar")
        
        # Link ingredients to recipe
        RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.flour,
            quantity=2.0,
            unit="cups"
        )
        RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.sugar,
            quantity=1.5,
            unit="cups"
        )
        
        # Create ratings
        Rating.objects.create(
            recipe=self.recipe,
            user=self.user2,
            stars=5,
            review_text="Amazing!"
        )
        
        # Create comments
        Comment.objects.create(
            recipe=self.recipe,
            user=self.user2,
            text="Can't wait to try this!"
        )
        
        # Create favorites
        Favorite.objects.create(
            recipe=self.recipe,
            user=self.user2
        )
    
    def test_all_relationships_exist(self):
        """Test all relationships are properly established"""
        # Recipe-Author
        self.assertEqual(self.recipe.author, self.user1)
        self.assertIn(self.recipe, self.user1.recipes.all())
        
        # Recipe-Category
        self.assertEqual(self.recipe.category, self.category)
        self.assertIn(self.recipe, self.category.recipes.all())
        
        # Recipe-Ingredients (ManyToMany)
        self.assertIn(self.flour, self.recipe.ingredients.all())
        self.assertIn(self.sugar, self.recipe.ingredients.all())
        self.assertIn(self.recipe, self.flour.recipes.all())
        
        # Recipe-Ratings
        self.assertEqual(self.recipe.ratings.count(), 1)
        self.assertEqual(self.recipe.ratings.first().user, self.user2)
        
        # Recipe-Comments
        self.assertEqual(self.recipe.comments.count(), 1)
        self.assertEqual(self.recipe.comments.first().user, self.user2)
        
        # Recipe-Favorites
        self.assertEqual(self.recipe.favorites.count(), 1)
        self.assertEqual(self.recipe.favorites.first().user, self.user2)
        
        # User-Ratings
        self.assertEqual(self.user2.recipe_ratings.count(), 1)
        
        # User-Comments
        self.assertEqual(self.user2.recipe_comments.count(), 1)
        
        # User-Favorites
        self.assertEqual(self.user2.favorite_recipes.count(), 1)
    
    def test_recipe_statistics(self):
        """Test recipe statistics calculations"""
        # Add more ratings
        Rating.objects.create(
            recipe=self.recipe,
            user=self.user1,
            stars=4
        )
        
        # Check statistics
        self.assertEqual(self.recipe.rating_count, 2)
        self.assertEqual(self.recipe.average_rating, 4.5)
        self.assertEqual(self.recipe.comment_count, 1)
        self.assertEqual(self.recipe.favorites.count(), 1)
