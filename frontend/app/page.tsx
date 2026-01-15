'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { recipeApi, RecipeList } from '@/lib/api';

export default function Home() {
  const router = useRouter();
  const [recipes, setRecipes] = useState<RecipeList[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadRecipes();
  }, []);

  const loadRecipes = async () => {
    try {
      setLoading(true);
      const response = await recipeApi.getAll();
      console.log('API Response:', response);
      const recipesData = response.results || response;
      console.log('Recipes Data:', recipesData);
      
      // Ensure all statistics are numbers
      const normalizedRecipes = Array.isArray(recipesData) ? recipesData.map((recipe: any) => {
        console.log('Processing recipe:', recipe.id, recipe.title);
        console.log('Recipe stats:', {
          view_count: recipe.view_count,
          comment_count: recipe.comment_count,
          favorite_count: recipe.favorite_count,
          rating_count: recipe.rating_count,
          average_rating: recipe.average_rating
        });
        
        return {
          ...recipe,
          view_count: recipe.view_count !== undefined && recipe.view_count !== null ? Number(recipe.view_count) : 0,
          comment_count: recipe.comment_count !== undefined && recipe.comment_count !== null ? Number(recipe.comment_count) : 0,
          favorite_count: recipe.favorite_count !== undefined && recipe.favorite_count !== null ? Number(recipe.favorite_count) : 0,
          rating_count: recipe.rating_count !== undefined && recipe.rating_count !== null ? Number(recipe.rating_count) : 0,
          average_rating: recipe.average_rating !== undefined && recipe.average_rating !== null ? Number(recipe.average_rating) : 0,
        };
      }) : [];
      
      console.log('Normalized recipes:', normalizedRecipes);
      setRecipes(normalizedRecipes);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load recipes');
      console.error('Error loading recipes:', err);
      console.error('Error details:', err.response?.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '1rem', color: '#333' }}>
          🍳 Recipe Sharing Platform
        </h1>
        <p style={{ fontSize: '1.2rem', color: '#666', marginBottom: '2rem' }}>
          Discover, share, and rate amazing recipes from our community
        </p>
      </div>

      {loading && (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <p>Loading recipes...</p>
        </div>
      )}

      {error && (
        <div style={{ 
          background: '#fee', 
          color: '#c33', 
          padding: '1rem', 
          borderRadius: '4px',
          marginBottom: '2rem'
        }}>
          {error}
        </div>
      )}

      {!loading && !error && recipes.length === 0 && (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ fontSize: '1.2rem', color: '#666', marginBottom: '1rem' }}>
            No recipes yet. Be the first to share!
          </p>
          <Link href="/recipes/create" className="btn-primary">
            Create Your First Recipe
          </Link>
        </div>
      )}

      {!loading && recipes.length > 0 && (
        <>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
            <h2 style={{ fontSize: '1.8rem' }}>Featured Recipes</h2>
            <Link href="/recipes" className="btn-outline">
              View All Recipes
            </Link>
          </div>
          
          <div className="recipe-grid">
            {recipes.slice(0, 6).map((recipe) => (
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
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </main>
  );
}
