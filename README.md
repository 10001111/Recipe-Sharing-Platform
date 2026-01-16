# Recipe Sharing Platform

A full-stack recipe sharing platform built with Django (backend) and Next.js (frontend).

## 🚀 Features

- ✅ User authentication (traditional + Google OAuth)
- ✅ Recipe CRUD operations
- ✅ Rating system (1-5 stars with reviews)
- ✅ Comments on recipes
- ✅ Favorite/Save recipes
- ✅ Recipe statistics (views, ratings, comments, favorites)
- ✅ User profiles with avatars
- ✅ Search and filter recipes
- ✅ Responsive design
- ✅ Image uploads (local dev / Vercel Blob for production)

## 📁 Project Structure

```
Recipe-Sharing-Platform/
├── apps/                    # Django apps
│   ├── recipes/            # Recipe models, views, API
│   ├── users/              # User models, authentication
│   └── api/                # REST API endpoints
├── config/                 # Django project settings
├── frontend/               # Next.js frontend
│   ├── app/               # Next.js app router pages
│   ├── components/        # React components
│   └── lib/               # Utilities and API clients
├── docs/                   # Documentation
└── media/                  # Uploaded images (local dev)
```

## 🛠️ Tech Stack

### Backend
- Django 4.2
- Django REST Framework
- PostgreSQL (Supabase) / SQLite (local dev)
- Supabase (Google OAuth)

### Frontend
- Next.js 14
- React 18
- TypeScript
- Axios
- Tailwind CSS (optional)

### Storage
- **Development**: Local filesystem (`media/` folder)
- **Production**: Vercel Blob Storage (recommended)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- PostgreSQL (optional, SQLite for local dev)

### Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py load_sample_data

# Run development server
python manage.py runserver 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Visit `http://localhost:3000` (or 3001 if 3000 is busy)

## 📦 Deployment

### Deploy to Vercel

See detailed guides:
- `docs/VERCEL_DEPLOYMENT.md` - Full deployment guide
- `docs/VERCEL_BLOB_SETUP.md` - Blob storage setup
- `DEPLOYMENT_CHECKLIST.md` - Deployment checklist

**Quick Steps:**
1. Set up Vercel Blob Storage
2. Deploy frontend to Vercel
3. Deploy Django backend (Railway/Render/etc.)
4. Configure environment variables
5. Test deployment

## 🖼️ Image Storage

### Development (Current)
- Images stored in `media/recipes/` folder
- Served by Django at `/media/recipes/image.jpg`

### Production (Vercel)
- Images stored in Vercel Blob Storage
- Global CDN included
- Free tier: 1GB storage, 100GB bandwidth/month

**Setup:** See `docs/VERCEL_BLOB_SETUP.md`

## 📚 Documentation

- `docs/MILESTONE_2.4_VERIFICATION.md` - Database & Testing
- `docs/MILESTONE_3.1_VERIFICATION.md` - HTML/CSS Setup
- `docs/PAGES_IMPLEMENTATION.md` - Pages documentation
- `docs/FEATURES_IMPLEMENTATION.md` - Features documentation
- `docs/VERCEL_DEPLOYMENT.md` - Deployment guide
- `docs/VERCEL_BLOB_SETUP.md` - Blob storage guide
- `docs/IMAGE_STORAGE.md` - Image storage options

## 🔧 Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=postgres  # Optional, uses SQLite if not set
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

## 🧪 Testing

```bash
# Run Django tests
python manage.py test

# Run specific app tests
python manage.py test apps.recipes.tests
python manage.py test apps.users.tests
```

## 📝 License

MIT License

## 👥 Contributing

Contributions welcome! Please feel free to submit a Pull Request.
