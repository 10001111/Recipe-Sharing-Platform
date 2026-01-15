"""
Django Admin Configuration for Recipes App

Enhanced admin interface with:
- Better list displays with computed fields
- Inline editing for related models
- Advanced filters and search
- Bulk actions
"""

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from .models import Recipe, Category, Ingredient, RecipeIngredient, Rating, Comment, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model"""
    list_display = ['name', 'slug', 'recipe_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        """Optimize queryset with recipe count"""
        qs = super().get_queryset(request)
        return qs.annotate(recipe_count=Count('recipes'))
    
    def recipe_count(self, obj):
        """Display recipe count for category"""
        return obj.recipe_count
    recipe_count.short_description = 'Recipes'
    recipe_count.admin_order_field = 'recipe_count'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Admin interface for Ingredient model"""
    list_display = ['name', 'recipe_count']
    search_fields = ['name']
    
    def get_queryset(self, request):
        """Optimize queryset with recipe count"""
        qs = super().get_queryset(request)
        return qs.annotate(recipe_count=Count('recipes'))
    
    def recipe_count(self, obj):
        """Display recipe count for ingredient"""
        return obj.recipe_count
    recipe_count.short_description = 'Used in Recipes'
    recipe_count.admin_order_field = 'recipe_count'


class RecipeIngredientInline(admin.TabularInline):
    """Inline editing for RecipeIngredients"""
    model = RecipeIngredient
    extra = 1
    fields = ['ingredient', 'quantity', 'unit', 'notes']
    autocomplete_fields = ['ingredient']


class RatingInline(admin.TabularInline):
    """Inline editing for Ratings"""
    model = Rating
    extra = 0
    fields = ['user', 'stars', 'review_text', 'created_at']
    readonly_fields = ['created_at']
    can_delete = True


class CommentInline(admin.TabularInline):
    """Inline editing for Comments"""
    model = Comment
    extra = 0
    fields = ['user', 'text', 'created_at']
    readonly_fields = ['created_at']
    can_delete = True


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin interface for Recipe model"""
    list_display = [
        'title', 'author', 'category', 'prep_time', 'cook_time',
        'total_time_display', 'view_count', 'rating_display',
        'comment_count', 'favorite_count', 'is_published', 'created_at'
    ]
    list_filter = ['category', 'is_published', 'created_at', 'author']
    search_fields = ['title', 'description', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'view_count', 'rating_display']
    inlines = [RecipeIngredientInline, RatingInline, CommentInline]
    autocomplete_fields = ['author', 'category']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'instructions', 'image')
        }),
        ('Timing', {
            'fields': ('prep_time', 'cook_time', 'total_time_display')
        }),
        ('Categorization', {
            'fields': ('category',)
        }),
        ('Statistics', {
            'fields': ('view_count', 'rating_display', 'comment_count', 'favorite_count')
        }),
        ('Metadata', {
            'fields': ('author', 'is_published', 'created_at', 'updated_at')
        }),
    )
    
    actions = ['publish_recipes', 'unpublish_recipes']
    
    def get_queryset(self, request):
        """Optimize queryset with annotations"""
        qs = super().get_queryset(request)
        return qs.select_related('author', 'category').prefetch_related(
            'ratings', 'comments', 'favorites'
        ).annotate(
            comment_count=Count('comments'),
            favorite_count=Count('favorites')
        )
    
    def total_time_display(self, obj):
        """Display total time"""
        return f"{obj.total_time} min"
    total_time_display.short_description = 'Total Time'
    total_time_display.admin_order_field = 'prep_time'
    
    def rating_display(self, obj):
        """Display rating with stars"""
        avg_rating = obj.average_rating
        count = obj.rating_count
        if avg_rating > 0:
            stars = '⭐' * int(avg_rating)
            return format_html(
                '{} ({:.1f}) - {} reviews',
                stars, avg_rating, count
            )
        return 'No ratings yet'
    rating_display.short_description = 'Rating'
    
    def comment_count(self, obj):
        """Display comment count"""
        return obj.comment_count
    comment_count.short_description = 'Comments'
    comment_count.admin_order_field = 'comment_count'
    
    def favorite_count(self, obj):
        """Display favorite count"""
        return obj.favorite_count
    favorite_count.short_description = 'Favorites'
    favorite_count.admin_order_field = 'favorite_count'
    
    def publish_recipes(self, request, queryset):
        """Bulk action to publish recipes"""
        count = queryset.update(is_published=True)
        self.message_user(request, f'{count} recipes published.')
    publish_recipes.short_description = 'Publish selected recipes'
    
    def unpublish_recipes(self, request, queryset):
        """Bulk action to unpublish recipes"""
        count = queryset.update(is_published=False)
        self.message_user(request, f'{count} recipes unpublished.')
    unpublish_recipes.short_description = 'Unpublish selected recipes'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Admin interface for Rating model"""
    list_display = ['recipe', 'user', 'stars_display', 'has_review', 'created_at']
    list_filter = ['stars', 'created_at']
    search_fields = ['recipe__title', 'user__username', 'review_text']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['recipe', 'user']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Rating Information', {
            'fields': ('recipe', 'user', 'stars', 'review_text')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def stars_display(self, obj):
        """Display stars visually"""
        return '⭐' * obj.stars
    stars_display.short_description = 'Rating'
    stars_display.admin_order_field = 'stars'
    
    def has_review(self, obj):
        """Check if rating has review text"""
        return 'Yes' if obj.review_text else 'No'
    has_review.short_description = 'Has Review'
    has_review.boolean = True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model"""
    list_display = ['recipe', 'user', 'text_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['recipe__title', 'user__username', 'text']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['recipe', 'user']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('recipe', 'user', 'text')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def text_preview(self, obj):
        """Show preview of comment text"""
        if len(obj.text) > 50:
            return obj.text[:50] + '...'
        return obj.text
    text_preview.short_description = 'Comment'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Admin interface for Favorite model"""
    list_display = ['recipe', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['recipe__title', 'user__username']
    readonly_fields = ['created_at']
    autocomplete_fields = ['recipe', 'user']
    date_hierarchy = 'created_at'
