# Fix for Port 3001 Network Error and Google Auth

## Problem
When the frontend runs on port 3001 (instead of 3000), you get:
- Network errors
- Google authentication doesn't work

## Root Cause
1. **CORS Settings**: Django backend only allowed port 3000
2. **Supabase Redirect URLs**: Need to be configured in Supabase dashboard

## Fixes Applied

### ✅ 1. Updated CORS Settings (Backend)
Added port 3001 to allowed origins in `config/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:3001',  # ✅ Added
    'http://127.0.0.1:3001',  # ✅ Added
    'http://localhost:8000'
]
```

### ⚠️ 2. Supabase Dashboard Configuration (You Need to Do This)

You need to add port 3001 to your Supabase allowed redirect URLs:

1. Go to your Supabase Dashboard: https://app.supabase.com
2. Select your project
3. Go to **Authentication** → **URL Configuration**
4. Under **Redirect URLs**, add:
   - `http://localhost:3001/login`
   - `http://localhost:3001/register`
   - `http://127.0.0.1:3001/login`
   - `http://127.0.0.1:3001/register`

5. Click **Save**

## Why Port 3001?

Port 3000 might be in use by another application, so Next.js automatically uses the next available port (3001).

## How to Use Port 3000 Instead

If you want to use port 3000 specifically:

1. **Stop any process using port 3000:**
   ```powershell
   netstat -ano | findstr :3000
   # Note the PID, then:
   taskkill /F /PID <PID>
   ```

2. **Start Next.js on port 3000:**
   ```powershell
   cd frontend
   npm run dev -- -p 3000
   ```

## Testing

After making these changes:

1. **Restart Django backend** (to pick up CORS changes)
2. **Restart Next.js frontend**
3. **Test Google Auth:**
   - Go to `http://localhost:3001/login`
   - Click "Sign in with Google"
   - Should redirect properly

## Current Status

✅ **Backend CORS**: Fixed (allows port 3001)
⚠️ **Supabase Config**: You need to add port 3001 redirect URLs in Supabase dashboard

