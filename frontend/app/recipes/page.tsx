'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { recipeApi, RecipeList } from '@/lib/api';
import SearchAutocomplete from '@/components/SearchAutocomplete';
import RecipeCard from '@/components/RecipeCard';

type SortOption = 'newest' | 'oldest' | 'rating' | 'views' | 'title';
type FilterOption = 'all' | 'breakfast' | 'lunch' | 'dinner' | 'dessert' | 'snack';

export default function RecipesPage() {
  const router = useRouter();
  const [recipes, setRecipes] = useState<RecipeList[]>([]);
  const [filteredRecipes, setFilteredRecipes] = useState<RecipeList[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [category, setCategory] = useState<FilterOption>('all');
  const [sortBy, setSortBy] = useState<SortOption>('newest');

  useEffect(() => {
    loadRecipes();
  }, []);

  useEffect(() => {
    filterAndSortRecipes();
  }, [recipes, category, sortBy, searchQuery]);

  const loadRecipes = async () => {
    try {
      setLoading(true);
      const response = await recipeApi.getAll();
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
  };

  const filterAndSortRecipes = () => {
    let filtered = [...recipes];

    // Filter by category
    if (category !== 'all') {
      filtered = filtered.filter(recipe => 
        recipe.category?.name?.toLowerCase() === category.toLowerCase()
      );
    }

    // Filter by search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(recipe =>
        recipe.title.toLowerCase().includes(query) ||
        recipe.description.toLowerCase().includes(query) ||
        recipe.author.username.toLowerCase().includes(query)
      );
    }

    // Sort recipes
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'newest':
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
        case 'oldest':
          return new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
        case 'rating':
          return (b.average_rating || 0) - (a.average_rating || 0);
        case 'views':
          return (b.view_count || 0) - (a.view_count || 0);
        case 'title':
          return a.title.localeCompare(b.title);
        default:
          return 0;
      }
    });

    setFilteredRecipes(filtered);
  };

  const handleSearchSelect = (recipe: RecipeList) => {
    router.push(`/recipes/${recipe.id}`);
  };

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
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1rem' }}>
            <div style={{ gridColumn: '1 / -1' }}>
              <label className="form-label" style={{ marginBottom: '0.5rem' }}>Search Recipes</label>
              <SearchAutocomplete 
                onSelect={handleSearchSelect}
                placeholder="Search by title, description, or author..."
              />
            </div>
            
            <div>
              <label className="form-label" style={{ marginBottom: '0.5rem' }}>Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value as FilterOption)}
                className="form-select"
                style={{ width: '100%' }}
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
                onChange={(e) => setSortBy(e.target.value as SortOption)}
                className="form-select"
                style={{ width: '100%' }}
              >
                <option value="newest">Newest First</option>
                <option value="oldest">Oldest First</option>
                <option value="rating">Highest Rated</option>
                <option value="views">Most Viewed</option>
                <option value="title">Title (A-Z)</option>
              </select>
            </div>
          </div>

          {/* Results count */}
          <div style={{ 
            paddingTop: '1rem', 
            borderTop: '1px solid #e0e0e0',
            fontSize: '0.9rem',
            color: '#666'
          }}>
            Showing {filteredRecipes.length} of {recipes.length} recipes
            {category !== 'all' && ` in ${category}`}
            {searchQuery && ` matching "${searchQuery}"`}
          </div>
        </div>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <p>Loading recipes...</p>
        </div>
      ) : filteredRecipes.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ fontSize: '1.2rem', color: '#666', marginBottom: '1rem' }}>
            No recipes found. Try adjusting your filters.
          </p>
          {(category !== 'all' || searchQuery) && (
            <button
              onClick={() => {
                setCategory('all');
                setSearchQuery('');
              }}
              className="btn-outline"
            >
              Clear Filters
            </button>
          )}
        </div>
      ) : (
        <div className="recipe-grid">
          {filteredRecipes.map((recipe) => (
            <RecipeCard key={recipe.id} recipe={recipe} />
          ))}
        </div>
      )}
    </main>
  );
}
