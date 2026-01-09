"""
Role-based security decorators for views

Provides decorators to enforce role-based access control (RBAC)
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    """
    Decorator that requires user to have one of the specified roles
    
    Usage:
        @role_required('admin', 'moderator')
        def admin_view(request):
            ...
    
    Args:
        *roles: Variable number of role names (strings)
    
    Returns:
        Decorated function that checks roles before execution
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'You must be logged in to access this page.')
                return redirect('users:login')
            
            # Check if user has any of the required roles
            user_roles = request.user.groups.values_list('name', flat=True)
            has_role = any(role in user_roles for role in roles)
            
            # Superusers bypass role checks
            if not has_role and not request.user.is_superuser:
                messages.error(request, 'You do not have permission to access this page.')
                raise PermissionDenied("Insufficient role permissions")
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def owner_or_role_required(*roles):
    """
    Decorator that allows access if:
    1. User is the owner of the resource, OR
    2. User has one of the specified roles
    
    Usage:
        @owner_or_role_required('admin', 'moderator')
        def edit_profile(request, username):
            # Must be owner OR admin/moderator
            ...
    
    Args:
        *roles: Variable number of role names (strings)
    
    Returns:
        Decorated function that checks ownership or roles
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'You must be logged in to access this page.')
                return redirect('users:login')
            
            # Get the username from kwargs (common pattern)
            username = kwargs.get('username')
            is_owner = username and request.user.username == username
            
            # Check roles
            user_roles = list(request.user.groups.values_list('name', flat=True))
            has_role = any(role in user_roles for role in roles)
            
            # Superusers bypass checks
            if not is_owner and not has_role and not request.user.is_superuser:
                messages.error(request, 'You do not have permission to access this page.')
                raise PermissionDenied("Insufficient permissions")
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def staff_required(view_func):
    """
    Decorator that requires user to be staff
    
    Usage:
        @staff_required
        def admin_view(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('users:login')
        
        if not request.user.is_staff:
            messages.error(request, 'You do not have permission to access this page.')
            raise PermissionDenied("Staff access required")
        
        return view_func(request, *args, **kwargs)
    return wrapper


def superuser_required(view_func):
    """
    Decorator that requires user to be superuser
    
    Usage:
        @superuser_required
        def super_admin_view(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('users:login')
        
        if not request.user.is_superuser:
            messages.error(request, 'You do not have permission to access this page.')
            raise PermissionDenied("Superuser access required")
        
        return view_func(request, *args, **kwargs)
    return wrapper

