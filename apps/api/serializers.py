"""
API Serializers for Recipe Sharing Platform

Serializers for REST API endpoints
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.recipes.models import Recipe, Category, Ingredient, RecipeIngredient, Rating, Comment, Favorite, RecipeImage
from apps.users.models import UserProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    user = UserSerializer(read_only=True)
    avatar_url = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'bio', 'avatar', 'avatar_url', 'dietary_preferences', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'user']
    
    def get_avatar_url(self, obj):
        """Get full URL for avatar"""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient model"""
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Serializer for RecipeIngredient through model"""
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient',
        write_only=True
    )
    
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'ingredient_id', 'quantity', 'unit', 'notes']
        read_only_fields = ['id']


class RatingSerializer(serializers.ModelSerializer):
    """Serializer for Rating model"""
    user = UserSerializer(read_only=True)
    recipe_title = serializers.CharField(source='recipe.title', read_only=True)
    
    class Meta:
        model = Rating
        fields = ['id', 'recipe', 'recipe_title', 'user', 'stars', 'review_text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def validate_stars(self, value):
        """Validate that stars are between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5 stars.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    user = UserSerializer(read_only=True)
    recipe_title = serializers.CharField(source='recipe.title', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'recipe', 'recipe_title', 'user', 'text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def validate_text(self, value):
        """Validate comment text length"""
        if len(value) > 1000:
            raise serializers.ValidationError("Comment cannot exceed 1000 characters.")
        return value


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for Favorite model"""
    user = UserSerializer(read_only=True)
    recipe_title = serializers.CharField(source='recipe.title', read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'recipe', 'recipe_title', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for RecipeImage model"""
    
    class Meta:
        model = RecipeImage
        fields = ['id', 'recipe', 'image_url', 'is_primary', 'order', 'alt_text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe model with statistics"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    ingredients_data = serializers.JSONField(write_only=True, required=False)
    images = RecipeImageSerializer(many=True, read_only=True)
    images_data = serializers.JSONField(write_only=True, required=False)
    
    # Statistics fields
    average_rating = serializers.ReadOnlyField()
    rating_count = serializers.SerializerMethodField()
    view_count = serializers.ReadOnlyField()
    total_time = serializers.ReadOnlyField()
    favorite_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    
    # User-specific fields (if authenticated)
    is_favorited = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'instructions',
            'prep_time',
            'cook_time',
            'total_time',
            'image',
            'author',
            'category',
            'category_id',
            'recipe_ingredients',
            'ingredients_data',
            'images',
            'images_data',
            'dietary_restrictions',
            'view_count',
            'average_rating',
            'rating_count',
            'favorite_count',
            'comment_count',
            'is_favorited',
            'user_rating',
            'dietary_restrictions',
            'is_published',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def get_rating_count(self, obj):
        """Get total number of ratings"""
        return obj.rating_count
    
    def get_favorite_count(self, obj):
        """Get total number of favorites"""
        return obj.favorites.count()
    
    def get_comment_count(self, obj):
        """Get total number of comments"""
        return obj.comments.count()
    
    def get_is_favorited(self, obj):
        """Check if current user has favorited this recipe"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False
    
    def get_user_rating(self, obj):
        """Get current user's rating if exists"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                rating = obj.ratings.get(user=request.user)
                return {
                    'id': rating.id,
                    'stars': rating.stars,
                    'review_text': rating.review_text,
                    'created_at': rating.created_at,
                    'updated_at': rating.updated_at,
                }
            except Rating.DoesNotExist:
                return None
        return None
    
    def create(self, validated_data):
        """Create recipe and handle ingredients and images"""
        ingredients_data = validated_data.pop('ingredients_data', [])
        images_data = validated_data.pop('images_data', [])
        recipe = Recipe.objects.create(**validated_data)
        
        # Handle ingredients
        if ingredients_data:
            for ing_data in ingredients_data:
                if ing_data.get('name') and ing_data.get('quantity'):
                    # Get or create ingredient
                    ingredient, _ = Ingredient.objects.get_or_create(
                        name=ing_data['name'].strip()
                    )
                    # Create RecipeIngredient
                    RecipeIngredient.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        quantity=ing_data.get('quantity', 0),
                        unit=ing_data.get('unit', ''),
                        notes=ing_data.get('notes', '')
                    )
        
        # Handle images
        if images_data:
            for idx, img_data in enumerate(images_data):
                if img_data.get('image_url'):
                    RecipeImage.objects.create(
                        recipe=recipe,
                        image_url=img_data['image_url'],
                        is_primary=img_data.get('is_primary', idx == 0),
                        order=img_data.get('order', idx),
                        alt_text=img_data.get('alt_text', '')
                    )
        
        return recipe
    
    def update(self, instance, validated_data):
        """Update recipe and handle ingredients and images"""
        ingredients_data = validated_data.pop('ingredients_data', None)
        images_data = validated_data.pop('images_data', None)
        
        # Update recipe fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Handle ingredients if provided
        if ingredients_data is not None:
            # Clear existing ingredients
            RecipeIngredient.objects.filter(recipe=instance).delete()
            
            # Add new ingredients
            if ingredients_data:
                for ing_data in ingredients_data:
                    if ing_data.get('name') and ing_data.get('quantity'):
                        # Get or create ingredient
                        ingredient, _ = Ingredient.objects.get_or_create(
                            name=ing_data['name'].strip()
                        )
                        # Create RecipeIngredient
                        RecipeIngredient.objects.create(
                            recipe=instance,
                            ingredient=ingredient,
                            quantity=ing_data.get('quantity', 0),
                            unit=ing_data.get('unit', ''),
                            notes=ing_data.get('notes', '')
                        )
        
        # Handle images if provided
        if images_data is not None:
            # Clear existing images
            RecipeImage.objects.filter(recipe=instance).delete()
            
            # Add new images
            if images_data:
                for idx, img_data in enumerate(images_data):
                    if img_data.get('image_url'):
                        RecipeImage.objects.create(
                            recipe=instance,
                            image_url=img_data['image_url'],
                            is_primary=img_data.get('is_primary', idx == 0),
                            order=img_data.get('order', idx),
                            alt_text=img_data.get('alt_text', '')
                        )
        
        return instance


class RecipeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for recipe list views"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    average_rating = serializers.ReadOnlyField()
    rating_count = serializers.SerializerMethodField()
    favorite_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'prep_time',
            'cook_time',
            'image',
            'author',
            'category',
            'dietary_restrictions',
            'average_rating',
            'rating_count',
            'favorite_count',
            'comment_count',
            'view_count',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_rating_count(self, obj):
        return obj.rating_count
    
    def get_favorite_count(self, obj):
        return obj.favorites.count()
    
    def get_comment_count(self, obj):
        return obj.comments.count()
