'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { recipeApi, Recipe } from '@/lib/api';
import ImageUpload from '@/components/ImageUpload';
import IngredientForm, { Ingredient } from '@/components/IngredientForm';
import InstructionStepEditor, { InstructionStep } from '@/components/InstructionStepEditor';
import { uploadToBlob } from '@/lib/vercel-blob';

export default function EditRecipePage() {
  const params = useParams();
  const router = useRouter();
  const recipeId = parseInt(params.id as string);

  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    prep_time: '',
    cook_time: '',
    category: '',
    dietary_restrictions: 'none',
    is_published: true,
  });
  const [image, setImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [instructionSteps, setInstructionSteps] = useState<InstructionStep[]>([]);
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
        prep_time: data.prep_time.toString(),
        cook_time: data.cook_time.toString(),
        category: data.category?.id?.toString() || '',
        dietary_restrictions: data.dietary_restrictions || 'none',
        is_published: data.is_published,
      });
      if (data.image) {
        setImagePreview(data.image.startsWith('http') ? data.image : `http://127.0.0.1:8000${data.image}`);
      }
      
      // Load ingredients if available
      if (data.recipe_ingredients && Array.isArray(data.recipe_ingredients)) {
        const loadedIngredients: Ingredient[] = data.recipe_ingredients.map((ri: any) => ({
          id: ri.id,
          name: ri.ingredient?.name || '',
          quantity: ri.quantity?.toString() || '',
          unit: ri.unit || '',
          notes: ri.notes || '',
        }));
        setIngredients(loadedIngredients);
      }

      // Load instruction steps
      try {
        const parsedInstructions = JSON.parse(data.instructions);
        if (Array.isArray(parsedInstructions)) {
          const loadedSteps: InstructionStep[] = parsedInstructions.map((step: any, index: number) => ({
            id: `step-${index}`,
            text: step.text || '',
            image: null,
            imageUrl: step.imageUrl || null,
          }));
          setInstructionSteps(loadedSteps.length > 0 ? loadedSteps : [{ id: '1', text: '', image: null, imageUrl: null }]);
        } else {
          // Fallback: parse as plain text
          const lines = data.instructions.split('\n').filter((line: string) => line.trim().length > 0);
          setInstructionSteps(lines.map((line: string, index: number) => ({
            id: `step-${index}`,
            text: line.replace(/^\d+\.\s*/, '').trim(),
            image: null,
            imageUrl: null,
          })));
        }
      } catch {
        // Not JSON, parse as plain text
        const lines = data.instructions.split('\n').filter((line: string) => line.trim().length > 0);
        setInstructionSteps(lines.length > 0 ? lines.map((line: string, index: number) => ({
          id: `step-${index}`,
          text: line.replace(/^\d+\.\s*/, '').trim(),
          image: null,
          imageUrl: null,
        })) : [{ id: '1', text: '', image: null, imageUrl: null }]);
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load recipe');
      console.error('Error loading recipe:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleImageChange = (file: File | null) => {
    setImage(file);
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    } else {
      setImagePreview(recipe?.image ? (recipe.image.startsWith('http') ? recipe.image : `http://127.0.0.1:8000${recipe.image}`) : null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSaving(true);

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

          <ImageUpload 
            onImageChange={handleImageChange}
            currentImage={recipe.image ? (recipe.image.startsWith('http') ? recipe.image : `http://127.0.0.1:8000${recipe.image}`) : null}
            label="Recipe Image"
          />

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

