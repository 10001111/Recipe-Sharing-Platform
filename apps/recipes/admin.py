"""
Django Admin Configuration for Recipes App
"""

from django.contrib import admin
from .models import Recipe, Category, Ingredient, RecipeIngredient, Rating, Comment, Favorite


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
    list_display = ['title', 'author', 'category', 'prep_time', 'cook_time', 'view_count', 'average_rating', 'is_published', 'created_at']
    list_filter = ['category', 'is_published', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'view_count']
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
        ('Statistics', {
            'fields': ('view_count',)
        }),
        ('Metadata', {
            'fields': ('author', 'is_published', 'created_at', 'updated_at')
        }),
    )


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user', 'stars', 'created_at']
    list_filter = ['stars', 'created_at']
    search_fields = ['recipe__title', 'user__username', 'review_text']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Rating Information', {
            'fields': ('recipe', 'user', 'stars', 'review_text')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['recipe__title', 'user__username', 'text']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Comment Information', {
            'fields': ('recipe', 'user', 'text')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['recipe__title', 'user__username']
    readonly_fields = ['created_at']
