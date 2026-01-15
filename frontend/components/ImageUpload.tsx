'use client';

import { useState, useRef } from 'react';

interface ImageUploadProps {
  onImageChange: (file: File | null) => void;
  currentImage?: string | null;
  label?: string;
}

export default function ImageUpload({ onImageChange, currentImage, label = 'Recipe Image' }: ImageUploadProps) {
  const [imagePreview, setImagePreview] = useState<string | null>(currentImage || null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
      }
      
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        alert('Image size must be less than 5MB');
        return;
      }

      onImageChange(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    } else {
      onImageChange(null);
      setImagePreview(currentImage || null);
    }
  };

  const handleRemoveImage = () => {
    onImageChange(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="form-group">
      <label className="form-label">{label}</label>
      
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
        </div>
      )}
      
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleImageChange}
        className="form-input"
      />
      <small style={{ color: '#666', display: 'block', marginTop: '0.5rem' }}>
        {currentImage && !imagePreview ? 'Leave empty to keep current image' : 'Max file size: 5MB. Supported formats: JPG, PNG, GIF, WebP'}
      </small>
    </div>
  );
}

