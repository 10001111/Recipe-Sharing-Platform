'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { favoriteApi, RecipeList } from '@/lib/api';
import { recipeApi } from '@/lib/api';

export default function FavoritesPage() {
  const [recipes, setRecipes] = useState<RecipeList[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadFavorites();
  }, []);

  const loadFavorites = async () => {
    try {
      setLoading(true);
      const favorites = await favoriteApi.getMine();
      const favoritesList = favorites.results || favorites;
      
      // Get recipe details for each favorite
      const recipePromises = favoritesList.map((fav: any) => 
        recipeApi.getById(fav.recipe)
      );
      
      const recipeData = await Promise.all(recipePromises);
      setRecipes(recipeData);
      setError(null);
    } catch (err: any) {
      if (err.response?.status === 401) {
        setError('Please login to view your favorites.');
      } else {
        setError('Failed to load favorites.');
      }
      console.error('Error loading favorites:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <h1 style={{ fontSize: '2rem', marginBottom: '2rem' }}>My Favorite Recipes</h1>

      {loading && (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <p>Loading favorites...</p>
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
            You haven't favorited any recipes yet.
          </p>
          <Link href="/recipes" className="btn-primary">
            Browse Recipes
          </Link>
        </div>
      )}

      {!loading && recipes.length > 0 && (
        <div className="recipe-grid">
          {recipes.map((recipe) => (
            <Link key={recipe.id} href={`/recipes/${recipe.id}`}>
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
                      <span>{recipe.average_rating.toFixed(1)}</span>
                      <span style={{ marginLeft: '0.5rem', color: '#999' }}>
                        ({recipe.rating_count})
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </main>
  );
}

