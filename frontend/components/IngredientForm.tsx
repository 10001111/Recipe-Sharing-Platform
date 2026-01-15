'use client';

import { useState } from 'react';

export interface Ingredient {
  id?: number;
  name: string;
  quantity: string;
  unit: string;
  notes: string;
}

interface IngredientFormProps {
  ingredients: Ingredient[];
  onChange: (ingredients: Ingredient[]) => void;
}

export default function IngredientForm({ ingredients, onChange }: IngredientFormProps) {
  const [localIngredients, setLocalIngredients] = useState<Ingredient[]>(ingredients);

  const updateIngredients = (newIngredients: Ingredient[]) => {
    setLocalIngredients(newIngredients);
    onChange(newIngredients);
  };

  const addIngredient = () => {
    const newIngredient: Ingredient = {
      name: '',
      quantity: '',
      unit: '',
      notes: '',
    };
    updateIngredients([...localIngredients, newIngredient]);
  };

  const removeIngredient = (index: number) => {
    const newIngredients = localIngredients.filter((_, i) => i !== index);
    updateIngredients(newIngredients);
  };

  const updateIngredient = (index: number, field: keyof Ingredient, value: string) => {
    const newIngredients = [...localIngredients];
    newIngredients[index] = {
      ...newIngredients[index],
      [field]: value,
    };
    updateIngredients(newIngredients);
  };

  const commonUnits = ['cup', 'cups', 'tbsp', 'tsp', 'oz', 'lb', 'g', 'kg', 'ml', 'l', 'piece', 'pieces', 'clove', 'cloves'];

  return (
    <div className="form-group">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <label className="form-label" style={{ marginBottom: 0 }}>Ingredients</label>
        <button
          type="button"
          onClick={addIngredient}
          className="btn-outline"
          style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}
        >
          + Add Ingredient
        </button>
      </div>

      {localIngredients.length === 0 ? (
        <div style={{ 
          padding: '2rem', 
          textAlign: 'center', 
          background: '#f8f9fa', 
          borderRadius: '8px',
          color: '#666'
        }}>
          <p>No ingredients added yet.</p>
          <button
            type="button"
            onClick={addIngredient}
            className="btn-primary"
            style={{ marginTop: '1rem' }}
          >
            Add First Ingredient
          </button>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {localIngredients.map((ingredient, index) => (
            <div
              key={index}
              style={{
                padding: '1rem',
                border: '1px solid #e0e0e0',
                borderRadius: '8px',
                background: '#fff',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                <span style={{ fontWeight: '600', color: '#333' }}>Ingredient #{index + 1}</span>
                <button
                  type="button"
                  onClick={() => removeIngredient(index)}
                  style={{
                    background: 'none',
                    border: '1px solid #dc3545',
                    color: '#dc3545',
                    padding: '0.25rem 0.75rem',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: '0.85rem',
                  }}
                >
                  Remove
                </button>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr', gap: '0.75rem', marginBottom: '0.75rem' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '0.25rem', color: '#666' }}>
                    Ingredient Name *
                  </label>
                  <input
                    type="text"
                    value={ingredient.name}
                    onChange={(e) => updateIngredient(index, 'name', e.target.value)}
                    placeholder="e.g., Flour"
                    className="form-input"
                    required={localIngredients.length > 0}
                  />
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '0.25rem', color: '#666' }}>
                    Quantity *
                  </label>
                  <input
                    type="text"
                    value={ingredient.quantity}
                    onChange={(e) => updateIngredient(index, 'quantity', e.target.value)}
                    placeholder="e.g., 2"
                    className="form-input"
                    required={localIngredients.length > 0}
                  />
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '0.25rem', color: '#666' }}>
                    Unit
                  </label>
                  <input
                    type="text"
                    value={ingredient.unit}
                    onChange={(e) => updateIngredient(index, 'unit', e.target.value)}
                    placeholder="e.g., cups"
                    className="form-input"
                    list={`units-${index}`}
                  />
                  <datalist id={`units-${index}`}>
                    {commonUnits.map((unit) => (
                      <option key={unit} value={unit} />
                    ))}
                  </datalist>
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '0.25rem', color: '#666' }}>
                  Notes (optional)
                </label>
                <input
                  type="text"
                  value={ingredient.notes}
                  onChange={(e) => updateIngredient(index, 'notes', e.target.value)}
                  placeholder="e.g., chopped, diced, optional"
                  className="form-input"
                />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

