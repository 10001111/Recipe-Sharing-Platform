"""
Recipe Models for Recipe Sharing Platform

Models:
1. Category - Recipe categories (breakfast, lunch, dinner, dessert, etc.)
2. Ingredient - Ingredients with name, quantity, and unit
3. Recipe - Main recipe model with title, description, instructions, times, images
4. RecipeIngredient - Through model for Recipe-Ingredient many-to-many relationship
5. Rating - User ratings for recipes (1-5 stars with review text)
6. Comment - User comments on recipes
7. Favorite - User saved/favorited recipes
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
    
    # Statistics
    view_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times this recipe has been viewed"
    )
    
    # Dietary Restrictions
    DIETARY_CHOICES = [
        ('none', 'No dietary restrictions'),
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('gluten-free', 'Gluten-Free'),
        ('keto', 'Keto'),
        ('paleo', 'Paleo'),
        ('pescatarian', 'Pescatarian'),
        ('halal', 'Halal'),
        ('kosher', 'Kosher'),
    ]
    
    dietary_restrictions = models.CharField(
        max_length=20,
        choices=DIETARY_CHOICES,
        default='none',
        help_text="Dietary restrictions for this recipe"
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
    
    @property
    def average_rating(self):
        """Calculate average rating from all ratings"""
        from django.db.models import Avg
        result = self.ratings.aggregate(avg_rating=Avg('stars'))
        return round(result['avg_rating'] or 0.0, 2)
    
    @property
    def rating_count(self):
        """Get total number of ratings"""
        return self.ratings.count()
    
    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])


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


class Rating(models.Model):
    """
    Rating Model - User ratings for recipes
    
    Allows users to rate recipes from 1-5 stars with optional review text
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ratings',
        help_text="Recipe being rated"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe_ratings',
        help_text="User who gave the rating"
    )
    stars = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="Rating from 1 to 5 stars"
    )
    review_text = models.TextField(
        blank=True,
        max_length=1000,
        help_text="Optional review text (max 1000 characters)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['recipe', 'user']  # One rating per user per recipe
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipe', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.stars} stars for {self.recipe.title}"


class Comment(models.Model):
    """
    Comment Model - User comments on recipes
    
    Allows users to leave comments on recipes
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="Recipe being commented on"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe_comments',
        help_text="User who wrote the comment"
    )
    text = models.TextField(
        max_length=1000,
        help_text="Comment text (max 1000 characters)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipe', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} commented on {self.recipe.title}"


class Favorite(models.Model):
    """
    Favorite Model - User saved/favorited recipes
    
    Allows users to save/favorite recipes for later
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        help_text="Recipe being favorited"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        help_text="User who favorited the recipe"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['recipe', 'user']  # One favorite per user per recipe
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipe', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"
    
    def __str__(self):
        return f"{self.user.username} favorited {self.recipe.title}"


class RecipeImage(models.Model):
    """
    Recipe Image Model
    
    Supports multiple images per recipe with ordering and primary image designation
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='images',
        help_text="Recipe this image belongs to"
    )
    image_url = models.URLField(
        max_length=500,
        help_text="URL from Vercel Blob Storage or other image hosting service"
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Primary/featured image for the recipe"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text="Alt text for accessibility"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Recipe Image"
        verbose_name_plural = "Recipe Images"
        # Ensure only one primary image per recipe
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'is_primary'],
                condition=models.Q(is_primary=True),
                name='unique_primary_image_per_recipe'
            )
        ]
    
    def __str__(self):
        return f"Image {self.order} for {self.recipe.title}"
    
    def save(self, *args, **kwargs):
        # If this is set as primary, unset other primary images for this recipe
        if self.is_primary:
            RecipeImage.objects.filter(
                recipe=self.recipe,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)


class MealPlan(models.Model):
    """
    Meal Plan Model
    
    Allows users to plan meals on specific dates
    """
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
        ('dessert', 'Dessert'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='meal_plans',
        help_text="User who created this meal plan"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='meal_plans',
        help_text="Recipe planned for this meal"
    )
    date = models.DateField(
        help_text="Date for this meal plan"
    )
    meal_type = models.CharField(
        max_length=20,
        choices=MEAL_TYPE_CHOICES,
        default='dinner',
        help_text="Type of meal (breakfast, lunch, dinner, snack, dessert)"
    )
    notes = models.TextField(
        blank=True,
        max_length=500,
        help_text="Optional notes for this meal plan"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'meal_type']
        verbose_name = "Meal Plan"
        verbose_name_plural = "Meal Plans"
        # Prevent duplicate meal plans for same user, date, and meal type
        unique_together = ['user', 'date', 'meal_type']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['date', 'meal_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_meal_type_display()} on {self.date}"
