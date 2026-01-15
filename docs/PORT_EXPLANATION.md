# Port 3000 vs Port 8000 - Explained

## Quick Summary

- **Port 3000**: Your **Frontend** (Next.js) - The user interface
- **Port 8000**: Your **Backend** (Django) - The API server

---

## Detailed Explanation

### Port 3000 - Frontend (Next.js)

**What it is:**
- This is where your **Next.js** application runs
- It's the **user-facing website** that users interact with
- Located in the `frontend/` folder

**What it does:**
- Serves HTML, CSS, and JavaScript to the browser
- Handles routing (like `/recipes`, `/login`, `/users/profile/username`)
- Makes API calls to the backend (port 8000) to get data
- Renders React components

**How to access:**
- URL: `http://localhost:3000`
- This is what you see in your browser

**Example:**
When you visit `http://localhost:3000/recipes`, the Next.js app:
1. Shows you the recipes page
2. Makes a request to `http://127.0.0.1:8000/api/recipes/` to get recipe data
3. Displays that data on the page

---

### Port 8000 - Backend (Django)

**What it is:**
- This is where your **Django** application runs
- It's the **API server** that handles data and business logic
- Located in the root folder (where `manage.py` is)

**What it does:**
- Stores and retrieves data from the database
- Handles authentication (login, logout)
- Processes API requests (GET, POST, PATCH, DELETE)
- Returns JSON data to the frontend
- Handles file uploads (images, avatars)

**How to access:**
- URL: `http://127.0.0.1:8000` or `http://localhost:8000`
- API endpoints: `http://127.0.0.1:8000/api/recipes/`, `/api/users/`, etc.

**Example:**
When the frontend requests recipes:
1. Frontend sends: `GET http://127.0.0.1:8000/api/recipes/`
2. Django queries the database
3. Django returns JSON: `{ "results": [{ "id": 1, "title": "Pasta", ... }] }`
4. Frontend receives the data and displays it

---

## How They Work Together

```
┌─────────────────┐         HTTP Requests          ┌─────────────────┐
│                 │  ────────────────────────────>  │                 │
│   Port 3000     │                                 │   Port 8000     │
│   (Frontend)    │  <──────────────────────────── │   (Backend)     │
│   Next.js       │      JSON Data Response         │   Django        │
│                 │                                 │                 │
└─────────────────┘                                 └─────────────────┘
      ↑                                                      ↑
      │                                                      │
      │                                                      │
   Browser                                              Database
   (You)                                                (PostgreSQL)
```

### Real Example Flow:

1. **User visits** `http://localhost:3000/users/profile/john`
   - Frontend (port 3000) loads the profile page

2. **Frontend makes API call:**
   ```javascript
   fetch('http://127.0.0.1:8000/api/users/profile/john/')
   ```

3. **Backend (port 8000) processes:**
   - Django receives the request
   - Queries database for user "john"
   - Returns JSON with profile data

4. **Frontend receives data:**
   - Next.js gets the JSON response
   - Updates the page with profile information

---

## Why Two Ports?

**Separation of Concerns:**
- **Frontend** = Presentation layer (what users see)
- **Backend** = Data layer (where data lives)

**Benefits:**
- ✅ Can develop frontend and backend independently
- ✅ Can deploy them separately
- ✅ Frontend can be replaced (React, Vue, etc.) without changing backend
- ✅ Backend can serve multiple frontends (web, mobile app, etc.)
- ✅ Better security (backend handles sensitive operations)

---

## Common Ports in Development

| Port | Common Use |
|------|------------|
| 3000 | React/Next.js frontend (very common) |
| 8000 | Django backend (very common) |
| 5000 | Flask backend, or alternative React port |
| 8080 | Alternative backend port |
| 3001 | Alternative frontend port (if 3000 is busy) |

---

## Troubleshooting

**"Can't connect to port 8000"**
- Make sure Django server is running: `python manage.py runserver 8000`
- Check if port 8000 is already in use

**"Can't connect to port 3000"**
- Make sure Next.js is running: `npm run dev` (in frontend folder)
- Check if port 3000 is already in use

**"CORS errors"**
- This happens when frontend (3000) tries to call backend (8000)
- Make sure CORS is configured in Django settings
- Check that `CORS_ALLOWED_ORIGINS` includes `http://localhost:3000`

---

## Summary

- **Port 3000** = Your website (what you see)
- **Port 8000** = Your API server (where data comes from)
- They work together: Frontend asks Backend for data, Backend responds with data
- Both need to be running for the app to work!

