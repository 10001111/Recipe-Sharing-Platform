'use client';

import { useState } from 'react';
import { getPlaceholderImage, handleImageError, PlaceholderType } from '@/lib/placeholders';

interface RecipeImageProps {
  src: string | null | undefined;
  alt: string;
  placeholderType?: PlaceholderType;
  className?: string;
  style?: React.CSSProperties;
  width?: number;
  height?: number;
  objectFit?: 'cover' | 'contain' | 'fill' | 'none' | 'scale-down';
}

export default function RecipeImage({
  src,
  alt,
  placeholderType = 'recipe',
  className = '',
  style = {},
  width,
  height,
  objectFit = 'cover',
}: RecipeImageProps) {
  const [imageSrc, setImageSrc] = useState<string>(
    src || getPlaceholderImage(placeholderType)
  );
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  const handleError = (e: React.SyntheticEvent<HTMLImageElement, Event>) => {
    setHasError(true);
    setIsLoading(false);
    handleImageError(e, placeholderType);
    setImageSrc(getPlaceholderImage(placeholderType));
  };

  const handleLoad = () => {
    setIsLoading(false);
  };

  return (
    <div
      style={{
        position: 'relative',
        width: width || '100%',
        height: height || 'auto',
        backgroundColor: '#f0f0f0',
        borderRadius: '8px',
        overflow: 'hidden',
        ...style,
      }}
      className={className}
    >
      {isLoading && !hasError && (
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#f0f0f0',
            zIndex: 1,
          }}
        >
          <div
            style={{
              width: '40px',
              height: '40px',
              border: '3px solid #e0e0e0',
              borderTopColor: '#666',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite',
            }}
          />
        </div>
      )}
      <img
        src={imageSrc}
        alt={alt}
        onError={handleError}
        onLoad={handleLoad}
        style={{
          width: '100%',
          height: height || '100%',
          objectFit,
          display: 'block',
          opacity: isLoading ? 0 : 1,
          transition: 'opacity 0.3s ease',
        }}
      />
      <style jsx>{`
        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }
      `}</style>
    </div>
  );
}

