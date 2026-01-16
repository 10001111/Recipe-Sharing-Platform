'use client';

import Link from 'next/link';
import { useState, useEffect, useRef } from 'react';
import { api } from '@/lib/api';
import { useRouter } from 'next/navigation';

export default function Navbar() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [showSearch, setShowSearch] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    checkAuth();
    
    const handleAuthChange = () => {
      checkAuth();
    };
    
    window.addEventListener('authStateChanged', handleAuthChange);
    
    return () => {
      window.removeEventListener('authStateChanged', handleAuthChange);
    };
  }, []);

  useEffect(() => {
    // Close dropdown when clicking outside
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setActiveDropdown(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const checkAuth = async () => {
    try {
      const response = await api.get('/api/users/me/');
      if (response.data && response.data.username) {
        setIsAuthenticated(true);
        setUsername(response.data.username);
      } else {
        setIsAuthenticated(false);
        setUsername(null);
      }
    } catch (error: any) {
      setIsAuthenticated(false);
      setUsername(null);
    }
  };

  const handleLogout = async () => {
    try {
      await api.post('/users/logout/');
      setIsAuthenticated(false);
      setUsername(null);
      window.dispatchEvent(new CustomEvent('authStateChanged'));
      window.location.href = '/';
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/recipes?search=${encodeURIComponent(searchQuery.trim())}`);
      setShowSearch(false);
      setSearchQuery('');
    }
  };

  const toggleDropdown = (menu: string) => {
    setActiveDropdown(activeDropdown === menu ? null : menu);
  };

  return (
    <nav className="navbar-delish">
      <div className="navbar-delish-container">
        {/* Logo */}
        <Link href="/" className="navbar-delish-logo">
          Recipe Sharing
        </Link>

        {/* Main Navigation */}
        <div className="navbar-delish-nav" ref={dropdownRef}>
          <div 
            className="navbar-delish-item"
            onMouseEnter={() => setActiveDropdown('recipes')}
            onMouseLeave={() => setActiveDropdown(null)}
          >
            <button className="navbar-delish-link">
              Recipes
              <span className="navbar-delish-arrow">▼</span>
            </button>
            {activeDropdown === 'recipes' && (
              <div className="navbar-delish-dropdown">
                <Link href="/recipes" onClick={() => setActiveDropdown(null)}>All Recipes</Link>
                <Link href="/recipes?category=breakfast" onClick={() => setActiveDropdown(null)}>Breakfast</Link>
                <Link href="/recipes?category=lunch" onClick={() => setActiveDropdown(null)}>Lunch</Link>
                <Link href="/recipes?category=dinner" onClick={() => setActiveDropdown(null)}>Dinner</Link>
                <Link href="/recipes?category=dessert" onClick={() => setActiveDropdown(null)}>Dessert</Link>
                <Link href="/recipes?category=snack" onClick={() => setActiveDropdown(null)}>Snacks</Link>
              </div>
            )}
          </div>

          <div 
            className="navbar-delish-item"
            onMouseEnter={() => setActiveDropdown('occasions')}
            onMouseLeave={() => setActiveDropdown(null)}
          >
            <button className="navbar-delish-link">
              Occasions
              <span className="navbar-delish-arrow">▼</span>
            </button>
            {activeDropdown === 'occasions' && (
              <div className="navbar-delish-dropdown">
                <Link href="/recipes?occasion=holiday" onClick={() => setActiveDropdown(null)}>Holidays</Link>
                <Link href="/recipes?occasion=party" onClick={() => setActiveDropdown(null)}>Party</Link>
                <Link href="/recipes?occasion=weekend" onClick={() => setActiveDropdown(null)}>Weekend</Link>
                <Link href="/recipes?occasion=quick" onClick={() => setActiveDropdown(null)}>Quick & Easy</Link>
              </div>
            )}
          </div>

          <Link href="/kitchen-tips" className="navbar-delish-link">
            Kitchen Tips
          </Link>

          {isAuthenticated && (
            <>
              <Link href="/recipes/create" className="navbar-delish-link">
                Create Recipe
              </Link>
              <Link href="/dashboard" className="navbar-delish-link">
                Dashboard
              </Link>
              <Link href="/favorites" className="navbar-delish-link">
                My Favorites
              </Link>
            </>
          )}
        </div>

        {/* Right Side: Search, Auth */}
        <div className="navbar-delish-right">
          {/* Search */}
          <div className="navbar-delish-search">
            {showSearch ? (
              <form onSubmit={handleSearch} className="navbar-delish-search-form">
                <input
                  type="text"
                  placeholder="Search recipes..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="navbar-delish-search-input"
                  autoFocus
                  onBlur={() => setTimeout(() => setShowSearch(false), 200)}
                />
                <button type="submit" className="navbar-delish-search-submit">Search</button>
                <button 
                  type="button" 
                  onClick={() => setShowSearch(false)}
                  className="navbar-delish-search-close"
                >
                  ✕
                </button>
              </form>
            ) : (
              <button 
                onClick={() => setShowSearch(true)}
                className="navbar-delish-search-toggle"
                aria-label="Search"
              >
                Search
              </button>
            )}
          </div>

          {/* Auth */}
          {isAuthenticated ? (
            <div className="navbar-delish-auth">
              {username && (
                <Link href={`/users/profile/${username}`} className="navbar-delish-link">
                  {username}
                </Link>
              )}
              <button onClick={handleLogout} className="navbar-delish-link navbar-delish-logout">
                Sign Out
              </button>
            </div>
          ) : (
            <div className="navbar-delish-auth">
              <Link href="/login" className="navbar-delish-link">
                Log In
              </Link>
              <Link href="/register" className="navbar-delish-btn-primary">
                Sign Up
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
