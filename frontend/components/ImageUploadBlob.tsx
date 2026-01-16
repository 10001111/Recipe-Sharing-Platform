'use client';

import { useState, useRef } from 'react';
import { uploadToBlob, deleteFromBlob } from '@/lib/vercel-blob';
import { validateImage, formatFileSize, ImageValidationOptions } from '@/lib/image-validation';
import { compressImage, getCompressionOptionsFor, getCompressionStats } from '@/lib/image-compression';

interface ImageUploadBlobProps {
  onImageUrlChange: (url: string | null) => void;
  currentImageUrl?: string | null;
  label?: string;
  path?: string;
  imageType?: 'recipe' | 'step' | 'avatar';
  validationOptions?: ImageValidationOptions;
  enableCompression?: boolean;
}

export default function ImageUploadBlob({ 
  onImageUrlChange, 
  currentImageUrl, 
  label = 'Recipe Image',
  path = 'recipes/',
  imageType = 'recipe',
  validationOptions,
  enableCompression = true,
}: ImageUploadBlobProps) {
  const [imagePreview, setImagePreview] = useState<string | null>(currentImageUrl || null);
  const [uploading, setUploading] = useState(false);
  const [compressing, setCompressing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [compressionStats, setCompressionStats] = useState<{ original: string; compressed: string; reduction: string } | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setError(null);
    setCompressionStats(null);
    setCompressing(false);
    setUploading(true);

    try {
      // Step 1: Validate image
      const validationResult = await validateImage(file, {
        maxSizeMB: validationOptions?.maxSizeMB || 5,
        maxWidth: validationOptions?.maxWidth,
        maxHeight: validationOptions?.maxHeight,
        minWidth: validationOptions?.minWidth,
        minHeight: validationOptions?.minHeight,
        checkDimensions: validationOptions?.checkDimensions !== false,
      });

      if (!validationResult.valid) {
        setError(validationResult.error || 'Invalid image file');
        if (fileInputRef.current) {
          fileInputRef.current.value = '';
        }
        setUploading(false);
        return;
      }

      // Step 2: Create preview immediately
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);

      // Step 3: Compress image (if enabled)
      let fileToUpload = file;
      if (enableCompression) {
        setCompressing(true);
        const compressionOptions = getCompressionOptionsFor(imageType);
        fileToUpload = await compressImage(file, compressionOptions);
        
        // Update preview with compressed version
        const compressedReader = new FileReader();
        compressedReader.onloadend = () => {
          setImagePreview(compressedReader.result as string);
        };
        compressedReader.readAsDataURL(fileToUpload);
        
        // Show compression stats
        const stats = getCompressionStats(file, fileToUpload);
        setCompressionStats({
          original: formatFileSize(stats.originalSize),
          compressed: formatFileSize(stats.compressedSize),
          reduction: `${stats.reductionPercent}%`,
        });
        setCompressing(false);
      }

      // Step 4: Upload to Vercel Blob Storage
      const blobResponse = await uploadToBlob(fileToUpload, path);
      
      // Step 5: Update parent with blob URL
      onImageUrlChange(blobResponse.url);
      setImagePreview(blobResponse.url);
    } catch (err: any) {
      setError(err.message || 'Failed to upload image');
      setImagePreview(null);
      onImageUrlChange(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } finally {
      setUploading(false);
      setCompressing(false);
    }
  };

  const handleRemoveImage = async () => {
    // Delete from blob storage if URL exists
    if (currentImageUrl && currentImageUrl.includes('blob.vercel-storage.com')) {
      try {
        await deleteFromBlob(currentImageUrl);
      } catch (err) {
        console.error('Error deleting blob:', err);
        // Continue with removal even if delete fails
      }
    }

    onImageUrlChange(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="form-group">
      <label className="form-label">{label}</label>
      
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
      
      {imagePreview && (
        <div style={{ 
          marginBottom: '1rem', 
          position: 'relative',
          display: 'inline-block'
        }}>
          <img 
            src={imagePreview} 
            alt="Preview" 
            style={{ 
              maxWidth: '100%', 
              maxHeight: '300px', 
              borderRadius: '8px',
              objectFit: 'cover',
              border: '2px solid #e0e0e0'
            }} 
          />
          {!uploading && (
            <button
              type="button"
              onClick={handleRemoveImage}
              style={{
                position: 'absolute',
                top: '8px',
                right: '8px',
                background: 'rgba(220, 53, 69, 0.9)',
                color: 'white',
                border: 'none',
                borderRadius: '50%',
                width: '32px',
                height: '32px',
                cursor: 'pointer',
                fontSize: '18px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
              }}
              title="Remove image"
            >
              ×
            </button>
          )}
        </div>
      )}
      
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleImageChange}
        className="form-input"
        disabled={uploading}
      />
      
      {(uploading || compressing) && (
        <div style={{ 
          marginTop: '0.5rem', 
          color: '#666', 
          fontSize: '0.9rem' 
        }}>
          {compressing ? '🔄 Compressing image...' : '⏳ Uploading to Vercel Blob Storage...'}
        </div>
      )}
      
      {compressionStats && !uploading && (
        <div style={{ 
          marginTop: '0.5rem', 
          color: '#28a745', 
          fontSize: '0.85rem',
          padding: '0.5rem',
          background: '#f0f9f0',
          borderRadius: '4px'
        }}>
          ✓ Compressed: {compressionStats.original} → {compressionStats.compressed} ({compressionStats.reduction} reduction)
        </div>
      )}
      
      <small style={{ color: '#666', display: 'block', marginTop: '0.5rem' }}>
        {currentImageUrl && !imagePreview ? 'Leave empty to keep current image' : 
         enableCompression 
           ? 'Max file size: 5MB. Images will be automatically compressed and optimized.'
           : 'Max file size: 5MB. Images stored on Vercel Blob Storage.'}
      </small>
    </div>
  );
}

