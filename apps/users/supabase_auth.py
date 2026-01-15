"""
Supabase Authentication Integration

Handles Supabase OAuth (Google) authentication and syncs with Django user system
"""

from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.conf import settings
import requests
import jwt
from jwt import PyJWKClient

User = get_user_model()

# Supabase JWT settings
SUPABASE_URL = getattr(settings, 'SUPABASE_URL', '')
SUPABASE_JWT_SECRET = getattr(settings, 'SUPABASE_JWT_SECRET', None)


def verify_supabase_token(access_token):
    """
    Verify Supabase JWT token and extract user info
    
    Args:
        access_token: Supabase access token from frontend
    
    Returns:
        dict with user info if valid, None otherwise
    """
    if not SUPABASE_JWT_SECRET:
        # Try to get from service role key (contains JWT secret)
        service_role_key = getattr(settings, 'SUPABASE_SERVICE_ROLE_KEY', '')
        if service_role_key:
            try:
                # Decode without verification to get the secret
                decoded = jwt.decode(service_role_key, options={"verify_signature": False})
                # For Supabase, we need to verify against their public key
                # This is a simplified version - in production, use proper JWT verification
                return None
            except:
                pass
        return None
    
    try:
        # Verify token
        decoded = jwt.decode(
            access_token,
            SUPABASE_JWT_SECRET,
            algorithms=['HS256'],
            audience='authenticated'
        )
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_supabase_user_info(access_token):
    """
    Get user info from Supabase using access token
    
    Args:
        access_token: Supabase access token
    
    Returns:
        dict with user info or None
    """
    supabase_url = getattr(settings, 'SUPABASE_URL', '')
    if not supabase_url:
        return None
    
    try:
        headers = {
            'Authorization': f'Bearer {access_token}',
            'apikey': getattr(settings, 'SUPABASE_ANON_KEY', '')
        }
        response = requests.get(
            f'{supabase_url}/auth/v1/user',
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            user_data = response.json()
            # Supabase returns user in 'user' key
            return user_data.get('user') or user_data
        return None
    except Exception as e:
        print(f"Error getting Supabase user: {e}")
        return None


def sync_supabase_user(supabase_user_data, request=None):
    """
    Sync Supabase user with Django user system
    
    Creates or updates Django user based on Supabase user data
    
    Args:
        supabase_user_data: User data from Supabase
        request: Django request object (for login)
    
    Returns:
        Django User object
    """
    email = supabase_user_data.get('email')
    supabase_id = supabase_user_data.get('id')
    
    if not email:
        return None
    
    # Generate username from email
    base_username = email.split('@')[0].replace('.', '_').replace('-', '_')
    username = base_username
    
    # Check if user exists by email
    try:
        user = User.objects.get(email=email)
        # User exists, update if needed
        if not user.is_active:
            user.is_active = True
            user.save()
    except User.DoesNotExist:
        # Create new user
        # Make sure username is unique
        counter = 1
        original_username = username
        while User.objects.filter(username=username).exists():
            username = f'{original_username}{counter}'
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=None,  # OAuth users don't have password - Django will handle this
            is_active=True
        )
        # Set unusable password for OAuth users
        user.set_unusable_password()
        user.save()
    
    # Log in the user if request provided
    if request and user.is_active:
        login(request, user)
    
    return user

