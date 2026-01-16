'use client';

import { useState } from 'react';
import ImageUpload from './ImageUpload';

export interface InstructionStep {
  id: string;
  text: string;
  image?: File | null;
  imageUrl?: string | null; // For existing images
}

interface InstructionStepEditorProps {
  steps: InstructionStep[];
  onChange: (steps: InstructionStep[]) => void;
}

export default function InstructionStepEditor({ steps, onChange }: InstructionStepEditorProps) {
  const addStep = () => {
    const newStep: InstructionStep = {
      id: Date.now().toString(),
      text: '',
      image: null,
      imageUrl: null,
    };
    onChange([...steps, newStep]);
  };

  const removeStep = (id: string) => {
    onChange(steps.filter(step => step.id !== id));
  };

  const updateStep = (id: string, field: keyof InstructionStep, value: any) => {
    onChange(
      steps.map(step =>
        step.id === id ? { ...step, [field]: value } : step
      )
    );
  };

  const moveStep = (index: number, direction: 'up' | 'down') => {
    const newSteps = [...steps];
    const newIndex = direction === 'up' ? index - 1 : index + 1;
    
    if (newIndex < 0 || newIndex >= steps.length) return;
    
    [newSteps[index], newSteps[newIndex]] = [newSteps[newIndex], newSteps[index]];
    onChange(newSteps);
  };

  return (
    <div className="instruction-steps-editor">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <label className="form-label">Instructions (Step-by-Step)</label>
        <button
          type="button"
          onClick={addStep}
          className="btn-outline"
          style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}
        >
          + Add Step
        </button>
      </div>

      {steps.length === 0 && (
        <div style={{ 
          padding: '2rem', 
          textAlign: 'center', 
          background: '#f8f9fa', 
          borderRadius: '8px',
          color: '#666',
          marginBottom: '1rem'
        }}>
          No steps added yet. Click "Add Step" to get started.
        </div>
      )}

      {steps.map((step, index) => (
        <div
          key={step.id}
          style={{
            background: 'white',
            border: '1px solid #e0e0e0',
            borderRadius: '8px',
            padding: '1.5rem',
            marginBottom: '1rem',
            position: 'relative',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem' }}>
            {/* Step Number */}
            <div
              style={{
                background: '#0066cc',
                color: 'white',
                borderRadius: '50%',
                width: '32px',
                height: '32px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 'bold',
                flexShrink: 0,
                marginTop: '0.25rem',
              }}
            >
              {index + 1}
            </div>

            {/* Step Content */}
            <div style={{ flex: 1 }}>
              <textarea
                value={step.text}
                onChange={(e) => updateStep(step.id, 'text', e.target.value)}
                placeholder={`Step ${index + 1} instructions...`}
                className="form-textarea"
                rows={3}
                required
                style={{ marginBottom: '1rem' }}
              />

              {/* Image Upload for this step */}
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem', display: 'block' }}>
                  Step Image (Optional)
                </label>
                <ImageUpload
                  onImageChange={(file) => updateStep(step.id, 'image', file)}
                  currentImage={step.imageUrl || undefined}
                  label=""
                />
                <small style={{ color: '#666', display: 'block', marginTop: '0.5rem' }}>
                  Add an image to illustrate this step
                </small>
              </div>

              {/* Step Actions */}
              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                {index > 0 && (
                  <button
                    type="button"
                    onClick={() => moveStep(index, 'up')}
                    className="btn-outline"
                    style={{ fontSize: '0.85rem', padding: '0.25rem 0.75rem' }}
                  >
                    ↑ Move Up
                  </button>
                )}
                {index < steps.length - 1 && (
                  <button
                    type="button"
                    onClick={() => moveStep(index, 'down')}
                    className="btn-outline"
                    style={{ fontSize: '0.85rem', padding: '0.25rem 0.75rem' }}
                  >
                    ↓ Move Down
                  </button>
                )}
                <button
                  type="button"
                  onClick={() => removeStep(step.id)}
                  style={{
                    fontSize: '0.85rem',
                    padding: '0.25rem 0.75rem',
                    background: '#dc3545',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                  }}
                >
                  Remove Step
                </button>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

