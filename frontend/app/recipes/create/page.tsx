'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { recipeApi } from '@/lib/api';
import ImageUploadBlob from '@/components/ImageUploadBlob';
import ImageGallery, { ImageItem } from '@/components/ImageGallery';
import IngredientForm, { Ingredient } from '@/components/IngredientForm';
import InstructionStepEditor, { InstructionStep } from '@/components/InstructionStepEditor';
import { uploadToBlob } from '@/lib/vercel-blob';

export default function CreateRecipePage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    prep_time: '',
    cook_time: '',
    category: '',
    dietary_restrictions: 'none',
    is_published: true,
  });
  const [imageUrl, setImageUrl] = useState<string | null>(null); // For backward compatibility
  const [images, setImages] = useState<ImageItem[]>([]); // Multiple images
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [instructionSteps, setInstructionSteps] = useState<InstructionStep[]>([
    { id: '1', text: '', image: null, imageUrl: null }
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Process instruction steps: upload images and format as JSON
      const processedSteps = await Promise.all(
        instructionSteps.map(async (step) => {
          let imageUrl = step.imageUrl || null;
          
          // Upload step image if provided
          if (step.image) {
            try {
              const blobResponse = await uploadToBlob(step.image, 'recipe-steps/');
              imageUrl = blobResponse.url;
            } catch (err) {
              console.error('Error uploading step image:', err);
              // Fall back to FormData upload if blob fails
            }
          }
          
          return {
            text: step.text,
            imageUrl: imageUrl,
          };
        })
      );

      // Format instructions as JSON string
      const instructionsJson = JSON.stringify(processedSteps);

      // Format ingredients data
      const ingredientsData = ingredients.map(ing => ({
        name: ing.name,
        quantity: parseFloat(ing.quantity) || 0,
        unit: ing.unit || '',
        notes: ing.notes || '',
      }));

      const formDataToSend = new FormData();
      formDataToSend.append('title', formData.title);
      formDataToSend.append('description', formData.description);
      formDataToSend.append('instructions', instructionsJson);
      formDataToSend.append('prep_time', formData.prep_time);
      formDataToSend.append('cook_time', formData.cook_time);
      if (formData.category) {
        formDataToSend.append('category_id', formData.category);
      }
      formDataToSend.append('dietary_restrictions', formData.dietary_restrictions);
      formDataToSend.append('is_published', formData.is_published.toString());
      formDataToSend.append('ingredients_data', JSON.stringify(ingredientsData));
      
      // Handle images: use multiple images if available, otherwise fall back to single image
      if (images.length > 0) {
        const imagesData = images.map(img => ({
          image_url: img.image_url,
          is_primary: img.is_primary,
          order: img.order,
          alt_text: img.alt_text || '',
        }));
        formDataToSend.append('images_data', JSON.stringify(imagesData));
      } else if (imageUrl) {
        // Backward compatibility: if only single image URL, create images_data with it
        formDataToSend.append('images_data', JSON.stringify([{
          image_url: imageUrl,
          is_primary: true,
          order: 0,
          alt_text: '',
        }]));
      }

      const recipe = await recipeApi.create(formDataToSend);
      router.push(`/recipes/${recipe.id}`);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to create recipe');
      console.error('Error creating recipe:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <div className="form-container">
        <h1 style={{ marginBottom: '1rem' }}>Create New Recipe</h1>

        {error && (
          <div style={{ 
            background: '#fee', 
            color: '#c33', 
            padding: '1rem', 
            borderRadius: '4px',
            marginBottom: '1rem'
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Title *</label>
            <input
              type="text"
              className="form-input"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Description *</label>
            <textarea
              className="form-textarea"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              required
              rows={4}
            />
          </div>

          <InstructionStepEditor 
            steps={instructionSteps}
            onChange={setInstructionSteps}
          />

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div className="form-group">
              <label className="form-label">Prep Time (minutes) *</label>
              <input
                type="number"
                className="form-input"
                value={formData.prep_time}
                onChange={(e) => setFormData({ ...formData, prep_time: e.target.value })}
                required
                min="0"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Cook Time (minutes) *</label>
              <input
                type="number"
                className="form-input"
                value={formData.cook_time}
                onChange={(e) => setFormData({ ...formData, cook_time: e.target.value })}
                required
                min="0"
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div className="form-group">
              <label className="form-label">Category</label>
              <select
                className="form-select"
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              >
                <option value="">Select a category</option>
                <option value="1">Breakfast</option>
                <option value="2">Lunch</option>
                <option value="3">Dinner</option>
                <option value="4">Dessert</option>
                <option value="5">Snack</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Dietary Restrictions</label>
              <select
                className="form-select"
                value={formData.dietary_restrictions}
                onChange={(e) => setFormData({ ...formData, dietary_restrictions: e.target.value })}
              >
                <option value="none">No Restrictions</option>
                <option value="vegetarian">Vegetarian</option>
                <option value="vegan">Vegan</option>
                <option value="gluten-free">Gluten-Free</option>
                <option value="keto">Keto</option>
                <option value="paleo">Paleo</option>
                <option value="pescatarian">Pescatarian</option>
                <option value="halal">Halal</option>
                <option value="kosher">Kosher</option>
              </select>
            </div>
          </div>

          {/* Multiple Images Gallery */}
          <ImageGallery
            images={images}
            onImagesChange={setImages}
            maxImages={10}
            imageType="recipe"
            path="recipes/"
          />
          
          {/* Single Image Upload (for backward compatibility) */}
          <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid #e0e0e0' }}>
            <small style={{ color: '#666', display: 'block', marginBottom: '0.5rem' }}>
              Or upload a single image (legacy):
            </small>
            <ImageUploadBlob
              onImageUrlChange={setImageUrl}
              currentImageUrl={imageUrl}
              label="Single Recipe Image (Optional)"
              path="recipes/"
              imageType="recipe"
            />
          </div>

          <IngredientForm 
            ingredients={ingredients}
            onChange={setIngredients}
          />

          <div className="form-group">
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <input
                type="checkbox"
                checked={formData.is_published}
                onChange={(e) => setFormData({ ...formData, is_published: e.target.checked })}
              />
              Publish recipe (make it visible to others)
            </label>
          </div>

          <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
            <button 
              type="submit" 
              className="btn-primary"
              disabled={loading}
              style={{ flex: '1' }}
            >
              {loading ? 'Creating...' : 'Create Recipe'}
            </button>
            <button 
              type="button"
              onClick={() => router.back()}
              className="btn-outline"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}

