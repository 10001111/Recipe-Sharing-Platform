# Vercel Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. Vercel Blob Storage Setup
- [ ] Create Vercel account
- [ ] Create Blob store in Vercel Dashboard
- [ ] Copy Store ID
- [ ] Copy Read/Write Token
- [ ] Note the public URL format

### 2. Environment Variables Setup

#### Frontend (Vercel Dashboard)
- [ ] `NEXT_PUBLIC_API_URL` - Your Django backend URL
- [ ] `NEXT_PUBLIC_BLOB_STORE_URL` - Blob store public URL
- [ ] `NEXT_PUBLIC_SUPABASE_URL` - Supabase URL
- [ ] `NEXT_PUBLIC_SUPABASE_ANON_KEY` - Supabase anon key

#### Backend API Routes (Vercel Dashboard)
- [ ] `BLOB_STORE_ID` - Your blob store ID
- [ ] `BLOB_READ_WRITE_TOKEN` - Blob read/write token

#### Django Backend (Separate Host)
- [ ] `SECRET_KEY` - Django secret key
- [ ] `DEBUG=False` - Production mode
- [ ] `ALLOWED_HOSTS` - Your domains
- [ ] Database credentials
- [ ] Supabase credentials
- [ ] CORS allowed origins

### 3. Code Updates
- [ ] Update `next.config.js` with production API URL
- [ ] Update recipe forms to use `ImageUploadBlob`
- [ ] Test image uploads locally
- [ ] Verify API routes work

### 4. Database Setup
- [ ] Run migrations on production database
- [ ] Create superuser
- [ ] Load sample data (optional)

### 5. Deployment
- [ ] Push code to Git repository
- [ ] Connect repository to Vercel
- [ ] Configure build settings
- [ ] Set environment variables
- [ ] Deploy frontend
- [ ] Deploy Django backend (separate host)
- [ ] Test deployment

## 🚀 Quick Start Deployment

### Step 1: Prepare Repository
```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### Step 2: Deploy Frontend to Vercel

1. **Via Dashboard:**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your Git repository
   - Set Root Directory: `frontend`
   - Add environment variables
   - Click "Deploy"

2. **Via CLI:**
   ```bash
   cd frontend
   npm install -g vercel
   vercel login
   vercel
   ```

### Step 3: Set Up Vercel Blob Storage

1. Go to Vercel Dashboard → Storage
2. Create Blob store: `recipe-images`
3. Copy credentials
4. Add to environment variables

### Step 4: Deploy Django Backend

**Recommended Platforms:**
- Railway: [railway.app](https://railway.app)
- Render: [render.com](https://render.com)
- Fly.io: [fly.io](https://fly.io)

**Steps:**
1. Create account on chosen platform
2. Connect repository
3. Set environment variables
4. Deploy
5. Get backend URL
6. Update frontend `NEXT_PUBLIC_API_URL`

### Step 5: Test Everything

- [ ] Frontend loads correctly
- [ ] API calls work
- [ ] Image uploads work
- [ ] Images display correctly
- [ ] Authentication works
- [ ] All features functional

## 📝 Environment Variables Reference

### Frontend (.env.local for local, Vercel Dashboard for production)
```env
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NEXT_PUBLIC_BLOB_STORE_URL=https://your-store-id.public.blob.vercel-storage.com
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
```

### Backend API Routes (Vercel Dashboard)
```env
BLOB_STORE_ID=recipe-images-xxxxx
BLOB_READ_WRITE_TOKEN=vercel_blob_xxxxx
```

### Django Backend (Railway/Render/etc.)
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-backend.railway.app,your-frontend.vercel.app
DB_NAME=postgres
DB_USER=postgres.xxxxx
DB_PASSWORD=your-password
DB_HOST=your-db-host
DB_PORT=5432
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

## 🔧 Troubleshooting

### Build Fails
- Check Node version (18+)
- Verify all dependencies in package.json
- Check build logs in Vercel

### Images Not Uploading
- Verify blob credentials are set
- Check API route logs
- Verify blob store exists

### API Errors
- Check CORS settings
- Verify API URL is correct
- Check backend is running
- Review backend logs

### Database Errors
- Verify database credentials
- Check migrations ran
- Verify database is accessible

## 📚 Documentation Files

- `docs/VERCEL_DEPLOYMENT.md` - Full deployment guide
- `docs/VERCEL_BLOB_SETUP.md` - Blob storage setup
- `docs/IMAGE_STORAGE.md` - Image storage options

## ✅ Post-Deployment

- [ ] Test all features
- [ ] Monitor error logs
- [ ] Set up monitoring (optional)
- [ ] Configure custom domain (optional)
- [ ] Set up SSL (automatic on Vercel)

