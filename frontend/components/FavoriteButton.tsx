'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { favoriteApi } from '@/lib/api';

interface FavoriteButtonProps {
  recipeId: number;
  initialFavorited: boolean;
  initialCount: number;
  onToggle?: (isFavorited: boolean, count: number) => void;
  variant?: 'default' | 'icon' | 'text';
}

export default function FavoriteButton({ 
  recipeId, 
  initialFavorited, 
  initialCount,
  onToggle,
  variant = 'default'
}: FavoriteButtonProps) {
  const router = useRouter();
  const [isFavorited, setIsFavorited] = useState(initialFavorited);
  const [favoriteCount, setFavoriteCount] = useState(initialCount);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setIsFavorited(initialFavorited);
    setFavoriteCount(initialCount);
  }, [initialFavorited, initialCount]);

  const handleToggle = async () => {
    if (loading) return;
    
    setLoading(true);
    try {
      const response = await favoriteApi.toggle(recipeId);
      setIsFavorited(response.is_favorited);
      setFavoriteCount(response.favorite_count);
      
      if (onToggle) {
        onToggle(response.is_favorited, response.favorite_count);
      }
    } catch (error: any) {
      console.error('Error toggling favorite:', error);
      if (error.response?.status === 401) {
        alert('Please login to favorite recipes.');
        router.push('/login');
      } else {
        alert('Failed to update favorite. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  if (variant === 'icon') {
    return (
      <button
        onClick={handleToggle}
        disabled={loading}
        style={{
          background: 'none',
          border: 'none',
          cursor: loading ? 'wait' : 'pointer',
          fontSize: '1.5rem',
          padding: '0.5rem',
          transition: 'transform 0.2s',
        }}
        onMouseEnter={(e) => {
          if (!loading) e.currentTarget.style.transform = 'scale(1.1)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1)';
        }}
        title={isFavorited ? 'Remove from favorites' : 'Add to favorites'}
      >
        {isFavorited ? '❤️' : '🤍'}
      </button>
    );
  }

  if (variant === 'text') {
    return (
      <button
        onClick={handleToggle}
        disabled={loading}
        style={{
          background: 'none',
          border: 'none',
          cursor: loading ? 'wait' : 'pointer',
          color: isFavorited ? '#ff6b6b' : '#666',
          padding: '0.5rem',
          fontSize: '0.9rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
        }}
      >
        <span>{isFavorited ? '❤️' : '🤍'}</span>
        <span>{isFavorited ? 'Favorited' : 'Favorite'}</span>
        {favoriteCount > 0 && (
          <span style={{ fontSize: '0.85rem', color: '#999' }}>
            ({favoriteCount})
          </span>
        )}
      </button>
    );
  }

  return (
    <button
      onClick={handleToggle}
      disabled={loading}
      className={isFavorited ? 'btn-primary' : 'btn-outline'}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        opacity: loading ? 0.6 : 1,
      }}
    >
      <span>{isFavorited ? '❤️' : '🤍'}</span>
      <span>{loading ? '...' : isFavorited ? 'Favorited' : 'Favorite'}</span>
      {favoriteCount > 0 && (
        <span style={{ fontSize: '0.85rem', opacity: 0.8 }}>
          ({favoriteCount})
        </span>
      )}
    </button>
  );
}

