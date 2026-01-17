'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { mealPlanApi, recipeApi, RecipeList } from '@/lib/api';
import MealPlanCalendar from '@/components/MealPlanCalendar';
import RecipeCard from '@/components/RecipeCard';

export default function MealPlanPage() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [recipes, setRecipes] = useState<RecipeList[]>([]);
  const [loading, setLoading] = useState(true);
  const [showRecipeList, setShowRecipeList] = useState(true);

  useEffect(() => {
    checkAuth();
    loadRecipes();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/users/me/', {
        credentials: 'include',
      });
      if (response.ok) {
        setIsAuthenticated(true);
      } else {
        setIsAuthenticated(false);
        // Redirect to login with return URL
        const returnUrl = encodeURIComponent(window.location.pathname);
        router.push(`/login?next=${returnUrl}`);
      }
    } catch (error) {
      setIsAuthenticated(false);
      const returnUrl = encodeURIComponent(window.location.pathname);
      router.push(`/login?next=${returnUrl}`);
    }
  };

  const loadRecipes = async () => {
    try {
      setLoading(true);
      const data = await recipeApi.getAll({ page: 1 });
      setRecipes(data.results || data);
    } catch (error: any) {
      console.error('Error loading recipes:', error);
      if (error.response?.status === 401) {
        // This shouldn't happen for public recipe list, but handle it anyway
        console.warn('Authentication error loading recipes');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleExportICal = async () => {
    try {
      const today = new Date();
      const nextMonth = new Date(today);
      nextMonth.setMonth(nextMonth.getMonth() + 1);
      
      const startDate = today.toISOString().split('T')[0];
      const endDate = nextMonth.toISOString().split('T')[0];
      
      const blob = await mealPlanApi.exportICal(startDate, endDate);
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'meal-plans.ics';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (error: any) {
      console.error('Error exporting iCal:', error);
      if (error.response?.status === 401) {
        alert('Please log in to export your meal plan calendar.');
        router.push('/login');
      } else {
        alert(error.response?.data?.error || error.response?.data?.detail || 'Failed to export calendar. Please try again.');
      }
    }
  };

  if (!isAuthenticated) {
    return (
      <main className="container">
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <p>Please log in to access meal planning.</p>
        </div>
      </main>
    );
  }

  return (
    <main className="container" style={{ padding: '2rem 1rem' }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '2rem',
        flexWrap: 'wrap',
        gap: '1rem'
      }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 'bold', margin: 0 }}>
          Meal Planning Calendar
        </h1>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button
            onClick={() => setShowRecipeList(!showRecipeList)}
            className="btn-outline"
          >
            {showRecipeList ? 'Hide' : 'Show'} Recipe List
          </button>
          <button
            onClick={handleExportICal}
            className="btn-primary"
          >
            📅 Export iCal
          </button>
        </div>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: showRecipeList ? '300px 1fr' : '1fr',
        gap: '2rem',
        alignItems: 'start'
      }}>
        {/* Recipe List Sidebar */}
        {showRecipeList && (
          <div style={{
            position: 'sticky',
            top: '2rem',
            maxHeight: 'calc(100vh - 4rem)',
            overflowY: 'auto',
          }}>
            <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>
              Drag Recipes Here
            </h2>
            <div style={{
              padding: '1rem',
              background: '#f8f9fa',
              borderRadius: '8px',
              marginBottom: '1rem',
              fontSize: '0.9rem',
              color: '#666',
            }}>
              💡 Drag recipes from the list below and drop them on calendar cells to plan meals.
            </div>
            
            {loading ? (
              <div style={{ textAlign: 'center', padding: '2rem' }}>
                <p>Loading recipes...</p>
              </div>
            ) : (
              <div style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '1rem',
              }}>
                {recipes.map(recipe => (
                  <div
                    key={recipe.id}
                    draggable
                    onDragStart={() => {
                      // Store recipe data for drag
                      const event = new CustomEvent('recipeDragStart', { detail: recipe });
                      window.dispatchEvent(event);
                    }}
                    style={{
                      cursor: 'grab',
                      border: '1px solid #e0e0e0',
                      borderRadius: '8px',
                      padding: '0.5rem',
                      background: 'white',
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
                    <RecipeCard recipe={recipe} />
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Calendar */}
        <div>
          <MealPlanCalendar onMealPlanChange={loadRecipes} />
        </div>
      </div>
    </main>
  );
}

