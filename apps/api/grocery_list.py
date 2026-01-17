"""
Grocery List Generation Utilities

Functions for generating grocery lists from meal plans
"""
from collections import defaultdict
from decimal import Decimal
from typing import Dict, List, Tuple
from apps.recipes.models import MealPlan, RecipeIngredient


# Ingredient categories for grouping
INGREDIENT_CATEGORIES = {
    'Produce': ['apple', 'banana', 'orange', 'lettuce', 'tomato', 'onion', 'garlic', 'carrot', 'celery', 'pepper', 'cucumber', 'potato', 'spinach', 'broccoli', 'cauliflower', 'mushroom', 'avocado', 'lemon', 'lime', 'herb', 'basil', 'parsley', 'cilantro', 'mint', 'thyme', 'rosemary', 'oregano'],
    'Dairy': ['milk', 'cheese', 'butter', 'cream', 'yogurt', 'sour cream', 'cottage cheese', 'mozzarella', 'cheddar', 'parmesan', 'feta'],
    'Meat & Seafood': ['chicken', 'beef', 'pork', 'turkey', 'fish', 'salmon', 'tuna', 'shrimp', 'bacon', 'sausage', 'ham', 'ground'],
    'Pantry': ['flour', 'sugar', 'salt', 'pepper', 'oil', 'vinegar', 'soy sauce', 'rice', 'pasta', 'noodle', 'bread', 'cereal', 'oat', 'quinoa', 'bean', 'lentil', 'chickpea'],
    'Spices & Seasonings': ['cumin', 'paprika', 'cinnamon', 'nutmeg', 'ginger', 'turmeric', 'coriander', 'cardamom', 'clove', 'bay leaf', 'chili', 'cayenne', 'red pepper'],
    'Baking': ['baking powder', 'baking soda', 'yeast', 'vanilla', 'cocoa', 'chocolate', 'chocolate chip'],
    'Beverages': ['juice', 'coffee', 'tea', 'soda', 'water'],
    'Frozen': ['frozen', 'ice cream'],
    'Other': []  # Default category
}


def categorize_ingredient(ingredient_name: str) -> str:
    """
    Categorize an ingredient based on its name
    
    Args:
        ingredient_name: Name of the ingredient
        
    Returns:
        Category name
    """
    ingredient_lower = ingredient_name.lower()
    
    for category, keywords in INGREDIENT_CATEGORIES.items():
        if category == 'Other':
            continue
        for keyword in keywords:
            if keyword in ingredient_lower:
                return category
    
    return 'Other'


def normalize_unit(unit: str) -> str:
    """
    Normalize unit names for better aggregation
    
    Args:
        unit: Unit string
        
    Returns:
        Normalized unit string
    """
    if not unit:
        return ''
    
    unit_lower = unit.lower().strip()
    
    # Normalize common variations
    unit_mapping = {
        'tbsp': 'tablespoon',
        'tbs': 'tablespoon',
        'tbsp.': 'tablespoon',
        'tbs.': 'tablespoon',
        'tsp': 'teaspoon',
        'tsp.': 'teaspoon',
        'cup': 'cup',
        'cups': 'cup',
        'c': 'cup',
        'c.': 'cup',
        'lb': 'pound',
        'lbs': 'pound',
        'lb.': 'pound',
        'lbs.': 'pound',
        'oz': 'ounce',
        'oz.': 'ounce',
        'ounce': 'ounce',
        'ounces': 'ounce',
        'g': 'gram',
        'gram': 'gram',
        'grams': 'gram',
        'kg': 'kilogram',
        'kilogram': 'kilogram',
        'ml': 'milliliter',
        'milliliter': 'milliliter',
        'l': 'liter',
        'liter': 'liter',
        'piece': 'piece',
        'pieces': 'piece',
        'pcs': 'piece',
        'pc': 'piece',
        'clove': 'clove',
        'cloves': 'clove',
        'head': 'head',
        'heads': 'head',
    }
    
    return unit_mapping.get(unit_lower, unit)


def can_aggregate_quantities(unit1: str, unit2: str) -> bool:
    """
    Check if two units can be aggregated (same unit type)
    
    Args:
        unit1: First unit
        unit2: Second unit
        
    Returns:
        True if units can be aggregated
    """
    unit1_norm = normalize_unit(unit1)
    unit2_norm = normalize_unit(unit2)
    
    # Same unit can be aggregated
    if unit1_norm == unit2_norm:
        return True
    
    # Empty units can be aggregated if both are empty
    if not unit1_norm and not unit2_norm:
        return True
    
    # Different units cannot be aggregated
    return False


def generate_grocery_list(meal_plans: List[MealPlan]) -> Dict:
    """
    Generate a grocery list from meal plans
    
    Args:
        meal_plans: List of MealPlan objects
        
    Returns:
        Dictionary with grocery list data:
        {
            'ingredients_by_category': {
                'category_name': [
                    {
                        'name': 'ingredient name',
                        'total_quantity': Decimal,
                        'unit': 'unit',
                        'recipes': ['recipe1', 'recipe2'],
                        'notes': ['note1', 'note2']
                    }
                ]
            },
            'total_items': int,
            'date_range': {'start': date, 'end': date}
        }
    """
    # Dictionary to aggregate ingredients: (name, unit) -> (total_quantity, recipes, notes)
    ingredient_dict = defaultdict(lambda: {
        'total_quantity': Decimal('0'),
        'unit': '',
        'recipes': set(),
        'notes': []
    })
    
    # Track date range
    dates = [mp.date for mp in meal_plans]
    start_date = min(dates) if dates else None
    end_date = max(dates) if dates else None
    
    # Collect ingredients from all meal plans
    for meal_plan in meal_plans:
        recipe = meal_plan.recipe
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe).select_related('ingredient')
        
        for recipe_ingredient in recipe_ingredients:
            ingredient_name = recipe_ingredient.ingredient.name
            quantity = recipe_ingredient.quantity
            unit = recipe_ingredient.unit or ''
            notes = recipe_ingredient.notes or ''
            
            # Normalize unit
            normalized_unit = normalize_unit(unit)
            
            # Create key for aggregation (name + normalized unit)
            key = (ingredient_name.lower(), normalized_unit)
            
            # Aggregate quantities
            ingredient_dict[key]['total_quantity'] += quantity
            ingredient_dict[key]['unit'] = normalized_unit if normalized_unit else unit
            ingredient_dict[key]['recipes'].add(recipe.title)
            if notes:
                ingredient_dict[key]['notes'].append(notes)
    
    # Group by category
    ingredients_by_category = defaultdict(list)
    
    # Create a mapping of lowercase names to original names (more efficient)
    ingredient_name_map = {}
    for meal_plan in meal_plans:
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=meal_plan.recipe).select_related('ingredient')
        for ri in recipe_ingredients:
            name_lower = ri.ingredient.name.lower()
            if name_lower not in ingredient_name_map:
                ingredient_name_map[name_lower] = ri.ingredient.name
    
    for (ingredient_name_lower, unit), data in ingredient_dict.items():
        # Get original ingredient name from map
        ingredient_name = ingredient_name_map.get(ingredient_name_lower, ingredient_name_lower.title())
        
        category = categorize_ingredient(ingredient_name)
        
        ingredients_by_category[category].append({
            'name': ingredient_name,
            'total_quantity': float(data['total_quantity']),
            'unit': data['unit'],
            'recipes': sorted(list(data['recipes'])),
            'notes': list(set(data['notes'])) if data['notes'] else [],
        })
    
    # Sort ingredients within each category by name
    for category in ingredients_by_category:
        ingredients_by_category[category].sort(key=lambda x: x['name'].lower())
    
    # Sort categories
    category_order = list(INGREDIENT_CATEGORIES.keys()) + ['Other']
    sorted_categories = sorted(
        ingredients_by_category.keys(),
        key=lambda x: (category_order.index(x) if x in category_order else 999, x)
    )
    
    # Create ordered dictionary
    ordered_ingredients = {
        category: ingredients_by_category[category]
        for category in sorted_categories
    }
    
    # Calculate total items
    total_items = sum(len(items) for items in ordered_ingredients.values())
    
    return {
        'ingredients_by_category': ordered_ingredients,
        'total_items': total_items,
        'date_range': {
            'start': start_date.isoformat() if start_date else None,
            'end': end_date.isoformat() if end_date else None,
        },
        'meal_plans_count': len(meal_plans),
    }

