'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { api } from '@/lib/api';

export default function Navbar() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState<string | null>(null);

  useEffect(() => {
    // Check if user is authenticated by trying to access a protected endpoint
    checkAuth();
    
    // Listen for auth state changes (when user logs in/out)
    const handleAuthChange = () => {
      checkAuth();
    };
    
    window.addEventListener('authStateChanged', handleAuthChange);
    
    return () => {
      window.removeEventListener('authStateChanged', handleAuthChange);
    };
  }, []);

  const checkAuth = async () => {
    try {
      // Use /api/users/me/ to check auth and get user info
      const response = await api.get('/api/users/me/');
      if (response.data && response.data.username) {
        setIsAuthenticated(true);
        setUsername(response.data.username);
        console.log('Auth check successful:', response.data.username);
      } else {
        setIsAuthenticated(false);
        setUsername(null);
      }
    } catch (error: any) {
      setIsAuthenticated(false);
      setUsername(null);
      // Only log if it's not a 401 (unauthorized is expected when not logged in)
      if (error.response?.status !== 401) {
        console.error('Auth check error:', error);
      }
    }
  };

  const handleLogout = async () => {
    try {
      await api.post('/users/logout/');
      setIsAuthenticated(false);
      setUsername(null);
      // Notify other components
      window.dispatchEvent(new CustomEvent('authStateChanged'));
      window.location.href = '/';
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link href="/" className="navbar-brand">
          🍳 Recipe Sharing
        </Link>
        
        <div className="navbar-links">
          <Link href="/recipes">Recipes</Link>
          {isAuthenticated ? (
            <>
              <Link href="/recipes/create">Create Recipe</Link>
              <Link href="/favorites">My Favorites</Link>
              {username && (
                <Link href={`/users/profile/${username}`} className="navbar-username">
                  {username}
                </Link>
              )}
              <button onClick={handleLogout} className="btn-logout">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link href="/login">Login</Link>
              <Link href="/register" className="btn-primary">
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

