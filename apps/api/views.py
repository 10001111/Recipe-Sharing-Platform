from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, NotFound
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authtoken.models import Token
from apps.recipes.models import Recipe, Rating, Comment, Favorite, MealPlan, Ingredient
from apps.users.models import UserProfile
from .models import APIKey
from .serializers import (
    RecipeSerializer, RecipeListSerializer,
    RatingSerializer, CommentSerializer, FavoriteSerializer,
    UserProfileSerializer, MealPlanSerializer, IngredientSerializer,
    APIKeySerializer
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
        'documentation': {
            'swagger': request.build_absolute_uri('/api/docs/'),
            'redoc': request.build_absolute_uri('/api/redoc/'),
            'schema': request.build_absolute_uri('/api/schema/'),
        },
        'endpoints': {
            'recipes': request.build_absolute_uri('/api/recipes/'),
            'ratings': request.build_absolute_uri('/api/ratings/'),
            'comments': request.build_absolute_uri('/api/comments/'),
            'favorites': request.build_absolute_uri('/api/favorites/'),
            'meal-plans': request.build_absolute_uri('/api/meal-plans/'),
            'users': request.build_absolute_uri('/api/users/me/'),
            'health': request.build_absolute_uri('/api/health/'),
        },
        'authentication': {
            'token': request.build_absolute_uri('/api/auth/token/'),
            'jwt': request.build_absolute_uri('/api/auth/token/'),
            'session': 'Use Django session cookies',
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])  # Public endpoint - anon key is safe to expose
def supabase_config(request):
    """
    Get Supabase configuration for frontend
    
    Returns Supabase URL and anonymous key for client-side authentication.
    This endpoint is public and safe to expose.
    """
    from django.conf import settings
    
    return Response({
        'supabase_url': getattr(settings, 'SUPABASE_URL', ''),
        'supabase_anon_key': getattr(settings, 'SUPABASE_ANON_KEY', ''),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Get current authenticated user information
    
    Returns the currently authenticated user's details.
    Requires authentication via Session, Token, or JWT.
    """
    from .serializers import UserSerializer
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_favorites(request):
    """
    Get current user's favorite recipes
    
    Returns a list of recipes that the current user has favorited.
    Requires authentication.
    """
    from .serializers import RecipeListSerializer
    from rest_framework.pagination import PageNumberPagination
    
    favorites = Favorite.objects.filter(user=request.user).select_related('recipe', 'recipe__author', 'recipe__category').prefetch_related(
        'recipe__recipe_ingredients__ingredient',
        'recipe__ratings',
        'recipe__comments',
        'recipe__favorites',
        'recipe__images'
    )
    
    recipes = [favorite.recipe for favorite in favorites]
    
    # Apply pagination
    paginator = PageNumberPagination()
    paginator.page_size = 20
    page = paginator.paginate_queryset(recipes, request)
    
    if page is not None:
        serializer = RecipeListSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    
    serializer = RecipeListSerializer(recipes, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_token(request):
    """
    Obtain API token for authentication
    
    POST with username and password to get an API token.
    Use this token in subsequent requests: Authorization: Token <token>
    """
    from django.contrib.auth import authenticate
    from .serializers import UserSerializer
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Get or create token
    token, created = Token.objects.get_or_create(user=user)
    user_serializer = UserSerializer(user)
    
    return Response({
        'token': token.key,
        'user': user_serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def revoke_token(request):
    """
    Revoke current user's API token
    
    Deletes the token, requiring re-authentication for token-based requests.
    """
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'message': 'Token revoked successfully'}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({'message': 'No token found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])  # Public endpoint - anyone can view profiles
def user_profile(request, username):
    """
    Get user profile by username
    
    Returns public profile information for a user.
    """
    from .serializers import UserProfileSerializer
    
    try:
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except UserProfile.DoesNotExist:
        # Return basic user info if profile doesn't exist
        from .serializers import UserSerializer
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_profile(request, username):
    """
    Update user profile
    
    Allows users to update their own profile information.
    """
    from .serializers import UserProfileSerializer
    
    if request.user.username != username:
        return Response(
            {'error': 'You can only update your own profile'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        profile = UserProfile.objects.create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])  # Public endpoint for monitoring
def health_check(request):
    """
    Health check endpoint
    
    Returns API health status. Useful for monitoring and load balancers.
    """
    from django.db import connection
    
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return Response({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': timezone.now().isoformat(),
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': timezone.now().isoformat(),
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Recipe CRUD operations
    
    - list: Get all published recipes (authors can see their own unpublished)
    - retrieve: Get a single recipe with statistics (authors can see their own unpublished)
    - create: Create a new recipe (authenticated users only)
    - update: Update a recipe (author or staff only)
    - destroy: Delete a recipe (author or staff only)
    
    Authentication: Session, Token, or JWT
    """
    queryset = Recipe.objects.all().select_related('author', 'category')
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
        """
        Filter recipes based on user permissions and query parameters
        
        - Published recipes are visible to everyone
        - Authors can see their own unpublished recipes
        - Supports filtering by category, search, author, ingredients, time, dietary restrictions
        - Supports sorting by newest, oldest, rating, views, title
        """
        from django.db.models import F
        
        # Base queryset
        if self.request.user.is_authenticated:
            # Authenticated users can see published recipes + their own unpublished
            queryset = Recipe.objects.filter(
                Q(is_published=True) | Q(author=self.request.user)
            )
        else:
            # Anonymous users can only see published recipes
            queryset = Recipe.objects.filter(is_published=True)
        
        queryset = queryset.select_related('author', 'category').prefetch_related(
            'recipe_ingredients__ingredient',
            'ratings',
            'comments',
            'favorites',
            'images'
        )

        # Filter by category
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Search by title or description
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(instructions__icontains=search_query)
            )

        # Filter by author username
        author_username = self.request.query_params.get('author_username', None)
        if author_username:
            queryset = queryset.filter(author__username=author_username)

        # Filter by ingredients
        ingredients_query = self.request.query_params.get('ingredients', None)
        if ingredients_query:
            ingredients_list = [i.strip() for i in ingredients_query.split(',') if i.strip()]
            if ingredients_list:
                queryset = queryset.filter(ingredients__name__in=ingredients_list).distinct()

        # Filter by prep/cook/total time
        max_prep_time = self.request.query_params.get('max_prep_time', None)
        if max_prep_time and max_prep_time.isdigit():
            queryset = queryset.filter(prep_time__lte=int(max_prep_time))

        max_cook_time = self.request.query_params.get('max_cook_time', None)
        if max_cook_time and max_cook_time.isdigit():
            queryset = queryset.filter(cook_time__lte=int(max_cook_time))

        max_total_time = self.request.query_params.get('max_total_time', None)
        if max_total_time and max_total_time.isdigit():
            queryset = queryset.annotate(total_time_calc=F('prep_time') + F('cook_time')).filter(total_time_calc__lte=int(max_total_time))

        # Filter by dietary restrictions
        dietary_filter = self.request.query_params.get('dietary', None)
        if dietary_filter and dietary_filter != 'all':
            queryset = queryset.filter(dietary_restrictions=dietary_filter)

        # Sorting
        sort_by = self.request.query_params.get('sort', '-created_at')
        if sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort_by == 'rating':
            queryset = queryset.annotate(avg_rating=Avg('ratings__stars')).order_by('-avg_rating', '-created_at')
        elif sort_by == 'views':
            queryset = queryset.order_by('-view_count', '-created_at')
        elif sort_by == 'title':
            queryset = queryset.order_by('title')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def retrieve(self, request, *args, **kwargs):
        """Get a single recipe with statistics"""
        instance = self.get_object()
        
        # Increment view count
        if request.user.is_authenticated and request.user != instance.author:
            instance.increment_view_count()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Set author to current user when creating recipe"""
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new recipe
        
        Handles FormData with nested ingredients_data and images_data.
        """
        # Handle ingredients_data from FormData
        if 'ingredients_data' in request.data:
            ingredients_data = request.data['ingredients_data']
            if isinstance(ingredients_data, str):
                import json
                try:
                    request.data._mutable = True
                    request.data['ingredients_data'] = json.loads(ingredients_data)
                    request.data._mutable = False
                except (json.JSONDecodeError, ValueError):
                    request.data._mutable = True
                    request.data['ingredients_data'] = []
                    request.data._mutable = False
        else:
            request.data._mutable = True
            request.data['ingredients_data'] = []
            request.data._mutable = False
        
        # Handle images_data from FormData
        if 'images_data' in request.data:
            images_data = request.data['images_data']
            if isinstance(images_data, str):
                import json
                try:
                    request.data._mutable = True
                    request.data['images_data'] = json.loads(images_data)
                    request.data._mutable = False
                except (json.JSONDecodeError, ValueError):
                    request.data._mutable = True
                    request.data['images_data'] = []
                    request.data._mutable = False
        else:
            request.data._mutable = True
            request.data['images_data'] = []
            request.data._mutable = False
        
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update a recipe
        
        Handles FormData with nested ingredients_data and images_data.
        """
        # Handle ingredients_data from FormData
        if 'ingredients_data' in request.data:
            ingredients_data = request.data['ingredients_data']
            if isinstance(ingredients_data, str):
                import json
                try:
                    request.data._mutable = True
                    request.data['ingredients_data'] = json.loads(ingredients_data)
                    request.data._mutable = False
                except (json.JSONDecodeError, ValueError):
                    request.data._mutable = True
                    request.data['ingredients_data'] = []
                    request.data._mutable = False
        
        # Handle images_data from FormData
        if 'images_data' in request.data:
            images_data = request.data['images_data']
            if isinstance(images_data, str):
                import json
                try:
                    request.data._mutable = True
                    request.data['images_data'] = json.loads(images_data)
                    request.data._mutable = False
                except (json.JSONDecodeError, ValueError):
                    request.data._mutable = True
                    request.data['images_data'] = []
                    request.data._mutable = False
        
        return super().update(request, *args, **kwargs)

    def get_object(self):
        """Get recipe object, allowing authors to see unpublished recipes"""
        obj = super().get_object()
        
        # Check if user can view this recipe
        if not obj.is_published and obj.author != self.request.user:
            if not self.request.user.is_staff:
                raise NotFound("Recipe not found or not published")
        
        return obj

    def check_permissions(self, request):
        """Check if user has permission for this action"""
        if self.action in ['update', 'partial_update', 'destroy']:
            obj = self.get_object()
            if obj.author != request.user and not request.user.is_staff:
                self.permission_denied(
                    request,
                    message="You can only modify your own recipes."
                )
        super().check_permissions(request)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def increment_view(self, request, pk=None):
        """Increment view count for a recipe"""
        recipe = self.get_object()
        recipe.increment_view_count()
        return Response({'view_count': recipe.view_count})
    
    @action(detail=False, methods=['get'], url_path='search', permission_classes=[AllowAny])
    def search(self, request):
        """
        Search recipes with filters
        
        Query parameters:
        - search: Text search in title, description, instructions
        - category: Category ID
        - author_username: Filter by author username
        - ingredients: Comma-separated ingredient names
        - max_prep_time: Maximum preparation time in minutes
        - max_cook_time: Maximum cooking time in minutes
        - max_total_time: Maximum total time in minutes
        - dietary: Dietary restriction filter
        - sort: Sort order (newest, oldest, rating, views, title)
        - page: Page number for pagination
        """
        # Use the existing get_queryset logic
        queryset = self.get_queryset()
        
        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='by-ingredients', permission_classes=[AllowAny])
    def by_ingredients(self, request):
        """
        Search recipes by ingredients
        
        Query parameters:
        - ingredients: Comma-separated list of ingredient names (required)
        - match_all: If 'true', recipe must contain ALL ingredients; if 'false' (default), recipe must contain ANY ingredient
        """
        ingredients_query = request.query_params.get('ingredients', None)
        match_all = request.query_params.get('match_all', 'false').lower() == 'true'
        
        if not ingredients_query:
            return Response(
                {'error': 'ingredients parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ingredients_list = [i.strip() for i in ingredients_query.split(',') if i.strip()]
        
        if not ingredients_list:
            return Response(
                {'error': 'At least one ingredient is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Base queryset
        if request.user.is_authenticated:
            queryset = Recipe.objects.filter(
                Q(is_published=True) | Q(author=request.user)
            )
        else:
            queryset = Recipe.objects.filter(is_published=True)
        
        queryset = queryset.select_related('author', 'category').prefetch_related(
            'recipe_ingredients__ingredient',
            'ratings',
            'comments',
            'favorites',
            'images'
        )
        
        if match_all:
            # Recipe must contain ALL specified ingredients
            for ingredient_name in ingredients_list:
                queryset = queryset.filter(ingredients__name__iexact=ingredient_name)
            queryset = queryset.distinct()
        else:
            # Recipe must contain ANY of the specified ingredients
            queryset = queryset.filter(ingredients__name__in=ingredients_list).distinct()
        
        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='export', permission_classes=[AllowAny])
    def export(self, request):
        """
        Export recipes in multiple formats for meal planner apps
        
        Query parameters:
        - format: Export format ('json', 'csv', 'recipeml', 'xml') - default: 'json'
        - category: Filter by category ID
        - author_username: Filter by author username
        - search: Text search
        - ingredients: Comma-separated ingredient names
        """
        import csv
        import json
        import xml.etree.ElementTree as ET
        from django.http import HttpResponse
        from io import StringIO
        
        format_type = request.query_params.get('format', 'json').lower()
        
        # Get filtered queryset
        queryset = self.get_queryset()
        
        if format_type == 'csv':
            # CSV Export
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="recipes.csv"'
            
            writer = csv.writer(response)
            # Write header
            writer.writerow([
                'ID', 'Title', 'Description', 'Author', 'Category', 
                'Prep Time (min)', 'Cook Time (min)', 'Total Time (min)',
                'Dietary Restrictions', 'View Count', 'Average Rating', 
                'Rating Count', 'Favorite Count', 'Comment Count',
                'Created At', 'Updated At'
            ])
            
            # Write data
            for recipe in queryset:
                writer.writerow([
                    recipe.id,
                    recipe.title,
                    recipe.description[:200] if recipe.description else '',  # Truncate long descriptions
                    recipe.author.username if recipe.author else '',
                    recipe.category.name if recipe.category else '',
                    recipe.prep_time,
                    recipe.cook_time,
                    recipe.total_time,
                    recipe.get_dietary_restrictions_display() if recipe.dietary_restrictions else '',
                    recipe.view_count,
                    recipe.average_rating,
                    recipe.rating_count,
                    recipe.favorites.count(),
                    recipe.comments.count(),
                    recipe.created_at.isoformat() if recipe.created_at else '',
                    recipe.updated_at.isoformat() if recipe.updated_at else '',
                ])
            
            return response
        
        elif format_type in ['recipeml', 'xml']:
            # RecipeML XML Export (standard format for meal planner apps)
            root = ET.Element('recipeml', version='0.5')
            recipe_collection = ET.SubElement(root, 'recipe')
            
            for recipe in queryset:
                recipe_elem = ET.SubElement(recipe_collection, 'recipe')
                
                # Recipe metadata
                head = ET.SubElement(recipe_elem, 'head')
                title_elem = ET.SubElement(head, 'title')
                title_elem.text = recipe.title
                
                if recipe.description:
                    description_elem = ET.SubElement(head, 'description')
                    description_elem.text = recipe.description
                
                # Categories
                if recipe.category:
                    categories = ET.SubElement(head, 'categories')
                    cat = ET.SubElement(categories, 'cat')
                    cat.text = recipe.category.name
                
                # Timing
                if recipe.prep_time or recipe.cook_time:
                    times = ET.SubElement(head, 'times')
                    if recipe.prep_time:
                        prep = ET.SubElement(times, 'prep')
                        prep.text = f"PT{recipe.prep_time}M"  # ISO 8601 duration format
                    if recipe.cook_time:
                        cook = ET.SubElement(times, 'cook')
                        cook.text = f"PT{recipe.cook_time}M"
                    if recipe.total_time:
                        total = ET.SubElement(times, 'total')
                        total.text = f"PT{recipe.total_time}M"
                
                # Ingredients
                ingredients = ET.SubElement(recipe_elem, 'ingredients')
                ingredient_list = ET.SubElement(ingredients, 'ing')
                
                for ri in recipe.recipe_ingredients.all():
                    item = ET.SubElement(ingredient_list, 'item')
                    if ri.quantity:
                        amt = ET.SubElement(item, 'amt')
                        qty = ET.SubElement(amt, 'qty')
                        qty.text = str(ri.quantity)
                        if ri.unit:
                            unit = ET.SubElement(amt, 'unit')
                            unit.text = ri.unit
                    if ri.ingredient:
                        ing_name = ET.SubElement(item, 'item')
                        ing_name.text = ri.ingredient.name
                    if ri.notes:
                        prep_note = ET.SubElement(item, 'prep')
                        prep_note.text = ri.notes
                
                # Directions
                directions = ET.SubElement(recipe_elem, 'directions')
                step_list = ET.SubElement(directions, 'step')
                
                # Parse instructions (assuming JSON format)
                try:
                    if recipe.instructions:
                        import json as json_lib
                        instructions_data = json_lib.loads(recipe.instructions)
                        if isinstance(instructions_data, list):
                            for idx, step in enumerate(instructions_data, 1):
                                step_elem = ET.SubElement(step_list, 'step')
                                step_elem.set('number', str(idx))
                                if isinstance(step, dict) and 'text' in step:
                                    step_elem.text = step['text']
                                elif isinstance(step, str):
                                    step_elem.text = step
                        else:
                            # Fallback: treat as plain text
                            step_elem = ET.SubElement(step_list, 'step')
                            step_elem.text = recipe.instructions
                except:
                    # Fallback: treat as plain text
                    step_elem = ET.SubElement(step_list, 'step')
                    step_elem.text = recipe.instructions or ''
            
            # Convert to XML string
            xml_str = ET.tostring(root, encoding='unicode', method='xml')
            
            response = HttpResponse(xml_str, content_type='application/xml')
            response['Content-Disposition'] = 'attachment; filename="recipes.recipeml"'
            return response
        
        else:  # JSON export (default)
            serializer = self.get_serializer(queryset, many=True)
            response = Response(serializer.data)
            response['Content-Disposition'] = 'attachment; filename="recipes.json"'
            response['Content-Type'] = 'application/json'
            return response
    
    @action(detail=True, methods=['get'], url_path='export-meal-planner', permission_classes=[AllowAny])
    def export_meal_planner(self, request, pk=None):
        """
        Export a single recipe in meal planner compatible format
        
        Query parameters:
        - format: Export format ('json', 'recipeml', 'xml') - default: 'json'
        - app: Target meal planner app ('paprika', 'mealime', 'anylist', 'generic')
        """
        recipe = self.get_object()
        format_type = request.query_params.get('format', 'json').lower()
        app_type = request.query_params.get('app', 'generic').lower()
        
        import json
        import xml.etree.ElementTree as ET
        from django.http import HttpResponse
        
        if format_type in ['recipeml', 'xml']:
            # RecipeML format
            root = ET.Element('recipeml', version='0.5')
            recipe_elem = ET.SubElement(root, 'recipe')
            
            # Recipe metadata
            head = ET.SubElement(recipe_elem, 'head')
            title_elem = ET.SubElement(head, 'title')
            title_elem.text = recipe.title
            
            if recipe.description:
                description_elem = ET.SubElement(head, 'description')
                description_elem.text = recipe.description
            
            # Categories
            if recipe.category:
                categories = ET.SubElement(head, 'categories')
                cat = ET.SubElement(categories, 'cat')
                cat.text = recipe.category.name
            
            # Timing
            if recipe.prep_time or recipe.cook_time:
                times = ET.SubElement(head, 'times')
                if recipe.prep_time:
                    prep = ET.SubElement(times, 'prep')
                    prep.text = f"PT{recipe.prep_time}M"
                if recipe.cook_time:
                    cook = ET.SubElement(times, 'cook')
                    cook.text = f"PT{recipe.cook_time}M"
            
            # Ingredients
            ingredients = ET.SubElement(recipe_elem, 'ingredients')
            ingredient_list = ET.SubElement(ingredients, 'ing')
            
            for ri in recipe.recipe_ingredients.all():
                item = ET.SubElement(ingredient_list, 'item')
                if ri.quantity:
                    amt = ET.SubElement(item, 'amt')
                    qty = ET.SubElement(amt, 'qty')
                    qty.text = str(ri.quantity)
                    if ri.unit:
                        unit = ET.SubElement(amt, 'unit')
                        unit.text = ri.unit
                if ri.ingredient:
                    ing_name = ET.SubElement(item, 'item')
                    ing_name.text = ri.ingredient.name
            
            # Directions
            directions = ET.SubElement(recipe_elem, 'directions')
            step_list = ET.SubElement(directions, 'step')
            
            try:
                if recipe.instructions:
                    instructions_data = json.loads(recipe.instructions)
                    if isinstance(instructions_data, list):
                        for idx, step in enumerate(instructions_data, 1):
                            step_elem = ET.SubElement(step_list, 'step')
                            step_elem.set('number', str(idx))
                            if isinstance(step, dict) and 'text' in step:
                                step_elem.text = step['text']
                            elif isinstance(step, str):
                                step_elem.text = step
            except:
                step_elem = ET.SubElement(step_list, 'step')
                step_elem.text = recipe.instructions or ''
            
            xml_str = ET.tostring(root, encoding='unicode', method='xml')
            response = HttpResponse(xml_str, content_type='application/xml')
            response['Content-Disposition'] = f'attachment; filename="{recipe.title.replace(" ", "_")}.recipeml"'
            return response
        
        else:  # JSON format (with app-specific formatting)
            serializer = RecipeSerializer(recipe, context={'request': request})
            data = serializer.data
            
            # Format for specific apps if requested
            if app_type == 'paprika':
                # Paprika Recipe Manager format
                data = {
                    'name': recipe.title,
                    'description': recipe.description,
                    'prep_time': recipe.prep_time,
                    'cook_time': recipe.cook_time,
                    'servings': '',  # Not stored in our model
                    'category': recipe.category.name if recipe.category else '',
                    'ingredients': [
                        f"{ri.quantity} {ri.unit} {ri.ingredient.name}".strip()
                        for ri in recipe.recipe_ingredients.all()
                    ],
                    'directions': self._parse_instructions(recipe.instructions),
                    'notes': '',
                    'nutritional_info': '',
                    'image_url': request.build_absolute_uri(recipe.image.url) if recipe.image else '',
                }
            elif app_type == 'mealime':
                # Mealime format
                data = {
                    'title': recipe.title,
                    'description': recipe.description,
                    'prep_time_minutes': recipe.prep_time,
                    'cook_time_minutes': recipe.cook_time,
                    'ingredients': [
                        {
                            'name': ri.ingredient.name,
                            'amount': ri.quantity,
                            'unit': ri.unit,
                        }
                        for ri in recipe.recipe_ingredients.all()
                    ],
                    'instructions': self._parse_instructions(recipe.instructions),
                }
            
            response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename="{recipe.title.replace(" ", "_")}.json"'
            return response
    
    def _parse_instructions(self, instructions):
        """Parse instructions JSON into list of strings"""
        if not instructions:
            return []
        try:
            import json
            data = json.loads(instructions)
            if isinstance(data, list):
                return [step.get('text', step) if isinstance(step, dict) else str(step) for step in data]
            return [instructions]
        except:
            return [instructions] if instructions else []


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Ingredient read operations
    
    - list: Get all ingredients
    - retrieve: Get a single ingredient
    
    Read-only endpoint for browsing available ingredients.
    """
    queryset = Ingredient.objects.all().order_by('name')
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]  # Public read access
    
    def get_queryset(self):
        """Filter ingredients by search query"""
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset


class RatingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Rating operations
    
    - list: Get ratings (filter by recipe or user)
    - create: Create a new rating
    - update: Update a rating
    - destroy: Delete a rating
    
    Authentication: Session, Token, or JWT
    """
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Rating.objects.select_related('user', 'recipe')
        recipe_id = self.request.query_params.get('recipe', None)
        user_id = self.request.query_params.get('user', None)
        
        if recipe_id:
            queryset = queryset.filter(recipe_id=recipe_id)
        elif user_id:
            queryset = queryset.filter(user_id=user_id)
        elif self.request.user.is_authenticated and self.request.query_params.get('mine') == 'true':
            queryset = queryset.filter(user=self.request.user)
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        """Set user to current user when creating rating"""
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """Allow public read access, require auth for write operations"""
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def check_permissions(self, request):
        """Check if user has permission for this action"""
        if self.action in ['update', 'partial_update', 'destroy']:
            obj = self.get_object()
            if obj.user != request.user and not request.user.is_staff:
                self.permission_denied(
                    request,
                    message="You can only modify your own ratings."
                )
        super().check_permissions(request)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment operations
    
    - list: Get comments (filter by recipe or user)
    - create: Create a new comment
    - update: Update a comment
    - destroy: Delete a comment
    
    Authentication: Session, Token, or JWT
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.select_related('user', 'recipe')
        recipe_id = self.request.query_params.get('recipe', None)
        user_id = self.request.query_params.get('user', None)
        
        if recipe_id:
            queryset = queryset.filter(recipe_id=recipe_id)
        elif user_id:
            queryset = queryset.filter(user_id=user_id)
        elif self.request.user.is_authenticated and self.request.query_params.get('mine') == 'true':
            queryset = queryset.filter(user=self.request.user)
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        """Set user to current user when creating comment"""
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """Allow public read access, require auth for write operations"""
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def check_permissions(self, request):
        """Check if user has permission for this action"""
        if self.action in ['update', 'partial_update', 'destroy']:
            obj = self.get_object()
            if obj.user != request.user and not request.user.is_staff:
                self.permission_denied(
                    request,
                    message="You can only modify your own comments."
                )
        super().check_permissions(request)


class FavoriteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Favorite operations
    
    - list: Get user's favorites
    - create: Toggle favorite (create if not exists, delete if exists)
    - destroy: Remove favorite
    
    Authentication: Session, Token, or JWT
    """
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get current user's favorites"""
        return Favorite.objects.filter(user=self.request.user).select_related('recipe', 'user')

    def create(self, request, *args, **kwargs):
        """Toggle favorite - create if not exists, delete if exists"""
        recipe_id = request.data.get('recipe')
        
        if not recipe_id:
            return Response(
                {'error': 'Recipe ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
        except Recipe.DoesNotExist:
            return Response(
                {'error': 'Recipe not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        
        if not created:
            # Already exists, delete it (toggle off)
            favorite.delete()
            is_favorited = False
        else:
            is_favorited = True
        
        # Get updated favorite count
        favorite_count = Favorite.objects.filter(recipe=recipe).count()
        
        return Response({
            'is_favorited': is_favorited,
            'favorite_count': favorite_count
        }, status=status.HTTP_200_OK if created else status.HTTP_200_OK)


class MealPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for MealPlan operations
    
    - list: Get all meal plans for the current user, with optional date range filtering
    - create: Add a recipe to the meal plan
    - retrieve: Get a specific meal plan entry
    - update: Update a meal plan entry
    - destroy: Remove a meal plan entry
    - grocery-list: Generate grocery list from meal plans
    - export_ical: Export meal plans as an iCal file
    
    Authentication: Session, Token, or JWT
    """
    serializer_class = MealPlanSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter meal plans by current user and optional date range"""
        queryset = MealPlan.objects.filter(user=self.request.user).select_related('recipe', 'user').order_by('date', 'meal_type')
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            try:
                from datetime import datetime
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                from datetime import datetime
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__lte=end_date)
            except ValueError:
                pass
        
        # Filter by meal type if provided
        meal_type = self.request.query_params.get('meal_type', None)
        if meal_type:
            queryset = queryset.filter(meal_type=meal_type)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set user to current user"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'], url_path='export/ical')
    def export_ical(self, request):
        """Export meal plans as iCal format"""
        from django.http import HttpResponse
        from datetime import datetime
        
        queryset = self.get_queryset()
        
        # Generate iCal content
        ical_content = [
            'BEGIN:VCALENDAR',
            'VERSION:2.0',
            'PRODID:-//Recipe Sharing Platform//Meal Plans//EN',
            'CALSCALE:GREGORIAN',
            'METHOD:PUBLISH',
        ]
        
        for meal_plan in queryset:
            # Format date for iCal (YYYYMMDD)
            date_str = meal_plan.date.strftime('%Y%m%d')
            
            # Create event
            ical_content.extend([
                'BEGIN:VEVENT',
                f'UID:mealplan-{meal_plan.id}@recipesharing.com',
                f'DTSTART;VALUE=DATE:{date_str}',
                f'DTEND;VALUE=DATE:{date_str}',
                f'SUMMARY:{meal_plan.recipe.title} - {meal_plan.get_meal_type_display()}',
                f'DESCRIPTION:{meal_plan.recipe.description[:200]}',
                f'LOCATION:Kitchen',
                f'STATUS:CONFIRMED',
                f'SEQUENCE:0',
                'END:VEVENT',
            ])
        
        ical_content.append('END:VCALENDAR')
        
        response = HttpResponse('\r\n'.join(ical_content), content_type='text/calendar')
        response['Content-Disposition'] = 'attachment; filename="meal-plans.ics"'
        return response
    
    @action(detail=False, methods=['get'], url_path='grocery-list')
    def grocery_list(self, request):
        """
        Generate grocery list from meal plans
        
        Query parameters:
        - start_date: Start date (YYYY-MM-DD)
        - end_date: End date (YYYY-MM-DD)
        - format: Response format (json, text, pdf) - default: json
        """
        from .grocery_list import generate_grocery_list
        from datetime import datetime
        
        queryset = self.get_queryset()
        
        # Get date range from query params
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        format_type = request.query_params.get('format', 'json').lower()
        
        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=start_date)
            except ValueError:
                pass
        
        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                queryset = queryset.filter(date__lte=end_date)
            except ValueError:
                pass
        
        meal_plans = list(queryset)
        
        if not meal_plans:
            return Response({
                'error': 'No meal plans found for the specified date range',
                'ingredients_by_category': {},
                'total_items': 0,
                'date_range': {
                    'start': start_date_str,
                    'end': end_date_str,
                },
                'meal_plans_count': 0,
            }, status=status.HTTP_200_OK)
        
        # Generate grocery list
        grocery_data = generate_grocery_list(meal_plans)
        
        # Return in requested format
        if format_type == 'text':
            return self._grocery_list_text(grocery_data)
        elif format_type == 'pdf':
            return self._grocery_list_pdf(grocery_data)
        else:  # json (default)
            return Response(grocery_data, status=status.HTTP_200_OK)
    
    def _grocery_list_text(self, grocery_data):
        """Generate plain text grocery list"""
        from django.http import HttpResponse
        
        lines = []
        lines.append("=" * 60)
        lines.append("GROCERY LIST")
        lines.append("=" * 60)
        lines.append("")
        
        if grocery_data['date_range']['start']:
            lines.append(f"Date Range: {grocery_data['date_range']['start']} to {grocery_data['date_range']['end']}")
            lines.append("")
        
        lines.append(f"Total Items: {grocery_data['total_items']}")
        lines.append(f"Meal Plans: {grocery_data['meal_plans_count']}")
        lines.append("")
        lines.append("=" * 60)
        lines.append("")
        
        for category, items in grocery_data['ingredients_by_category'].items():
            if not items:
                continue
            
            lines.append(f"\n{category.upper()}")
            lines.append("-" * 60)
            
            for item in items:
                quantity_str = f"{item['total_quantity']:.2f}".rstrip('0').rstrip('.')
                unit_str = f" {item['unit']}" if item['unit'] else ""
                name_str = item['name']
                
                line = f"  • {quantity_str}{unit_str} {name_str}"
                
                if item['notes']:
                    notes_str = ", ".join(item['notes'])
                    line += f" ({notes_str})"
                
                lines.append(line)
            
            lines.append("")
        
        text_content = "\n".join(lines)
        
        response = HttpResponse(text_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="grocery-list.txt"'
        return response
    
    def _grocery_list_pdf(self, grocery_data):
        """Generate PDF grocery list"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.units import inch
            from io import BytesIO
            from django.http import HttpResponse
        except ImportError:
            return Response({
                'error': 'PDF generation requires reportlab library. Install with: pip install reportlab'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12,
            alignment=1,  # Center
        )
        category_style = ParagraphStyle(
            'CategoryStyle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#555555'),
            spaceAfter=6,
            spaceBefore=12,
        )
        
        story = []
        
        # Title
        story.append(Paragraph("GROCERY LIST", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Date range and summary
        if grocery_data['date_range']['start']:
            date_text = f"Date Range: {grocery_data['date_range']['start']} to {grocery_data['date_range']['end']}"
            story.append(Paragraph(date_text, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        summary_text = f"Total Items: {grocery_data['total_items']} | Meal Plans: {grocery_data['meal_plans_count']}"
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Ingredients by category
        for category, items in grocery_data['ingredients_by_category'].items():
            if not items:
                continue
            
            story.append(Paragraph(category.upper(), category_style))
            
            # Create table for items
            table_data = [['Quantity', 'Ingredient', 'Notes']]
            
            for item in items:
                quantity_str = f"{item['total_quantity']:.2f}".rstrip('0').rstrip('.')
                unit_str = f" {item['unit']}" if item['unit'] else ""
                quantity = f"{quantity_str}{unit_str}"
                name = item['name']
                notes = ", ".join(item['notes']) if item['notes'] else ""
                
                table_data.append([quantity, name, notes])
            
            table = Table(table_data, colWidths=[1.5*inch, 3.5*inch, 2*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            
            story.append(table)
            story.append(Spacer(1, 0.2*inch))
        
        doc.build(story)
        
        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="grocery-list.pdf"'
        return response


class APIKeyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing API keys for meal planner apps
    
    Allows users to create, list, update, and delete API keys
    for integrating meal planner apps with the Recipe Sharing Platform.
    """
    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only API keys for the current user"""
        return APIKey.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set user when creating API key"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def regenerate(self, request, pk=None):
        """Regenerate API key (creates new key, deactivates old one)"""
        api_key = self.get_object()
        api_key.is_active = False
        api_key.save()
        
        # Create new API key with same name
        new_key = APIKey.objects.create(
            name=api_key.name,
            user=request.user,
            expires_at=api_key.expires_at
        )
        
        serializer = self.get_serializer(new_key)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle API key active status"""
        api_key = self.get_object()
        api_key.is_active = not api_key.is_active
        api_key.save()
        
        serializer = self.get_serializer(api_key)
        return Response(serializer.data)
