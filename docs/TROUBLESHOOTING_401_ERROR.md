# Troubleshooting 401 Unauthorized Errors

## What is a 401 Error?

A **401 Unauthorized** error means the server is rejecting your request because you're not authenticated (not logged in) or your session has expired.

## Common Causes

### 1. **Not Logged In**
- You're trying to access a protected endpoint without being authenticated
- **Solution**: Log in first, then try again

### 2. **Session Expired**
- Your login session has expired (default: 2 weeks)
- **Solution**: Log out and log back in

### 3. **Cookies Not Being Sent**
- Browser is blocking cookies or CORS is misconfigured
- **Solution**: Check browser settings and CORS configuration

### 4. **CSRF Token Issues**
- Missing or invalid CSRF token
- **Solution**: Ensure cookies are enabled and CORS is configured correctly

## How to Fix

### Step 1: Check if You're Logged In

1. Look at the navbar - do you see your username?
2. If not, click "Log In" and authenticate
3. After logging in, try the action again

### Step 2: Clear Browser Data (if session seems stuck)

1. Open browser DevTools (F12)
2. Go to **Application** tab → **Cookies**
3. Delete cookies for `localhost:3000` and `127.0.0.1:8000`
4. Refresh the page and log in again

### Step 3: Check Browser Console

1. Open DevTools (F12)
2. Go to **Console** tab
3. Look for error messages
4. Check **Network** tab for failed requests

### Step 4: Verify Backend is Running

```bash
# Make sure Django backend is running
python manage.py runserver
```

### Step 5: Check CORS Configuration

Make sure `config/settings.py` has:

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
CORS_ALLOW_CREDENTIALS = True
```

### Step 6: Verify Session Authentication

The app uses **session-based authentication** (cookies), not tokens. Make sure:

1. Cookies are enabled in your browser
2. You're accessing from the same domain (localhost:3000 → localhost:8000)
3. `withCredentials: true` is set in axios (already configured)

## Testing Authentication

### Check if You're Authenticated:

```javascript
// In browser console
fetch('http://127.0.0.1:8000/api/users/me/', {
  credentials: 'include'
})
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

If you see your user data, you're authenticated. If you get 401, you need to log in.

## Common Scenarios

### Scenario 1: Meal Plan Calendar Shows 401

**Problem**: Trying to access `/meal-plan` without being logged in

**Solution**: 
1. The page should redirect you to `/login`
2. Log in with your credentials
3. You'll be redirected back to `/meal-plan`

### Scenario 2: Can't Save Meal Plans

**Problem**: Getting 401 when dragging recipes to calendar

**Solution**:
1. Check if you're logged in (look at navbar)
2. If not logged in, log in first
3. Try dragging again

### Scenario 3: Session Expired Mid-Session

**Problem**: Was working, suddenly getting 401 errors

**Solution**:
1. Log out completely
2. Clear browser cookies
3. Log back in
4. Try again

## Debugging Steps

### 1. Check Network Tab

1. Open DevTools → **Network** tab
2. Try the action that causes 401
3. Click on the failed request
4. Check:
   - **Request Headers**: Is `Cookie` header present?
   - **Response**: What's the error message?

### 2. Check Application Tab

1. Open DevTools → **Application** tab
2. Go to **Cookies** → `http://127.0.0.1:8000`
3. Look for:
   - `sessionid` cookie (should exist if logged in)
   - `csrftoken` cookie (should exist)

### 3. Check Console for Errors

Look for messages like:
- "401 Unauthorized"
- "Authentication credentials were not provided"
- "CSRF token missing"

## Quick Fixes

### Fix 1: Force Re-login

```javascript
// In browser console
fetch('http://127.0.0.1:8000/users/logout/', {
  method: 'POST',
  credentials: 'include'
})
  .then(() => window.location.href = '/login')
```

### Fix 2: Clear All Cookies

```javascript
// In browser console
document.cookie.split(";").forEach(c => {
  document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
});
window.location.reload();
```

### Fix 3: Check Backend Logs

Look at Django console output for:
- Authentication errors
- CSRF errors
- Session errors

## Prevention

### For Users:
1. **Stay logged in**: Don't clear cookies unnecessarily
2. **Use same browser**: Don't switch browsers mid-session
3. **Check login status**: Look at navbar before using protected features

### For Developers:
1. **Handle 401 gracefully**: Show user-friendly messages
2. **Redirect to login**: Automatically redirect on 401
3. **Check auth before API calls**: Verify user is logged in first

## Still Having Issues?

1. **Check Django logs**: Look for authentication errors
2. **Check browser console**: Look for detailed error messages
3. **Verify CORS**: Make sure CORS is configured correctly
4. **Test with curl**: Test API directly to isolate frontend issues

```bash
# Test authentication with curl
curl -X GET http://127.0.0.1:8000/api/users/me/ \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -v
```

## Summary

**Most Common Fix**: Just log in! The 401 error usually means you need to authenticate first.

**If still not working**: Clear cookies, restart backend, and log in again.

