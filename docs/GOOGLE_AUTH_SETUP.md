# Google Authentication Setup

## ✅ Google OAuth Added to Login and Signup Pages

Google authentication has been added to both the login and signup pages in the Next.js frontend.

---

## 🔧 Setup Instructions

### 1. Configure Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```bash
cd frontend
cp .env.local.example .env.local
```

Then edit `.env.local` and add your Supabase credentials:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here
```

### 2. Get Supabase Credentials

1. Go to your Supabase project dashboard
2. Navigate to **Settings** → **API**
3. Copy:
   - **Project URL** → `NEXT_PUBLIC_SUPABASE_URL`
   - **anon/public key** → `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### 3. Enable Google OAuth in Supabase

1. Go to **Authentication** → **Providers** in Supabase dashboard
2. Enable **Google** provider
3. Add your OAuth credentials:
   - Client ID (from Google Cloud Console)
   - Client Secret (from Google Cloud Console)
4. Add redirect URL: `http://localhost:3000/login` (for development)

### 4. Restart Next.js Server

After adding environment variables, restart the Next.js dev server:

```bash
cd frontend
npm run dev
```

---

## 🎨 Features Added

### Login Page (`/login`)
- ✅ Traditional username/password login
- ✅ **Google Sign In button** with Google logo
- ✅ OAuth callback handling
- ✅ Automatic sync with Django backend
- ✅ Error handling and loading states

### Register Page (`/register`)
- ✅ Traditional registration form
- ✅ **Google Sign Up button** with Google logo
- ✅ OAuth callback handling
- ✅ Automatic user creation in Django
- ✅ Error handling and loading states

---

## 🔄 How It Works

1. **User clicks "Sign in with Google"**
   - Frontend calls Supabase Auth API
   - User is redirected to Google OAuth

2. **Google Authentication**
   - User authenticates with Google
   - Google redirects back to your app

3. **Supabase Issues Token**
   - Supabase verifies Google authentication
   - Issues JWT access token

4. **Frontend Syncs with Django**
   - Frontend sends token to `/users/supabase-auth/`
   - Django verifies token with Supabase
   - Django creates/updates user account
   - Django logs user into session

5. **User is Logged In**
   - Redirected to home page or profile
   - Session is active
   - Can use all features

---

## 🐛 Troubleshooting

### Google Button Not Showing
- Check that `.env.local` has `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- Restart Next.js dev server after adding env vars
- Check browser console for errors

### Google OAuth Not Working
- Verify Google OAuth is enabled in Supabase dashboard
- Check redirect URLs are configured correctly
- Ensure Google Cloud Console OAuth credentials are correct

### "Authentication failed" Error
- Check Supabase credentials in `.env.local`
- Verify backend `/users/supabase-auth/` endpoint is working
- Check browser console and Django server logs

---

## 📝 Notes

- The Supabase SDK is loaded via CDN (no npm install needed)
- Google OAuth works for both login and signup (same flow)
- Users created via Google OAuth get default 'user' role
- OAuth users don't have passwords (set to unusable)

---

## 🔒 Security

- Supabase handles OAuth securely
- Tokens are verified server-side
- CSRF protection via Django
- Session-based authentication after OAuth

