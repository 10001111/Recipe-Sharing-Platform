# Vercel Environment Variables Fix

## The Error Explained

**Error**: `Environment Variable "NEXT_PUBLIC_API_URL" references Secret "api_url", which does not exist.`

### What This Means

Your `vercel.json` files were trying to reference a Vercel secret called `api_url` using the `@api_url` syntax. However, this secret was never created in your Vercel account.

In Vercel:
- **Environment Variables**: Simple key-value pairs set in the dashboard
- **Secrets**: Encrypted values referenced with `@secret_name` syntax (requires creating the secret first)

For this project, we don't need secrets - we just need regular environment variables.

## What I Fixed

✅ Removed the `env` section from `frontend/vercel.json`  
✅ Removed the `env` section from root `vercel.json`

Now you'll set environment variables directly in the Vercel dashboard instead.

## How to Set Environment Variables in Vercel

### Step 1: Go to Your Project Settings

1. In Vercel Dashboard, select your project
2. Click **Settings** (top navigation)
3. Click **Environment Variables** (left sidebar)

### Step 2: Add Environment Variables

Click **Add New** and add these variables:

#### Required Variable

**Name**: `NEXT_PUBLIC_API_URL`  
**Value**: Your Django backend URL

**Examples:**
- If backend is on Railway: `https://your-app.railway.app`
- If backend is on Render: `https://your-app.onrender.com`
- If backend is on Fly.io: `https://your-app.fly.dev`
- If backend is localhost (development only): `http://127.0.0.1:8000`

**Important**: 
- ✅ Add for **Production**
- ✅ Add for **Preview** 
- ✅ Add for **Development** (if you want to test locally)

#### Optional Variables (if using Supabase)

**Name**: `NEXT_PUBLIC_SUPABASE_URL`  
**Value**: Your Supabase project URL (e.g., `https://xxxxx.supabase.co`)

**Name**: `NEXT_PUBLIC_SUPABASE_ANON_KEY`  
**Value**: Your Supabase anonymous key

#### Optional Variables (if using Vercel Blob Storage)

**Name**: `NEXT_PUBLIC_BLOB_STORE_URL`  
**Value**: Your Vercel Blob store URL (e.g., `https://xxxxx.public.blob.vercel-storage.com`)

### Step 3: Redeploy

After adding environment variables:
1. Go to **Deployments** tab
2. Click the **⋯** (three dots) on the latest deployment
3. Click **Redeploy**
4. Or push a new commit to trigger a new deployment

## What Value Should I Use for NEXT_PUBLIC_API_URL?

### If Your Backend is Already Deployed

Use your backend's production URL:
- Railway: `https://your-app-name.railway.app`
- Render: `https://your-app-name.onrender.com`
- Fly.io: `https://your-app-name.fly.dev`
- DigitalOcean: `https://your-app-name.ondigitalocean.app`

### If Your Backend is NOT Deployed Yet

**Option 1**: Deploy backend first, then use that URL  
**Option 2**: Use a placeholder for now, update later:
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

**Option 3**: If testing locally, you can use:
```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```
(Note: This only works for local development, not production)

## Verification

After setting environment variables and redeploying:

1. ✅ Build should succeed (no more secret error)
2. ✅ Check deployment logs to confirm variables are loaded
3. ✅ Test your app - API calls should work if backend URL is correct

## Troubleshooting

### Still Getting Errors?

1. **Make sure you added the variable for all environments** (Production, Preview, Development)
2. **Redeploy after adding variables** - they don't apply to existing deployments
3. **Check variable name** - must be exactly `NEXT_PUBLIC_API_URL` (case-sensitive)
4. **Check variable value** - no trailing slashes, use full URL with `https://`

### How to Check if Variables Are Set

1. Go to **Deployments** → Click on a deployment
2. Click **Build Logs**
3. Look for environment variables being loaded (they won't show values for security)

### Backend Not Responding?

- Verify your backend URL is correct and accessible
- Check CORS settings on your Django backend
- Ensure backend allows requests from your Vercel domain

## Next Steps

1. ✅ Set `NEXT_PUBLIC_API_URL` in Vercel dashboard
2. ⬜ Deploy your Django backend (if not already deployed)
3. ⬜ Update CORS settings on backend to allow Vercel domain
4. ⬜ Test the deployment

## Summary

- **Problem**: Secret `@api_url` didn't exist
- **Solution**: Removed secret references, use regular environment variables instead
- **Action**: Set `NEXT_PUBLIC_API_URL` in Vercel dashboard → Environment Variables
- **Result**: Build will succeed, app will connect to your backend

