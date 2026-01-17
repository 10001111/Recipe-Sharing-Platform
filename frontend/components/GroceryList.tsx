'use client';

import { useState, useEffect, useCallback } from 'react';
import { mealPlanApi } from '@/lib/api';

interface GroceryItem {
  name: string;
  total_quantity: number;
  unit: string;
  recipes: string[];
  notes: string[];
}

interface GroceryListData {
  ingredients_by_category: {
    [category: string]: GroceryItem[];
  };
  total_items: number;
  date_range: {
    start: string | null;
    end: string | null;
  };
  meal_plans_count: number;
}

interface GroceryListProps {
  startDate?: string;
  endDate?: string;
  onClose?: () => void;
}

export default function GroceryList({ startDate, endDate, onClose }: GroceryListProps) {
  const [groceryData, setGroceryData] = useState<GroceryListData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadGroceryList = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await mealPlanApi.getGroceryList({
        start_date: startDate,
        end_date: endDate,
        format: 'json',
      });
      setGroceryData(data);
    } catch (err: any) {
      console.error('Error loading grocery list:', err);
      setError(err.response?.data?.error || 'Failed to load grocery list');
    } finally {
      setLoading(false);
    }
  }, [startDate, endDate]);

  useEffect(() => {
    loadGroceryList();
  }, [loadGroceryList]);

  const handleExport = async (format: 'pdf' | 'text' | 'json') => {
    try {
      const blob = await mealPlanApi.getGroceryList({
        start_date: startDate,
        end_date: endDate,
        format,
      });

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      
      const extension = format === 'pdf' ? 'pdf' : format === 'text' ? 'txt' : 'json';
      link.download = `grocery-list.${extension}`;
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      console.error(`Error exporting ${format}:`, err);
      alert(`Failed to export grocery list as ${format.toUpperCase()}`);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '3rem' }}>
        <p>Loading grocery list...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ 
        background: '#fee', 
        color: '#c33', 
        padding: '1rem', 
        borderRadius: '4px',
        marginBottom: '1rem'
      }}>
        {error}
      </div>
    );
  }

  if (!groceryData || groceryData.total_items === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '3rem' }}>
        <p style={{ fontSize: '1.2rem', color: '#666', marginBottom: '1rem' }}>
          No ingredients found for the selected date range.
        </p>
        <p style={{ color: '#999' }}>
          Add some meals to your meal plan to generate a grocery list.
        </p>
      </div>
    );
  }

  return (
    <div className="grocery-list-container" style={{ padding: '2rem' }}>
      {/* Header */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '2rem',
        flexWrap: 'wrap',
        gap: '1rem'
      }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 'bold', margin: 0, marginBottom: '0.5rem' }}>
            Grocery List
          </h1>
          {groceryData.date_range.start && (
            <p style={{ color: '#666', margin: 0 }}>
              {new Date(groceryData.date_range.start).toLocaleDateString()} - {new Date(groceryData.date_range.end || '').toLocaleDateString()}
            </p>
          )}
          <p style={{ color: '#999', fontSize: '0.9rem', margin: '0.5rem 0 0 0' }}>
            {groceryData.total_items} items from {groceryData.meal_plans_count} meal plan{groceryData.meal_plans_count !== 1 ? 's' : ''}
          </p>
        </div>
        
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          <button onClick={() => handleExport('pdf')} className="btn-primary">
            📄 Export PDF
          </button>
          <button onClick={() => handleExport('text')} className="btn-outline">
            📝 Export Text
          </button>
          <button onClick={() => handleExport('json')} className="btn-outline">
            💾 Export JSON
          </button>
          <button onClick={handlePrint} className="btn-outline">
            🖨️ Print
          </button>
          {onClose && (
            <button onClick={onClose} className="btn-outline">
              ✕ Close
            </button>
          )}
        </div>
      </div>

      {/* Grocery List by Category */}
      <div className="grocery-list-content">
        {Object.entries(groceryData.ingredients_by_category).map(([category, items]) => {
          if (!items || items.length === 0) return null;
          
          return (
            <div key={category} style={{ marginBottom: '2rem' }}>
              <h2 style={{ 
                fontSize: '1.5rem', 
                fontWeight: 'bold', 
                color: '#333',
                marginBottom: '1rem',
                paddingBottom: '0.5rem',
                borderBottom: '2px solid #e0e0e0'
              }}>
                {category}
              </h2>
              
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
                gap: '1rem',
              }}>
                {items.map((item, index) => (
                  <div
                    key={`${item.name}-${index}`}
                    style={{
                      padding: '1rem',
                      background: '#f8f9fa',
                      borderRadius: '8px',
                      border: '1px solid #e0e0e0',
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.5rem' }}>
                      <div style={{ flex: 1 }}>
                        <div style={{ 
                          fontSize: '1.1rem', 
                          fontWeight: '600', 
                          color: '#333',
                          marginBottom: '0.25rem'
                        }}>
                          {item.name}
                        </div>
                        <div style={{ fontSize: '0.9rem', color: '#666' }}>
                          {item.total_quantity > 0 
                            ? `${item.total_quantity.toString().replace(/\.?0+$/, '')} ${item.unit || ''}`.trim()
                            : item.unit || 'As needed'}
                        </div>
                      </div>
                    </div>
                    
                    {item.notes && item.notes.length > 0 && (
                      <div style={{ 
                        fontSize: '0.85rem', 
                        color: '#999', 
                        fontStyle: 'italic',
                        marginTop: '0.5rem'
                      }}>
                        {item.notes.join(', ')}
                      </div>
                    )}
                    
                    {item.recipes && item.recipes.length > 0 && (
                      <div style={{ 
                        fontSize: '0.8rem', 
                        color: '#999', 
                        marginTop: '0.5rem',
                        paddingTop: '0.5rem',
                        borderTop: '1px solid #e0e0e0'
                      }}>
                        <strong>Used in:</strong> {item.recipes.join(', ')}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      {/* Print Styles */}
      <style jsx>{`
        @media print {
          .grocery-list-container {
            padding: 0;
          }
          
          .grocery-list-container button {
            display: none;
          }
          
          .grocery-list-content {
            page-break-inside: avoid;
          }
          
          .grocery-list-content > div {
            page-break-inside: avoid;
            margin-bottom: 1rem;
          }
        }
      `}</style>
    </div>
  );
}

