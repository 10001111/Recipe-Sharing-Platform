"""
RLS Middleware for Django

This middleware sets the current user ID in PostgreSQL session variables
so that RLS policies can check user permissions.

IMPORTANT: This only works with PostgreSQL/Supabase!
"""

from django.utils.deprecation import MiddlewareMixin
from django.db import connection


class RLSAuthMiddleware(MiddlewareMixin):
    """
    Middleware to set current user ID for RLS policies
    
    Sets PostgreSQL session variable 'app.current_user_id' so RLS policies
    can check user permissions.
    """
    
    def process_request(self, request):
        """Set current user ID in PostgreSQL session"""
        # Only for PostgreSQL
        db_engine = connection.settings_dict['ENGINE']
        if 'postgresql' not in db_engine.lower():
            return None
        
        # Get current user ID
        user_id = None
        if request.user and request.user.is_authenticated:
            user_id = str(request.user.id)
        
        # Set PostgreSQL session variable
        try:
            with connection.cursor() as cursor:
                if user_id:
                    cursor.execute("SET app.current_user_id = %s", [user_id])
                else:
                    cursor.execute("SET app.current_user_id = NULL")
        except Exception as e:
            # If RLS is not set up, this will fail silently
            # That's okay - RLS is optional
            pass
        
        return None
    
    def process_response(self, request, response):
        """Clear session variable after request"""
        db_engine = connection.settings_dict['ENGINE']
        if 'postgresql' not in db_engine.lower():
            return response
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SET app.current_user_id = NULL")
        except:
            pass
        
        return response

