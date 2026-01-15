from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, NotFound
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model
from apps.recipes.models import Recipe, Rating, Comment, Favorite
from apps.users.models import UserProfile
from .serializers import (
    RecipeSerializer, RecipeListSerializer,
    RatingSerializer, CommentSerializer, FavoriteSerializer,
    UserProfileSerializer
)

User = get_user_model()


@api_view(['GET'])
@permission_classes([AllowAny])  # Public endpoint
def api_root(request):
    """
    API Root endpoint.
    Returns basic API information and available endpoints.
    """
    return Response({
        'message': 'Welcome to Recipe Sharing Platform API',
        'version': '1.0.0',
        'endpoints': {
            'recipes': '/api/recipes/',
            'ratings': '/api/ratings/',
            'comments': '/api/comments/',
            'favorites': '/api/favorites/',
            'health': '/api/health/',
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])  # Public endpoint - anon key is safe to expose
def supabase_config(request):
    """
    Get Supabase configuration for frontend
    Returns Supabase URL and anon key (safe to expose publicly)
    """
    from django.conf import settings
    supabase_url = getattr(settings, 'SUPABASE_URL', '')
    supabase_anon_key = getattr(settings, 'SUPABASE_ANON_KEY', '')
    
    return Response({
        'supabase_url': supabase_url,
        'supabase_anon_key': supabase_anon_key,
        'enabled': bool(supabase_url and supabase_anon_key)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Get current authenticated user information
    """
    from .serializers import UserSerializer
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])  # Public endpoint - anyone can view profiles
def user_profile(request, username):
    """
    Get user profile by username
    """
    try:
        user = User.objects.get(username=username)
        profile, created = UserProfile.objects.get_or_create(user=user)
        serializer = UserProfileSerializer(profile, context={'request': request})
        
        # Add recipe statistics
        user_recipes = Recipe.objects.filter(author=user, is_published=True)
        recipe_count = user_recipes.count()
        
        return Response({
            **serializer.data,
            'recipe_count': recipe_count,
        })
    except User.DoesNotExist:
        raise NotFound("User not found")


@api_view(['PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request, username):
    """
    Update user profile (username and avatar)
    Only the profile owner can update
    """
    try:
        user = User.objects.get(username=username)
        
        # Check if user is updating their own profile
        if request.user != user:
            return Response(
                {'error': 'You can only update your own profile'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Update username if provided
        if 'username' in request.data:
            new_username = request.data['username']
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                return Response(
                    {'error': 'Username already taken'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.username = new_username
            user.save()
        
        # Prepare data for profile update (exclude username as it's handled separately)
        profile_data = {}
        if 'bio' in request.data:
            profile_data['bio'] = request.data['bio']
        if 'avatar' in request.FILES:
            profile_data['avatar'] = request.FILES['avatar']
        if 'dietary_preferences' in request.data:
            profile_data['dietary_preferences'] = request.data['dietary_preferences']
        
        # Update profile fields
        serializer = UserProfileSerializer(profile, data=profile_data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            
            # Return updated profile
            updated_serializer = UserProfileSerializer(profile, context={'request': request})
            user_recipes = Recipe.objects.filter(author=user, is_published=True)
            recipe_count = user_recipes.count()
            
            return Response({
                **updated_serializer.data,
                'recipe_count': recipe_count,
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except User.DoesNotExist:
        raise NotFound("User not found")


@api_view(['GET'])
@permission_classes([AllowAny])  # Public endpoint for monitoring
def health_check(request):
    """
    Health check endpoint.
    Useful for monitoring and testing database connection.
    """
    from django.db import connection
    
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return Response({
        'status': 'healthy',
        'database': db_status,
    }, status=status.HTTP_200_OK)


# ========== RECIPE API VIEWS ==========

class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Recipe CRUD operations
    
    list: Get all published recipes
    retrieve: Get a single recipe with statistics
    create: Create a new recipe (authenticated users only)
    update: Update a recipe (author or staff only)
    destroy: Delete a recipe (author or staff only)
    """
    queryset = Recipe.objects.filter(is_published=True).select_related('author', 'category')
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeListSerializer
        return RecipeSerializer
    
    def get_serializer_context(self):
        """Pass request context to serializer"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_permissions(self):
        """Allow public read access, require auth for write operations"""
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """Filter recipes based on query parameters"""
        # Use prefetch_related to optimize statistics queries
        queryset = Recipe.objects.filter(is_published=True).select_related('author', 'category').prefetch_related(
            'ratings',
            'comments',
            'favorites'
        )
        
        # Filter by category
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(ingredients__name__icontains=search)
            ).distinct()
        
        # Filter by author (ID or username)
        author_id = self.request.query_params.get('author', None)
        author_username = self.request.query_params.get('author_username', None)
        
        if author_username:
            queryset = queryset.filter(author__username=author_username)
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """Set the author to the current user"""
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        """Check permissions before updating"""
        recipe = self.get_object()
        if recipe.author != self.request.user and not self.request.user.is_staff:
            raise ValidationError("You do not have permission to edit this recipe.")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Check permissions before deleting"""
        if instance.author != self.request.user and not self.request.user.is_staff:
            raise ValidationError("You do not have permission to delete this recipe.")
        instance.delete()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def increment_view(self, request, pk=None):
        """Increment view count for a recipe"""
        recipe = self.get_object()
        recipe.increment_view_count()
        return Response({
            'view_count': recipe.view_count
        }, status=status.HTTP_200_OK)


# ========== RATING API VIEWS ==========

class RatingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Rating operations
    
    list: Get all ratings for a recipe
    create: Create or update a rating for a recipe
    retrieve: Get a specific rating
    update: Update a rating (owner only)
    destroy: Delete a rating (owner only)
    """
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter ratings by recipe if provided"""
        queryset = Rating.objects.select_related('user', 'recipe')
        recipe_id = self.request.query_params.get('recipe', None)
        if recipe_id:
            queryset = queryset.filter(recipe_id=recipe_id)
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """Create or update rating for current user"""
        recipe_id = self.request.data.get('recipe')
        recipe = get_object_or_404(Recipe, pk=recipe_id, is_published=True)
        
        # Get or create rating
        rating, created = Rating.objects.get_or_create(
            recipe=recipe,
            user=self.request.user,
            defaults={'stars': serializer.validated_data['stars']}
        )
        
        if not created:
            # Update existing rating
            rating.stars = serializer.validated_data['stars']
            rating.review_text = serializer.validated_data.get('review_text', rating.review_text)
            rating.save()
    
    def perform_update(self, serializer):
        """Check permissions before updating"""
        rating = self.get_object()
        if rating.user != self.request.user:
            raise ValidationError("You can only update your own ratings.")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Check permissions before deleting"""
        if instance.user != self.request.user:
            raise ValidationError("You can only delete your own ratings.")
        instance.delete()


# ========== COMMENT API VIEWS ==========

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment operations
    
    list: Get all comments for a recipe
    create: Create a comment on a recipe
    retrieve: Get a specific comment
    update: Update a comment (owner only)
    destroy: Delete a comment (owner or staff only)
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter comments by recipe if provided"""
        queryset = Comment.objects.select_related('user', 'recipe')
        recipe_id = self.request.query_params.get('recipe', None)
        if recipe_id:
            queryset = queryset.filter(recipe_id=recipe_id)
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """Create comment for current user"""
        recipe_id = self.request.data.get('recipe')
        recipe = get_object_or_404(Recipe, pk=recipe_id, is_published=True)
        serializer.save(user=self.request.user, recipe=recipe)
    
    def perform_update(self, serializer):
        """Check permissions before updating"""
        comment = self.get_object()
        if comment.user != self.request.user:
            raise ValidationError("You can only update your own comments.")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Check permissions before deleting"""
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise ValidationError("You do not have permission to delete this comment.")
        instance.delete()


# ========== FAVORITE API VIEWS ==========

class FavoriteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Favorite operations
    
    list: Get all favorites (user's favorites if no recipe filter)
    create: Add a recipe to favorites
    destroy: Remove a recipe from favorites
    """
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter favorites by user or recipe"""
        queryset = Favorite.objects.select_related('user', 'recipe')
        
        # If recipe parameter provided, get favorites for that recipe
        recipe_id = self.request.query_params.get('recipe', None)
        if recipe_id:
            queryset = queryset.filter(recipe_id=recipe_id)
        else:
            # Otherwise, get current user's favorites
            queryset = queryset.filter(user=self.request.user)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """Create favorite for current user"""
        recipe_id = self.request.data.get('recipe')
        recipe = get_object_or_404(Recipe, pk=recipe_id, is_published=True)
        
        # Check if already favorited
        favorite, created = Favorite.objects.get_or_create(
            recipe=recipe,
            user=self.request.user
        )
        
        if not created:
            raise ValidationError("Recipe is already in your favorites.")
        
        serializer.instance = favorite
    
    def perform_destroy(self, instance):
        """Check permissions before deleting"""
        if instance.user != self.request.user:
            raise ValidationError("You can only remove your own favorites.")
        instance.delete()
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle(self, request):
        """Toggle favorite status for a recipe"""
        recipe_id = request.data.get('recipe')
        if not recipe_id:
            return Response(
                {'error': 'Recipe ID is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        recipe = get_object_or_404(Recipe, pk=recipe_id, is_published=True)
        
        favorite, created = Favorite.objects.get_or_create(
            recipe=recipe,
            user=request.user
        )
        
        if not created:
            favorite.delete()
            is_favorited = False
        else:
            is_favorited = True
        
        return Response({
            'is_favorited': is_favorited,
            'favorite_count': recipe.favorites.count()
        }, status=status.HTTP_200_OK)
