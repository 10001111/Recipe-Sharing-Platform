# Vercel Blob Storage Setup Guide

## Quick Answer: Yes, You Can Use Vercel Storage!

**Vercel Blob Storage** is perfect for storing recipe images. It's:
- ✅ Built into Vercel platform
- ✅ Global CDN included
- ✅ Easy to integrate
- ✅ Free tier available (1GB storage, 100GB bandwidth/month)

## How It Works

### Architecture
```
User uploads image → Next.js API Route → Vercel Blob Storage → Returns URL → Save URL in Django
```

### Storage Flow
1. User selects image in frontend
2. Frontend uploads to Next.js API route (`/api/upload-blob`)
3. API route uploads to Vercel Blob Storage
4. Blob Storage returns public URL
5. Frontend sends URL to Django API
6. Django saves URL in database (not the file)

## Setup Steps

### 1. Create Vercel Blob Store

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **Storage** → **Create Database**
3. Select **Blob**
4. Name: `recipe-images`
5. Region: Choose closest to your users
6. Click **Create**

### 2. Get Credentials

After creating:
- **Store ID**: `recipe-images-xxxxx` (copy this)
- **Read/Write Token**: `vercel_blob_xxxxx` (keep secret!)

### 3. Add Environment Variables

In Vercel Dashboard → Your Project → **Settings** → **Environment Variables**:

**For Production:**
```
BLOB_STORE_ID=recipe-images-xxxxx
BLOB_READ_WRITE_TOKEN=vercel_blob_xxxxx
BLOB_STORE_URL=https://recipe-images-xxxxx.public.blob.vercel-storage.com
```

**For Frontend (Public):**
```
NEXT_PUBLIC_BLOB_STORE_URL=https://recipe-images-xxxxx.public.blob.vercel-storage.com
```

### 4. Update Image Upload Components

The project includes:
- ✅ `ImageUploadBlob.tsx` - Component for Vercel Blob uploads
- ✅ `frontend/app/api/upload-blob/route.ts` - Upload API route
- ✅ `frontend/app/api/delete-blob/route.ts` - Delete API route
- ✅ `frontend/lib/vercel-blob.ts` - Blob utilities

**To use in recipe forms:**
Replace `ImageUpload` with `ImageUploadBlob`:

```tsx
import ImageUploadBlob from '@/components/ImageUploadBlob';

// In your form:
<ImageUploadBlob 
  onImageUrlChange={(url) => setImageUrl(url)}
  currentImageUrl={existingImageUrl}
  label="Recipe Image"
/>
```

## Pricing

### Free Tier
- 1 GB storage
- 100 GB bandwidth/month
- Perfect for small-medium projects

### Pro Plan ($20/month)
- 100 GB storage
- 1 TB bandwidth/month
- Good for larger projects

### Enterprise
- Custom pricing
- For high-traffic sites

## Advantages Over Local Storage

| Feature | Local Storage | Vercel Blob |
|---------|--------------|-------------|
| Scalability | ❌ Limited | ✅ Unlimited |
| CDN | ❌ No | ✅ Global CDN |
| Backup | ❌ Manual | ✅ Automatic |
| Performance | ⚠️ Depends on server | ✅ Fast globally |
| Cost | ✅ Free | ✅ Free tier available |

## Migration Path

### Current (Local Storage)
```
media/recipes/image.jpg → http://127.0.0.1:8000/media/recipes/image.jpg
```

### With Vercel Blob
```
Vercel Blob → https://recipe-images-xxxxx.public.blob.vercel-storage.com/recipes/image.jpg
```

## Implementation Status

✅ **Already Implemented:**
- Blob upload API route
- Blob delete API route
- Blob client utilities
- ImageUploadBlob component

🔄 **Next Steps:**
- Update recipe create/edit forms to use `ImageUploadBlob`
- Update Django to accept image URLs instead of files
- Test upload flow

## Testing Locally

To test Vercel Blob locally:

1. **Set up environment variables** in `.env.local`:
```env
BLOB_STORE_ID=your-store-id
BLOB_READ_WRITE_TOKEN=your-token
BLOB_STORE_URL=https://your-store-id.public.blob.vercel-storage.com
NEXT_PUBLIC_BLOB_STORE_URL=https://your-store-id.public.blob.vercel-storage.com
```

2. **Run frontend**:
```bash
cd frontend
npm run dev
```

3. **Test upload**: Create a recipe with an image

## Production Deployment

1. **Deploy frontend to Vercel**
2. **Add environment variables** in Vercel dashboard
3. **Test image uploads**
4. **Verify images load correctly**

## Troubleshooting

### Images Not Uploading
- Check `BLOB_STORE_ID` and `BLOB_READ_WRITE_TOKEN` are set
- Verify blob store exists in Vercel dashboard
- Check API route logs in Vercel

### Images Not Displaying
- Verify `NEXT_PUBLIC_BLOB_STORE_URL` is correct
- Check blob URLs are public
- Verify CORS settings

### Upload Errors
- Check file size (max 5MB)
- Verify file type (images only)
- Check network connectivity

## Alternative Options

If Vercel Blob doesn't work for you:

1. **Cloudinary** - Free tier, image optimization
2. **Supabase Storage** - Already using Supabase
3. **AWS S3** - Most control, more setup

## Summary

✅ **Yes, you can use Vercel Blob Storage!**
- Perfect for recipe images
- Free tier available
- Easy integration
- Global CDN included
- Already implemented in the project

Just need to:
1. Create blob store in Vercel
2. Add environment variables
3. Update forms to use `ImageUploadBlob`
4. Deploy!

