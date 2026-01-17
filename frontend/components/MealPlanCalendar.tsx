'use client';

import { useState, useEffect, useCallback } from 'react';
import { mealPlanApi, MealPlan, recipeApi, RecipeList } from '@/lib/api';
import RecipeCard from './RecipeCard';
import RecipeImage from './RecipeImage';

type ViewMode = 'week' | 'month';
type MealType = 'breakfast' | 'lunch' | 'dinner' | 'snack' | 'dessert';

interface MealPlanCalendarProps {
  onMealPlanChange?: () => void;
}

export default function MealPlanCalendar({ onMealPlanChange }: MealPlanCalendarProps) {
  const [viewMode, setViewMode] = useState<ViewMode>('week');
  const [currentDate, setCurrentDate] = useState(new Date());
  const [mealPlans, setMealPlans] = useState<MealPlan[]>([]);
  const [loading, setLoading] = useState(true);
  const [draggedRecipe, setDraggedRecipe] = useState<RecipeList | null>(null);
  const [showRecipeSelector, setShowRecipeSelector] = useState(false);
  const [recipes, setRecipes] = useState<RecipeList[]>([]);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [selectedMealType, setSelectedMealType] = useState<MealType | null>(null);

  // Get start and end dates for current view
  const getDateRange = useCallback(() => {
    const start = new Date(currentDate);
    const end = new Date(currentDate);

    if (viewMode === 'week') {
      // Start of week (Sunday)
      start.setDate(start.getDate() - start.getDay());
      // End of week (Saturday)
      end.setDate(end.getDate() + (6 - end.getDay()));
    } else {
      // Start of month
      start.setDate(1);
      // End of month
      end.setMonth(end.getMonth() + 1);
      end.setDate(0);
    }

    return {
      start: start.toISOString().split('T')[0],
      end: end.toISOString().split('T')[0],
    };
  }, [currentDate, viewMode]);

  // Load meal plans
  const loadMealPlans = useCallback(async () => {
    try {
      setLoading(true);
      const { start, end } = getDateRange();
      const data = await mealPlanApi.getAll({ start_date: start, end_date: end });
      setMealPlans(data.results || data);
    } catch (error: any) {
      console.error('Error loading meal plans:', error);
      if (error.response?.status === 401) {
        // User not authenticated - clear meal plans and show message
        setMealPlans([]);
        console.warn('User not authenticated. Please log in to view meal plans.');
      }
    } finally {
      setLoading(false);
    }
  }, [getDateRange]);

  useEffect(() => {
    // Only load meal plans if component is mounted
    loadMealPlans();
    
    // Listen for recipe drag events from parent
    const handleRecipeDragStart = (event: CustomEvent) => {
      setDraggedRecipe(event.detail);
    };
    
    window.addEventListener('recipeDragStart', handleRecipeDragStart as EventListener);
    
    return () => {
      window.removeEventListener('recipeDragStart', handleRecipeDragStart as EventListener);
    };
  }, [loadMealPlans]);

  // Load recipes for selector
  const loadRecipes = async () => {
    try {
      const data = await recipeApi.getAll({ page: 1 });
      setRecipes(data.results || data);
    } catch (error) {
      console.error('Error loading recipes:', error);
    }
  };

  // Get meal plan for specific date and meal type
  const getMealPlan = (date: string, mealType: MealType): MealPlan | undefined => {
    return mealPlans.find(
      mp => mp.date === date && mp.meal_type === mealType
    );
  };

  // Handle drag start
  const handleDragStart = (recipe: RecipeList) => {
    setDraggedRecipe(recipe);
  };

  // Handle drop
  const handleDrop = async (date: string, mealType: MealType) => {
    if (!draggedRecipe) return;

    try {
      const existingPlan = getMealPlan(date, mealType);
      
      if (existingPlan) {
        // Update existing meal plan
        await mealPlanApi.update(existingPlan.id, {
          recipe_id: draggedRecipe.id,
        });
      } else {
        // Create new meal plan
        await mealPlanApi.create({
          recipe_id: draggedRecipe.id,
          date,
          meal_type: mealType,
        });
      }

      await loadMealPlans();
      if (onMealPlanChange) {
        onMealPlanChange();
      }
    } catch (error: any) {
      console.error('Error saving meal plan:', error);
      if (error.response?.status === 401) {
        alert('Please log in to save meal plans.');
        window.location.href = '/login';
      } else {
        alert(error.response?.data?.error || error.response?.data?.detail || 'Failed to save meal plan');
      }
    } finally {
      setDraggedRecipe(null);
    }
  };

  // Handle delete
  const handleDelete = async (mealPlanId: number) => {
    if (!confirm('Are you sure you want to remove this meal plan?')) return;

    try {
      await mealPlanApi.delete(mealPlanId);
      await loadMealPlans();
      if (onMealPlanChange) {
        onMealPlanChange();
      }
    } catch (error: any) {
      console.error('Error deleting meal plan:', error);
      if (error.response?.status === 401) {
        alert('Please log in to delete meal plans.');
        window.location.href = '/login';
      } else {
        alert(error.response?.data?.error || error.response?.data?.detail || 'Failed to delete meal plan');
      }
    }
  };

  // Handle edit
  const handleEdit = (date: string, mealType: MealType) => {
    setSelectedDate(date);
    setSelectedMealType(mealType);
    setShowRecipeSelector(true);
    loadRecipes();
  };

  // Handle recipe select from selector
  const handleRecipeSelect = async (recipe: RecipeList) => {
    if (!selectedDate || !selectedMealType) return;

    try {
      const existingPlan = getMealPlan(selectedDate, selectedMealType);
      
      if (existingPlan) {
        await mealPlanApi.update(existingPlan.id, {
          recipe_id: recipe.id,
        });
      } else {
        await mealPlanApi.create({
          recipe_id: recipe.id,
          date: selectedDate,
          meal_type: selectedMealType,
        });
      }

      await loadMealPlans();
      setShowRecipeSelector(false);
      setSelectedDate(null);
      setSelectedMealType(null);
      if (onMealPlanChange) {
        onMealPlanChange();
      }
    } catch (error: any) {
      console.error('Error saving meal plan:', error);
      if (error.response?.status === 401) {
        alert('Please log in to save meal plans.');
        window.location.href = '/login';
      } else {
        alert(error.response?.data?.error || error.response?.data?.detail || 'Failed to save meal plan');
      }
    }
  };

  // Navigate dates
  const navigateDate = (direction: 'prev' | 'next') => {
    const newDate = new Date(currentDate);
    if (viewMode === 'week') {
      newDate.setDate(newDate.getDate() + (direction === 'next' ? 7 : -7));
    } else {
      newDate.setMonth(newDate.getMonth() + (direction === 'next' ? 1 : -1));
    }
    setCurrentDate(newDate);
  };

  // Get dates for current view
  const getDates = (): Date[] => {
    const dates: Date[] = [];
    const { start, end } = getDateRange();
    const startDate = new Date(start);
    const endDate = new Date(end);

    for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
      dates.push(new Date(d));
    }

    return dates;
  };

  const mealTypes: MealType[] = ['breakfast', 'lunch', 'dinner', 'snack', 'dessert'];
  const mealTypeLabels: Record<MealType, string> = {
    breakfast: 'Breakfast',
    lunch: 'Lunch',
    dinner: 'Dinner',
    snack: 'Snack',
    dessert: 'Dessert',
  };

  const dates = getDates();

  return (
    <div style={{ padding: '2rem' }}>
      {/* Header Controls */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '2rem',
        flexWrap: 'wrap',
        gap: '1rem'
      }}>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button
            onClick={() => navigateDate('prev')}
            className="btn-outline"
          >
            ← Prev
          </button>
          <h2 style={{ margin: 0, minWidth: '200px', textAlign: 'center' }}>
            {viewMode === 'week' 
              ? `Week of ${currentDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`
              : currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
            }
          </h2>
          <button
            onClick={() => navigateDate('next')}
            className="btn-outline"
          >
            Next →
          </button>
          <button
            onClick={() => setCurrentDate(new Date())}
            className="btn-outline"
          >
            Today
          </button>
        </div>

        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button
            onClick={() => setViewMode('week')}
            className={viewMode === 'week' ? 'btn-primary' : 'btn-outline'}
          >
            Week
          </button>
          <button
            onClick={() => setViewMode('month')}
            className={viewMode === 'month' ? 'btn-primary' : 'btn-outline'}
          >
            Month
          </button>
        </div>
      </div>

      {/* Calendar Grid */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <p>Loading calendar...</p>
        </div>
      ) : (
        <div style={{
          overflowX: 'auto',
          border: '1px solid #e0e0e0',
          borderRadius: '8px',
        }}>
          <table style={{
            width: '100%',
            borderCollapse: 'collapse',
            minWidth: '800px',
          }}>
            <thead>
              <tr>
                <th style={{
                  padding: '1rem',
                  background: '#f8f9fa',
                  borderBottom: '2px solid #e0e0e0',
                  textAlign: 'left',
                  position: 'sticky',
                  left: 0,
                  background: '#f8f9fa',
                  zIndex: 2,
                }}>
                  Date / Meal
                </th>
                {mealTypes.map(mealType => (
                  <th
                    key={mealType}
                    style={{
                      padding: '1rem',
                      background: '#f8f9fa',
                      borderBottom: '2px solid #e0e0e0',
                      textAlign: 'center',
                      minWidth: '150px',
                    }}
                  >
                    {mealTypeLabels[mealType]}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {dates.map((date, dateIndex) => {
                const dateStr = date.toISOString().split('T')[0];
                const isToday = dateStr === new Date().toISOString().split('T')[0];
                
                return (
                  <tr key={dateStr}>
                    <td style={{
                      padding: '1rem',
                      borderBottom: '1px solid #e0e0e0',
                      background: isToday ? '#fff5e6' : 'white',
                      position: 'sticky',
                      left: 0,
                      zIndex: 1,
                      fontWeight: isToday ? 'bold' : 'normal',
                    }}>
                      <div style={{ fontSize: '0.9rem' }}>
                        {date.toLocaleDateString('en-US', { weekday: 'short' })}
                      </div>
                      <div style={{ fontSize: '1.1rem', fontWeight: 'bold' }}>
                        {date.getDate()}
                      </div>
                      <div style={{ fontSize: '0.8rem', color: '#666' }}>
                        {date.toLocaleDateString('en-US', { month: 'short' })}
                      </div>
                    </td>
                    {mealTypes.map(mealType => {
                      const mealPlan = getMealPlan(dateStr, mealType);
                      
                      return (
                        <td
                          key={`${dateStr}-${mealType}`}
                          onDragOver={(e) => {
                            e.preventDefault();
                            e.currentTarget.style.background = '#f0f9ff';
                          }}
                          onDragLeave={(e) => {
                            e.currentTarget.style.background = 'white';
                          }}
                          onDrop={(e) => {
                            e.preventDefault();
                            e.currentTarget.style.background = 'white';
                            handleDrop(dateStr, mealType);
                          }}
                          style={{
                            padding: '0.5rem',
                            borderBottom: '1px solid #e0e0e0',
                            background: 'white',
                            minHeight: '120px',
                            verticalAlign: 'top',
                            cursor: 'pointer',
                          }}
                          onClick={() => handleEdit(dateStr, mealType)}
                        >
                          {mealPlan ? (
                            <div style={{
                              padding: '0.5rem',
                              background: '#f8f9fa',
                              borderRadius: '4px',
                              border: '1px solid #e0e0e0',
                              position: 'relative',
                            }}>
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleDelete(mealPlan.id);
                                }}
                                style={{
                                  position: 'absolute',
                                  top: '4px',
                                  right: '4px',
                                  background: 'rgba(220, 53, 69, 0.9)',
                                  color: 'white',
                                  border: 'none',
                                  borderRadius: '50%',
                                  width: '20px',
                                  height: '20px',
                                  cursor: 'pointer',
                                  fontSize: '12px',
                                  display: 'flex',
                                  alignItems: 'center',
                                  justifyContent: 'center',
                                }}
                                title="Remove"
                              >
                                ×
                              </button>
                              <div style={{ fontSize: '0.85rem', fontWeight: 'bold', marginBottom: '0.25rem' }}>
                                {mealPlan.recipe_title}
                              </div>
                              <div style={{ fontSize: '0.75rem', color: '#666' }}>
                                {mealTypeLabels[mealType]}
                              </div>
                            </div>
                          ) : (
                            <div style={{
                              padding: '0.5rem',
                              color: '#999',
                              fontSize: '0.85rem',
                              textAlign: 'center',
                              border: '2px dashed #e0e0e0',
                              borderRadius: '4px',
                              minHeight: '80px',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                            }}>
                              Click to add
                            </div>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Recipe Selector Modal */}
      {showRecipeSelector && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
        }}
        onClick={() => {
          setShowRecipeSelector(false);
          setSelectedDate(null);
          setSelectedMealType(null);
        }}
        >
          <div
            style={{
              background: 'white',
              borderRadius: '8px',
              padding: '2rem',
              maxWidth: '800px',
              maxHeight: '80vh',
              overflow: 'auto',
              width: '90%',
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <h3 style={{ marginTop: 0 }}>
              Select Recipe for {selectedDate && new Date(selectedDate).toLocaleDateString()} - {selectedMealType && mealTypeLabels[selectedMealType]}
            </h3>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
              gap: '1rem',
              marginTop: '1rem',
            }}>
              {recipes.map(recipe => (
                <div
                  key={recipe.id}
                  onClick={() => handleRecipeSelect(recipe)}
                  style={{
                    border: '1px solid #e0e0e0',
                    borderRadius: '8px',
                    padding: '1rem',
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = 'var(--primary-color)';
                    e.currentTarget.style.transform = 'scale(1.02)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = '#e0e0e0';
                    e.currentTarget.style.transform = 'scale(1)';
                  }}
                >
                  <RecipeImage
                    src={recipe.image || (recipe as any).images?.[0]?.image_url}
                    alt={recipe.title}
                    placeholderType="recipe"
                    style={{ width: '100%', height: '120px', marginBottom: '0.5rem' }}
                  />
                  <div style={{ fontSize: '0.9rem', fontWeight: 'bold' }}>
                    {recipe.title}
                  </div>
                </div>
              ))}
            </div>
            <button
              onClick={() => {
                setShowRecipeSelector(false);
                setSelectedDate(null);
                setSelectedMealType(null);
              }}
              className="btn-outline"
              style={{ marginTop: '1rem' }}
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Drag Instructions */}
      <div style={{
        marginTop: '2rem',
        padding: '1rem',
        background: '#f8f9fa',
        borderRadius: '8px',
        fontSize: '0.9rem',
        color: '#666',
      }}>
        <strong>💡 Tip:</strong> Drag recipes from the recipe list and drop them on calendar cells to plan meals. 
        Click on any cell to edit or add a meal plan.
      </div>
    </div>
  );
}

