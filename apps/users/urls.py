"""
URL Configuration for Users App

URLs map web addresses (like /users/profile/john/) to views (Python functions)

URL Pattern Structure:
- path('pattern/', view_function, name='url_name')
- pattern: The URL path (what appears in browser address bar)
- view_function: The Python function that handles the request
- name: A name for the URL (used in templates with {% url %})

Example:
- URL: /users/register/
- View: register_view function
- Name: 'register' (can use {% url 'users:register' %} in templates)
"""

from django.urls import path
from . import views

app_name = 'users'  # Namespace for URLs (prevents conflicts)

urlpatterns = [
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('supabase-auth/', views.supabase_auth_callback, name='supabase_auth'),
    
    # Profile URLs
    # <username> is a URL parameter - it captures the username from the URL
    path('profile/<str:username>/', views.UserProfileDetailView.as_view(), name='profile'),
    path('profile/<str:username>/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/<str:username>/delete/', views.profile_delete_view, name='profile_delete'),
]
