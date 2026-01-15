from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'recipes', views.RecipeViewSet, basename='recipe')
router.register(r'ratings', views.RatingViewSet, basename='rating')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'favorites', views.FavoriteViewSet, basename='favorite')

urlpatterns = [
    # API root and health check
    path('', views.api_root, name='api-root'),
    path('health/', views.health_check, name='health-check'),
    path('config/supabase/', views.supabase_config, name='supabase-config'),
    path('users/me/', views.current_user, name='current-user'),
    path('users/profile/<str:username>/', views.user_profile, name='user-profile'),
    path('users/profile/<str:username>/update/', views.update_user_profile, name='update-user-profile'),
    
    # Include router URLs
    path('', include(router.urls)),
]


