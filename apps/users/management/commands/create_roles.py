"""
Django management command to create default roles

Usage:
    python manage.py create_roles
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates default roles (groups) for the application'

    def handle(self, *args, **options):
        # Define roles and their permissions
        roles_config = {
            'admin': {
                'description': 'Full administrative access',
                'permissions': ['all']  # Special flag for all permissions
            },
            'moderator': {
                'description': 'Can moderate content and manage users',
                'permissions': [
                    'change_user',
                    'delete_user',
                    'view_user',
                    'change_userprofile',
                    'delete_userprofile',
                    'view_userprofile',
                ]
            },
            'content_manager': {
                'description': 'Can manage recipes and content',
                'permissions': [
                    'add_recipe',
                    'change_recipe',
                    'delete_recipe',
                    'view_recipe',
                ]
            },
            'user': {
                'description': 'Standard user with basic permissions',
                'permissions': [
                    'view_userprofile',
                    'change_userprofile',  # Only their own
                ]
            }
        }
        
        created_count = 0
        updated_count = 0
        
        for role_name, config in roles_config.items():
            group, created = Group.objects.get_or_create(name=role_name)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created role: {role_name}')
                )
                created_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f'Role already exists: {role_name}')
                )
                updated_count += 1
            
            # Add permissions
            if config['permissions'] == ['all']:
                # Add all permissions
                all_permissions = Permission.objects.all()
                group.permissions.set(all_permissions)
                self.stdout.write(f'  Added all permissions to {role_name}')
            else:
                # Add specific permissions
                permissions_added = 0
                for perm_codename in config['permissions']:
                    # Try to find permission
                    # Format: app_label.permission_codename
                    perm_found = False
                    if '.' in perm_codename:
                        app_label, codename = perm_codename.split('.', 1)
                        try:
                            perm = Permission.objects.get(
                                content_type__app_label=app_label,
                                codename=codename
                            )
                            group.permissions.add(perm)
                            permissions_added += 1
                            perm_found = True
                        except Permission.DoesNotExist:
                            pass
                    else:
                        # Try common apps
                        for app_label in ['users', 'recipes', 'auth', 'contenttypes']:
                            try:
                                perm = Permission.objects.get(
                                    content_type__app_label=app_label,
                                    codename=perm_codename
                                )
                                group.permissions.add(perm)
                                permissions_added += 1
                                perm_found = True
                                break
                            except Permission.DoesNotExist:
                                continue
                        
                        # Direct codename search as fallback
                        if not perm_found:
                            try:
                                perm = Permission.objects.get(codename=perm_codename)
                                group.permissions.add(perm)
                                permissions_added += 1
                                perm_found = True
                            except Permission.DoesNotExist:
                                self.stdout.write(
                                    self.style.WARNING(f'  Permission not found: {perm_codename}')
                                )
                
                if permissions_added > 0:
                    self.stdout.write(
                        f'  Added {permissions_added} permissions to {role_name}'
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSummary: Created {created_count} roles, {updated_count} already existed'
            )
        )

