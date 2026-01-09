"""
Forms for User Authentication and Profile Management

Forms are Django's way of handling HTML forms:
- Validation (checking if data is correct)
- Rendering (creating HTML)
- Processing (handling submitted data)

Think of forms as a bridge between HTML and Python code.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import UserProfile

# Get our CustomUser model
User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Form for user registration (signing up)
    
    Extends Django's UserCreationForm to include email
    
    What does this form do?
    - Collects username, email, password1, password2
    - Validates the data (email format, password strength, etc.)
    - Creates a new user account
    """
    
    email = forms.EmailField(
        required=True,
        help_text="Required. Enter a valid email address.",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    class Meta:
        """
        Meta class tells Django:
        - Which model to use (CustomUser)
        - Which fields to include in the form
        - How to display them
        """
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        """
        Customize the form's appearance
        Adds CSS classes to make it look nice
        """
        super().__init__(*args, **kwargs)
        # Add CSS classes to password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    
    def save(self, commit=True):
        """
        Override save to set email
        When user is created, ensure email is saved
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating user information (admin use)
    
    Used in Django admin panel for editing users
    """
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class UserProfileForm(forms.ModelForm):
    """
    Form for creating/editing user profiles
    
    ModelForm automatically creates form fields from model
    - bio field → textarea
    - avatar field → file input
    - dietary_preferences → dropdown
    
    This is much easier than creating forms manually!
    """
    
    class Meta:
        model = UserProfile
        fields = ('bio', 'avatar', 'dietary_preferences')
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'  # Only accept images
            }),
            'dietary_preferences': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        help_texts = {
            'bio': 'Tell us about yourself! (max 500 characters)',
            'avatar': 'Upload your profile picture (JPG, PNG, etc.)',
            'dietary_preferences': 'Select your dietary preferences',
        }

