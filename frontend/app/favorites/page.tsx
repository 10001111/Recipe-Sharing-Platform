'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { favoriteApi, RecipeList } from '@/lib/api';
import { recipeApi } from '@/lib/api';
import RecipeCard from '@/components/RecipeCard';
import { RecipeGridSkeleton } from '@/components/LoadingSkeleton';

export default function FavoritesPage() {
  const router = useRouter();
  const [recipes, setRecipes] = useState<RecipeList[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadFavorites();
  }, []);

  const loadFavorites = async () => {
    try {
      setLoading(true);
      const favorites = await favoriteApi.getUserFavorites();
      const favoritesList = favorites.results || favorites;
      
      if (Array.isArray(favoritesList) && favoritesList.length > 0) {
        // Get recipe details for each favorite
        const recipePromises = favoritesList.map((fav: any) => 
          recipeApi.getById(fav.recipe)
        );
        
        const recipeData = await Promise.all(recipePromises);
        const normalizedRecipes = recipeData.map((recipe: any) => ({
          ...recipe,
          view_count: Number(recipe.view_count || 0),
          comment_count: Number(recipe.comment_count || 0),
          favorite_count: Number(recipe.favorite_count || 0),
          rating_count: Number(recipe.rating_count || 0),
          average_rating: Number(recipe.average_rating || 0),
        }));
        setRecipes(normalizedRecipes);
      } else {
        setRecipes([]);
      }
      setError(null);
    } catch (err: any) {
      if (err.response?.status === 401) {
        setError('Please login to view your favorites.');
        router.push('/login');
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

      {loading ? (
        <RecipeGridSkeleton />
      ) : recipes.length > 0 ? (
        <>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginBottom: '1.5rem'
          }}>
            <p style={{ color: '#666', fontSize: '1rem' }}>
              You have {recipes.length} favorite{recipes.length !== 1 ? 's' : ''}
            </p>
            <Link href="/recipes" className="btn-outline">
              Browse More Recipes
            </Link>
          </div>
          <div className="recipe-grid">
            {recipes.map((recipe) => (
              <RecipeCard key={recipe.id} recipe={recipe} />
            ))}
          </div>
        </>
      ) : null}
    </main>
  );
}

