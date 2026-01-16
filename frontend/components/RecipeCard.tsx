'use client';

import { useRouter } from 'next/navigation';
import { RecipeList } from '@/lib/api';
import RecipeImage from './RecipeImage';
import { getImageUrlOrPlaceholder } from '@/lib/placeholders';

interface RecipeCardProps {
  recipe: RecipeList;
}

export default function RecipeCard({ recipe }: RecipeCardProps) {
  const router = useRouter();

  // Get primary image or first image, or use placeholder
  const primaryImage = (recipe as any).images?.find((img: any) => img.is_primary) 
    || (recipe as any).images?.[0] 
    || null;
  const imageUrl = primaryImage?.image_url || recipe.image || null;
  const displayImageUrl = getImageUrlOrPlaceholder(imageUrl, 'recipe');

  return (
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
        <RecipeImage
          src={displayImageUrl}
          alt={recipe.title}
          placeholderType="recipe"
          className="recipe-card-image"
          style={{
            width: '100%',
            height: '200px',
            objectFit: 'cover',
          }}
        />
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
          {recipe.category && (
            <div style={{ marginTop: '0.75rem' }}>
              <span style={{ 
                background: '#f0f0f0', 
                padding: '0.25rem 0.5rem', 
                borderRadius: '4px',
                fontSize: '0.85rem',
                color: '#666'
              }}>
                {recipe.category.name}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

