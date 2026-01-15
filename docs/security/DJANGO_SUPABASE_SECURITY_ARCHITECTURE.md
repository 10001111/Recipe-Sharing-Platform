# 🔐 Django + Supabase Security Architecture Explained

## 📋 Overview

This document explains how authentication and authorization work in your Recipe Sharing Platform, specifically how Django and Supabase work together.

---

## 🏗️ The Architecture: Two Layers of Security

Your application uses a **hybrid architecture** with two security layers:

```
┌─────────────────────────────────────────────────────────────┐
│                    USER'S BROWSER                           │
│                                                             │
│  User clicks "Sign in with Google"                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: SUPABASE (Authentication)                        │
│  ────────────────────────────────────────                    │
│  • Handles Google OAuth login                               │
│  • Verifies user identity                                   │
│  • Issues JWT tokens                                        │
│  • Stores auth session                                      │
│                                                             │
│  ✅ "WHO are you?" (Authentication)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Access Token
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: DJANGO (Authorization & Application Logic)         │
│  ────────────────────────────────────────                    │
│  • Receives Supabase token                                  │
│  • Creates/updates Django user                              │
│  • Manages permissions (Groups/Roles)                       │
│  • Controls what users can see/do                           │
│                                                             │
│  ✅ "WHAT can you do?" (Authorization)                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔑 Key Concepts

### Authentication vs Authorization

**Authentication (Supabase):**
- **Question:** "WHO are you?"
- **Answer:** "I'm john@example.com, verified by Google"
- **Handled by:** Supabase Auth
- **Result:** User gets a JWT token proving their identity

**Authorization (Django):**
- **Question:** "WHAT can you do?"
- **Answer:** "You're a regular user, so you can view recipes and edit your own profile"
- **Handled by:** Django Groups/Permissions
- **Result:** User can only access allowed features

---

## 🔄 What Happens When a User Signs In with Google

### Step-by-Step Flow:

```
1. USER CLICKS "Sign in with Google"
   └─> Frontend calls Supabase Auth API
   
2. SUPABASE HANDLES GOOGLE OAUTH
   └─> User authenticates with Google
   └─> Supabase verifies identity
   └─> Supabase issues JWT access token
   
3. FRONTEND SENDS TOKEN TO DJANGO
   └─> JavaScript sends access_token to Django backend
   └─> POST request to /users/supabase-auth-callback/
   
4. DJANGO VERIFIES & SYNCs USER
   └─> Django calls Supabase API to verify token
   └─> Gets user info (email, name, etc.)
   └─> Creates Django User if doesn't exist
   └─> Assigns default 'user' role (Group)
   └─> Logs user into Django session
   
5. USER IS NOW LOGGED IN
   └─> Django session active
   └─> User has 'user' role by default
   └─> Can access features based on Django permissions
```

---

## 🎯 Where Security is Managed

### ✅ **Authentication: Managed by Supabase**

**Location:** Supabase Dashboard → Authentication → Providers

**What Supabase Controls:**
- Google OAuth configuration
- User identity verification
- JWT token generation
- Session management
- Password reset (if using email/password)

**You DON'T manage this in Django** - Supabase handles it all.

---

### ✅ **Authorization: Managed by Django**

**Location:** Django codebase (Groups, Permissions, Decorators)

**What Django Controls:**
- User roles (admin, moderator, content_manager, user)
- Permissions (what each role can do)
- Access control (who can see/edit what)
- Default role assignment for new users

**This is where you manage "what users can see and do"**

---

## 📍 Where to Manage Default Security

### When a User Authenticates with Google:

**Default Role Assignment** happens in **Django**, not Supabase!

**Location:** `apps/users/models.py` (lines 156-180)

```python
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        
        # Assign default 'user' role to new users
        from django.contrib.auth.models import Group
        try:
            user_group = Group.objects.get(name='user')
            instance.groups.add(user_group)  # ← DEFAULT ROLE ASSIGNED HERE
        except Group.DoesNotExist:
            pass
```

**This means:**
- Every new user (including Google OAuth users) gets the `'user'` role automatically
- The `'user'` role has basic permissions (view profiles, edit own profile)
- You can change this default behavior here

---

## 🛡️ How Permissions Work

### Django Groups = Roles

**Current Roles in Your System:**

1. **`user`** (Default for new users)
   - Can view profiles
   - Can edit own profile
   - Can create recipes (when implemented)

2. **`content_manager`**
   - All user permissions
   - Can add/edit/delete recipes
   - Can moderate recipe content

3. **`moderator`**
   - All content_manager permissions
   - Can view/edit/delete any user profile
   - Can manage user accounts

4. **`admin`**
   - All permissions
   - Can delete user accounts
   - Full system access

### How Permissions Are Enforced

**In Views (Python code):**

```python
# Example from apps/users/views.py
@login_required
@owner_or_role_required('admin', 'moderator')
def profile_edit_view(request, username):
    # Only owner OR admin/moderator can edit
    ...
```

**What this does:**
1. `@login_required` - User must be logged in
2. `@owner_or_role_required('admin', 'moderator')` - User must be:
   - The owner of the profile, OR
   - Have 'admin' role, OR
   - Have 'moderator' role

**In Templates (HTML):**

```django
{% if user.groups.all %}
    {% for group in user.groups.all %}
        {% if group.name == 'admin' %}
            <a href="/admin/">Admin Panel</a>
        {% endif %}
    {% endfor %}
{% endif %}
```

---

## 🔍 Django vs Supabase RLS: Which One?

### Current Setup: **Django-Managed Security**

**Your project currently uses Django Groups/Permissions, NOT Supabase RLS.**

**Why Django?**
- ✅ More flexible for complex business logic
- ✅ Easier to test and debug
- ✅ Works with Django admin
- ✅ Can check permissions in Python code
- ✅ Better for role-based access control

**When to use Supabase RLS?**
- ✅ If you want database-level security (defense in depth)
- ✅ If you're using Supabase client directly from frontend
- ✅ If you want to prevent SQL injection from bypassing Django
- ✅ If you need row-level filtering (e.g., users can only see their own data)

---

## 🎨 Recommended Approach: Hybrid Security

### Best Practice: Use Both!

**Django (Primary):**
- Main authorization logic
- Role-based access control
- Business rules

**Supabase RLS (Secondary - Optional):**
- Database-level backup security
- Prevents direct database access bypassing Django
- Extra layer of protection

**Example:**
```sql
-- Supabase RLS Policy (if you add it)
CREATE POLICY "Users can only see their own profiles"
ON user_profiles
FOR SELECT
USING (auth.uid() = user_id);
```

This ensures that even if someone bypasses Django, they can't see other users' data.

---

## 📝 How to Change Default Permissions

### Option 1: Change Default Role for New Users

**File:** `apps/users/models.py`

```python
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        
        # Change this line to assign different default role:
        user_group = Group.objects.get(name='content_manager')  # Changed from 'user'
        instance.groups.add(user_group)
```

### Option 2: Assign Role Based on Email Domain

```python
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        
        # Assign role based on email domain
        if instance.email.endswith('@yourcompany.com'):
            admin_group = Group.objects.get(name='admin')
            instance.groups.add(admin_group)
        else:
            user_group = Group.objects.get(name='user')
            instance.groups.add(user_group)
```

### Option 3: Assign Role After Google OAuth

**File:** `apps/users/supabase_auth.py`

Modify `sync_supabase_user()` function:

```python
def sync_supabase_user(supabase_user_data, request=None):
    # ... existing code ...
    
    if created:
        # New user created - assign role
        from django.contrib.auth.models import Group
        
        # Assign based on your logic
        if some_condition:
            admin_group = Group.objects.get(name='admin')
            user.groups.add(admin_group)
        else:
            user_group = Group.objects.get(name='user')
            user.groups.add(user_group)
```

---

## 🚀 Quick Reference

### Where to Manage What:

| Security Aspect | Managed In | Location |
|----------------|------------|----------|
| **Google OAuth Setup** | Supabase Dashboard | Settings → Authentication → Providers |
| **User Identity** | Supabase | Automatic (handled by Supabase Auth) |
| **Default Role** | Django | `apps/users/models.py` (signal) |
| **Role Permissions** | Django | `apps/users/management/commands/create_roles.py` |
| **Access Control** | Django | `apps/users/decorators.py` + views |
| **Database RLS** | Supabase (Optional) | SQL migrations or Supabase Dashboard |

---

## ❓ Common Questions

### Q: When a user logs in with Google, where is their default role set?

**A:** In Django, in the `create_user_profile` signal (`apps/users/models.py`). By default, all new users get the `'user'` role.

### Q: Can I set different default roles for Google OAuth users vs regular users?

**A:** Yes! Modify the `sync_supabase_user()` function in `apps/users/supabase_auth.py` to assign roles based on any criteria you want.

### Q: Do I need Supabase RLS if I'm using Django permissions?

**A:** Not required, but recommended for defense in depth. Django handles your main security, RLS adds an extra database-level layer.

### Q: How do I check what role a user has?

**A:** In Python:
```python
user.groups.all()  # List of groups/roles
user.groups.filter(name='admin').exists()  # Check if user is admin
```

In templates:
```django
{% if user.groups.all %}
    User has roles: {{ user.groups.all|join:", " }}
{% endif %}
```

### Q: Can I change a user's role after they sign up?

**A:** Yes! Via Django admin or Python code:
```python
from django.contrib.auth.models import Group
admin_group = Group.objects.get(name='admin')
user.groups.add(admin_group)
```

---

## 📚 Summary

**TL;DR:**

1. **Supabase** handles authentication (WHO you are) - Google OAuth, identity verification
2. **Django** handles authorization (WHAT you can do) - roles, permissions, access control
3. **Default role** is assigned in Django when user is created (`apps/users/models.py`)
4. **You manage permissions** in Django using Groups and decorators
5. **Supabase RLS** is optional but recommended for extra security

**Your current setup:** Django-managed security (recommended for most use cases)

**To change default permissions:** Modify the signal in `apps/users/models.py` or the `sync_supabase_user()` function in `apps/users/supabase_auth.py`

