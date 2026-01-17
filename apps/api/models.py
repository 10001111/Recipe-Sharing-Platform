"""
API Models for Recipe Sharing Platform

Models:
- APIKey: API keys for meal planner apps and external integrations
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
import secrets

User = get_user_model()


class APIKey(models.Model):
    """
    API Key Model for Meal Planner Apps
    
    Allows meal planner apps and external services to authenticate
    and access the Recipe Sharing Platform API.
    """
    name = models.CharField(
        max_length=200,
        help_text="Name/description of the application using this API key"
    )
    key = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        help_text="The API key string"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='api_keys',
        help_text="User who created this API key"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this API key is active and can be used"
    )
    last_used = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last time this API key was used"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Optional expiration date for this API key"
    )
    
    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['key', 'is_active']),
            models.Index(fields=['user', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
    def save(self, *args, **kwargs):
        # Generate key if it doesn't exist
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_key():
        """Generate a secure random API key"""
        return secrets.token_urlsafe(32)  # 32 bytes = 43 characters base64
    
    def is_valid(self):
        """Check if the API key is valid (active and not expired)"""
        if not self.is_active:
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        return True
    
    def mark_used(self):
        """Mark this API key as used (update last_used timestamp)"""
        self.last_used = timezone.now()
        self.save(update_fields=['last_used'])
    
    def clean(self):
        """Validate the API key"""
        if self.expires_at and self.expires_at < timezone.now():
            raise ValidationError("Expiration date cannot be in the past")

