'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import { recipeApi, ratingApi, commentApi, favoriteApi, userApi, Recipe, Rating, Comment } from '@/lib/api';
import RatingStars from '@/components/RatingStars';
import CommentForm from '@/components/CommentForm';
import CommentList from '@/components/CommentList';
import FavoriteButton from '@/components/FavoriteButton';
import InstructionDisplay from '@/components/InstructionDisplay';
import RecipeImage from '@/components/RecipeImage';
import ImageGallery from '@/components/ImageGallery';
import { getImageUrlOrPlaceholder } from '@/lib/placeholders';

export default function RecipeDetailPage() {
  const params = useParams();
  const router = useRouter();
  const recipeId = parseInt(params.id as string);

  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [ratings, setRatings] = useState<Rating[]>([]);
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isFavorited, setIsFavorited] = useState(false);
  const [userRating, setUserRating] = useState<Rating | null>(null);
  const [currentUser, setCurrentUser] = useState<any>(null);
  const [isAuthor, setIsAuthor] = useState(false);
  const [ingredientScale, setIngredientScale] = useState(1); // For scaling ingredients

  useEffect(() => {
    if (recipeId && !isNaN(recipeId)) {
      // Load recipe first, then load ratings/comments
      checkCurrentUser();
      loadRecipe().then((success) => {
        // Only load ratings/comments if recipe loaded successfully
        if (success) {
          loadRatings();
          loadComments();
        }
      }).catch(() => {
        // Recipe failed to load, don't load ratings/comments
      });
    } else {
      setError('Invalid recipe ID');
      setLoading(false);
    }
  }, [recipeId]);

  useEffect(() => {
    if (currentUser && recipe) {
      setIsAuthor(currentUser.id === recipe.author.id);
    } else {
      setIsAuthor(false);
    }
  }, [currentUser, recipe]);

  const checkCurrentUser = async () => {
    try {
      const user = await userApi.getCurrent();
      setCurrentUser(user);
    } catch (error) {
      setCurrentUser(null);
    }
  };

  const loadRecipe = async (): Promise<boolean> => {
    try {
      setError(null);
      setLoading(true);
      
      // Validate recipeId
      if (!recipeId || isNaN(recipeId)) {
        setError('Invalid recipe ID');
        setLoading(false);
        return false;
      }
      
      const data = await recipeApi.getById(recipeId);
      setRecipe(data);
      setIsFavorited(data.is_favorited || false);
      if (data.user_rating) {
        setUserRating(data.user_rating as any);
      }
      if (currentUser && data.author.id === currentUser.id) {
        setIsAuthor(true);
      } else {
        setIsAuthor(false);
      }
      
      // Try to increment view count, but don't fail if it errors
      try {
        await recipeApi.incrementView(recipeId);
      } catch (viewError) {
        console.warn('Failed to increment view count:', viewError);
      }
      
      return true;
    } catch (error: any) {
      console.error('Error loading recipe:', error);
      console.error('Error details:', {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        message: error.message,
        url: error.config?.url
      });
      
      if (error.response?.status === 404) {
        setError(`Recipe #${recipeId} not found. It may have been deleted or is not published.`);
      } else if (error.response?.status === 403) {
        setError('You do not have permission to view this recipe.');
      } else if (error.response?.status >= 500) {
        setError('Server error. Please try again later.');
      } else if (error.code === 'ECONNREFUSED' || error.message?.includes('Network Error')) {
        setError('Cannot connect to server. Please make sure the backend is running on http://127.0.0.1:8000');
      } else {
        setError(`Failed to load recipe: ${error.response?.data?.detail || error.message || 'Unknown error'}`);
      }
      
      return false;
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

  const handleDelete = async () => {
    if (!recipe) return;
    
    const confirmed = window.confirm(
      `Are you sure you want to delete "${recipe.title}"? This action cannot be undone.`
    );
    
    if (!confirmed) return;
    
    try {
      await recipeApi.delete(recipeId);
      router.push('/recipes');
    } catch (error: any) {
      console.error('Error deleting recipe:', error);
      if (error.response?.status === 403 || error.response?.status === 401) {
        alert('You do not have permission to delete this recipe.');
      } else {
        alert('Failed to delete recipe. Please try again.');
      }
    }
  };

  // Format ingredients from recipe_ingredients data
  const formatIngredients = (recipeIngredients: any[], scale: number = 1) => {
    if (!recipeIngredients || recipeIngredients.length === 0) {
      return ['No ingredients listed'];
    }
    
    return recipeIngredients.map((ri: any) => {
      const quantity = ri.quantity ? (parseFloat(ri.quantity) * scale).toFixed(2).replace(/\.?0+$/, '') : '';
      const unit = ri.unit || '';
      const ingredientName = ri.ingredient?.name || 'Unknown';
      const notes = ri.notes ? ` (${ri.notes})` : '';
      
      if (quantity && unit) {
        return `${quantity} ${unit} ${ingredientName}${notes}`;
      } else if (quantity) {
        return `${quantity} ${ingredientName}${notes}`;
      } else {
        return `${ingredientName}${notes}`;
      }
    });
  };

  const getImageUrl = (image: string | undefined) => {
    if (!image) return null;
    if (image.startsWith('http')) return image;
    return `http://127.0.0.1:8000${image}`;
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

  if (error || !recipe) {
    return (
      <main className="container">
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <h1 style={{ fontSize: '3rem', fontWeight: '300', marginBottom: '1rem', color: '#333' }}>404</h1>
          <p style={{ color: '#666', marginBottom: '2rem', fontSize: '1.2rem' }}>
            {error || 'Recipe not found'}
          </p>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
            <button
              onClick={() => router.back()}
              className="btn-outline"
            >
              Go Back
            </button>
            <button
              onClick={() => router.push('/recipes')}
              className="btn-primary"
            >
              Browse Recipes
            </button>
          </div>
        </div>
      </main>
    );
  }

  // Get primary image or first image, or use placeholder
  const primaryImage = (recipe as any).images?.find((img: any) => img.is_primary) 
    || (recipe as any).images?.[0] 
    || null;
  const imageUrl = primaryImage?.image_url || recipe.image || recipe.image_url || null;
  const displayImageUrl = imageUrl ? getImageUrl(imageUrl) : null;
  const allImages = (recipe as any).images || [];
  const ingredients = formatIngredients((recipe as any).recipe_ingredients || [], ingredientScale);

  return (
    <main className="container" style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem 1rem' }}>
      {/* Back Button */}
      <button 
        onClick={() => router.back()}
        style={{ 
          background: 'none', 
          border: 'none', 
          cursor: 'pointer',
          marginBottom: '1.5rem',
          color: '#666',
          fontSize: '1rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem'
        }}
      >
        ← Back to Recipes
      </button>

      {/* Hero Image Section - Primary Image */}
      {displayImageUrl && (
        <div style={{ 
          width: '100%', 
          marginBottom: '2rem',
          borderRadius: '8px',
          overflow: 'hidden',
          boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
        }}>
          <RecipeImage
            src={displayImageUrl}
            alt={recipe.title}
            placeholderType="recipe"
            style={{
              width: '100%',
              height: '500px',
            }}
            objectFit="cover"
          />
        </div>
      )}

      {/* Image Gallery - Multiple Images */}
      {allImages.length > 1 && (
        <div style={{ marginBottom: '2rem' }}>
          <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem', color: '#333' }}>
            More Images ({allImages.length})
          </h3>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
            gap: '1rem'
          }}>
            {allImages.map((img: any, index: number) => (
              <RecipeImage
                key={img.id || index}
                src={img.image_url}
                alt={img.alt_text || `${recipe.title} - Image ${index + 1}`}
                placeholderType="recipe"
                style={{
                  width: '100%',
                  height: '200px',
                }}
                objectFit="cover"
              />
            ))}
          </div>
        </div>
      )}

      {/* Title and Rating Section - Allrecipes Style */}
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ 
          fontSize: '2.5rem', 
          fontWeight: 'bold',
          marginBottom: '1rem',
          color: '#333',
          lineHeight: '1.2'
        }}>
          {recipe.title}
        </h1>
        
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '1rem',
          marginBottom: '1rem',
          flexWrap: 'wrap'
        }}>
          {/* Rating Display */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#333' }}>
              {recipe.average_rating.toFixed(1)}
            </span>
            <span style={{ fontSize: '1.2rem', color: '#ffc107' }}>⭐</span>
            <span style={{ color: '#666', fontSize: '0.95rem' }}>
              ({recipe.rating_count} {recipe.rating_count === 1 ? 'rating' : 'ratings'})
            </span>
          </div>

          {/* Reviews Count */}
          <span style={{ color: '#666', fontSize: '0.95rem' }}>
            {recipe.comment_count} {recipe.comment_count === 1 ? 'review' : 'reviews'}
          </span>

          {/* Views Count */}
          <span style={{ color: '#666', fontSize: '0.95rem' }}>
            {recipe.view_count} {recipe.view_count === 1 ? 'view' : 'views'}
          </span>

          {/* Action Buttons */}
          <div style={{ marginLeft: 'auto', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <FavoriteButton
              recipeId={recipeId}
              initialFavorited={isFavorited}
              initialCount={recipe.favorite_count}
              onToggle={(favorited, count) => {
                setIsFavorited(favorited);
                if (recipe) {
                  setRecipe({ ...recipe, favorite_count: count });
                }
              }}
            />
            {isAuthor && (
              <>
                <Link href={`/recipes/${recipeId}/edit`} className="btn-outline" style={{ padding: '0.5rem 1rem' }}>
                  ✏️ Edit Recipe
                </Link>
                <button
                  onClick={handleDelete}
                  className="btn-outline"
                  style={{ 
                    padding: '0.5rem 1rem',
                    borderColor: '#dc3545',
                    color: '#dc3545'
                  }}
                >
                  🗑️ Delete Recipe
                </button>
              </>
            )}
          </div>
        </div>

        {/* Description */}
        <p style={{ 
          color: '#666', 
          fontSize: '1.1rem',
          lineHeight: '1.6',
          marginBottom: '1.5rem'
        }}>
          {recipe.description}
        </p>

        {/* Author Info */}
        <div style={{ color: '#666', fontSize: '0.95rem', marginBottom: '1rem' }}>
          <strong>By:</strong> <Link href={`/users/profile/${recipe.author.username}`} style={{ color: '#0066cc' }}>
            {recipe.author.username}
          </Link>
          {recipe.category && (
            <> • <strong>Category:</strong> {recipe.category.name}</>
          )}
        </div>
      </div>

      {/* Quick Stats Bar - Allrecipes Style */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))', 
        gap: '1.5rem',
        padding: '1.5rem',
        background: '#f8f9fa',
        borderRadius: '8px',
        marginBottom: '2rem',
        border: '1px solid #e0e0e0'
      }}>
        <div>
          <div style={{ fontSize: '0.85rem', color: '#666', marginBottom: '0.25rem' }}>Prep Time</div>
          <div style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#333' }}>{recipe.prep_time} min</div>
        </div>
        <div>
          <div style={{ fontSize: '0.85rem', color: '#666', marginBottom: '0.25rem' }}>Cook Time</div>
          <div style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#333' }}>{recipe.cook_time} min</div>
        </div>
        <div>
          <div style={{ fontSize: '0.85rem', color: '#666', marginBottom: '0.25rem' }}>Total Time</div>
          <div style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#333' }}>{recipe.total_time} min</div>
        </div>
        <div>
          <div style={{ fontSize: '0.85rem', color: '#666', marginBottom: '0.25rem' }}>Servings</div>
          <div style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#333' }}>N/A</div>
        </div>
      </div>

      {/* Two Column Layout: Ingredients | Directions */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
        gap: '2rem',
        marginBottom: '2rem'
      }}>
        {/* Ingredients Section - Allrecipes Style */}
        <div style={{ 
          background: 'white',
          padding: '2rem',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginBottom: '1.5rem'
          }}>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#333' }}>Ingredients</h2>
            {/* Scaling Options */}
            <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
              <span style={{ fontSize: '0.85rem', color: '#666' }}>Scale:</span>
              <button
                onClick={() => setIngredientScale(0.5)}
                style={{
                  padding: '0.25rem 0.5rem',
                  border: ingredientScale === 0.5 ? '2px solid #0066cc' : '1px solid #ddd',
                  background: ingredientScale === 0.5 ? '#e6f2ff' : 'white',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '0.85rem'
                }}
              >
                1/2x
              </button>
              <button
                onClick={() => setIngredientScale(1)}
                style={{
                  padding: '0.25rem 0.5rem',
                  border: ingredientScale === 1 ? '2px solid #0066cc' : '1px solid #ddd',
                  background: ingredientScale === 1 ? '#e6f2ff' : 'white',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '0.85rem'
                }}
              >
                1x
              </button>
              <button
                onClick={() => setIngredientScale(2)}
                style={{
                  padding: '0.25rem 0.5rem',
                  border: ingredientScale === 2 ? '2px solid #0066cc' : '1px solid #ddd',
                  background: ingredientScale === 2 ? '#e6f2ff' : 'white',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '0.85rem'
                }}
              >
                2x
              </button>
            </div>
          </div>
          
          <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
            {ingredients.map((ingredient, index) => (
              <li key={index} style={{ 
                padding: '0.75rem 0',
                borderBottom: index < ingredients.length - 1 ? '1px solid #e0e0e0' : 'none',
                fontSize: '1rem',
                lineHeight: '1.6'
              }}>
                {ingredient}
              </li>
            ))}
          </ul>
        </div>

        {/* Directions Section - Allrecipes Style */}
        <div style={{ 
          background: 'white',
          padding: '2rem',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#333', marginBottom: '1.5rem' }}>
            Directions
          </h2>
          
          <InstructionDisplay instructions={recipe.instructions} />
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
        <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem', color: '#333' }}>
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
        <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem', color: '#333' }}>
          Reviews ({recipe.comment_count})
        </h2>
        <CommentForm onSubmit={handleCommentSubmit} />
        <CommentList comments={comments} onDelete={loadComments} />
      </div>
    </main>
  );
}
