# 🎯 Milestone 2.1: User System - Complete Guide

## 📚 Table of Contents
1. [Overview](#overview)
2. [What We Built](#what-we-built)
3. [Understanding the Code](#understanding-the-code)
4. [How to Use](#how-to-use)
5. [Testing](#testing)

---

## 🎯 Overview

### What is Milestone 2.1?

We built a complete **User System** for the Recipe Sharing Platform. This includes:
- Custom user accounts
- User profiles with additional information
- Registration and login functionality
- Profile management (view, edit, delete)

### Why This Matters

**Think of it like this:**
- **User System** = The foundation of your app
- Without users, you can't have recipes, comments, favorites, etc.
- It's like building a house - you need the foundation first!

---

## 🏗️ What We Built

### 1. CustomUser Model (`apps/users/models.py`)

**What is it?**
- A custom user model that extends Django's built-in User
- Gives us more control and flexibility

**Why CustomUser instead of default User?**
- ✅ Can add custom fields later if needed
- ✅ Better for future customization
- ✅ Industry best practice
- ✅ Easier to extend

**Key Features:**
- Username, email, password (from AbstractUser)
- Email is required and unique
- All Django authentication features included

### 2. UserProfile Model (`apps/users/models.py`)

**What is it?**
- Stores additional information about users
- Separate from authentication data

**Fields:**
- `bio` - User's biography (text, max 500 characters)
- `avatar` - Profile picture (image file)
- `dietary_preferences` - Dropdown with options (vegetarian, vegan, etc.)
- `created_at` / `updated_at` - Timestamps

**OneToOne Relationship:**
- Each User has exactly ONE Profile
- Each Profile belongs to exactly ONE User
- Like a person and their driver's license

**Automatic Creation:**
- Profile is automatically created when user registers
- Uses Django signals (magic that runs automatically)

### 3. Forms (`apps/users/forms.py`)

**What are forms?**
- Handle HTML form data
- Validate user input
- Make it easy to create/edit data

**Forms Created:**
1. **CustomUserCreationForm** - For registration
2. **UserProfileForm** - For editing profiles

### 4. Views (`apps/users/views.py`)

**What are views?**
- Python functions that handle web requests
- Receive data → Process it → Return response

**Views Created:**
1. `register_view` - User registration
2. `login_view` - User login
3. `logout_view` - User logout
4. `UserProfileDetailView` - View profile (Read)
5. `profile_edit_view` - Edit profile (Update)
6. `profile_delete_view` - Delete account (Delete)

### 5. URLs (`apps/users/urls.py`)

**What are URLs?**
- Map web addresses to views
- Like a phone book for your website

**URLs Created:**
- `/users/register/` - Registration page
- `/users/login/` - Login page
- `/users/logout/` - Logout
- `/users/profile/<username>/` - View profile
- `/users/profile/<username>/edit/` - Edit profile
- `/users/profile/<username>/delete/` - Delete account

### 6. Templates (`templates/users/`)

**What are templates?**
- HTML files with Django template language
- Define how pages look

**Templates Created:**
- `base.html` - Base template (header, navigation)
- `register.html` - Registration form
- `login.html` - Login form
- `profile_detail.html` - View profile
- `profile_edit.html` - Edit profile
- `profile_delete_confirm.html` - Delete confirmation

---

## 🧠 Understanding the Code (For Beginners)

### Models Explained

#### CustomUser Model
```python
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
```

**What this means:**
- `AbstractUser` = Django's base user model (gives us username, password, etc.)
- `email = models.EmailField(unique=True)` = Email field that must be unique
- We get all the authentication features for free!

#### UserProfile Model
```python
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, ...)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    dietary_preferences = models.CharField(max_length=20, choices=DIETARY_CHOICES)
```

**What this means:**
- `OneToOneField` = One user, one profile (like a person and their ID card)
- `bio` = Text field for biography
- `avatar` = Image field for profile picture
- `dietary_preferences` = Dropdown with predefined choices

### Views Explained

#### Registration View
```python
def register_view(request):
    if request.method == 'POST':
        # User submitted form - process it
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:profile', username=username)
    else:
        # User visiting page - show form
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
```

**What this does:**
1. If POST (form submitted) → Create user, log them in, redirect
2. If GET (just visiting) → Show registration form

### Signals Explained

```python
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

**What this does:**
- Automatically creates a profile when a user is created
- No manual work needed!
- Runs "behind the scenes"

---

## 🚀 How to Use

### Step 1: Run Migrations

**What are migrations?**
- Create database tables based on your models
- Like building the structure of your database

```bash
# Create migration files
python manage.py makemigrations users

# Apply migrations to database
python manage.py migrate
```

**Note:** You'll need your database connection working first!

### Step 2: Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

This creates an admin account for accessing Django admin panel.

### Step 3: Start Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

### Step 4: Test the Features

1. **Register:** Go to `/users/register/` and create an account
2. **Login:** Go to `/users/login/` and login
3. **View Profile:** Go to `/users/profile/<your-username>/`
4. **Edit Profile:** Click "Edit Profile" button
5. **Logout:** Click "Logout" in navigation

---

## 🧪 Testing

### Manual Testing Checklist

- [ ] Can register a new account
- [ ] Can login with registered account
- [ ] Can view own profile
- [ ] Can edit own profile (bio, avatar, dietary preferences)
- [ ] Can logout
- [ ] Cannot edit someone else's profile
- [ ] Profile is automatically created when user registers
- [ ] Avatar uploads work correctly

### Testing URLs

- Registration: http://127.0.0.1:8000/users/register/
- Login: http://127.0.0.1:8000/users/login/
- Profile: http://127.0.0.1:8000/users/profile/<username>/
- Edit Profile: http://127.0.0.1:8000/users/profile/<username>/edit/

---

## 📁 File Structure

```
apps/users/
├── models.py          # CustomUser and UserProfile models
├── forms.py           # Registration and profile forms
├── views.py           # All user-related views
├── urls.py            # URL routing
├── admin.py           # Django admin configuration
└── ...

templates/users/
├── register.html      # Registration page
├── login.html         # Login page
├── profile_detail.html # View profile
├── profile_edit.html   # Edit profile
└── profile_delete_confirm.html # Delete confirmation
```

---

## 🔑 Key Concepts Explained

### 1. Model Relationships

**OneToOne:**
- One User → One Profile
- Like a person and their passport

**ForeignKey (we'll use this later):**
- One Recipe → One User (author)
- Like a book and its author

**ManyToMany (we'll use this later):**
- Many Users → Many Recipes (favorites)
- Like students and courses

### 2. Authentication vs Authorization

**Authentication (Who are you?):**
- Login, logout, registration
- Verifying identity

**Authorization (What can you do?):**
- Can you edit this profile?
- Can you delete this recipe?
- Permissions and access control

### 3. CRUD Operations

**CRUD = Create, Read, Update, Delete**

- **Create:** Registration (create user)
- **Read:** View profile
- **Update:** Edit profile
- **Delete:** Delete account

---

## 🎓 Learning Resources

- [Django User Model](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/)
- [Django Forms](https://docs.djangoproject.com/en/4.2/topics/forms/)
- [Django Views](https://docs.djangoproject.com/en/4.2/topics/http/views/)
- [Django Signals](https://docs.djangoproject.com/en/4.2/topics/signals/)

---

## ✅ Milestone Checklist

- [x] CustomUser model created
- [x] UserProfile model created
- [x] Django settings configured to use CustomUser
- [x] Registration form and view created
- [x] Login/logout views created
- [x] Profile CRUD operations implemented
- [x] URLs configured
- [x] Templates created
- [x] Admin interface configured
- [ ] Migrations created and run (pending database connection)

---

**Congratulations!** You've built a complete user system! 🎉

**Next Milestone:** 2.2 - Recipe Models (we'll build the recipe system next)

