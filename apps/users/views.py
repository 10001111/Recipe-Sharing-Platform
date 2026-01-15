"""
Views for User Authentication and Profile Management

Views are Python functions/classes that handle web requests:
- Receive request from browser
- Process the request (get data, save data, etc.)
- Return a response (HTML page, JSON, redirect, etc.)

Think of views as the "brain" of your web application.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserProfile
from .decorators import owner_or_role_required, role_required
from .supabase_auth import get_supabase_user_info, sync_supabase_user

User = get_user_model()


def register_view(request):
    """
    View for user registration (signing up)
    
    What does this do?
    1. If user submits form (POST request) → Process registration
    2. If user just visits page (GET request) → Show registration form
    3. After successful registration → Log them in and redirect
    
    HTTP Methods:
    - GET: User wants to see the form
    - POST: User submitted the form
    """
    if request.method == 'POST':
        # User submitted the registration form
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            # Form data is valid - create the user
            user = form.save()
            
            # Log the user in automatically after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            # Show success message
            messages.success(request, f'Welcome, {username}! Your account has been created.')
            
            # Redirect to profile page
            return redirect('users:profile', username=username)
        else:
            # Form has errors - show them to user
            messages.error(request, 'Please correct the errors below.')
    else:
        # User is just visiting the page - show empty form
        form = CustomUserCreationForm()
    
    # Render the registration template with the form
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """
    View for user login
    
    What does this do?
    1. If user submits login form → Check credentials
    2. If credentials are correct → Log them in
    3. If wrong → Return error flag for pop-up
    """
    if request.method == 'POST':
        # Get username and password from form
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if user exists
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_exists = User.objects.filter(username=username).exists()
        
        # Authenticate the user (check if credentials are correct)
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Credentials are correct - log them in
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            
            # Redirect to next page (or profile if no next specified)
            next_url = request.GET.get('next', 'users:profile')
            return redirect(next_url, username=username)
        else:
            # Credentials are wrong - return with error flag
            error_message = "User isn't registered." if not user_exists else "Invalid password."
            return render(request, 'users/login.html', {
                'login_error': error_message,
                'username': username,
                'supabase_url': getattr(settings, 'SUPABASE_URL', ''),
                'supabase_anon_key': getattr(settings, 'SUPABASE_ANON_KEY', ''),
            })
    
    # Render login template
    supabase_url = getattr(settings, 'SUPABASE_URL', '')
    supabase_anon_key = getattr(settings, 'SUPABASE_ANON_KEY', '')
    return render(request, 'users/login.html', {
        'supabase_url': supabase_url,
        'supabase_anon_key': supabase_anon_key,
    })


@csrf_exempt
def supabase_auth_callback(request):
    """
    Handle Supabase OAuth callback
    
    Receives Supabase session token and syncs with Django user
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            access_token = data.get('access_token')
            
            if not access_token:
                return JsonResponse({'error': 'No access token provided'}, status=400)
            
            # Get user info from Supabase
            supabase_user = get_supabase_user_info(access_token)
            
            if not supabase_user:
                return JsonResponse({'error': 'Invalid token'}, status=400)
            
            # Sync with Django user
            user = sync_supabase_user(supabase_user, request)
            
            if user:
                return JsonResponse({
                    'success': True,
                    'redirect_url': '/users/profile/{}/'.format(user.username)
                })
            else:
                return JsonResponse({'error': 'Failed to create user'}, status=400)
                
        except Exception as e:
            import traceback
            print(f"Supabase auth error: {traceback.format_exc()}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def logout_view(request):
    """
    View for user logout
    
    What does this do?
    - Logs out the current user (if logged in)
    - Redirects to home page
    
    Note: No @login_required decorator needed - logout should work
    even if session expired or user already logged out
    """
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


class UserProfileDetailView(DetailView):
    """
    View for displaying a user's profile (Read operation)
    
    DetailView is a Django class-based view that:
    - Automatically gets the object (user profile)
    - Renders a template with that object
    - Handles 404 errors automatically
    
    Much simpler than writing a function view!
    """
    model = User
    template_name = 'users/profile_detail.html'
    context_object_name = 'user_obj'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        """
        Add extra data to the template context
        We want to include the user's profile in the template
        """
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        # Get or create profile (should already exist due to signal)
        profile, created = UserProfile.objects.get_or_create(user=user)
        context['profile'] = profile
        return context


@login_required
@owner_or_role_required('admin', 'moderator')
def profile_edit_view(request, username):
    """
    View for editing user profile (Update operation)
    
    Security: Only profile owner, admins, or moderators can edit
    
    What does this do?
    1. Only the profile owner or admin/moderator can edit
    2. If user submits form → Update profile
    3. If user visits page → Show edit form with current data
    """
    # Get the user whose profile we're editing
    user_obj = get_object_or_404(User, username=username)
    
    # Decorator handles permission check - owner or admin/moderator
    # Get or create the profile
    profile, created = UserProfile.objects.get_or_create(user=user_obj)
    
    if request.method == 'POST':
        # User submitted the edit form
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            # Form is valid - save the profile
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:profile', username=username)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # User is just visiting - show form with current data
        form = UserProfileForm(instance=profile)
    
    return render(request, 'users/profile_edit.html', {
        'form': form,
        'user_obj': user_obj,
        'profile': profile
    })


@login_required
@owner_or_role_required('admin')
def profile_delete_view(request, username):
    """
    View for deleting user account (Delete operation)
    
    Security: Only account owner or admin can delete
    
    WARNING: This is a destructive operation!
    - Deletes the user account
    - Deletes the profile
    - User will be logged out
    
    In production, you might want to:
    - Soft delete (mark as inactive instead of deleting)
    - Require password confirmation
    - Send confirmation email
    """
    user_obj = get_object_or_404(User, username=username)
    
    # Decorator handles permission check - owner or admin only
    if request.method == 'POST':
        # User confirmed deletion
        # Log out the user first (before deleting the account)
        logout(request)
        # Delete user (profile will be deleted automatically due to CASCADE)
        user_obj.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('home')
    
    # Show confirmation page
    return render(request, 'users/profile_delete_confirm.html', {
        'user_obj': user_obj
    })
