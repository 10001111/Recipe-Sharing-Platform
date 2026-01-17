from django.contrib import admin
from .models import APIKey


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'key_preview', 'is_active', 'last_used', 'created_at', 'expires_at']
    list_filter = ['is_active', 'created_at', 'expires_at']
    search_fields = ['name', 'user__username', 'key']
    readonly_fields = ['key', 'created_at', 'last_used']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'user', 'key')
        }),
        ('Status', {
            'fields': ('is_active', 'expires_at', 'last_used')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def key_preview(self, obj):
        """Show masked version of API key"""
        if obj.key:
            return f"{obj.key[:8]}...{obj.key[-4:]}"
        return '-'
    key_preview.short_description = 'API Key Preview'
    
    def get_readonly_fields(self, request, obj=None):
        """Make key readonly after creation"""
        readonly = list(self.readonly_fields)
        if obj:  # Editing existing object
            readonly.append('key')
        return readonly

