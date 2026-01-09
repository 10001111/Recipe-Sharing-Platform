# Role-Based Security System

## Overview

The application uses Django's built-in Groups system for role-based access control (RBAC). This provides secure, flexible permission management.

## Roles

### Default Roles

1. **user** - Standard user with basic permissions
   - Can view profiles
   - Can edit their own profile
   - Can create recipes (when implemented)

2. **content_manager** - Can manage recipes and content
   - All user permissions
   - Can add/edit/delete recipes
   - Can moderate recipe content

3. **moderator** - Can moderate content and manage users
   - All content_manager permissions
   - Can view/edit/delete user profiles
   - Can manage user accounts

4. **admin** - Full administrative access
   - All permissions
   - Can delete user accounts
   - Full system access

## Setup

### Create Roles

Run the management command to create default roles:

```bash
python manage.py create_roles
```

This will create all default roles and assign appropriate permissions.

### Assign Roles to Users

#### Via Django Admin
1. Go to `/admin/`
2. Navigate to Groups
3. Add users to appropriate groups

#### Via Python Shell
```python
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()
admin_group = Group.objects.get(name='admin')
user = User.objects.get(username='john')
user.groups.add(admin_group)
```

#### Via Management Command (create one)
```bash
python manage.py shell
>>> from django.contrib.auth.models import Group
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.get(username='john')
>>> admin_group = Group.objects.get(name='admin')
>>> user.groups.add(admin_group)
```

## Security Decorators

### Available Decorators

#### `@role_required('admin', 'moderator')`
Requires user to have one of the specified roles.

```python
from apps.users.decorators import role_required

@role_required('admin', 'moderator')
def admin_view(request):
    # Only admins or moderators can access
    pass
```

#### `@owner_or_role_required('admin', 'moderator')`
Allows access if user is the owner OR has one of the specified roles.

```python
from apps.users.decorators import owner_or_role_required

@owner_or_role_required('admin', 'moderator')
def edit_profile(request, username):
    # Owner can edit, or admin/moderator can edit any profile
    pass
```

#### `@staff_required`
Requires user to be staff member.

```python
from apps.users.decorators import staff_required

@staff_required
def staff_view(request):
    # Only staff can access
    pass
```

#### `@superuser_required`
Requires user to be superuser.

```python
from apps.users.decorators import superuser_required

@superuser_required
def super_admin_view(request):
    # Only superusers can access
    pass
```

## Protected Views

### Currently Protected

1. **Profile Edit** (`profile_edit_view`)
   - Owner can edit their own profile
   - Admin/Moderator can edit any profile
   - Decorator: `@owner_or_role_required('admin', 'moderator')`

2. **Profile Delete** (`profile_delete_view`)
   - Owner can delete their own account
   - Admin can delete any account
   - Decorator: `@owner_or_role_required('admin')`

### API Endpoints

- **Public**: `/api/` (root), `/api/health/`
- **Authenticated**: All other API endpoints require authentication
- Default permission: `IsAuthenticated`

## Security Best Practices

1. **Always use decorators** for sensitive operations
2. **Check ownership** before allowing modifications
3. **Log security events** (to be implemented)
4. **Use HTTPS** in production
5. **Validate input** on both client and server
6. **Rate limiting** (to be implemented)

## Adding New Roles

1. Update `create_roles.py` management command
2. Add role configuration with permissions
3. Run `python manage.py create_roles`
4. Assign roles to users as needed

## Testing Security

Test role-based access:

```python
# In Django shell
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

# Create test user
user = User.objects.create_user('testuser', 'test@test.com', 'password')

# Assign role
admin_group = Group.objects.get(name='admin')
user.groups.add(admin_group)

# Verify
print(user.groups.all())  # Should show admin group
```

