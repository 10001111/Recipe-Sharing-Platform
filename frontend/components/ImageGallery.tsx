'use client';

import { useState } from 'react';
import { uploadToBlob, deleteFromBlob } from '@/lib/vercel-blob';
import { validateImage, formatFileSize } from '@/lib/image-validation';
import { compressImage, getCompressionOptionsFor, getCompressionStats } from '@/lib/image-compression';
import RecipeImage from './RecipeImage';

export interface ImageItem {
  id?: number;
  image_url: string;
  is_primary: boolean;
  order: number;
  alt_text?: string;
}

interface ImageGalleryProps {
  images: ImageItem[];
  onImagesChange: (images: ImageItem[]) => void;
  maxImages?: number;
  imageType?: 'recipe' | 'step' | 'avatar';
  path?: string;
}

export default function ImageGallery({
  images,
  onImagesChange,
  maxImages = 10,
  imageType = 'recipe',
  path = 'recipes/',
}: ImageGalleryProps) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [draggedIndex, setDraggedIndex] = useState<number | null>(null);

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    if (files.length === 0) return;

    // Check max images limit
    if (images.length + files.length > maxImages) {
      setError(`Maximum ${maxImages} images allowed. Please remove some images first.`);
      return;
    }

    setError(null);
    setUploading(true);

    try {
      const newImages: ImageItem[] = [];

      for (const file of files) {
        // Validate image
        const validationResult = await validateImage(file, {
          maxSizeMB: 5,
          checkDimensions: true,
        });

        if (!validationResult.valid) {
          setError(`Invalid image: ${validationResult.error}`);
          continue;
        }

        // Compress image
        const compressionOptions = getCompressionOptionsFor(imageType);
        const compressedFile = await compressImage(file, compressionOptions);

        // Upload to Vercel Blob
        const blobResponse = await uploadToBlob(compressedFile, path);

        // Add to images array
        newImages.push({
          image_url: blobResponse.url,
          is_primary: images.length === 0 && newImages.length === 0, // First image is primary
          order: images.length + newImages.length,
          alt_text: file.name.replace(/\.[^/.]+$/, ''), // Remove extension for alt text
        });
      }

      // Update images
      onImagesChange([...images, ...newImages]);
    } catch (err: any) {
      setError(err.message || 'Failed to upload images');
    } finally {
      setUploading(false);
      // Reset file input
      e.target.value = '';
    }
  };

  const handleRemoveImage = async (index: number) => {
    const imageToRemove = images[index];
    
    // Delete from blob storage if URL exists
    if (imageToRemove.image_url && imageToRemove.image_url.includes('blob.vercel-storage.com')) {
      try {
        await deleteFromBlob(imageToRemove.image_url);
      } catch (err) {
        console.error('Error deleting blob:', err);
        // Continue with removal even if delete fails
      }
    }

    const newImages = images.filter((_, i) => i !== index);
    
    // If removed image was primary, make first image primary
    if (imageToRemove.is_primary && newImages.length > 0) {
      newImages[0].is_primary = true;
    }
    
    // Reorder images
    newImages.forEach((img, idx) => {
      img.order = idx;
    });

    onImagesChange(newImages);
  };

  const handleSetPrimary = (index: number) => {
    const newImages = images.map((img, idx) => ({
      ...img,
      is_primary: idx === index,
    }));
    onImagesChange(newImages);
  };

  const handleDragStart = (index: number) => {
    setDraggedIndex(index);
  };

  const handleDragOver = (e: React.DragEvent, index: number) => {
    e.preventDefault();
    if (draggedIndex === null || draggedIndex === index) return;

    const newImages = [...images];
    const draggedImage = newImages[draggedIndex];
    newImages.splice(draggedIndex, 1);
    newImages.splice(index, 0, draggedImage);
    
    // Update order
    newImages.forEach((img, idx) => {
      img.order = idx;
    });

    onImagesChange(newImages);
    setDraggedIndex(index);
  };

  const handleDragEnd = () => {
    setDraggedIndex(null);
  };

  return (
    <div className="form-group">
      <label className="form-label">Recipe Images</label>
      
      {error && (
        <div style={{
          background: '#fee',
          color: '#c33',
          padding: '0.75rem',
          borderRadius: '4px',
          marginBottom: '1rem',
          fontSize: '0.9rem'
        }}>
          {error}
        </div>
      )}

      {/* Image Grid */}
      {images.length > 0 && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))',
          gap: '1rem',
          marginBottom: '1rem'
        }}>
          {images.map((image, index) => (
            <div
              key={index}
              draggable
              onDragStart={() => handleDragStart(index)}
              onDragOver={(e) => handleDragOver(e, index)}
              onDragEnd={handleDragEnd}
              style={{
                position: 'relative',
                border: image.is_primary ? '3px solid var(--primary-color)' : '2px solid #e0e0e0',
                borderRadius: '8px',
                overflow: 'hidden',
                cursor: 'move',
                opacity: draggedIndex === index ? 0.5 : 1,
              }}
            >
              <RecipeImage
                src={image.image_url}
                alt={image.alt_text || `Recipe image ${index + 1}`}
                placeholderType="recipe"
                style={{
                  width: '100%',
                  height: '150px',
                }}
              />
              
              {/* Primary Badge */}
              {image.is_primary && (
                <div style={{
                  position: 'absolute',
                  top: '4px',
                  left: '4px',
                  background: 'var(--primary-color)',
                  color: 'white',
                  padding: '0.25rem 0.5rem',
                  borderRadius: '4px',
                  fontSize: '0.75rem',
                  fontWeight: 'bold'
                }}>
                  Primary
                </div>
              )}

              {/* Actions */}
              <div style={{
                position: 'absolute',
                top: '4px',
                right: '4px',
                display: 'flex',
                gap: '0.25rem'
              }}>
                {!image.is_primary && (
                  <button
                    type="button"
                    onClick={() => handleSetPrimary(index)}
                    style={{
                      background: 'rgba(255, 255, 255, 0.9)',
                      border: 'none',
                      borderRadius: '4px',
                      padding: '0.25rem 0.5rem',
                      cursor: 'pointer',
                      fontSize: '0.75rem',
                      fontWeight: 'bold'
                    }}
                    title="Set as primary"
                  >
                    ⭐
                  </button>
                )}
                <button
                  type="button"
                  onClick={() => handleRemoveImage(index)}
                  style={{
                    background: 'rgba(220, 53, 69, 0.9)',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    padding: '0.25rem 0.5rem',
                    cursor: 'pointer',
                    fontSize: '0.75rem'
                  }}
                  title="Remove image"
                >
                  ×
                </button>
              </div>

              {/* Order Number */}
              <div style={{
                position: 'absolute',
                bottom: '4px',
                left: '4px',
                background: 'rgba(0, 0, 0, 0.7)',
                color: 'white',
                padding: '0.25rem 0.5rem',
                borderRadius: '4px',
                fontSize: '0.75rem',
                fontWeight: 'bold'
              }}>
                #{index + 1}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Upload Input */}
      <div>
        <input
          type="file"
          accept="image/*"
          multiple
          onChange={handleFileSelect}
          disabled={uploading || images.length >= maxImages}
          className="form-input"
        />
        <small style={{ color: '#666', display: 'block', marginTop: '0.5rem' }}>
          {images.length >= maxImages 
            ? `Maximum ${maxImages} images reached`
            : `Upload multiple images (${images.length}/${maxImages}). Drag to reorder, click ⭐ to set primary.`}
        </small>
        {uploading && (
          <div style={{ marginTop: '0.5rem', color: '#666', fontSize: '0.9rem' }}>
            ⏳ Uploading images...
          </div>
        )}
      </div>
    </div>
  );
}

