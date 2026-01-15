'use client';

import { useEffect, useState, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { userApi, recipeApi, RecipeList } from '@/lib/api';
import { ProfileSkeleton, RecipeGridSkeleton } from '@/components/LoadingSkeleton';

interface UserProfile {
  user: {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
  };
  username: string;
  bio: string;
  avatar: string | null;
  avatar_url: string | null;
  dietary_preferences: string;
  created_at: string;
  updated_at: string;
  recipe_count: number;
}

export default function UserProfilePage() {
  const params = useParams();
  const router = useRouter();
  const username = params?.username as string;
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [recipes, setRecipes] = useState<RecipeList[]>([]);
  const [profileLoading, setProfileLoading] = useState(true);
  const [recipesLoading, setRecipesLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editUsername, setEditUsername] = useState('');
  const [editBio, setEditBio] = useState('');
  const [saving, setSaving] = useState(false);
  const [currentUser, setCurrentUser] = useState<any>(null);

  useEffect(() => {
    if (username) {
      Promise.all([
        loadProfile(),
        loadUserRecipes(),
        checkCurrentUser()
      ]);
    }
  }, [username]);

  const checkCurrentUser = async () => {
    try {
      const user = await userApi.getCurrent();
      setCurrentUser(user);
      if (user && user.username === username) {
        setIsEditing(false);
      }
    } catch (err) {
      // Not logged in or error
    }
  };

  const loadProfile = async () => {
    try {
      setProfileLoading(true);
      const profileData = await userApi.getProfile(username);
      setProfile(profileData);
      setEditUsername(profileData.username || profileData.user.username);
      setEditBio(profileData.bio || '');
      setError(null);
    } catch (err: any) {
      if (err.response?.status === 404) {
        setError('User not found');
      } else {
        setError('Failed to load profile');
      }
    } finally {
      setProfileLoading(false);
    }
  };

  const loadUserRecipes = async () => {
    try {
      setRecipesLoading(true);
      const response = await recipeApi.getAll({ author_username: username });
      const recipesData = response.results || response;
      const userRecipes = Array.isArray(recipesData) ? recipesData : [];
      setRecipes(userRecipes);
    } catch (err) {
      console.error('Error loading recipes:', err);
    } finally {
      setRecipesLoading(false);
    }
  };

  const handleEdit = () => {
    if (profile) {
      setEditUsername(profile.username || profile.user.username);
      setEditBio(profile.bio || '');
      setIsEditing(true);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    if (profile) {
      setEditUsername(profile.username || profile.user.username);
      setEditBio(profile.bio || '');
    }
  };

  const handleSave = async () => {
    if (!profile) return;
    
    try {
      setSaving(true);
      const formData = new FormData();
      
      if (editUsername !== (profile.username || profile.user.username)) {
        formData.append('username', editUsername);
      }
      if (editBio !== profile.bio) {
        formData.append('bio', editBio);
      }
      
      const avatarFile = fileInputRef.current?.files?.[0];
      if (avatarFile) {
        formData.append('avatar', avatarFile);
      }
      
      const updatedProfile = await userApi.updateProfile(username, formData);
      setProfile(updatedProfile);
      setIsEditing(false);
      
      // If username changed, redirect to new URL
      if (editUsername !== username) {
        router.push(`/users/profile/${editUsername}`);
      } else {
        loadProfile();
      }
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const handleAvatarClick = () => {
    if (isEditing && fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleSave();
    }
  };

  const isOwnProfile = currentUser && profile && (currentUser.username === username || currentUser.username === profile.user.username);

  if (error && !profileLoading) {
    return (
      <main className="container" style={{ minHeight: '60vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ textAlign: 'center' }}>
          <h1 style={{ fontSize: '3rem', fontWeight: '300', marginBottom: '1rem', color: '#333' }}>404</h1>
          <p style={{ color: '#666', marginBottom: '2rem' }}>{error || 'User not found'}</p>
          <Link href="/" style={{ color: '#333', textDecoration: 'underline' }}>
            Go back home
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="container" style={{ maxWidth: '1200px', margin: '0 auto', padding: '3rem 1rem' }}>
      {profileLoading ? (
        <ProfileSkeleton />
      ) : profile ? (
        <div className="fade-in">
          {/* Minimal Profile Header */}
          <div style={{
            marginBottom: '4rem',
            paddingBottom: '2rem',
            borderBottom: '1px solid #e5e5e5'
          }}>
            <div style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '2rem',
              flexWrap: 'wrap'
            }}>
              {/* Avatar */}
              <div style={{ position: 'relative' }}>
                {profile.avatar_url ? (
                  <img
                    src={profile.avatar_url}
                    alt={profile.username || profile.user.username}
                    style={{
                      width: '100px',
                      height: '100px',
                      borderRadius: '50%',
                      objectFit: 'cover',
                      border: '2px solid #e5e5e5',
                      cursor: isEditing ? 'pointer' : 'default',
                      transition: 'opacity 0.2s'
                    }}
                    onClick={handleAvatarClick}
                    onMouseEnter={(e) => {
                      if (isEditing) e.currentTarget.style.opacity = '0.8';
                    }}
                    onMouseLeave={(e) => {
                      if (isEditing) e.currentTarget.style.opacity = '1';
                    }}
                  />
                ) : (
                  <div
                    onClick={handleAvatarClick}
                    style={{
                      width: '100px',
                      height: '100px',
                      borderRadius: '50%',
                      background: '#f0f0f0',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '2.5rem',
                      color: '#999',
                      fontWeight: '300',
                      border: '2px solid #e5e5e5',
                      cursor: isEditing ? 'pointer' : 'default',
                      transition: 'opacity 0.2s'
                    }}
                    onMouseEnter={(e) => {
                      if (isEditing) e.currentTarget.style.opacity = '0.8';
                    }}
                    onMouseLeave={(e) => {
                      if (isEditing) e.currentTarget.style.opacity = '1';
                    }}
                  >
                    {(profile.username || profile.user.username).charAt(0).toUpperCase()}
                  </div>
                )}
                {isEditing && (
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    style={{ display: 'none' }}
                    onChange={handleAvatarChange}
                  />
                )}
              </div>

              {/* Profile Info */}
              <div style={{ flex: 1, minWidth: '300px' }}>
                {isEditing ? (
                  <div style={{ marginBottom: '1.5rem' }}>
                    <input
                      type="text"
                      value={editUsername}
                      onChange={(e) => setEditUsername(e.target.value)}
                      style={{
                        fontSize: '2rem',
                        fontWeight: '400',
                        border: 'none',
                        borderBottom: '1px solid #e5e5e5',
                        padding: '0.5rem 0',
                        width: '100%',
                        background: 'transparent',
                        color: '#333',
                        outline: 'none',
                        fontFamily: 'inherit'
                      }}
                      placeholder="Username"
                    />
                  </div>
                ) : (
                  <h1 style={{
                    fontSize: '2rem',
                    fontWeight: '400',
                    margin: '0 0 0.5rem 0',
                    color: '#333',
                    letterSpacing: '-0.02em'
                  }}>
                    {profile.username || profile.user.username}
                  </h1>
                )}

                {isEditing ? (
                  <textarea
                    value={editBio}
                    onChange={(e) => setEditBio(e.target.value)}
                    placeholder="Add a bio..."
                    style={{
                      width: '100%',
                      minHeight: '80px',
                      border: 'none',
                      borderBottom: '1px solid #e5e5e5',
                      padding: '0.5rem 0',
                      background: 'transparent',
                      color: '#666',
                      fontSize: '0.95rem',
                      fontFamily: 'inherit',
                      resize: 'vertical',
                      outline: 'none',
                      lineHeight: '1.6'
                    }}
                  />
                ) : (
                  <p style={{
                    color: '#666',
                    fontSize: '0.95rem',
                    lineHeight: '1.6',
                    margin: '0 0 1rem 0',
                    maxWidth: '600px'
                  }}>
                    {profile.bio || 'No bio yet'}
                  </p>
                )}

                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '2rem',
                  marginTop: '1rem',
                  flexWrap: 'wrap'
                }}>
                  <span style={{ color: '#999', fontSize: '0.875rem' }}>
                    {recipes.length} recipe{recipes.length !== 1 ? 's' : ''}
                  </span>
                  <span style={{ color: '#999', fontSize: '0.875rem' }}>
                    Joined {new Date(profile.created_at).toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
                  </span>
                </div>

                {/* Edit Controls */}
                {isOwnProfile && (
                  <div style={{ marginTop: '1.5rem', display: 'flex', gap: '1rem' }}>
                    {isEditing ? (
                      <>
                        <button
                          onClick={handleSave}
                          disabled={saving}
                          style={{
                            padding: '0.5rem 1.5rem',
                            background: '#333',
                            color: 'white',
                            border: 'none',
                            borderRadius: '2px',
                            cursor: saving ? 'not-allowed' : 'pointer',
                            fontSize: '0.875rem',
                            fontWeight: '400',
                            opacity: saving ? 0.6 : 1,
                            transition: 'opacity 0.2s'
                          }}
                        >
                          {saving ? 'Saving...' : 'Save'}
                        </button>
                        <button
                          onClick={handleCancel}
                          disabled={saving}
                          style={{
                            padding: '0.5rem 1.5rem',
                            background: 'transparent',
                            color: '#666',
                            border: '1px solid #e5e5e5',
                            borderRadius: '2px',
                            cursor: saving ? 'not-allowed' : 'pointer',
                            fontSize: '0.875rem',
                            fontWeight: '400'
                          }}
                        >
                          Cancel
                        </button>
                      </>
                    ) : (
                      <button
                        onClick={handleEdit}
                        style={{
                          padding: '0.5rem 1.5rem',
                          background: 'transparent',
                          color: '#333',
                          border: '1px solid #e5e5e5',
                          borderRadius: '2px',
                          cursor: 'pointer',
                          fontSize: '0.875rem',
                          fontWeight: '400',
                          transition: 'background 0.2s'
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.background = '#f5f5f5';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.background = 'transparent';
                        }}
                      >
                        Edit Profile
                      </button>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Recipes Section */}
          <div>
            <h2 style={{
              fontSize: '1.25rem',
              fontWeight: '400',
              marginBottom: '2rem',
              color: '#333',
              letterSpacing: '-0.01em'
            }}>
              Recipes
            </h2>
            {recipesLoading ? (
              <RecipeGridSkeleton count={6} />
            ) : recipes.length > 0 ? (
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
                gap: '2rem'
              }}>
                {recipes.map((recipe) => (
                  <div
                    key={recipe.id}
                    onClick={() => router.push(`/recipes/${recipe.id}`)}
                    style={{
                      cursor: 'pointer',
                      transition: 'opacity 0.2s'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.opacity = '0.8';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.opacity = '1';
                    }}
                  >
                    {recipe.image && (
                      <img
                        src={recipe.image}
                        alt={recipe.title}
                        style={{
                          width: '100%',
                          height: '200px',
                          objectFit: 'cover',
                          borderRadius: '2px',
                          marginBottom: '1rem'
                        }}
                        loading="lazy"
                      />
                    )}
                    <h3 style={{
                      fontSize: '1rem',
                      fontWeight: '400',
                      margin: '0 0 0.5rem 0',
                      color: '#333'
                    }}>
                      {recipe.title}
                    </h3>
                    <p style={{
                      color: '#999',
                      fontSize: '0.875rem',
                      margin: 0,
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      overflow: 'hidden',
                      lineHeight: '1.5'
                    }}>
                      {recipe.description}
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <div style={{
                padding: '3rem',
                textAlign: 'center',
                color: '#999'
              }}>
                <p>No recipes yet</p>
              </div>
            )}
          </div>
        </div>
      ) : null}
    </main>
  );
}
