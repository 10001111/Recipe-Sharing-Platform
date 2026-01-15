# Frontend URL Clarification

## ⚠️ IMPORTANT: Use the Correct URL

You have **TWO** different interfaces:

### 1. Django Backend Templates (Port 8000)
- **URL:** `http://127.0.0.1:8000/recipes/`
- **What it is:** Django's server-side rendered templates
- **Features:** Basic recipe listing, but **NO** modern React components
- **Statistics:** May not show properly

### 2. Next.js Frontend (Port 3000) ⭐ USE THIS ONE
- **URL:** `http://localhost:3000` or `http://127.0.0.1:3000`
- **What it is:** Modern React/Next.js frontend with all features
- **Features:** 
  - ✅ Clickable recipe cards
  - ✅ Statistics display (views, comments, favorites, ratings)
  - ✅ Rating system
  - ✅ Comment system
  - ✅ Favorite system
  - ✅ Modern UI

## How to Access the Correct Frontend

1. **Make sure Next.js is running:**
   ```bash
   cd frontend
   npm run dev
   ```

2. **Or use the batch file:**
   ```bash
   start_dev.bat
   ```

3. **Open in browser:**
   - ✅ **CORRECT:** `http://localhost:3000`
   - ❌ **WRONG:** `http://127.0.0.1:8000/recipes/`

## The Error You're Seeing

The error "A listener indicated an asynchronous response..." is typically from:
- Browser extensions (ad blockers, password managers, etc.)
- Chrome DevTools
- **NOT** from your application code

## To Fix

1. **Use the Next.js frontend** on port 3000
2. **Check browser console** for actual application errors (not extension errors)
3. **Look for our debug logs:**
   - "API Response:"
   - "Recipes Data:"
   - "Processing recipe:"
   - "Recipe stats:"

## Quick Test

1. Open `http://localhost:3000` in your browser
2. You should see the modern React interface with:
   - Navigation bar at top
   - Recipe cards with statistics
   - Clickable cards
3. Open browser console (F12)
4. Check for our debug logs showing recipe data

