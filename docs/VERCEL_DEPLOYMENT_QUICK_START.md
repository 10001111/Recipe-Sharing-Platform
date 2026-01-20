# Vercel Deployment Quick Start

## Current Issue
**Error**: Project name "recipe-sharing-platform1" already exists.

## Solution
Choose a different project name when deploying, such as:
- `recipe-sharing-platform-v2`
- `recipe-sharing-app`
- `recipe-platform-2024`
- `my-recipe-sharing-platform`

## Deployment Steps

### 1. Import Repository
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **Add New Project** or **Import Project**
3. Select your Git repository (GitHub/GitLab/Bitbucket)

### 2. Configure Project Settings

**Important Settings:**
- **Project Name**: Choose a unique name (NOT "recipe-sharing-platform1")
- **Root Directory**: `frontend` ⚠️ **CRITICAL** - Your Next.js app is in the `frontend` folder
- **Framework Preset**: Next.js (auto-detected)
- **Build Command**: `npm run build` (default)
- **Output Directory**: `.next` (default)
- **Install Command**: `npm install` (default)

### 3. Environment Variables

Add these in **Settings → Environment Variables**:

```env
# API Configuration
NEXT_PUBLIC_API_URL=https://your-django-backend-url.com

# Supabase (if using)
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key

# Vercel Blob Storage (if using)
NEXT_PUBLIC_BLOB_STORE_URL=https://your-store-id.public.blob.vercel-storage.com
```

**Important**: Add these for **Production**, **Preview**, and **Development** environments.

### 4. Deploy

Click **Deploy** and wait for the build to complete.

Your site will be live at: `https://your-new-project-name.vercel.app`

## Troubleshooting

### Build Fails
- Check that **Root Directory** is set to `frontend`
- Verify all environment variables are set
- Check build logs in Vercel dashboard

### Project Name Already Exists
- Use a different name (add numbers, dates, or descriptive words)
- Or delete the existing project from Vercel dashboard first

### API Not Working
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS settings on your Django backend
- Ensure backend is deployed and accessible

## Next Steps

1. ✅ Deploy frontend to Vercel
2. ⬜ Deploy Django backend (Railway, Render, etc.)
3. ⬜ Set up Vercel Blob Storage (if needed)
4. ⬜ Configure environment variables
5. ⬜ Test the deployment

## Need Help?

See full deployment guide: [VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md)

