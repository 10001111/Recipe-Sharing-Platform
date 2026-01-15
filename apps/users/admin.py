"""
Django Admin Configuration for Users App

Django Admin is a built-in admin interface:
- Automatically creates CRUD interface for models
- Great for managing data during development
- Can be customized to show/hide fields, add filters, etc.

What does this do?
- Registers our models with Django admin
- Customizes how they appear in the admin panel
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.db.models import Count
from .models import UserProfile

User = get_user_model()


class RecipeInline(admin.TabularInline):
    """Inline editing for user's recipes"""
    from apps.recipes.models import Recipe
    model = Recipe
    extra = 0
    fields = ['title', 'category', 'is_published', 'view_count', 'created_at']
    readonly_fields = ['created_at']
    can_delete = False
    show_change_link = True
    fk_name = 'author'  # Specify the ForeignKey field name


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Admin interface for CustomUser model
    
    Extends Django's default UserAdmin to include email field
    """
    # Fields to show in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    # Fields to filter by
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    # Fields to search by
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Ordering
    ordering = ('-date_joined',)
    
    # Fieldsets for add/edit forms
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fieldsets for add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    # Inline editing for user's recipes
    inlines = [RecipeInline]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model
    """
    # Fields to show in the profile list
    list_display = ('user', 'dietary_preferences', 'recipe_count', 'created_at', 'updated_at')
    
    # Fields to filter by
    list_filter = ('dietary_preferences', 'created_at')
    
    # Fields to search by
    search_fields = ('user__username', 'user__email', 'bio')
    
    # Fieldsets - organize fields into sections
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Profile Information', {
            'fields': ('bio', 'avatar', 'dietary_preferences')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Collapsed by default
        }),
    )
    
    # Read-only fields (can't be edited)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        """Optimize queryset with recipe count"""
        qs = super().get_queryset(request)
        return qs.select_related('user').annotate(
            recipe_count=Count('user__recipes')
        )
    
    def recipe_count(self, obj):
        """Display recipe count for user"""
        return obj.recipe_count
    recipe_count.short_description = 'Recipes'
    recipe_count.admin_order_field = 'recipe_count'
