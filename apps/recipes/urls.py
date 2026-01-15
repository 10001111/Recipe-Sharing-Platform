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
    
    # Social Features URLs
    path('<int:pk>/rate/', views.rate_recipe_view, name='rate'),
    path('<int:pk>/rate/delete/', views.delete_rating_view, name='delete_rating'),
    path('<int:pk>/comment/', views.add_comment_view, name='add_comment'),
    path('<int:pk>/comment/<int:comment_id>/delete/', views.delete_comment_view, name='delete_comment'),
    path('<int:pk>/favorite/', views.toggle_favorite_view, name='toggle_favorite'),
    path('favorites/', views.favorite_recipes_view, name='favorites'),
]
