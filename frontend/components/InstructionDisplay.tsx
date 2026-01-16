'use client';

import Image from 'next/image';

export interface InstructionStepData {
  text: string;
  imageUrl?: string | null;
}

interface InstructionDisplayProps {
  instructions: string; // Can be plain text or JSON string
  stepImages?: { [stepIndex: number]: string }; // Optional step images
}

/**
 * Parse instructions and display them with images
 * Supports:
 * 1. Plain text (line-by-line)
 * 2. JSON format: [{"text": "...", "imageUrl": "..."}, ...]
 * 3. Markdown-style: ![alt](url) or [IMAGE:url]
 */
export default function InstructionDisplay({ instructions, stepImages }: InstructionDisplayProps) {
  // Try to parse as JSON first
  let steps: InstructionStepData[] = [];
  
  try {
    const parsed = JSON.parse(instructions);
    if (Array.isArray(parsed)) {
      steps = parsed;
    } else {
      throw new Error('Not an array');
    }
  } catch {
    // Not JSON, parse as plain text with markdown-style images
    const lines = instructions.split('\n').filter(line => line.trim().length > 0);
    
    steps = lines.map((line, index) => {
      // Check for markdown-style image: ![alt](url)
      const markdownImageMatch = line.match(/!\[([^\]]*)\]\(([^)]+)\)/);
      if (markdownImageMatch) {
        return {
          text: line.replace(/!\[([^\]]*)\]\(([^)]+)\)/, '').trim(),
          imageUrl: markdownImageMatch[2],
        };
      }
      
      // Check for [IMAGE:url] format
      const imageTagMatch = line.match(/\[IMAGE:([^\]]+)\]/);
      if (imageTagMatch) {
        return {
          text: line.replace(/\[IMAGE:[^\]]+\]/, '').trim(),
          imageUrl: imageTagMatch[1],
        };
      }
      
      // Check if stepImages has an image for this step
      const stepImageUrl = stepImages?.[index];
      
      return {
        text: line.replace(/^\d+\.\s*/, '').trim(), // Remove leading step numbers
        imageUrl: stepImageUrl || null,
      };
    });
  }

  if (steps.length === 0) {
    return (
      <div style={{ color: '#666', fontStyle: 'italic' }}>
        No instructions available.
      </div>
    );
  }

  return (
    <ol className="recipe-directions-list" style={{ paddingLeft: '1.5rem', margin: 0 }}>
      {steps.map((step, index) => (
        <li key={index} className="recipe-direction-step" style={{ marginBottom: '1.5rem' }}>
          <div style={{ fontSize: '1rem', lineHeight: '1.8', color: '#333', marginBottom: step.imageUrl ? '1rem' : 0 }}>
            {step.text || `Step ${index + 1}`}
          </div>
          
          {step.imageUrl && (
            <div style={{ 
              marginTop: '1rem',
              borderRadius: '8px',
              overflow: 'hidden',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              maxWidth: '100%'
            }}>
              <img
                src={step.imageUrl.startsWith('http') ? step.imageUrl : `http://127.0.0.1:8000${step.imageUrl}`}
                alt={`Step ${index + 1} illustration`}
                style={{
                  width: '100%',
                  maxHeight: '400px',
                  objectFit: 'cover',
                  display: 'block',
                }}
                loading="lazy"
              />
            </div>
          )}
        </li>
      ))}
    </ol>
  );
}

