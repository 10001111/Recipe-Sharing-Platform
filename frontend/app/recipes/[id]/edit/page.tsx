'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { recipeApi, Recipe } from '@/lib/api';

export default function EditRecipePage() {
  const params = useParams();
  const router = useRouter();
  const recipeId = parseInt(params.id as string);

  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    instructions: '',
    prep_time: '',
    cook_time: '',
    category: '',
    is_published: true,
  });
  const [image, setImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (recipeId) {
      loadRecipe();
    }
  }, [recipeId]);

  const loadRecipe = async () => {
    try {
      setLoading(true);
      const data = await recipeApi.getById(recipeId);
      setRecipe(data);
      setFormData({
        title: data.title,
        description: data.description,
        instructions: data.instructions,
        prep_time: data.prep_time.toString(),
        cook_time: data.cook_time.toString(),
        category: data.category?.id?.toString() || '',
        is_published: data.is_published,
      });
      if (data.image) {
        setImagePreview(data.image.startsWith('http') ? data.image : `http://127.0.0.1:8000${data.image}`);
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load recipe');
      console.error('Error loading recipe:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSaving(true);

    try {
      const formDataToSend = new FormData();
      formDataToSend.append('title', formData.title);
      formDataToSend.append('description', formData.description);
      formDataToSend.append('instructions', formData.instructions);
      formDataToSend.append('prep_time', formData.prep_time);
      formDataToSend.append('cook_time', formData.cook_time);
      if (formData.category) {
        formDataToSend.append('category_id', formData.category);
      }
      formDataToSend.append('is_published', formData.is_published.toString());
      if (image) {
        formDataToSend.append('image', image);
      }

      await recipeApi.update(recipeId, formDataToSend);
      router.push(`/recipes/${recipeId}`);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to update recipe');
      console.error('Error updating recipe:', err);
    } finally {
      setSaving(false);
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
          <p>Recipe not found</p>
          <button onClick={() => router.back()} className="btn-primary" style={{ marginTop: '1rem' }}>
            Go Back
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="container">
      <div className="form-container">
        <h1 style={{ marginBottom: '1rem' }}>Edit Recipe</h1>

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

          <div className="form-group">
            <label className="form-label">Instructions *</label>
            <textarea
              className="form-textarea"
              value={formData.instructions}
              onChange={(e) => setFormData({ ...formData, instructions: e.target.value })}
              required
              rows={10}
            />
          </div>

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
            <label className="form-label">Recipe Image</label>
            {imagePreview && (
              <div style={{ marginBottom: '1rem' }}>
                <img 
                  src={imagePreview} 
                  alt="Preview" 
                  style={{ 
                    maxWidth: '100%', 
                    maxHeight: '300px', 
                    borderRadius: '8px',
                    objectFit: 'cover'
                  }} 
                />
              </div>
            )}
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              className="form-input"
            />
            <small style={{ color: '#666', display: 'block', marginTop: '0.5rem' }}>
              Leave empty to keep current image
            </small>
          </div>

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
              disabled={saving}
              style={{ flex: '1' }}
            >
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
            <button 
              type="button"
              onClick={() => router.push(`/recipes/${recipeId}`)}
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

