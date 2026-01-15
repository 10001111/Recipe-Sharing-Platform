'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { recipeApi, ratingApi, commentApi, favoriteApi, Recipe, Rating, Comment } from '@/lib/api';
import RatingStars from '@/components/RatingStars';
import CommentForm from '@/components/CommentForm';
import CommentList from '@/components/CommentList';

export default function RecipeDetailPage() {
  const params = useParams();
  const router = useRouter();
  const recipeId = parseInt(params.id as string);

  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [ratings, setRatings] = useState<Rating[]>([]);
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);
  const [isFavorited, setIsFavorited] = useState(false);
  const [userRating, setUserRating] = useState<Rating | null>(null);

  useEffect(() => {
    if (recipeId) {
      loadRecipe();
      loadRatings();
      loadComments();
    }
  }, [recipeId]);

  const loadRecipe = async () => {
    try {
      const data = await recipeApi.getById(recipeId);
      setRecipe(data);
      setIsFavorited(data.is_favorited || false);
      if (data.user_rating) {
        setUserRating(data.user_rating as any);
      }
      // Increment view count
      await recipeApi.incrementView(recipeId);
    } catch (error) {
      console.error('Error loading recipe:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadRatings = async () => {
    try {
      const response = await ratingApi.getByRecipe(recipeId);
      setRatings(response.results || response);
    } catch (error) {
      console.error('Error loading ratings:', error);
    }
  };

  const loadComments = async () => {
    try {
      const response = await commentApi.getByRecipe(recipeId);
      setComments(response.results || response);
    } catch (error) {
      console.error('Error loading comments:', error);
    }
  };

  const handleRating = async (stars: number, reviewText?: string) => {
    try {
      if (userRating) {
        await ratingApi.update(userRating.id, stars, reviewText);
      } else {
        await ratingApi.createOrUpdate(recipeId, stars, reviewText);
      }
      await loadRecipe();
      await loadRatings();
    } catch (error: any) {
      console.error('Error submitting rating:', error);
      if (error.response?.status === 401) {
        alert('Please login to rate recipes.');
        router.push('/login');
      } else {
        alert('Failed to submit rating. Please try again.');
      }
    }
  };

  const handleDeleteRating = async () => {
    if (!userRating) return;
    
    try {
      await ratingApi.delete(userRating.id);
      setUserRating(null);
      await loadRecipe();
      await loadRatings();
    } catch (error: any) {
      console.error('Error deleting rating:', error);
      if (error.response?.status === 403 || error.response?.status === 401) {
        alert('You can only delete your own ratings.');
      } else {
        alert('Failed to delete rating. Please try again.');
      }
    }
  };

  const handleToggleFavorite = async () => {
    try {
      const response = await favoriteApi.toggle(recipeId);
      setIsFavorited(response.is_favorited);
      if (recipe) {
        setRecipe({ ...recipe, favorite_count: response.favorite_count });
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
      alert('Please login to favorite recipes.');
      router.push('/login');
    }
  };

  const handleCommentSubmit = async (text: string) => {
    try {
      await commentApi.create(recipeId, text);
      await loadComments();
      if (recipe) {
        setRecipe({ ...recipe, comment_count: recipe.comment_count + 1 });
      }
    } catch (error) {
      console.error('Error submitting comment:', error);
      alert('Please login to comment.');
      router.push('/login');
    }
  };

  if (loading) {
    return (
      <main className="container">
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <p>Loading recipe...</p>
        </div>
      </main>
    );
  }

  if (!recipe) {
    return (
      <main className="container">
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <p>Recipe not found.</p>
        </div>
      </main>
    );
  }

  return (
    <main className="container">
      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
        {/* Recipe Header */}
        <div style={{ marginBottom: '2rem' }}>
          <button 
            onClick={() => router.back()}
            style={{ 
              background: 'none', 
              border: 'none', 
              cursor: 'pointer',
              marginBottom: '1rem',
              color: '#666'
            }}
          >
            ← Back
          </button>
          
          <div style={{ display: 'flex', gap: '2rem', marginBottom: '2rem', flexWrap: 'wrap' }}>
            {recipe.image ? (
              <img 
                src={recipe.image.startsWith('http') ? recipe.image : `http://127.0.0.1:8000${recipe.image}`}
                alt={recipe.title}
                style={{ 
                  width: '100%', 
                  maxWidth: '400px', 
                  height: '300px', 
                  objectFit: 'cover',
                  borderRadius: '8px'
                }}
              />
            ) : (
              <div style={{ 
                width: '100%', 
                maxWidth: '400px', 
                height: '300px', 
                background: '#f0f0f0',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '4rem',
                borderRadius: '8px'
              }}>
                🍽️
              </div>
            )}
            
            <div style={{ flex: '1', minWidth: '300px' }}>
              <h1 style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>{recipe.title}</h1>
              <p style={{ color: '#666', marginBottom: '1.5rem', fontSize: '1.1rem' }}>
                {recipe.description}
              </p>
              
              <div style={{ display: 'flex', gap: '2rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
                <div>
                  <strong>Author:</strong> {recipe.author.username}
                </div>
                {recipe.category && (
                  <div>
                    <strong>Category:</strong> {recipe.category.name}
                  </div>
                )}
                <div>
                  <strong>Views:</strong> {recipe.view_count}
                </div>
              </div>

              <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', marginBottom: '1rem' }}>
                <div className="recipe-card-rating">
                  <span className="star">⭐</span>
                  <span style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>
                    {recipe.average_rating.toFixed(1)}
                  </span>
                  <span style={{ marginLeft: '0.5rem', color: '#999' }}>
                    ({recipe.rating_count} ratings)
                  </span>
                </div>
                <button 
                  onClick={handleToggleFavorite}
                  className={isFavorited ? 'btn-primary' : 'btn-outline'}
                  style={{ marginLeft: 'auto' }}
                >
                  {isFavorited ? '❤️ Favorited' : '🤍 Favorite'}
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Recipe Info */}
        <div style={{ 
          background: 'white', 
          padding: '2rem', 
          borderRadius: '8px',
          marginBottom: '2rem',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '2rem', marginBottom: '2rem' }}>
            <div>
              <div style={{ fontSize: '0.9rem', color: '#666' }}>Prep Time</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{recipe.prep_time} min</div>
            </div>
            <div>
              <div style={{ fontSize: '0.9rem', color: '#666' }}>Cook Time</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{recipe.cook_time} min</div>
            </div>
            <div>
              <div style={{ fontSize: '0.9rem', color: '#666' }}>Total Time</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{recipe.total_time} min</div>
            </div>
          </div>

          <div>
            <h2 style={{ marginBottom: '1rem' }}>Instructions</h2>
            <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.8' }}>
              {recipe.instructions}
            </div>
          </div>
        </div>

        {/* Rating Section */}
        <div style={{ 
          background: 'white', 
          padding: '2rem', 
          borderRadius: '8px',
          marginBottom: '2rem',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          <h2 style={{ marginBottom: '1rem' }}>
            {userRating ? 'Your Rating' : 'Rate This Recipe'}
          </h2>
          <RatingStars 
            currentRating={userRating?.stars || 0}
            onSubmit={handleRating}
            onDelete={handleDeleteRating}
            reviewText={userRating?.review_text || ''}
            canDelete={!!userRating}
          />
        </div>

        {/* Comments Section */}
        <div style={{ 
          background: 'white', 
          padding: '2rem', 
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          <h2 style={{ marginBottom: '1rem' }}>
            Comments ({recipe.comment_count})
          </h2>
          <CommentForm onSubmit={handleCommentSubmit} />
          <CommentList comments={comments} onDelete={loadComments} />
        </div>
      </div>
    </main>
  );
}

