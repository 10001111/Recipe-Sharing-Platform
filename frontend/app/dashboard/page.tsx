'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { userApi, recipeApi, favoriteApi, ratingApi, commentApi, RecipeList, Rating, Comment } from '@/lib/api';
import RecipeCard from '@/components/RecipeCard';
import { RecipeGridSkeleton } from '@/components/LoadingSkeleton';

export default function DashboardPage() {
  const router = useRouter();
  const [currentUser, setCurrentUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'recipes' | 'favorites' | 'ratings' | 'comments'>('recipes');
  
  // Data states
  const [myRecipes, setMyRecipes] = useState<RecipeList[]>([]);
  const [favorites, setFavorites] = useState<RecipeList[]>([]);
  const [ratings, setRatings] = useState<Rating[]>([]);
  const [comments, setComments] = useState<Comment[]>([]);
  
  // Loading states
  const [recipesLoading, setRecipesLoading] = useState(false);
  const [favoritesLoading, setFavoritesLoading] = useState(false);
  const [ratingsLoading, setRatingsLoading] = useState(false);
  const [commentsLoading, setCommentsLoading] = useState(false);
  
  // Statistics
  const [stats, setStats] = useState({
    totalRecipes: 0,
    totalFavorites: 0,
    totalRatings: 0,
    totalComments: 0,
    averageRatingGiven: 0,
  });

  useEffect(() => {
    checkAuthAndLoadData();
  }, []);

  useEffect(() => {
    if (!currentUser || loading) return;
    
    if (activeTab === 'recipes' && myRecipes.length === 0 && !recipesLoading) {
      loadMyRecipes();
    } else if (activeTab === 'favorites' && favorites.length === 0 && !favoritesLoading) {
      loadFavorites();
    } else if (activeTab === 'ratings' && ratings.length === 0 && !ratingsLoading) {
      loadRatings();
    } else if (activeTab === 'comments' && comments.length === 0 && !commentsLoading) {
      loadComments();
    }
  }, [activeTab, currentUser, loading]);

  const checkAuthAndLoadData = async () => {
    try {
      setLoading(true);
      const user = await userApi.getCurrent();
      setCurrentUser(user);
      
      // Load all data in parallel after user is set
      // Pass user directly to avoid race condition
      await Promise.all([
        loadMyRecipes(user),
        loadFavorites(user),
        loadRatings(user),
        loadComments(user),
      ]);
    } catch (error: any) {
      if (error.response?.status === 401) {
        router.push('/login');
      } else {
        console.error('Error loading dashboard:', error);
      }
    } finally {
      setLoading(false);
    }
  };

  const loadMyRecipes = async (user?: any) => {
    const userToUse = user || currentUser;
    if (!userToUse) return;
    try {
      setRecipesLoading(true);
      const response = await recipeApi.getAll({ author_username: userToUse.username });
      const recipesData = response.results || response;
      const normalizedRecipes = Array.isArray(recipesData) ? recipesData.map((recipe: any) => ({
        ...recipe,
        view_count: Number(recipe.view_count || 0),
        comment_count: Number(recipe.comment_count || 0),
        favorite_count: Number(recipe.favorite_count || 0),
        rating_count: Number(recipe.rating_count || 0),
        average_rating: Number(recipe.average_rating || 0),
      })) : [];
      setMyRecipes(normalizedRecipes);
      setStats(prev => ({ ...prev, totalRecipes: normalizedRecipes.length }));
    } catch (error) {
      console.error('Error loading recipes:', error);
    } finally {
      setRecipesLoading(false);
    }
  };

  const loadFavorites = async (user?: any) => {
    const userToUse = user || currentUser;
    if (!userToUse) return;
    try {
      setFavoritesLoading(true);
      const favoritesResponse = await favoriteApi.getUserFavorites();
      const favoritesList = favoritesResponse.results || favoritesResponse;
      
      if (Array.isArray(favoritesList) && favoritesList.length > 0) {
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
        setFavorites(normalizedRecipes);
        setStats(prev => ({ ...prev, totalFavorites: normalizedRecipes.length }));
      } else {
        setFavorites([]);
        setStats(prev => ({ ...prev, totalFavorites: 0 }));
      }
    } catch (error) {
      console.error('Error loading favorites:', error);
    } finally {
      setFavoritesLoading(false);
    }
  };

  const loadRatings = async (user?: any) => {
    const userToUse = user || currentUser;
    if (!userToUse) return;
    try {
      setRatingsLoading(true);
      const response = await ratingApi.getMine();
      const ratingsData = response.results || response;
      const userRatings = Array.isArray(ratingsData) ? ratingsData : [];
      setRatings(userRatings);
      
      // Calculate average rating given
      if (userRatings.length > 0) {
        const avgRating = userRatings.reduce((sum, r) => sum + r.stars, 0) / userRatings.length;
        setStats(prev => ({ 
          ...prev, 
          totalRatings: userRatings.length,
          averageRatingGiven: avgRating 
        }));
      } else {
        setStats(prev => ({ 
          ...prev, 
          totalRatings: 0,
          averageRatingGiven: 0 
        }));
      }
    } catch (error) {
      console.error('Error loading ratings:', error);
    } finally {
      setRatingsLoading(false);
    }
  };

  const loadComments = async (user?: any) => {
    const userToUse = user || currentUser;
    if (!userToUse) return;
    try {
      setCommentsLoading(true);
      const response = await commentApi.getMine();
      const commentsData = response.results || response;
      const userComments = Array.isArray(commentsData) ? commentsData : [];
      setComments(userComments);
      setStats(prev => ({ ...prev, totalComments: userComments.length }));
    } catch (error) {
      console.error('Error loading comments:', error);
    } finally {
      setCommentsLoading(false);
    }
  };

  if (loading) {
    return (
      <main className="container">
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <p>Loading dashboard...</p>
        </div>
      </main>
    );
  }

  if (!currentUser) {
    return (
      <main className="container">
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <p>Please login to view your dashboard.</p>
          <Link href="/login" className="btn-primary" style={{ marginTop: '1rem', display: 'inline-block' }}>
            Login
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="container" style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem 1rem' }}>
      {/* Header */}
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#333' }}>
          My Dashboard
        </h1>
        <p style={{ color: '#666', fontSize: '1.1rem' }}>
          Welcome back, <strong>{currentUser.username}</strong>! Manage your recipes and activity.
        </p>
      </div>

      {/* Statistics Cards */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
        gap: '1.5rem',
        marginBottom: '2rem'
      }}>
        <div style={{
          background: 'white',
          padding: '1.5rem',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>📝</div>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#333' }}>{stats.totalRecipes}</div>
          <div style={{ color: '#666', fontSize: '0.9rem' }}>My Recipes</div>
        </div>

        <div style={{
          background: 'white',
          padding: '1.5rem',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>❤️</div>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#333' }}>{stats.totalFavorites}</div>
          <div style={{ color: '#666', fontSize: '0.9rem' }}>Favorites</div>
        </div>

        <div style={{
          background: 'white',
          padding: '1.5rem',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>⭐</div>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#333' }}>{stats.totalRatings}</div>
          <div style={{ color: '#666', fontSize: '0.9rem' }}>Ratings Given</div>
          {stats.averageRatingGiven > 0 && (
            <div style={{ color: '#999', fontSize: '0.85rem', marginTop: '0.25rem' }}>
              Avg: {stats.averageRatingGiven.toFixed(1)} ⭐
            </div>
          )}
        </div>

        <div style={{
          background: 'white',
          padding: '1.5rem',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>💬</div>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#333' }}>{stats.totalComments}</div>
          <div style={{ color: '#666', fontSize: '0.9rem' }}>Comments</div>
        </div>
      </div>

      {/* Quick Actions */}
      <div style={{ 
        display: 'flex', 
        gap: '1rem', 
        marginBottom: '2rem',
        flexWrap: 'wrap'
      }}>
        <Link href="/recipes/create" className="btn-primary">
          ➕ Create New Recipe
        </Link>
        <Link href="/favorites" className="btn-outline">
          ❤️ View Favorites
        </Link>
        <Link href={`/users/profile/${currentUser.username}`} className="btn-outline">
          👤 View Profile
        </Link>
      </div>

      {/* Tabs */}
      <div style={{
        background: 'white',
        borderRadius: '8px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        padding: '1.5rem'
      }}>
        <div style={{
          display: 'flex',
          gap: '1rem',
          borderBottom: '2px solid #e0e0e0',
          marginBottom: '2rem',
          flexWrap: 'wrap'
        }}>
          {(['recipes', 'favorites', 'ratings', 'comments'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{
                padding: '0.75rem 1.5rem',
                background: 'none',
                border: 'none',
                borderBottom: activeTab === tab ? '3px solid var(--primary-color)' : '3px solid transparent',
                cursor: 'pointer',
                fontSize: '1rem',
                fontWeight: activeTab === tab ? '600' : '400',
                color: activeTab === tab ? 'var(--primary-color)' : '#666',
                transition: 'all 0.2s',
                textTransform: 'capitalize'
              }}
            >
              {tab === 'recipes' && '📝 My Recipes'}
              {tab === 'favorites' && '❤️ Favorites'}
              {tab === 'ratings' && '⭐ My Ratings'}
              {tab === 'comments' && '💬 My Comments'}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div>
          {activeTab === 'recipes' && (
            <div>
              {recipesLoading ? (
                <RecipeGridSkeleton />
              ) : myRecipes.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '3rem' }}>
                  <p style={{ fontSize: '1.2rem', color: '#666', marginBottom: '1rem' }}>
                    You haven't created any recipes yet.
                  </p>
                  <Link href="/recipes/create" className="btn-primary">
                    Create Your First Recipe
                  </Link>
                </div>
              ) : (
                <>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                    <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#333' }}>
                      My Recipes ({myRecipes.length})
                    </h2>
                    <Link href="/recipes/create" className="btn-primary">
                      ➕ Create New
                    </Link>
                  </div>
                  <div className="recipe-grid">
                    {myRecipes.map((recipe) => (
                      <div key={recipe.id} style={{ position: 'relative' }}>
                        <RecipeCard recipe={recipe} />
                        <div style={{
                          position: 'absolute',
                          top: '0.5rem',
                          right: '0.5rem',
                          display: 'flex',
                          gap: '0.5rem'
                        }}>
                          <Link
                            href={`/recipes/${recipe.id}/edit`}
                            className="btn-outline"
                            style={{
                              padding: '0.5rem',
                              fontSize: '0.85rem',
                              background: 'white'
                            }}
                            onClick={(e) => e.stopPropagation()}
                          >
                            ✏️ Edit
                          </Link>
                        </div>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>
          )}

          {activeTab === 'favorites' && (
            <div>
              {favoritesLoading ? (
                <RecipeGridSkeleton />
              ) : favorites.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '3rem' }}>
                  <p style={{ fontSize: '1.2rem', color: '#666', marginBottom: '1rem' }}>
                    You haven't favorited any recipes yet.
                  </p>
                  <Link href="/recipes" className="btn-primary">
                    Browse Recipes
                  </Link>
                </div>
              ) : (
                <>
                  <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#333', marginBottom: '1.5rem' }}>
                    Favorite Recipes ({favorites.length})
                  </h2>
                  <div className="recipe-grid">
                    {favorites.map((recipe) => (
                      <RecipeCard key={recipe.id} recipe={recipe} />
                    ))}
                  </div>
                </>
              )}
            </div>
          )}

          {activeTab === 'ratings' && (
            <div>
              {ratingsLoading ? (
                <div style={{ textAlign: 'center', padding: '3rem' }}>
                  <p>Loading ratings...</p>
                </div>
              ) : ratings.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '3rem' }}>
                  <p style={{ fontSize: '1.2rem', color: '#666', marginBottom: '1rem' }}>
                    You haven't rated any recipes yet.
                  </p>
                  <Link href="/recipes" className="btn-primary">
                    Browse Recipes
                  </Link>
                </div>
              ) : (
                <>
                  <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#333', marginBottom: '1.5rem' }}>
                    My Ratings ({ratings.length})
                  </h2>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    {ratings.map((rating) => (
                      <div
                        key={rating.id}
                        style={{
                          padding: '1.5rem',
                          background: '#f8f9fa',
                          borderRadius: '8px',
                          border: '1px solid #e0e0e0'
                        }}
                      >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.5rem' }}>
                          <div>
                            <Link 
                              href={`/recipes/${rating.recipe}`}
                              style={{ 
                                fontSize: '1.1rem', 
                                fontWeight: '600', 
                                color: '#333',
                                textDecoration: 'none'
                              }}
                            >
                              {rating.recipe_title}
                            </Link>
                            <div style={{ marginTop: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                              <span style={{ fontSize: '1.2rem' }}>
                                {'⭐'.repeat(rating.stars)}{'☆'.repeat(5 - rating.stars)}
                              </span>
                              <span style={{ color: '#666', fontSize: '0.9rem' }}>
                                {rating.stars} out of 5 stars
                              </span>
                            </div>
                          </div>
                          <span style={{ color: '#999', fontSize: '0.85rem' }}>
                            {new Date(rating.created_at).toLocaleDateString()}
                          </span>
                        </div>
                        {rating.review_text && (
                          <p style={{ color: '#666', marginTop: '0.75rem', lineHeight: '1.6' }}>
                            {rating.review_text}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>
          )}

          {activeTab === 'comments' && (
            <div>
              {commentsLoading ? (
                <div style={{ textAlign: 'center', padding: '3rem' }}>
                  <p>Loading comments...</p>
                </div>
              ) : comments.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '3rem' }}>
                  <p style={{ fontSize: '1.2rem', color: '#666', marginBottom: '1rem' }}>
                    You haven't commented on any recipes yet.
                  </p>
                  <Link href="/recipes" className="btn-primary">
                    Browse Recipes
                  </Link>
                </div>
              ) : (
                <>
                  <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#333', marginBottom: '1.5rem' }}>
                    My Comments ({comments.length})
                  </h2>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    {comments.map((comment) => (
                      <div
                        key={comment.id}
                        style={{
                          padding: '1.5rem',
                          background: '#f8f9fa',
                          borderRadius: '8px',
                          border: '1px solid #e0e0e0'
                        }}
                      >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.5rem' }}>
                          <Link 
                            href={`/recipes/${comment.recipe}`}
                            style={{ 
                              fontSize: '1.1rem', 
                              fontWeight: '600', 
                              color: '#333',
                              textDecoration: 'none'
                            }}
                          >
                            {comment.recipe_title}
                          </Link>
                          <span style={{ color: '#999', fontSize: '0.85rem' }}>
                            {new Date(comment.created_at).toLocaleDateString()}
                          </span>
                        </div>
                        <p style={{ color: '#666', marginTop: '0.75rem', lineHeight: '1.6' }}>
                          {comment.text}
                        </p>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}

