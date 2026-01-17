"""
API Key Authentication for Meal Planner Apps
"""

from rest_framework import authentication, exceptions
from django.utils import timezone
from .models import APIKey


class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class for API keys.
    
    Allows meal planner apps to authenticate using API keys.
    Usage: Include 'X-API-Key' header in requests
    """
    
    def authenticate(self, request):
        """
        Authenticate the request using API key.
        
        Looks for API key in:
        1. X-API-Key header (preferred)
        2. api_key query parameter (for GET requests)
        """
        api_key = None
        
        # Check header first
        api_key_header = request.META.get('HTTP_X_API_KEY')
        if api_key_header:
            api_key = api_key_header.strip()
        
        # Fallback to query parameter
        if not api_key:
            api_key = request.query_params.get('api_key')
        
        if not api_key:
            return None  # No API key provided, let other auth methods try
        
        try:
            api_key_obj = APIKey.objects.get(key=api_key, is_active=True)
            
            # Check if expired
            if api_key_obj.expires_at and timezone.now() > api_key_obj.expires_at:
                raise exceptions.AuthenticationFailed('API key has expired')
            
            # Mark as used
            api_key_obj.mark_used()
            
            # Return user and API key object
            return (api_key_obj.user, api_key_obj)
            
        except APIKey.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid API key')
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Authentication failed: {str(e)}')

