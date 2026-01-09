from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [
    # API root and health check
    path('', views.api_root, name='api-root'),
    path('health/', views.health_check, name='health-check'),
    
    # App-specific API routes (will be added as we build features)
    # path('recipes/', include('apps.recipes.urls')),
    # path('users/', include('apps.users.urls')),
]


