# Milestone 2.4: Quick Start Guide

## Quick Commands

### 1. Run Migrations
```bash
# Activate virtual environment
venv\Scripts\activate

# Run all migrations
python manage.py migrate

# Or use custom command
python manage.py run_migrations
```

### 2. Load Sample Data
```bash
# Load fixtures
python manage.py loaddata apps/recipes/fixtures/sample_data.json

# Or use custom command
python manage.py load_sample_data
```

### 3. Run Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.recipes.tests
python manage.py test apps.users.tests

# Run with verbose output
python manage.py test --verbosity=2
```

### 4. Access Admin Interface
```bash
# Create superuser (first time only)
python manage.py createsuperuser

# Start server
python manage.py runserver 8000

# Visit admin at
http://localhost:8000/admin/
```

## What Was Created

### Fixtures
- **Location**: `apps/recipes/fixtures/sample_data.json`
- **Contains**: Users, profiles, categories, ingredients, recipes, ratings, comments, favorites

### Tests
- **Location**: `apps/recipes/tests.py`, `apps/users/tests.py`
- **Coverage**: All model relationships and functionality

### Admin Enhancements
- **Location**: `apps/recipes/admin.py`, `apps/users/admin.py`
- **Features**: Enhanced displays, filters, search, inline editing, bulk actions

### Management Commands
- `load_sample_data` - Load fixtures easily
- `run_migrations` - Run migrations with options

## Test Coverage

### Recipe Models
- ✅ Category creation and relationships
- ✅ Ingredient creation and relationships
- ✅ Recipe creation and all relationships
- ✅ RecipeIngredient ManyToMany relationship
- ✅ Rating relationships and constraints
- ✅ Comment relationships
- ✅ Favorite relationships and constraints
- ✅ Integration tests for all relationships

### User Models
- ✅ CustomUser creation and authentication
- ✅ UserProfile OneToOne relationship
- ✅ User-Recipe relationships
- ✅ User-Rating relationships
- ✅ User-Comment relationships
- ✅ User-Favorite relationships

## Admin Features

### Recipe Admin
- List display with statistics
- Inline editing for ingredients, ratings, comments
- Bulk actions (publish/unpublish)
- Visual rating display with stars
- Computed fields (total time, rating, counts)

### User Admin
- Enhanced user list with email
- Profile admin with recipe count
- Inline editing for user's recipes

## Troubleshooting

### Database Connection Issues
- Check `.env` file for database credentials
- Project falls back to SQLite if PostgreSQL unavailable
- Use SQLite for local development/testing

### Migration Issues
```bash
# Check migration status
python manage.py showmigrations

# Fake initial migrations if tables exist
python manage.py migrate --fake-initial
```

### Fixture Loading Issues
- Ensure migrations are run first
- Check JSON syntax is valid
- Handle duplicate errors if loading multiple times

### Test Issues
- Tests use separate test database
- Ensure all dependencies installed
- Check test output for specific errors

