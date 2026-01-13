"""
Recipe Models for Recipe Sharing Platform

Models:
1. Category - Recipe categories (breakfast, lunch, dinner, dessert, etc.)
2. Ingredient - Ingredients with name, quantity, and unit
3. Recipe - Main recipe model with title, description, instructions, times, images
4. RecipeIngredient - Through model for Recipe-Ingredient many-to-many relationship
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    """
    Recipe Category Model
    
    Categories like: breakfast, lunch, dinner, dessert, snack, etc.
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Category name (e.g., Breakfast, Lunch, Dinner)"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        help_text="URL-friendly version of name"
    )
    description = models.TextField(
        blank=True,
        help_text="Optional description of this category"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('recipes:category_detail', kwargs={'slug': self.slug})


class Ingredient(models.Model):
    """
    Ingredient Model
    
    Stores ingredient information: name, quantity, and unit
    """
    name = models.CharField(
        max_length=200,
        help_text="Ingredient name (e.g., Flour, Sugar, Chicken)"
    )
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Recipe Model
    
    Main recipe model with all recipe information
    """
    # Basic Information
    title = models.CharField(
        max_length=200,
        help_text="Recipe title"
    )
    description = models.TextField(
        help_text="Brief description of the recipe"
    )
    instructions = models.TextField(
        help_text="Step-by-step cooking instructions"
    )
    
    # Timing Information
    prep_time = models.PositiveIntegerField(
        help_text="Preparation time in minutes",
        default=0
    )
    cook_time = models.PositiveIntegerField(
        help_text="Cooking time in minutes",
        default=0
    )
    
    # Image Upload
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True,
        help_text="Recipe image"
    )
    
    # Relationships
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        help_text="User who created this recipe"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recipes',
        help_text="Recipe category"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        help_text="Ingredients used in this recipe"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(
        default=True,
        help_text="Whether this recipe is published and visible to others"
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['category', '-created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'pk': self.pk})
    
    @property
    def total_time(self):
        """Calculate total time (prep + cook)"""
        return self.prep_time + self.cook_time


class RecipeIngredient(models.Model):
    """
    Through Model for Recipe-Ingredient Many-to-Many Relationship
    
    Stores quantity and unit for each ingredient in a recipe
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Quantity of ingredient"
    )
    unit = models.CharField(
        max_length=50,
        help_text="Unit of measurement (e.g., cups, tablespoons, grams, pieces)",
        default=''
    )
    notes = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional notes (e.g., 'chopped', 'diced', 'optional')"
    )
    
    class Meta:
        unique_together = ['recipe', 'ingredient']
        ordering = ['ingredient__name']
    
    def __str__(self):
        if self.unit:
            return f"{self.quantity} {self.unit} {self.ingredient.name}"
        return f"{self.quantity} {self.ingredient.name}"
