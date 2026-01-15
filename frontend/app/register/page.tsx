'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import Script from 'next/script';

export default function RegisterPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password1: '',
    password2: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);
  const [supabaseClient, setSupabaseClient] = useState<any>(null);
  const [supabaseConfig, setSupabaseConfig] = useState<{url: string; key: string} | null>(null);
  const [configLoading, setConfigLoading] = useState(true);

  useEffect(() => {
    // Fetch Supabase config from backend
    const fetchSupabaseConfig = async () => {
      setConfigLoading(true);
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
        const url = `${apiUrl}/api/config/supabase/`;
        console.log('Fetching Supabase config from:', url);
        
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
          },
        });
        
        console.log('Response status:', response.status, response.statusText);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const config = await response.json();
        console.log('Supabase config received:', { 
          enabled: config.enabled, 
          has_url: !!config.supabase_url, 
          has_key: !!config.supabase_anon_key 
        });
        
        if (config.enabled && config.supabase_url && config.supabase_anon_key) {
          setSupabaseConfig({
            url: config.supabase_url,
            key: config.supabase_anon_key
          });
          console.log('Supabase config set successfully');
        } else {
          console.warn('Supabase config incomplete:', config);
        }
      } catch (err) {
        console.error('Error fetching Supabase config:', err);
        // Don't set error here - just log it, let the UI show the default message
      } finally {
        setConfigLoading(false);
      }
    };

    fetchSupabaseConfig();
  }, []);

  useEffect(() => {
    // Initialize Supabase client when config is available and SDK is loaded
    if (supabaseConfig && typeof window !== 'undefined' && (window as any).supabase) {
      const supabase = (window as any).supabase.createClient(supabaseConfig.url, supabaseConfig.key);
      setSupabaseClient(supabase);
      
      // Only check for OAuth callback if we're coming back from OAuth redirect
      // Check URL for OAuth callback parameters
      const urlParams = new URLSearchParams(window.location.search);
      const hasOAuthParams = urlParams.has('code') || urlParams.has('access_token');
      
      if (hasOAuthParams) {
        checkOAuthCallback(supabase);
      }
      
      // Listen for auth state changes (only when user explicitly signs in)
      supabase.auth.onAuthStateChange(async (event: string, session: any) => {
        // Only auto-sync if it's a new sign-in event (not on page load)
        if (event === 'SIGNED_IN' && session && hasOAuthParams) {
          await syncWithBackend(session.access_token);
        }
      });
    }
  }, [supabaseConfig]);

  const checkOAuthCallback = async (supabase: any) => {
    try {
      const { data: { session }, error } = await supabase.auth.getSession();
      if (session && session.access_token) {
        await syncWithBackend(session.access_token);
      }
    } catch (err) {
      console.error('Error checking session:', err);
    }
  };

  const syncWithBackend = async (accessToken: string) => {
    try {
      setGoogleLoading(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}/users/supabase-auth/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          access_token: accessToken
        }),
        credentials: 'include',
      });

      const result = await response.json();

      if (result.success) {
        // Small delay to ensure session cookie is set
        await new Promise(resolve => setTimeout(resolve, 100));
        // Notify navbar to refresh auth state
        window.dispatchEvent(new CustomEvent('authStateChanged'));
        const redirectUrl = result.redirect_url || '/';
        // Force a full page reload to ensure session is picked up
        setTimeout(() => {
          window.location.href = redirectUrl;
        }, 200);
      } else {
        setErrors({ general: result.error || 'Authentication failed' });
        setGoogleLoading(false);
      }
    } catch (err: any) {
      console.error('Error syncing with backend:', err);
      setErrors({ general: 'Error connecting to server. Please try again.' });
      setGoogleLoading(false);
    }
  };

  const handleGoogleSignup = async () => {
    if (!supabaseClient) {
      setErrors({ general: 'Google authentication not available. Please configure Supabase credentials.' });
      return;
    }

    try {
      setGoogleLoading(true);
      setErrors({});

      const { data, error } = await supabaseClient.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${window.location.origin}/register`
        }
      });

      if (error) {
        setErrors({ general: 'Error: ' + error.message });
        setGoogleLoading(false);
      }
      // If successful, user will be redirected to Google, then back to this page
    } catch (err: any) {
      setErrors({ general: 'Error connecting to Google. Please try again.' });
      console.error('Google OAuth error:', err);
      setGoogleLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    // Validation
    if (formData.password1 !== formData.password2) {
      setErrors({ password2: 'Passwords do not match' });
      return;
    }

    if (formData.password1.length < 8) {
      setErrors({ password1: 'Password must be at least 8 characters' });
      return;
    }

    setLoading(true);

    try {
      // Django registration expects form data
      const formDataToSend = new URLSearchParams();
      formDataToSend.append('username', formData.username);
      formDataToSend.append('email', formData.email);
      formDataToSend.append('password1', formData.password1);
      formDataToSend.append('password2', formData.password2);

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}/users/register/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formDataToSend.toString(),
        credentials: 'include',
      });

      if (response.ok) {
        // Small delay to ensure session cookie is set
        await new Promise(resolve => setTimeout(resolve, 100));
        // Notify navbar to refresh auth state
        window.dispatchEvent(new CustomEvent('authStateChanged'));
        // Force a full page reload to ensure session is picked up
        setTimeout(() => {
          window.location.href = '/';
        }, 200);
      } else {
        const data = await response.json().catch(() => ({}));
        if (data) {
          setErrors(data);
        } else {
          setErrors({ general: 'Registration failed. Please try again.' });
        }
      }
    } catch (err: any) {
      setErrors({ general: 'Registration failed. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <div className="form-container">
        <h1 style={{ marginBottom: '1rem', textAlign: 'center' }}>Create Account</h1>
        
        {errors.general && (
          <div style={{ 
            background: '#fee', 
            color: '#c33', 
            padding: '1rem', 
            borderRadius: '4px',
            marginBottom: '1rem'
          }}>
            {errors.general}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Username</label>
            <input
              type="text"
              className="form-input"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              required
            />
            {errors.username && <div className="form-error">{errors.username}</div>}
          </div>

          <div className="form-group">
            <label className="form-label">Email</label>
            <input
              type="email"
              className="form-input"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
            />
            {errors.email && <div className="form-error">{errors.email}</div>}
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-input"
              value={formData.password1}
              onChange={(e) => setFormData({ ...formData, password1: e.target.value })}
              required
            />
            {errors.password1 && <div className="form-error">{errors.password1}</div>}
          </div>

          <div className="form-group">
            <label className="form-label">Confirm Password</label>
            <input
              type="password"
              className="form-input"
              value={formData.password2}
              onChange={(e) => setFormData({ ...formData, password2: e.target.value })}
              required
            />
            {errors.password2 && <div className="form-error">{errors.password2}</div>}
          </div>

          <button 
            type="submit" 
            className="btn-primary"
            style={{ width: '100%', marginTop: '1rem' }}
            disabled={loading || googleLoading}
          >
            {loading ? 'Creating account...' : 'Sign Up'}
          </button>
        </form>

        {/* Divider */}
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          margin: '1.5rem 0',
          gap: '1rem'
        }}>
          <div style={{ flex: 1, height: '1px', background: '#ddd' }}></div>
          <span style={{ color: '#666', fontSize: '0.9rem' }}>OR</span>
          <div style={{ flex: 1, height: '1px', background: '#ddd' }}></div>
        </div>

        {/* Google Signup Button */}
        {configLoading ? (
          <div style={{
            width: '100%',
            padding: '0.75rem',
            background: '#f0f0f0',
            color: '#666',
            border: 'none',
            borderRadius: '4px',
            fontSize: '0.9rem',
            textAlign: 'center'
          }}>
            Loading authentication options...
          </div>
        ) : supabaseConfig ? (
          <button
            type="button"
            onClick={handleGoogleSignup}
            disabled={googleLoading || loading}
            style={{
              width: '100%',
              padding: '0.75rem',
              background: '#4285f4',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: googleLoading || loading ? 'not-allowed' : 'pointer',
              fontSize: '1rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.75rem',
              opacity: googleLoading || loading ? 0.7 : 1,
              transition: 'opacity 0.2s'
            }}
          >
            {googleLoading ? (
              'Connecting...'
            ) : (
              <>
                <svg width="20" height="20" viewBox="0 0 24 24">
                  <path fill="white" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="white" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="white" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="white" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Sign up with Google
              </>
            )}
          </button>
        ) : (
          <div style={{
            width: '100%',
            padding: '0.75rem',
            background: '#f0f0f0',
            color: '#666',
            border: 'none',
            borderRadius: '4px',
            fontSize: '0.9rem',
            textAlign: 'center'
          }}>
            Google authentication not configured. Please set SUPABASE_URL and SUPABASE_ANON_KEY in your backend .env file.
          </div>
        )}

        <div style={{ marginTop: '1.5rem', textAlign: 'center', color: '#666' }}>
          Already have an account? <Link href="/login" style={{ color: 'var(--primary-color)' }}>Login</Link>
        </div>
      </div>

      {/* Load Supabase SDK */}
      {supabaseConfig && (
        <Script
          src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"
          onLoad={() => {
            if (typeof window !== 'undefined' && (window as any).supabase && supabaseConfig) {
              const supabase = (window as any).supabase.createClient(supabaseConfig.url, supabaseConfig.key);
              setSupabaseClient(supabase);
              checkOAuthCallback(supabase);
              
              supabase.auth.onAuthStateChange(async (event: string, session: any) => {
                if (event === 'SIGNED_IN' && session) {
                  await syncWithBackend(session.access_token);
                }
              });
            }
          }}
        />
      )}
    </main>
  );
}

