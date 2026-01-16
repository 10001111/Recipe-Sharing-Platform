'use client';

import { useEffect, useState, useCallback } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { recipeApi, RecipeList } from '@/lib/api';
import SearchAutocomplete from '@/components/SearchAutocomplete';
import RecipeCard from '@/components/RecipeCard';

type SortOption = 'newest' | 'oldest' | 'rating' | 'views' | 'title';
type DietaryOption = 'all' | 'none' | 'vegetarian' | 'vegan' | 'gluten-free' | 'keto' | 'paleo' | 'pescatarian' | 'halal' | 'kosher';

export default function RecipesPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const [recipes, setRecipes] = useState<RecipeList[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState(searchParams.get('search') || '');
  const [category, setCategory] = useState(searchParams.get('category') || 'all');
  const [sortBy, setSortBy] = useState<SortOption>((searchParams.get('sort') as SortOption) || 'newest');
  const [ingredients, setIngredients] = useState(searchParams.get('ingredients') || '');
  const [maxPrepTime, setMaxPrepTime] = useState(searchParams.get('max_prep_time') || '');
  const [maxCookTime, setMaxCookTime] = useState(searchParams.get('max_cook_time') || '');
  const [maxTotalTime, setMaxTotalTime] = useState(searchParams.get('max_total_time') || '');
  const [dietary, setDietary] = useState<DietaryOption>((searchParams.get('dietary') as DietaryOption) || 'all');
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);

  const loadRecipes = useCallback(async () => {
    try {
      setLoading(true);
      const params: any = {};
      
      if (searchQuery.trim()) {
        params.search = searchQuery.trim();
      }
      if (category !== 'all') {
        params.category = category;
      }
      if (sortBy) {
        params.sort = sortBy;
      }
      if (ingredients.trim()) {
        params.ingredients = ingredients.trim();
      }
      if (maxPrepTime) {
        params.max_prep_time = parseInt(maxPrepTime);
      }
      if (maxCookTime) {
        params.max_cook_time = parseInt(maxCookTime);
      }
      if (maxTotalTime) {
        params.max_total_time = parseInt(maxTotalTime);
      }
      if (dietary !== 'all') {
        params.dietary = dietary;
      }

      const response = await recipeApi.getAll(params);
      const recipesData = response.results || response;
      
      const normalizedRecipes = Array.isArray(recipesData) ? recipesData.map((recipe: any) => ({
        ...recipe,
        view_count: Number(recipe.view_count || 0),
        comment_count: Number(recipe.comment_count || 0),
        favorite_count: Number(recipe.favorite_count || 0),
        rating_count: Number(recipe.rating_count || 0),
        average_rating: Number(recipe.average_rating || 0),
      })) : [];
      
      setRecipes(normalizedRecipes);
    } catch (error: any) {
      console.error('Error loading recipes:', error);
    } finally {
      setLoading(false);
    }
  }, [searchQuery, category, sortBy, ingredients, maxPrepTime, maxCookTime, maxTotalTime, dietary]);

  // Load recipes on initial mount
  useEffect(() => {
    loadRecipes();
  }, []);

  const handleSearchSelect = (recipe: RecipeList) => {
    router.push(`/recipes/${recipe.id}`);
  };

  const clearFilters = () => {
    setSearchQuery('');
    setCategory('all');
    setSortBy('newest');
    setIngredients('');
    setMaxPrepTime('');
    setMaxCookTime('');
    setMaxTotalTime('');
    setDietary('all');
    setShowAdvancedFilters(false);
  };

  const hasActiveFilters = category !== 'all' || searchQuery || ingredients || maxPrepTime || maxCookTime || maxTotalTime || dietary !== 'all';

  return (
    <main className="container">
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2rem', marginBottom: '1.5rem' }}>All Recipes</h1>
        
        {/* Search and Filters */}
        <div style={{ 
          background: 'white', 
          padding: '1.5rem', 
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          marginBottom: '2rem'
        }}>
          {/* Basic Filters */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1rem' }}>
            <div style={{ gridColumn: '1 / -1' }}>
              <label className="form-label" style={{ marginBottom: '0.5rem' }}>Search Recipes</label>
              <input
                type="text"
                className="form-input"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by title or description..."
                style={{ width: '100%' }}
              />
            </div>
            
            <div>
              <label className="form-label" style={{ marginBottom: '0.5rem' }}>Category</label>
              <select
                value={category}
                onChange={(e) => {
                  e.preventDefault();
                  setCategory(e.target.value);
                }}
                className="form-select"
                style={{ width: '100%', zIndex: 1 }}
                onBlur={(e) => e.stopPropagation()}
              >
                <option value="all">All Categories</option>
                <option value="breakfast">Breakfast</option>
                <option value="lunch">Lunch</option>
                <option value="dinner">Dinner</option>
                <option value="dessert">Dessert</option>
                <option value="snack">Snack</option>
              </select>
            </div>

            <div>
              <label className="form-label" style={{ marginBottom: '0.5rem' }}>Sort By</label>
              <select
                value={sortBy}
                onChange={(e) => {
                  e.preventDefault();
                  setSortBy(e.target.value as SortOption);
                }}
                className="form-select"
                style={{ width: '100%', zIndex: 1 }}
                onBlur={(e) => e.stopPropagation()}
              >
                <option value="newest">Newest First</option>
                <option value="oldest">Oldest First</option>
                <option value="rating">Highest Rated</option>
                <option value="views">Most Viewed</option>
                <option value="title">Title (A-Z)</option>
              </select>
            </div>

            <div>
              <label className="form-label" style={{ marginBottom: '0.5rem' }}>Dietary Restrictions</label>
              <select
                value={dietary}
                onChange={(e) => {
                  e.preventDefault();
                  setDietary(e.target.value as DietaryOption);
                }}
                className="form-select"
                style={{ width: '100%', zIndex: 1 }}
                onBlur={(e) => e.stopPropagation()}
              >
                <option value="all">All</option>
                <option value="none">No Restrictions</option>
                <option value="vegetarian">Vegetarian</option>
                <option value="vegan">Vegan</option>
                <option value="gluten-free">Gluten-Free</option>
                <option value="keto">Keto</option>
                <option value="paleo">Paleo</option>
                <option value="pescatarian">Pescatarian</option>
                <option value="halal">Halal</option>
                <option value="kosher">Kosher</option>
              </select>
            </div>
          </div>

          {/* Advanced Filters Toggle */}
          <div style={{ marginBottom: '1rem' }}>
            <button
              type="button"
              onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
              className="btn-outline"
              style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}
            >
              {showAdvancedFilters ? '▼' : '▶'} Advanced Filters
            </button>
          </div>

          {/* Advanced Filters */}
          {showAdvancedFilters && (
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
              gap: '1rem',
              padding: '1rem',
              background: '#f8f9fa',
              borderRadius: '8px',
              marginBottom: '1rem'
            }}>
              <div>
                <label className="form-label" style={{ marginBottom: '0.5rem' }}>Ingredients (comma-separated)</label>
                <input
                  type="text"
                  className="form-input"
                  value={ingredients}
                  onChange={(e) => setIngredients(e.target.value)}
                  placeholder="e.g., chicken, tomato, onion"
                  style={{ width: '100%' }}
                />
                <small style={{ color: '#666', fontSize: '0.85rem' }}>Find recipes with these ingredients</small>
              </div>

              <div>
                <label className="form-label" style={{ marginBottom: '0.5rem' }}>Max Prep Time (minutes)</label>
                <input
                  type="number"
                  className="form-input"
                  value={maxPrepTime}
                  onChange={(e) => setMaxPrepTime(e.target.value)}
                  placeholder="e.g., 30"
                  min="0"
                  style={{ width: '100%' }}
                />
              </div>

              <div>
                <label className="form-label" style={{ marginBottom: '0.5rem' }}>Max Cook Time (minutes)</label>
                <input
                  type="number"
                  className="form-input"
                  value={maxCookTime}
                  onChange={(e) => setMaxCookTime(e.target.value)}
                  placeholder="e.g., 60"
                  min="0"
                  style={{ width: '100%' }}
                />
              </div>

              <div>
                <label className="form-label" style={{ marginBottom: '0.5rem' }}>Max Total Time (minutes)</label>
                <input
                  type="number"
                  className="form-input"
                  value={maxTotalTime}
                  onChange={(e) => setMaxTotalTime(e.target.value)}
                  placeholder="e.g., 90"
                  min="0"
                  style={{ width: '100%' }}
                />
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            {hasActiveFilters && (
              <button
                onClick={clearFilters}
                className="btn-outline"
                style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}
              >
                Clear All Filters
              </button>
            )}
            <button
              onClick={() => loadRecipes()}
              className="btn-primary"
              style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}
            >
              Apply Filters
            </button>
          </div>

          {/* Results count */}
          <div style={{ 
            paddingTop: '1rem', 
            borderTop: '1px solid #e0e0e0',
            fontSize: '0.9rem',
            color: '#666',
            marginTop: '1rem'
          }}>
            Showing {recipes.length} recipe{recipes.length !== 1 ? 's' : ''}
            {category !== 'all' && ` in ${category}`}
            {searchQuery && ` matching "${searchQuery}"`}
            {ingredients && ` with ingredients: ${ingredients}`}
            {dietary !== 'all' && ` (${dietary})`}
          </div>
        </div>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <p>Loading recipes...</p>
        </div>
      ) : recipes.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ fontSize: '1.2rem', color: '#666', marginBottom: '1rem' }}>
            No recipes found. Try adjusting your filters.
          </p>
          {hasActiveFilters && (
            <button
              onClick={clearFilters}
              className="btn-outline"
            >
              Clear Filters
            </button>
          )}
        </div>
      ) : (
        <div className="recipe-grid">
          {recipes.map((recipe) => (
            <RecipeCard key={recipe.id} recipe={recipe} />
          ))}
        </div>
      )}
    </main>
  );
}
