'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { recipeApi, RecipeList } from '@/lib/api';

export default function RecipesPage() {
  const router = useRouter();
  const [recipes, setRecipes] = useState<RecipeList[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [category, setCategory] = useState('');

  useEffect(() => {
    loadRecipes();
  }, [category, searchQuery]);

  const loadRecipes = async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (category) params.category = category;
      if (searchQuery) params.search = searchQuery;
      
      const response = await recipeApi.getAll(params);
      const recipesData = response.results || response;
      
      // Ensure all statistics are numbers
      const normalizedRecipes = Array.isArray(recipesData) ? recipesData.map((recipe: any) => {
        return {
          ...recipe,
          view_count: recipe.view_count !== undefined && recipe.view_count !== null ? Number(recipe.view_count) : 0,
          comment_count: recipe.comment_count !== undefined && recipe.comment_count !== null ? Number(recipe.comment_count) : 0,
          favorite_count: recipe.favorite_count !== undefined && recipe.favorite_count !== null ? Number(recipe.favorite_count) : 0,
          rating_count: recipe.rating_count !== undefined && recipe.rating_count !== null ? Number(recipe.rating_count) : 0,
          average_rating: recipe.average_rating !== undefined && recipe.average_rating !== null ? Number(recipe.average_rating) : 0,
        };
      }) : [];
      
      setRecipes(normalizedRecipes);
    } catch (error: any) {
      console.error('Error loading recipes:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2rem', marginBottom: '1.5rem' }}>All Recipes</h1>
        
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', flexWrap: 'wrap' }}>
          <input
            type="text"
            placeholder="Search recipes..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="form-input"
            style={{ flex: '1', minWidth: '200px' }}
          />
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="form-select"
            style={{ minWidth: '150px' }}
          >
            <option value="">All Categories</option>
            <option value="breakfast">Breakfast</option>
            <option value="lunch">Lunch</option>
            <option value="dinner">Dinner</option>
            <option value="dessert">Dessert</option>
            <option value="snack">Snack</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <p>Loading recipes...</p>
        </div>
      ) : recipes.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ fontSize: '1.2rem', color: '#666' }}>
            No recipes found. Try adjusting your search.
          </p>
        </div>
      ) : (
        <div className="recipe-grid">
          {recipes.map((recipe) => (
            <div 
              key={recipe.id} 
              className="recipe-card-wrapper"
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                router.push(`/recipes/${recipe.id}`);
              }}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  router.push(`/recipes/${recipe.id}`);
                }
              }}
            >
              <div className="recipe-card">
                {recipe.image ? (
                  <img 
                    src={recipe.image.startsWith('http') ? recipe.image : `http://127.0.0.1:8000${recipe.image}`}
                    alt={recipe.title}
                    className="recipe-card-image"
                  />
                ) : (
                  <div className="recipe-card-image" style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center',
                    fontSize: '3rem'
                  }}>
                    🍽️
                  </div>
                )}
                <div className="recipe-card-content">
                  <h3 className="recipe-card-title">{recipe.title}</h3>
                  <p className="recipe-card-description">{recipe.description}</p>
                  <div className="recipe-card-meta">
                    <span>👤 {recipe.author.username}</span>
                    <div className="recipe-card-rating">
                      <span className="star">⭐</span>
                      <span>{(recipe.average_rating || 0).toFixed(1)}</span>
                      <span style={{ marginLeft: '0.5rem', color: '#999' }}>
                        ({recipe.rating_count || 0})
                      </span>
                    </div>
                  </div>
                  {/* Statistics Section - Always Visible */}
                  <div style={{ 
                    display: 'flex', 
                    gap: '0.75rem', 
                    marginTop: '0.75rem', 
                    fontSize: '0.9rem',
                    color: '#333',
                    flexWrap: 'wrap',
                    alignItems: 'center',
                    paddingTop: '0.75rem',
                    borderTop: '1px solid #e0e0e0',
                    fontWeight: '500',
                    minHeight: '40px'
                  }}>
                    <span title="Views" style={{ 
                      display: 'inline-flex', 
                      alignItems: 'center', 
                      gap: '0.35rem',
                      background: '#f8f9fa',
                      padding: '0.25rem 0.5rem',
                      borderRadius: '4px',
                      minWidth: '60px'
                    }}>
                      <span style={{ fontSize: '1rem' }}>👁️</span>
                      <strong style={{ color: '#333' }}>{recipe.view_count || 0}</strong>
                    </span>
                    <span title="Comments" style={{ 
                      display: 'inline-flex', 
                      alignItems: 'center', 
                      gap: '0.35rem',
                      background: '#f8f9fa',
                      padding: '0.25rem 0.5rem',
                      borderRadius: '4px',
                      minWidth: '70px'
                    }}>
                      <span style={{ fontSize: '1rem' }}>💬</span>
                      <strong style={{ color: '#333' }}>{recipe.comment_count || 0}</strong>
                    </span>
                    <span title="Favorites" style={{ 
                      display: 'inline-flex', 
                      alignItems: 'center', 
                      gap: '0.35rem',
                      background: '#f8f9fa',
                      padding: '0.25rem 0.5rem',
                      borderRadius: '4px',
                      minWidth: '70px'
                    }}>
                      <span style={{ fontSize: '1rem' }}>❤️</span>
                      <strong style={{ color: '#333' }}>{recipe.favorite_count || 0}</strong>
                    </span>
                    <span title="Ratings" style={{ 
                      display: 'inline-flex', 
                      alignItems: 'center', 
                      gap: '0.35rem',
                      background: '#f8f9fa',
                      padding: '0.25rem 0.5rem',
                      borderRadius: '4px',
                      minWidth: '60px'
                    }}>
                      <span style={{ fontSize: '1rem' }}>⭐</span>
                      <strong style={{ color: '#333' }}>{recipe.rating_count || 0}</strong>
                    </span>
                  </div>
                  {recipe.category && (
                    <div style={{ marginTop: '0.5rem' }}>
                      <span style={{ 
                        background: '#f0f0f0', 
                        padding: '0.25rem 0.5rem', 
                        borderRadius: '4px',
                        fontSize: '0.85rem'
                      }}>
                        {recipe.category.name}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}

