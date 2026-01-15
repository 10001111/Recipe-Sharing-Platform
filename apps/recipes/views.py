"""
Views for Recipe Management

CRUD operations for recipes
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Recipe, Category, Ingredient, RecipeIngredient, Rating, Comment, Favorite
from .forms import RecipeForm, RecipeIngredientForm, RatingForm, CommentForm


class RecipeListView(ListView):
    """List all published recipes"""
    model = Recipe
    template_name = 'recipes/list.html'
    context_object_name = 'recipes'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Recipe.objects.filter(is_published=True).select_related('author', 'category')
        
        # Filter by category if provided
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(ingredients__name__icontains=search_query)
            ).distinct()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class RecipeDetailView(DetailView):
    """View a single recipe"""
    model = Recipe
    template_name = 'recipes/detail.html'
    context_object_name = 'recipe'
    
    def get_queryset(self):
        return Recipe.objects.select_related('author', 'category').prefetch_related(
            'recipe_ingredients__ingredient',
            'ratings__user',
            'comments__user',
            'favorites__user'
        )
    
    def get_object(self, queryset=None):
        """Get recipe and increment view count"""
        recipe = super().get_object(queryset)
        # Increment view count (only for published recipes)
        if recipe.is_published:
            recipe.increment_view_count()
        return recipe
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        
        # Check if user can edit/delete
        context['can_edit'] = (
            self.request.user.is_authenticated and
            (recipe.author == self.request.user or self.request.user.is_staff)
        )
        
        # Check if user has favorited this recipe
        context['is_favorited'] = False
        if self.request.user.is_authenticated:
            context['is_favorited'] = recipe.favorites.filter(user=self.request.user).exists()
        
        # Check if user has rated this recipe
        context['user_rating'] = None
        if self.request.user.is_authenticated:
            try:
                context['user_rating'] = recipe.ratings.get(user=self.request.user)
            except:
                pass
        
        # Get recent comments
        context['comments'] = recipe.comments.select_related('user').all()[:10]
        
        # Get ratings summary
        context['ratings'] = recipe.ratings.select_related('user').all()[:10]
        
        return context


@login_required
def recipe_create_view(request):
    """Create a new recipe"""
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            
            # Handle ingredients
            ingredients_json = request.POST.get('ingredients_data', '[]')
            import json
            try:
                ingredients_list = json.loads(ingredients_json)
                for ing_data in ingredients_list:
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
            except (json.JSONDecodeError, ValueError):
                pass  # Skip invalid ingredient data
            
            messages.success(request, f'Recipe "{recipe.title}" created successfully!')
            return redirect('recipes:detail', pk=recipe.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RecipeForm()
    
    return render(request, 'recipes/form.html', {
        'form': form,
        'title': 'Create Recipe',
        'categories': Category.objects.all()
    })


@login_required
def recipe_edit_view(request, pk):
    """Edit an existing recipe"""
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Check permissions
    if recipe.author != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this recipe.')
        return redirect('recipes:detail', pk=recipe.pk)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        
        if form.is_valid():
            recipe = form.save()
            
            # Handle ingredients - clear existing and add new ones
            RecipeIngredient.objects.filter(recipe=recipe).delete()
            ingredients_json = request.POST.get('ingredients_data', '[]')
            import json
            try:
                ingredients_list = json.loads(ingredients_json)
                for ing_data in ingredients_list:
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
            except (json.JSONDecodeError, ValueError):
                pass  # Skip invalid ingredient data
            
            messages.success(request, f'Recipe "{recipe.title}" updated successfully!')
            return redirect('recipes:detail', pk=recipe.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RecipeForm(instance=recipe)
        # Get existing ingredients for the form
        existing_ingredients = recipe.recipe_ingredients.all()
    
    return render(request, 'recipes/form.html', {
        'form': form,
        'recipe': recipe,
        'title': 'Edit Recipe',
        'categories': Category.objects.all(),
        'existing_ingredients': existing_ingredients if request.method == 'GET' else []
    })


@login_required
def recipe_delete_view(request, pk):
    """Delete a recipe"""
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Check permissions
    if recipe.author != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this recipe.')
        return redirect('recipes:detail', pk=recipe.pk)
    
    if request.method == 'POST':
        title = recipe.title
        recipe.delete()
        messages.success(request, f'Recipe "{title}" deleted successfully.')
        return redirect('recipes:list')
    
    return render(request, 'recipes/delete_confirm.html', {
        'recipe': recipe
    })


def category_detail_view(request, slug):
    """View all recipes in a category"""
    category = get_object_or_404(Category, slug=slug)
    recipes = Recipe.objects.filter(
        category=category,
        is_published=True
    ).select_related('author').order_by('-created_at')
    
    paginator = Paginator(recipes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'recipes/category.html', {
        'category': category,
        'recipes': page_obj,
        'categories': Category.objects.all()
    })


# ========== SOCIAL FEATURES VIEWS ==========

@login_required
@require_POST
def rate_recipe_view(request, pk):
    """Rate or update rating for a recipe"""
    recipe = get_object_or_404(Recipe, pk=pk, is_published=True)
    
    # Get or create rating
    rating, created = Rating.objects.get_or_create(
        recipe=recipe,
        user=request.user,
        defaults={'stars': 0}
    )
    
    # Update rating
    stars = int(request.POST.get('stars', 0))
    review_text = request.POST.get('review_text', '').strip()
    
    if stars < 1 or stars > 5:
        messages.error(request, 'Rating must be between 1 and 5 stars.')
        return redirect('recipes:detail', pk=recipe.pk)
    
    rating.stars = stars
    rating.review_text = review_text[:1000]  # Enforce max length
    rating.save()
    
    if created:
        messages.success(request, 'Thank you for rating this recipe!')
    else:
        messages.success(request, 'Your rating has been updated!')
    
    return redirect('recipes:detail', pk=recipe.pk)


@login_required
@require_POST
def delete_rating_view(request, pk):
    """Delete a user's rating for a recipe"""
    recipe = get_object_or_404(Recipe, pk=pk)
    
    try:
        rating = Rating.objects.get(recipe=recipe, user=request.user)
        rating.delete()
        messages.success(request, 'Your rating has been removed.')
    except Rating.DoesNotExist:
        messages.error(request, 'Rating not found.')
    
    return redirect('recipes:detail', pk=recipe.pk)


@login_required
@require_POST
def add_comment_view(request, pk):
    """Add a comment to a recipe"""
    recipe = get_object_or_404(Recipe, pk=pk, is_published=True)
    
    text = request.POST.get('text', '').strip()
    if not text:
        messages.error(request, 'Comment text cannot be empty.')
        return redirect('recipes:detail', pk=recipe.pk)
    
    if len(text) > 1000:
        messages.error(request, 'Comment is too long (max 1000 characters).')
        return redirect('recipes:detail', pk=recipe.pk)
    
    Comment.objects.create(
        recipe=recipe,
        user=request.user,
        text=text
    )
    
    messages.success(request, 'Your comment has been added!')
    return redirect('recipes:detail', pk=recipe.pk)


@login_required
@require_POST
def delete_comment_view(request, pk, comment_id):
    """Delete a comment"""
    recipe = get_object_or_404(Recipe, pk=pk)
    comment = get_object_or_404(Comment, pk=comment_id, recipe=recipe)
    
    # Check permissions
    if comment.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('recipes:detail', pk=recipe.pk)
    
    comment.delete()
    messages.success(request, 'Comment deleted successfully.')
    return redirect('recipes:detail', pk=recipe.pk)


@login_required
@require_POST
def toggle_favorite_view(request, pk):
    """Toggle favorite status for a recipe"""
    recipe = get_object_or_404(Recipe, pk=pk, is_published=True)
    
    favorite, created = Favorite.objects.get_or_create(
        recipe=recipe,
        user=request.user
    )
    
    if not created:
        # Already favorited, remove it
        favorite.delete()
        messages.success(request, 'Recipe removed from favorites.')
        is_favorited = False
    else:
        messages.success(request, 'Recipe added to favorites!')
        is_favorited = True
    
    # Return JSON response for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'is_favorited': is_favorited,
            'favorite_count': recipe.favorites.count()
        })
    
    return redirect('recipes:detail', pk=recipe.pk)


@login_required
def favorite_recipes_view(request):
    """View user's favorite recipes"""
    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related('recipe', 'recipe__author', 'recipe__category').order_by('-created_at')
    
    recipes = [fav.recipe for fav in favorites if fav.recipe.is_published]
    
    paginator = Paginator(recipes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'recipes/list.html', {
        'recipes': page_obj,
        'title': 'My Favorite Recipes',
        'categories': Category.objects.all()
    })
