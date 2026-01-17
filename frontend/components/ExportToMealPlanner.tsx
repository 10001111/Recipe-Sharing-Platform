'use client';

import { useState } from 'react';

interface ExportToMealPlannerProps {
  recipeId: number;
  recipeTitle: string;
}

type ExportFormat = 'json' | 'recipeml' | 'csv';
type MealPlannerApp = 'generic' | 'paprika' | 'mealime' | 'anylist';

export default function ExportToMealPlanner({ recipeId, recipeTitle }: ExportToMealPlannerProps) {
  const [showDropdown, setShowDropdown] = useState(false);
  const [exporting, setExporting] = useState(false);

  const handleExport = async (format: ExportFormat, app: MealPlannerApp = 'generic') => {
    setExporting(true);
    setShowDropdown(false);

    try {
      let url = '';
      
      if (format === 'recipeml' || format === 'csv') {
        // Use export-meal-planner endpoint for single recipe
        url = `${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}/api/recipes/${recipeId}/export-meal-planner/?format=${format}`;
        if (app !== 'generic') {
          url += `&app=${app}`;
        }
      } else {
        // JSON format
        url = `${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}/api/recipes/${recipeId}/export-meal-planner/?format=json&app=${app}`;
      }

      const response = await fetch(url, {
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Export failed');
      }

      // Get content type and filename from response
      const contentType = response.headers.get('content-type') || '';
      const contentDisposition = response.headers.get('content-disposition') || '';
      
      let filename = `${recipeTitle.replace(/\s+/g, '_')}.${format}`;
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }

      // Get blob data
      const blob = await response.blob();
      
      // Create download link
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(downloadUrl);

      // Show success message
      alert(`Recipe exported successfully as ${filename}`);
    } catch (error) {
      console.error('Export error:', error);
      alert('Failed to export recipe. Please try again.');
    } finally {
      setExporting(false);
    }
  };

  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      <button
        onClick={() => setShowDropdown(!showDropdown)}
        disabled={exporting}
        className="btn-outline"
        style={{
          padding: '0.5rem 1rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          position: 'relative',
          cursor: exporting ? 'wait' : 'pointer',
        }}
      >
        {exporting ? '⏳ Exporting...' : '📤 Export to Meal Planner'}
        <span style={{ fontSize: '0.8rem' }}>▼</span>
      </button>

      {showDropdown && (
        <>
          {/* Overlay to close dropdown when clicking outside */}
          <div
            style={{
              position: 'fixed',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              zIndex: 998,
            }}
            onClick={() => setShowDropdown(false)}
          />

          {/* Dropdown Menu */}
          <div
            style={{
              position: 'absolute',
              top: '100%',
              right: 0,
              marginTop: '0.5rem',
              backgroundColor: 'white',
              border: '1px solid #ddd',
              borderRadius: '8px',
              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
              minWidth: '250px',
              zIndex: 999,
              overflow: 'hidden',
            }}
          >
            <div style={{ padding: '0.5rem', borderBottom: '1px solid #eee', backgroundColor: '#f8f9fa' }}>
              <strong style={{ fontSize: '0.9rem', color: '#333' }}>Export Format</strong>
            </div>

            {/* Format Options */}
            <div style={{ padding: '0.5rem 0' }}>
              <button
                onClick={() => handleExport('json', 'generic')}
                style={{
                  width: '100%',
                  padding: '0.75rem 1rem',
                  textAlign: 'left',
                  border: 'none',
                  background: 'transparent',
                  cursor: 'pointer',
                  fontSize: '0.9rem',
                  transition: 'background 0.2s',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.background = '#f0f7ff')}
                onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
              >
                📄 JSON (Generic)
              </button>

              <button
                onClick={() => handleExport('recipeml', 'generic')}
                style={{
                  width: '100%',
                  padding: '0.75rem 1rem',
                  textAlign: 'left',
                  border: 'none',
                  background: 'transparent',
                  cursor: 'pointer',
                  fontSize: '0.9rem',
                  transition: 'background 0.2s',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.background = '#f0f7ff')}
                onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
              >
                📋 RecipeML (Standard)
              </button>

              <button
                onClick={() => handleExport('csv', 'generic')}
                style={{
                  width: '100%',
                  padding: '0.75rem 1rem',
                  textAlign: 'left',
                  border: 'none',
                  background: 'transparent',
                  cursor: 'pointer',
                  fontSize: '0.9rem',
                  transition: 'background 0.2s',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.background = '#f0f7ff')}
                onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
              >
                📊 CSV (Spreadsheet)
              </button>
            </div>

            <div style={{ padding: '0.5rem', borderTop: '1px solid #eee', backgroundColor: '#f8f9fa' }}>
              <strong style={{ fontSize: '0.9rem', color: '#333' }}>Meal Planner Apps</strong>
            </div>

            {/* App-Specific Options */}
            <div style={{ padding: '0.5rem 0' }}>
              <button
                onClick={() => handleExport('json', 'paprika')}
                style={{
                  width: '100%',
                  padding: '0.75rem 1rem',
                  textAlign: 'left',
                  border: 'none',
                  background: 'transparent',
                  cursor: 'pointer',
                  fontSize: '0.9rem',
                  transition: 'background 0.2s',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.background = '#f0f7ff')}
                onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
              >
                🍎 Paprika Recipe Manager
              </button>

              <button
                onClick={() => handleExport('json', 'mealime')}
                style={{
                  width: '100%',
                  padding: '0.75rem 1rem',
                  textAlign: 'left',
                  border: 'none',
                  background: 'transparent',
                  cursor: 'pointer',
                  fontSize: '0.9rem',
                  transition: 'background 0.2s',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.background = '#f0f7ff')}
                onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
              >
                🥗 Mealime
              </button>

              <button
                onClick={() => handleExport('json', 'anylist')}
                style={{
                  width: '100%',
                  padding: '0.75rem 1rem',
                  textAlign: 'left',
                  border: 'none',
                  background: 'transparent',
                  cursor: 'pointer',
                  fontSize: '0.9rem',
                  transition: 'background 0.2s',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.background = '#f0f7ff')}
                onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
              >
                📝 AnyList
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

