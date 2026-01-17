# Meal Planner API Documentation

## Overview

This documentation is specifically designed for **meal planner app developers** who want to integrate with the Recipe Sharing Platform API.

---

## 🔑 Authentication

### API Key Authentication

Meal planner apps should use **API Key authentication** to access the Recipe Sharing Platform API.

#### Getting an API Key

1. **Create an account** on the Recipe Sharing Platform
2. **Generate an API Key**:
   ```bash
   POST /api/api-keys/
   Authorization: Bearer <user-token>
   Content-Type: application/json
   
   {
     "name": "My Meal Planner App",
     "expires_at": "2025-12-31T23:59:59Z"  # Optional
   }
   ```
3. **Save the API key** - you'll only see it once!

#### Using API Keys

Include your API key in requests using one of these methods:

**Option 1: Header (Recommended)**
```bash
X-API-Key: your-api-key-here
```

**Option 2: Query Parameter**
```bash
GET /api/recipes/?api_key=your-api-key-here
```

#### Example Request

```bash
curl -H "X-API-Key: your-api-key-here" \
     "http://127.0.0.1:8000/api/recipes/"
```

---

## 📋 API Endpoints for Meal Planners

### 1. List Recipes

**Endpoint**: `GET /api/recipes/`

**Description**: Get a list of all recipes with filtering options

**Query Parameters**:
- `search`: Text search in title, description, instructions
- `category`: Category ID filter
- `max_prep_time`: Maximum preparation time (minutes)
- `max_cook_time`: Maximum cooking time (minutes)
- `dietary`: Dietary restriction filter (vegetarian, vegan, gluten-free, etc.)
- `ingredients`: Comma-separated ingredient names
- `sort`: Sort order (newest, oldest, rating, views, title)
- `page`: Page number (default: 1, 20 items per page)

**Example**:
```bash
GET /api/recipes/?search=pasta&max_prep_time=30&dietary=vegetarian&sort=rating
```

**Response**:
```json
{
  "count": 50,
  "next": "http://api.example.com/api/recipes/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Vegetarian Pasta",
      "description": "Delicious pasta recipe",
      "prep_time": 15,
      "cook_time": 20,
      "total_time": 35,
      "category": {"id": 1, "name": "Dinner"},
      "recipe_ingredients": [
        {
          "ingredient": {"id": 1, "name": "pasta"},
          "quantity": 500,
          "unit": "g"
        }
      ],
      "average_rating": 4.5,
      "rating_count": 10
    }
  ]
}
```

---

### 2. Get Single Recipe

**Endpoint**: `GET /api/recipes/{id}/`

**Description**: Get detailed information about a specific recipe

**Example**:
```bash
GET /api/recipes/1/
```

**Response**: Full recipe object with all details

---

### 3. Export Recipe for Meal Planner

**Endpoint**: `GET /api/recipes/{id}/export-meal-planner/`

**Description**: Export a single recipe in meal planner compatible format

**Query Parameters**:
- `format`: Export format (`json`, `recipeml`, `xml`) - default: `json`
- `app`: Target meal planner app (`paprika`, `mealime`, `anylist`, `generic`) - default: `generic`

**Example**:
```bash
# Export as RecipeML (standard format)
GET /api/recipes/1/export-meal-planner/?format=recipeml

# Export for Paprika Recipe Manager
GET /api/recipes/1/export-meal-planner/?format=json&app=paprika

# Export for Mealime
GET /api/recipes/1/export-meal-planner/?format=json&app=mealime
```

**Response Formats**:

**RecipeML (XML)**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<recipeml version="0.5">
  <recipe>
    <head>
      <title>Vegetarian Pasta</title>
      <description>Delicious pasta recipe</description>
      <times>
        <prep>PT15M</prep>
        <cook>PT20M</cook>
      </times>
    </head>
    <ingredients>
      <ing>
        <item>
          <amt><qty>500</qty><unit>g</unit></amt>
          <item>pasta</item>
        </item>
      </ing>
    </ingredients>
    <directions>
      <step>
        <step number="1">Boil water</step>
        <step number="2">Add pasta</step>
      </step>
    </directions>
  </recipe>
</recipeml>
```

**Paprika Format (JSON)**:
```json
{
  "name": "Vegetarian Pasta",
  "description": "Delicious pasta recipe",
  "prep_time": 15,
  "cook_time": 20,
  "category": "Dinner",
  "ingredients": [
    "500 g pasta",
    "2 tomatoes",
    "1 onion"
  ],
  "directions": [
    "Boil water",
    "Add pasta",
    "Cook for 10 minutes"
  ]
}
```

**Mealime Format (JSON)**:
```json
{
  "title": "Vegetarian Pasta",
  "description": "Delicious pasta recipe",
  "prep_time_minutes": 15,
  "cook_time_minutes": 20,
  "ingredients": [
    {
      "name": "pasta",
      "amount": 500,
      "unit": "g"
    }
  ],
  "instructions": [
    "Boil water",
    "Add pasta"
  ]
}
```

---

### 4. Search Recipes

**Endpoint**: `GET /api/recipes/search/`

**Description**: Search recipes with comprehensive filters

**Query Parameters**: Same as list endpoint

**Example**:
```bash
GET /api/recipes/search/?search=chicken&max_prep_time=30&dietary=gluten-free
```

---

### 5. Search by Ingredients

**Endpoint**: `GET /api/recipes/by-ingredients/`

**Description**: Find recipes that contain specific ingredients

**Query Parameters**:
- `ingredients`: Comma-separated list of ingredient names (required)
- `match_all`: If `true`, recipe must contain ALL ingredients; if `false` (default), recipe must contain ANY ingredient

**Example**:
```bash
# Find recipes with ANY of these ingredients
GET /api/recipes/by-ingredients/?ingredients=chicken,tomato,onion

# Find recipes with ALL of these ingredients
GET /api/recipes/by-ingredients/?ingredients=chicken,tomato,onion&match_all=true
```

---

### 6. Export Multiple Recipes

**Endpoint**: `GET /api/recipes/export/`

**Description**: Export multiple recipes in bulk

**Query Parameters**:
- `format`: Export format (`json`, `csv`, `recipeml`, `xml`) - default: `json`
- All filtering parameters from list endpoint

**Example**:
```bash
# Export all vegetarian recipes as RecipeML
GET /api/recipes/export/?format=recipeml&dietary=vegetarian

# Export as CSV
GET /api/recipes/export/?format=csv&category=1
```

---

## 🔄 Recipe Format Compatibility

### Supported Formats

1. **JSON** (Default)
   - Standard API response format
   - Works with most modern meal planner apps

2. **RecipeML** (XML)
   - Standard recipe format (RecipeML 0.5)
   - Compatible with many meal planner apps
   - Use `format=recipeml` or `format=xml`

3. **CSV**
   - Simple spreadsheet format
   - Good for bulk imports
   - Use `format=csv`

### App-Specific Formats

- **Paprika Recipe Manager**: Use `app=paprika`
- **Mealime**: Use `app=mealime`
- **AnyList**: Use `app=anylist` (generic JSON format)
- **Generic**: Use `app=generic` (default API format)

---

## 📊 Rate Limits

Currently, there are **no rate limits** on API requests. However, please be respectful:
- Don't make excessive requests
- Cache responses when possible
- Use pagination for large datasets

---

## 🛠️ Integration Examples

### Python Example

```python
import requests

API_KEY = "your-api-key-here"
BASE_URL = "http://127.0.0.1:8000/api"

headers = {
    "X-API-Key": API_KEY
}

# Get recipes
response = requests.get(
    f"{BASE_URL}/recipes/",
    headers=headers,
    params={"dietary": "vegetarian", "max_prep_time": 30}
)

recipes = response.json()

# Export recipe for meal planner
recipe_id = recipes["results"][0]["id"]
export_response = requests.get(
    f"{BASE_URL}/recipes/{recipe_id}/export-meal-planner/",
    headers=headers,
    params={"format": "recipeml"}
)

recipeml_xml = export_response.text
# Save to file or import into meal planner app
```

### JavaScript Example

```javascript
const API_KEY = "your-api-key-here";
const BASE_URL = "http://127.0.0.1:8000/api";

// Get recipes
const response = await fetch(
  `${BASE_URL}/recipes/?dietary=vegetarian&max_prep_time=30`,
  {
    headers: {
      "X-API-Key": API_KEY
    }
  }
);

const data = await response.json();

// Export recipe for meal planner
const recipeId = data.results[0].id;
const exportResponse = await fetch(
  `${BASE_URL}/recipes/${recipeId}/export-meal-planner/?format=recipeml`,
  {
    headers: {
      "X-API-Key": API_KEY
    }
  }
);

const recipemlXml = await exportResponse.text();
// Save to file or import into meal planner app
```

---

## 🐛 Error Handling

### Common Error Responses

**401 Unauthorized**:
```json
{
  "detail": "Invalid API key"
}
```

**404 Not Found**:
```json
{
  "detail": "Not found."
}
```

**400 Bad Request**:
```json
{
  "error": "Invalid parameters"
}
```

---

## 📝 Best Practices

1. **Cache Responses**: Don't fetch the same recipe multiple times
2. **Use Pagination**: Fetch recipes in pages, not all at once
3. **Handle Errors**: Always check for error responses
4. **Respect Rate Limits**: Don't make excessive requests
5. **Store API Keys Securely**: Never expose API keys in client-side code

---

## 🔗 Additional Resources

- **API Documentation**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **API Root**: http://127.0.0.1:8000/api/

---

## 💬 Support

For questions or issues:
1. Check the main API documentation at `/api/docs/`
2. Review error messages carefully
3. Test with Swagger UI first
4. Contact support if needed

---

## 📄 License

API access is subject to the Recipe Sharing Platform Terms of Service.

