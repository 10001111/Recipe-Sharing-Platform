# Vercel Deployment Guide

## Overview
This guide will help you deploy your Recipe Sharing Platform to Vercel, including setting up Vercel Blob Storage for images.

## Architecture

### Deployment Structure
- **Frontend (Next.js)**: Deployed on Vercel
- **Backend (Django)**: Can be deployed on Vercel (Serverless Functions) or separate hosting (Railway, Render, etc.)
- **Database**: PostgreSQL (Supabase recommended)
- **Image Storage**: Vercel Blob Storage

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub/GitLab/Bitbucket**: Repository for your project
3. **Supabase Account**: For database and OAuth (already configured)
4. **Vercel CLI** (optional): `npm i -g vercel`

## Step 1: Set Up Vercel Blob Storage

### 1.1 Create Blob Store

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Navigate to **Storage** → **Create Database**
3. Select **Blob**
4. Name it: `recipe-images` (or your preferred name)
5. Select region: `US East (iad1)` or closest to your users
6. Click **Create**

### 1.2 Get Blob Credentials

After creating the blob store:

1. Go to **Storage** → Your blob store → **Settings**
2. Copy the following:
   - **Store ID** (e.g., `recipe-images-xxxxx`)
   - **Read/Write Token** (keep this secret!)

### 1.3 Add Environment Variables

In Vercel Dashboard → Your Project → **Settings** → **Environment Variables**, add:

```
BLOB_STORE_ID=recipe-images-xxxxx
BLOB_READ_WRITE_TOKEN=vercel_blob_xxxxx
BLOB_STORE_URL=https://your-store-id.public.blob.vercel-storage.com
```

Also add to **Frontend Environment Variables**:
```
NEXT_PUBLIC_BLOB_STORE_URL=https://your-store-id.public.blob.vercel-storage.com
```

## Step 2: Prepare Django Backend

### Option A: Deploy Django on Vercel (Serverless)

**Note**: Django on Vercel requires special setup. Consider Option B for easier deployment.

### Option B: Deploy Django Separately (Recommended)

**Recommended Platforms:**
- **Railway**: Easy Django deployment
- **Render**: Free tier available
- **Fly.io**: Good performance
- **DigitalOcean App Platform**: Reliable

**Steps:**
1. Deploy Django backend separately
2. Get your backend URL (e.g., `https://your-api.railway.app`)
3. Update frontend API URL in Vercel environment variables

## Step 3: Configure Environment Variables

### Frontend Environment Variables (Vercel)

Add these in Vercel Dashboard → Project → Settings → Environment Variables:

```env
# API Configuration
NEXT_PUBLIC_API_URL=https://your-django-backend.railway.app

# Vercel Blob Storage (Public)
NEXT_PUBLIC_BLOB_STORE_URL=https://your-store-id.public.blob.vercel-storage.com

# Supabase (for OAuth)
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
```

### Backend Environment Variables (Django Host)

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-django-backend.railway.app,your-frontend.vercel.app

# Database (Supabase PostgreSQL)
DB_NAME=postgres
DB_USER=postgres.xxxxx
DB_PASSWORD=your-password
DB_HOST=aws-0-us-west-2.pooler.supabase.com
DB_PORT=5432

# Supabase OAuth
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app

# Vercel Blob (if Django handles uploads)
VERCEL_BLOB_STORE_ID=recipe-images-xxxxx
VERCEL_BLOB_READ_WRITE_TOKEN=vercel_blob_xxxxx
VERCEL_BLOB_STORE_URL=https://your-store-id.public.blob.vercel-storage.com
```

## Step 4: Update Image Upload Flow

### Current Flow (Local Storage)
```
Frontend → Django API → Local media/ folder
```

### New Flow (Vercel Blob)
```
Frontend → Next.js API Route → Vercel Blob Storage → Return URL → Django API (save URL)
```

### Implementation

The project already includes:
- ✅ `frontend/app/api/upload-blob/route.ts` - Upload endpoint
- ✅ `frontend/app/api/delete-blob/route.ts` - Delete endpoint
- ✅ `frontend/lib/vercel-blob.ts` - Blob client utilities

**Next Step**: Update recipe create/edit forms to use Vercel Blob instead of direct Django upload.

## Step 5: Deploy Frontend to Vercel

### Method 1: Vercel Dashboard (Recommended)

1. **Connect Repository**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click **Add New Project**
   - Import your Git repository
   - Select the repository

2. **Configure Project**
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)
   - **Install Command**: `npm install` (default)

3. **Environment Variables**
   - Add all environment variables from Step 3
   - Make sure to add for **Production**, **Preview**, and **Development**

4. **Deploy**
   - Click **Deploy**
   - Wait for build to complete
   - Your site will be live at `https://your-project.vercel.app`

### Method 2: Vercel CLI

```bash
cd frontend
npm install -g vercel
vercel login
vercel
```

Follow the prompts to deploy.

## Step 6: Update Frontend Code for Blob Storage

### Update Recipe Create/Edit Forms

The forms need to upload to Vercel Blob first, then send the URL to Django.

**Example Update** (in `frontend/app/recipes/create/page.tsx`):

```typescript
import { uploadToBlob } from '@/lib/vercel-blob';

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  
  let imageUrl = '';
  
  // Upload image to Vercel Blob first
  if (image) {
    const blobResponse = await uploadToBlob(image, 'recipes/');
    imageUrl = blobResponse.url;
  }
  
  // Then send recipe data with image URL to Django
  const recipeData = {
    ...formData,
    image_url: imageUrl, // Send URL instead of file
  };
  
  await recipeApi.create(recipeData);
};
```

## Step 7: Update Django Model (Optional)

If you want Django to accept image URLs instead of files:

```python
# Add to Recipe model
image_url = models.URLField(blank=True, null=True, help_text="Image URL from Vercel Blob")
```

## Step 8: Database Migration

1. **Run migrations** on your Django backend:
   ```bash
   python manage.py migrate
   ```

2. **Load sample data** (optional):
   ```bash
   python manage.py load_sample_data
   ```

## Step 9: Test Deployment

1. **Frontend**: Visit `https://your-project.vercel.app`
2. **Test Image Upload**: Create a recipe with an image
3. **Verify**: Check that image appears and is served from Vercel Blob
4. **Test API**: Verify API calls work correctly

## Troubleshooting

### Images Not Loading

1. **Check Blob Store URL**: Verify `NEXT_PUBLIC_BLOB_STORE_URL` is correct
2. **Check CORS**: Ensure blob store allows your domain
3. **Check Image URLs**: Verify URLs are public and accessible

### API Errors

1. **Check API URL**: Verify `NEXT_PUBLIC_API_URL` points to your Django backend
2. **Check CORS**: Ensure Django allows requests from Vercel domain
3. **Check Environment Variables**: Verify all are set correctly

### Build Errors

1. **Check Node Version**: Vercel uses Node 18+ by default
2. **Check Dependencies**: Ensure `package.json` has all required packages
3. **Check Build Logs**: Review build output in Vercel dashboard

## Vercel Blob Storage Pricing

- **Free Tier**: 
  - 1 GB storage
  - 100 GB bandwidth/month
- **Pro Plan**: 
  - $20/month
  - 100 GB storage
  - 1 TB bandwidth/month
- **Enterprise**: Custom pricing

**Note**: For recipe images, free tier should be sufficient for small-medium projects.

## Alternative: Cloudinary (If Needed)

If Vercel Blob doesn't meet your needs, consider Cloudinary:

1. **Free Tier**: 25GB storage, 25GB bandwidth
2. **Image Optimization**: Automatic resizing, compression
3. **Easy Integration**: Simple API

## Production Checklist

- [ ] Environment variables configured
- [ ] Vercel Blob Storage set up
- [ ] Django backend deployed
- [ ] Database migrations run
- [ ] CORS configured correctly
- [ ] SSL certificates active (automatic on Vercel)
- [ ] Image upload flow tested
- [ ] API endpoints working
- [ ] Error handling in place
- [ ] Monitoring set up (optional)

## Next Steps

1. **Set up Vercel Blob Storage** (Step 1)
2. **Deploy frontend** (Step 5)
3. **Deploy Django backend** (Step 2, Option B)
4. **Update image upload flow** (Step 6)
5. **Test everything** (Step 9)

## Support

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Blob Storage Docs](https://vercel.com/docs/storage/vercel-blob)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

