"""
Django Admin Configuration for Recipes App
"""

from django.contrib import admin
from .models import Recipe, Category, Ingredient, RecipeIngredient


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    fields = ['ingredient', 'quantity', 'unit', 'notes']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'prep_time', 'cook_time', 'is_published', 'created_at']
    list_filter = ['category', 'is_published', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [RecipeIngredientInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'instructions', 'image')
        }),
        ('Timing', {
            'fields': ('prep_time', 'cook_time')
        }),
        ('Categorization', {
            'fields': ('category',)
        }),
        ('Metadata', {
            'fields': ('author', 'is_published', 'created_at', 'updated_at')
        }),
    )
