'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { recipeApi, RecipeList } from '@/lib/api';
import { RecipeGridSkeleton } from '@/components/LoadingSkeleton';

export default function Home() {
  const router = useRouter();
  const [featuredRecipes, setFeaturedRecipes] = useState<RecipeList[]>([]);
  const [recentRecipes, setRecentRecipes] = useState<RecipeList[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadRecipes();
  }, []);

  const loadRecipes = async () => {
    try {
      setLoading(true);
      const response = await recipeApi.getAll();
      const recipesData = response.results || response;
      
      // Normalize recipes
      const normalizedRecipes = Array.isArray(recipesData) ? recipesData.map((recipe: any) => ({
        ...recipe,
        view_count: Number(recipe.view_count || 0),
        comment_count: Number(recipe.comment_count || 0),
        favorite_count: Number(recipe.favorite_count || 0),
        rating_count: Number(recipe.rating_count || 0),
        average_rating: Number(recipe.average_rating || 0),
      })) : [];
      
      // Sort by rating for featured (top rated)
      const sortedByRating = [...normalizedRecipes].sort((a, b) => 
        (b.average_rating || 0) - (a.average_rating || 0)
      );
      
      // Sort by date for recent (newest first)
      const sortedByDate = [...normalizedRecipes].sort((a, b) => 
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );
      
      setFeaturedRecipes(sortedByRating.slice(0, 6));
      setRecentRecipes(sortedByDate.slice(0, 6));
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load recipes');
      console.error('Error loading recipes:', err);
    } finally {
      setLoading(false);
    }
  };

  const RecipeCard = ({ recipe }: { recipe: RecipeList }) => (
    <div 
      className="recipe-card-wrapper"
      onClick={() => router.push(`/recipes/${recipe.id}`)}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
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
            fontSize: '3rem',
            background: 'linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%)'
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
          <div className="recipe-stats">
            <span className="stat-badge" title="Views">
              👁️ <strong>{recipe.view_count || 0}</strong>
            </span>
            <span className="stat-badge" title="Comments">
              💬 <strong>{recipe.comment_count || 0}</strong>
            </span>
            <span className="stat-badge" title="Favorites">
              ❤️ <strong>{recipe.favorite_count || 0}</strong>
            </span>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <main className="container">
      {/* Hero Section */}
      <section className="hero-section">
        <h1 className="hero-title">🍳 Recipe Sharing Platform</h1>
        <p className="hero-subtitle">
          Discover, share, and rate amazing recipes from our community
        </p>
        <div className="hero-cta">
          <Link href="/recipes" className="btn-primary">
            Browse Recipes
          </Link>
          <Link href="/recipes/create" className="btn-outline" style={{ background: 'rgba(255,255,255,0.2)', color: 'white', borderColor: 'white' }}>
            Share Your Recipe
          </Link>
        </div>
      </section>

      {error && (
        <div className="form-error" style={{ 
          background: '#fee', 
          color: '#c33', 
          padding: '1rem', 
          borderRadius: '4px',
          marginBottom: '2rem'
        }}>
          {error}
        </div>
      )}

      {loading ? (
        <RecipeGridSkeleton />
      ) : (
        <>
          {/* Featured Recipes Section */}
          {featuredRecipes.length > 0 && (
            <section className="featured-section">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <div>
                  <h2 className="section-title" style={{ marginBottom: '0.5rem', textAlign: 'left' }}>
                    ⭐ Featured Recipes
                  </h2>
                  <p className="section-description" style={{ textAlign: 'left', marginBottom: 0 }}>
                    Top-rated recipes from our community
                  </p>
                </div>
                <Link href="/recipes" className="btn-outline">
                  View All
                </Link>
              </div>
              
              <div className="recipe-grid">
                {featuredRecipes.map((recipe) => (
                  <RecipeCard key={recipe.id} recipe={recipe} />
                ))}
              </div>
            </section>
          )}

          {/* Recent Uploads Section */}
          {recentRecipes.length > 0 && (
            <section className="featured-section" style={{ marginTop: '4rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <div>
                  <h2 className="section-title" style={{ marginBottom: '0.5rem', textAlign: 'left' }}>
                    🆕 Recent Uploads
                  </h2>
                  <p className="section-description" style={{ textAlign: 'left', marginBottom: 0 }}>
                    Latest recipes shared by our community
                  </p>
                </div>
                <Link href="/recipes" className="btn-outline">
                  View All
                </Link>
              </div>
              
              <div className="recipe-grid">
                {recentRecipes.map((recipe) => (
                  <RecipeCard key={recipe.id} recipe={recipe} />
                ))}
              </div>
            </section>
          )}

          {/* Empty State */}
          {!loading && featuredRecipes.length === 0 && recentRecipes.length === 0 && (
            <div className="empty-state">
              <div className="empty-state-icon">🍽️</div>
              <h3 className="empty-state-title">No recipes yet</h3>
              <p className="empty-state-description">
                Be the first to share your favorite recipe with the community!
              </p>
              <Link href="/recipes/create" className="btn-primary">
                Create Your First Recipe
              </Link>
            </div>
          )}
        </>
      )}
    </main>
  );
}
