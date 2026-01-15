'use client';

import { useState, useEffect, useRef } from 'react';
import { recipeApi, RecipeList } from '@/lib/api';

interface SearchAutocompleteProps {
  onSelect: (recipe: RecipeList) => void;
  placeholder?: string;
  className?: string;
}

export default function SearchAutocomplete({ onSelect, placeholder = 'Search recipes...', className = '' }: SearchAutocompleteProps) {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<RecipeList[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [loading, setLoading] = useState(false);
  const searchRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    const searchRecipes = async () => {
      if (query.length < 2) {
        setSuggestions([]);
        setShowSuggestions(false);
        return;
      }

      setLoading(true);
      try {
        const response = await recipeApi.getAll({ search: query });
        const recipesData = response.results || response;
        const limitedSuggestions = Array.isArray(recipesData) ? recipesData.slice(0, 5) : [];
        setSuggestions(limitedSuggestions);
        setShowSuggestions(limitedSuggestions.length > 0);
      } catch (error) {
        console.error('Error fetching suggestions:', error);
        setSuggestions([]);
      } finally {
        setLoading(false);
      }
    };

    const debounceTimer = setTimeout(searchRecipes, 300);
    return () => clearTimeout(debounceTimer);
  }, [query]);

  const handleSelect = (recipe: RecipeList) => {
    setQuery(recipe.title);
    setShowSuggestions(false);
    onSelect(recipe);
  };

  return (
    <div ref={searchRef} style={{ position: 'relative', width: '100%' }}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onFocus={() => {
          if (suggestions.length > 0) {
            setShowSuggestions(true);
          }
        }}
        placeholder={placeholder}
        className={`form-input ${className}`}
        style={{ width: '100%' }}
      />
      
      {loading && (
        <div style={{ 
          position: 'absolute', 
          right: '10px', 
          top: '50%', 
          transform: 'translateY(-50%)',
          color: '#666'
        }}>
          <span style={{ fontSize: '0.85rem' }}>Searching...</span>
        </div>
      )}

      {showSuggestions && suggestions.length > 0 && (
        <div style={{
          position: 'absolute',
          top: '100%',
          left: 0,
          right: 0,
          background: 'white',
          border: '1px solid #e0e0e0',
          borderRadius: '8px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          zIndex: 1000,
          maxHeight: '300px',
          overflowY: 'auto',
          marginTop: '4px',
        }}>
          {suggestions.map((recipe) => (
            <div
              key={recipe.id}
              onClick={() => handleSelect(recipe)}
              style={{
                padding: '0.75rem 1rem',
                cursor: 'pointer',
                borderBottom: '1px solid #f0f0f0',
                transition: 'background-color 0.2s',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = '#f8f9fa';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'white';
              }}
            >
              <div style={{ fontWeight: '600', color: '#333', marginBottom: '0.25rem' }}>
                {recipe.title}
              </div>
              <div style={{ fontSize: '0.85rem', color: '#666' }}>
                {recipe.description.substring(0, 60)}...
              </div>
              <div style={{ fontSize: '0.75rem', color: '#999', marginTop: '0.25rem' }}>
                👤 {recipe.author.username} • ⭐ {recipe.average_rating.toFixed(1)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

