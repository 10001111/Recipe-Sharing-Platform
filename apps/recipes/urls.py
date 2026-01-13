"""
URL Configuration for Recipes App
"""

from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    # Recipe URLs
    path('', views.RecipeListView.as_view(), name='list'),
    path('<int:pk>/', views.RecipeDetailView.as_view(), name='detail'),
    path('create/', views.recipe_create_view, name='create'),
    path('<int:pk>/edit/', views.recipe_edit_view, name='edit'),
    path('<int:pk>/delete/', views.recipe_delete_view, name='delete'),
    
    # Category URLs
    path('category/<slug:slug>/', views.category_detail_view, name='category_detail'),
]
