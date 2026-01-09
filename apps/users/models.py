"""
User Models for Recipe Sharing Platform

This file defines our custom user models:
1. CustomUser - Extends Django's built-in User model
2. UserProfile - Stores additional user information (bio, avatar, dietary preferences)

Why CustomUser?
- Django's default User model is good, but we want to customize it
- We can add our own fields and methods
- Better control over authentication
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    """
    Custom User Model extending Django's AbstractUser
    
    What is AbstractUser?
    - Django provides a base User model with username, email, password, etc.
    - AbstractUser lets us extend it with our own fields
    - We get all the built-in features PLUS our customizations
    
    Why extend instead of creating from scratch?
    - Saves time - we get authentication, permissions, etc. for free
    - Industry best practice
    - Easier to maintain
    """
    
    # We can add custom fields here if needed
    # For now, we'll use the default fields from AbstractUser:
    # - username
    # - email
    # - password (hashed)
    # - first_name, last_name
    # - is_active, is_staff, is_superuser
    # - date_joined, last_login
    
    # Optional: Add email as required field
    email = models.EmailField(unique=True, help_text="Required. Enter a valid email address.")
    
    class Meta:
        """
        Meta class provides metadata about the model
        
        verbose_name: Human-readable name (singular)
        verbose_name_plural: Human-readable name (plural)
        """
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    def __str__(self):
        """
        String representation of the user
        When you print a user object, this is what shows
        """
        return self.username
    
    def get_absolute_url(self):
        """
        Returns the URL to access a particular user instance
        Used by Django admin and other parts of Django
        """
        return reverse("users:profile", kwargs={"username": self.username})


class UserProfile(models.Model):
    """
    User Profile Model - Stores additional user information
    
    This is a separate model linked to CustomUser via OneToOne relationship
    
    Why separate model?
    - Keeps user authentication data separate from profile data
    - Easier to extend without touching the User model
    - Better organization
    
    OneToOne relationship means:
    - Each User has exactly ONE Profile
    - Each Profile belongs to exactly ONE User
    - Like a person and their driver's license
    """
    
    # Link to the User (OneToOne relationship)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile',
        help_text="The user this profile belongs to"
    )
    
    # Bio - Short description about the user
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text="Tell us about yourself! (max 500 characters)"
    )
    
    # Avatar - Profile picture
    # upload_to specifies where images will be stored
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text="Upload your profile picture"
    )
    
    # Dietary Preferences - What diets does this user follow?
    # Using choices for predefined options
    DIETARY_CHOICES = [
        ('none', 'No dietary restrictions'),
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('gluten-free', 'Gluten-Free'),
        ('keto', 'Keto'),
        ('paleo', 'Paleo'),
        ('pescatarian', 'Pescatarian'),
        ('halal', 'Halal'),
        ('kosher', 'Kosher'),
    ]
    
    dietary_preferences = models.CharField(
        max_length=20,
        choices=DIETARY_CHOICES,
        default='none',
        help_text="Select your dietary preferences"
    )
    
    # Timestamps - When was this profile created/updated?
    created_at = models.DateTimeField(auto_now_add=True, help_text="When this profile was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When this profile was last updated")
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ['-created_at']  # Newest profiles first
    
    def __str__(self):
        """String representation"""
        return f"{self.user.username}'s Profile"
    
    def get_absolute_url(self):
        """URL to view this profile"""
        return reverse("users:profile", kwargs={"username": self.user.username})


# Signal to automatically create profile when user is created
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver - Automatically creates a profile when a user is created
    
    What is a signal?
    - Django signals allow certain senders to notify receivers when actions occur
    - post_save signal fires after a model instance is saved
    
    What does this do?
    - When a new CustomUser is created, automatically create a UserProfile for them
    - This ensures every user always has a profile
    - Also assigns default 'user' role to new users
    """
    if created:
        UserProfile.objects.create(user=instance)
        
        # Assign default 'user' role to new users
        from django.contrib.auth.models import Group
        try:
            user_group = Group.objects.get(name='user')
            instance.groups.add(user_group)
        except Group.DoesNotExist:
            # Role doesn't exist yet - will be created by create_roles command
            pass


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal receiver - Saves the profile when user is saved
    
    This ensures the profile stays in sync with the user
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
