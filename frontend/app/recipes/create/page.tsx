'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { recipeApi } from '@/lib/api';

export default function CreateRecipePage() {
  const router = useRouter();
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
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

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
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setImage(e.target.files?.[0] || null)}
              className="form-input"
            />
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

