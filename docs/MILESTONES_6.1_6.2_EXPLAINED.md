# Milestones 6.1 & 6.2 Explained - Complete Guide

## 📚 Overview

This document explains **Milestone 6.1** (REST API Setup) and **Milestone 6.2** (API Endpoints Implementation), and shows you how to access all the API endpoints including meal plans.

---

## 🎯 Milestone 6.1: REST API Setup

### What is Milestone 6.1?

**Milestone 6.1** is about **setting up the foundation** for your REST API. Think of it as building the infrastructure that allows your application to communicate with other applications, mobile apps, or external services.

### What Was Implemented?

#### 1. **Django REST Framework (DRF) Installation** ✅
- **What it is**: A powerful toolkit for building Web APIs in Django
- **Why it matters**: Makes it easy to create REST APIs without writing everything from scratch
- **Status**: Already installed (version 3.14.0)

#### 2. **Serializers** ✅
- **What they are**: Converters that transform your Django models (database data) into JSON format that APIs can understand
- **Examples**:
  - `RecipeSerializer` - Converts recipe data to/from JSON
  - `UserSerializer` - Converts user data to/from JSON
  - `IngredientSerializer` - Converts ingredient data to/from JSON
- **Why it matters**: APIs need data in JSON format, not Django model format

#### 3. **API Authentication** ✅
Three ways to authenticate API requests:

**a) Token Authentication**
- **How it works**: You get a token (like a key) by logging in, then use that token for all API requests
- **Endpoints**:
  - `POST /api/auth/token/obtain/` - Get your token
  - `POST /api/auth/token/revoke/` - Delete your token
- **Use case**: Simple API clients, scripts

**b) JWT Authentication** (JSON Web Tokens)
- **How it works**: More secure tokens that expire and can be refreshed
- **Endpoints**:
  - `POST /api/auth/token/` - Get access + refresh tokens
  - `POST /api/auth/token/refresh/` - Get new access token
  - `POST /api/auth/token/verify/` - Check if token is valid
- **Use case**: Mobile apps, modern web apps
- **Features**: 
  - Access token expires in 1 hour
  - Refresh token expires in 7 days
  - Automatic token rotation

**c) Session Authentication**
- **How it works**: Uses browser cookies (like regular website login)
- **Use case**: Web frontend (your Next.js app)

#### 4. **API Documentation (Swagger/OpenAPI)** ✅
- **What it is**: Interactive documentation that shows all your API endpoints
- **Where to access**:
  - **Swagger UI**: http://127.0.0.1:8000/api/docs/
  - **ReDoc**: http://127.0.0.1:8000/api/redoc/
  - **Schema**: http://127.0.0.1:8000/api/schema/
- **Why it matters**: You can test APIs directly in the browser, see all available endpoints, and understand what data to send/receive

### Summary of Milestone 6.1

**Milestone 6.1 = Building the API Foundation**
- ✅ Installed Django REST Framework
- ✅ Created serializers for all models
- ✅ Set up 3 authentication methods
- ✅ Created interactive API documentation

**Think of it as**: Setting up the plumbing and electrical systems before building the house.

---

## 🎯 Milestone 6.2: API Endpoints Implementation

### What is Milestone 6.2?

**Milestone 6.2** is about **creating the actual API endpoints** that your frontend or external applications can call. These are the specific URLs that return data or perform actions.

### What Was Implemented?

#### Core Recipe Endpoints ✅

1. **GET /api/recipes/** - List all recipes
   - **What it does**: Returns a list of recipes with pagination
   - **Filters available**: search, category, author, ingredients, time, dietary restrictions, sorting
   - **Public**: Yes (anyone can view)

2. **GET /api/recipes/{id}/** - Get single recipe
   - **What it does**: Returns detailed information about one recipe
   - **Public**: Yes

3. **GET /api/recipes/search/** - Search recipes
   - **What it does**: Search recipes with filters
   - **Example**: `/api/recipes/search/?search=pasta&max_prep_time=30`
   - **Public**: Yes

4. **GET /api/recipes/by-ingredients/** - Find recipes by ingredients
   - **What it does**: Find recipes that contain specific ingredients
   - **Features**: 
     - `match_all=false` (default): Recipe contains ANY ingredient
     - `match_all=true`: Recipe contains ALL ingredients
   - **Example**: `/api/recipes/by-ingredients/?ingredients=chicken,tomato&match_all=true`
   - **Public**: Yes

5. **POST /api/recipes/** - Create recipe
   - **What it does**: Create a new recipe
   - **Authentication**: Required
   - **Example**: Send JSON data with recipe details

6. **GET /api/recipes/export/** - Export recipes
   - **What it does**: Export recipes as JSON or CSV file
   - **Formats**: JSON (default) or CSV
   - **Example**: `/api/recipes/export/?format=csv&category=1`
   - **Public**: Yes

#### User Endpoints ✅

7. **GET /api/user/favorites/** - Get user's favorite recipes
   - **What it does**: Returns all recipes the current user has favorited
   - **Authentication**: Required
   - **Pagination**: Yes (20 per page)

8. **GET /api/users/me/** - Get current user info
   - **What it does**: Returns information about the logged-in user
   - **Authentication**: Required

#### Meal Plan Endpoints ✅

9. **GET /api/meal-plans/** - Get meal plans
   - **What it does**: Returns meal plans for the current user
   - **Authentication**: Required
   - **Filters**: 
     - `start_date`: Filter from date (YYYY-MM-DD)
     - `end_date`: Filter to date (YYYY-MM-DD)
     - `meal_type`: Filter by meal type (breakfast, lunch, dinner, snack, dessert)
   - **Example**: `/api/meal-plans/?start_date=2024-01-01&end_date=2024-01-31`

10. **POST /api/meal-plans/** - Create meal plan
    - **What it does**: Add a recipe to meal plan for a specific date
    - **Authentication**: Required

11. **GET /api/meal-plans/grocery-list/** - Generate grocery list
    - **What it does**: Creates a grocery list from planned meals
    - **Formats**: JSON (default), TXT, or PDF
    - **Example**: `/api/meal-plans/grocery-list/?start_date=2024-01-01&end_date=2024-01-31&format=pdf`
    - **Authentication**: Required

12. **GET /api/meal-plans/export/ical/** - Export meal plan as iCal
    - **What it does**: Exports meal plans as .ics file (for Google Calendar, Outlook, etc.)
    - **Authentication**: Required

### Summary of Milestone 6.2

**Milestone 6.2 = Creating the API Endpoints**
- ✅ Recipe CRUD endpoints (Create, Read, Update, Delete)
- ✅ Recipe search and filtering endpoints
- ✅ Ingredient-based search endpoint
- ✅ User favorites endpoint
- ✅ Meal plan endpoints
- ✅ Export functionality (JSON, CSV, PDF, iCal)

**Think of it as**: Building the rooms and features of the house after the foundation is ready.

---

## 🔗 How to Access API Endpoints

### Step 1: Start Your Django Server

```bash
python manage.py runserver
```

Your API will be available at: **http://127.0.0.1:8000/api/**

### Step 2: Access Interactive Documentation

**Option A: Swagger UI** (Recommended for testing)
```
http://127.0.0.1:8000/api/docs/
```
- Interactive interface
- Test endpoints directly in browser
- See request/response examples
- Try authentication

**Option B: ReDoc** (Better for reading)
```
http://127.0.0.1:8000/api/redoc/
```
- Clean, readable documentation
- Better for understanding API structure

### Step 3: Access Meal Plans API

#### Get All Meal Plans
```bash
# Using curl
curl -H "Authorization: Bearer <your-token>" \
     "http://127.0.0.1:8000/api/meal-plans/"

# Or in browser (if logged in via session)
http://127.0.0.1:8000/api/meal-plans/
```

#### Get Meal Plans for Date Range
```bash
curl -H "Authorization: Bearer <your-token>" \
     "http://127.0.0.1:8000/api/meal-plans/?start_date=2024-01-01&end_date=2024-01-31"
```

#### Generate Grocery List
```bash
# As JSON
curl -H "Authorization: Bearer <your-token>" \
     "http://127.0.0.1:8000/api/meal-plans/grocery-list/?start_date=2024-01-01&end_date=2024-01-31"

# As PDF
curl -H "Authorization: Bearer <your-token>" \
     "http://127.0.0.1:8000/api/meal-plans/grocery-list/?start_date=2024-01-01&end_date=2024-01-31&format=pdf" \
     -o grocery_list.pdf

# As Text
curl -H "Authorization: Bearer <your-token>" \
     "http://127.0.0.1:8000/api/meal-plans/grocery-list/?start_date=2024-01-01&end_date=2024-01-31&format=txt" \
     -o grocery_list.txt
```

### Step 4: Get Authentication Token

#### Option A: JWT Token (Recommended)
```bash
# Get tokens
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Response:
# {
#   "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
# }

# Use access token
curl -H "Authorization: Bearer <access-token>" \
     "http://127.0.0.1:8000/api/meal-plans/"
```

#### Option B: Token Authentication
```bash
# Get token
curl -X POST http://127.0.0.1:8000/api/auth/token/obtain/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Response:
# {
#   "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
#   "user": {...}
# }

# Use token
curl -H "Authorization: Token <your-token>" \
     "http://127.0.0.1:8000/api/meal-plans/"
```

---

## 📋 Complete API Endpoint List

### Public Endpoints (No Authentication Required)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/recipes/` | GET | List all recipes |
| `/api/recipes/{id}/` | GET | Get recipe details |
| `/api/recipes/search/` | GET | Search recipes |
| `/api/recipes/by-ingredients/` | GET | Find recipes by ingredients |
| `/api/recipes/export/` | GET | Export recipes (JSON/CSV) |
| `/api/ingredients/` | GET | List ingredients |
| `/api/ratings/` | GET | List ratings |
| `/api/comments/` | GET | List comments |
| `/api/docs/` | GET | Swagger UI documentation |
| `/api/redoc/` | GET | ReDoc documentation |
| `/api/schema/` | GET | OpenAPI schema |

### Protected Endpoints (Authentication Required)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/recipes/` | POST | Create recipe |
| `/api/recipes/{id}/` | PUT/PATCH | Update recipe |
| `/api/recipes/{id}/` | DELETE | Delete recipe |
| `/api/user/favorites/` | GET | Get user's favorites |
| `/api/favorites/` | POST | Toggle favorite |
| `/api/meal-plans/` | GET | Get meal plans |
| `/api/meal-plans/` | POST | Create meal plan |
| `/api/meal-plans/{id}/` | PUT/PATCH | Update meal plan |
| `/api/meal-plans/{id}/` | DELETE | Delete meal plan |
| `/api/meal-plans/grocery-list/` | GET | Generate grocery list |
| `/api/meal-plans/export/ical/` | GET | Export iCal |
| `/api/users/me/` | GET | Get current user |
| `/api/ratings/` | POST | Create rating |
| `/api/comments/` | POST | Create comment |

---

## 🧪 Quick Test Examples

### Test 1: View All Recipes (No Auth Needed)
```bash
curl http://127.0.0.1:8000/api/recipes/
```

### Test 2: Search Recipes
```bash
curl "http://127.0.0.1:8000/api/recipes/search/?search=pasta&max_prep_time=30"
```

### Test 3: Get Meal Plans (Auth Required)
```bash
# First, get token
TOKEN=$(curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your_user","password":"your_pass"}' | jq -r '.access')

# Then use token
curl -H "Authorization: Bearer $TOKEN" \
     "http://127.0.0.1:8000/api/meal-plans/"
```

### Test 4: Generate Grocery List PDF
```bash
curl -H "Authorization: Bearer $TOKEN" \
     "http://127.0.0.1:8000/api/meal-plans/grocery-list/?format=pdf&start_date=2024-01-01&end_date=2024-01-31" \
     -o my_grocery_list.pdf
```

---

## 🎓 Key Concepts Explained

### What is a REST API?
- **REST** = Representational State Transfer
- **API** = Application Programming Interface
- **In simple terms**: A way for different applications to talk to each other using HTTP requests (GET, POST, PUT, DELETE)

### What is a Serializer?
- Converts Django models ↔ JSON
- Validates incoming data
- Formats outgoing data
- **Think of it as**: A translator between your database and the API

### What is Authentication?
- **Token**: A string that proves you're logged in
- **JWT**: A more secure token that expires and can be refreshed
- **Session**: Browser cookies (like regular website login)

### What is Pagination?
- When you have many results, they're split into pages
- Default: 20 items per page
- Prevents loading too much data at once

---

## 📖 Summary

### Milestone 6.1: REST API Setup
**Purpose**: Build the foundation for APIs
- ✅ Installed Django REST Framework
- ✅ Created serializers
- ✅ Set up authentication (Token, JWT, Session)
- ✅ Created API documentation

### Milestone 6.2: API Endpoints Implementation
**Purpose**: Create the actual API endpoints
- ✅ Recipe endpoints (CRUD, search, export)
- ✅ User endpoints (favorites, profile)
- ✅ Meal plan endpoints (CRUD, grocery list, iCal export)

### How to Access
1. Start server: `python manage.py runserver`
2. Visit Swagger: http://127.0.0.1:8000/api/docs/
3. Test endpoints directly in browser
4. Use authentication tokens for protected endpoints

---

## 🚀 Next Steps

1. **Explore Swagger UI**: Visit http://127.0.0.1:8000/api/docs/ and try endpoints
2. **Test Authentication**: Get a token and try protected endpoints
3. **Test Meal Plans**: Create meal plans and generate grocery lists
4. **Integrate with Frontend**: Use these endpoints in your Next.js app

---

## 💡 Tips

- **Swagger UI** is your best friend for testing APIs
- **JWT tokens** expire after 1 hour - use refresh token to get new ones
- **All endpoints support pagination** - use `?page=2` for next page
- **Export endpoints** return files - use `-o filename` with curl to save
- **Meal plan endpoints** require authentication - make sure you're logged in

