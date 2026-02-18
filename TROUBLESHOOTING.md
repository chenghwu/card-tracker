# Troubleshooting Guide

Common issues and solutions for deploying and running the Credit Card Benefits Tracker.

---

## Table of Contents

1. [Backend Issues (Render)](#backend-issues-render)
2. [Frontend Issues (Vercel)](#frontend-issues-vercel)
3. [Database Issues (Supabase)](#database-issues-supabase)
4. [CORS Errors](#cors-errors)
5. [OAuth Issues](#oauth-issues)
6. [Performance Issues](#performance-issues)
7. [Environment Variable Issues](#environment-variable-issues)

---

## Backend Issues (Render)

### Build Fails: "ModuleNotFoundError: No module named 'X'"

**Symptom**: Render build logs show import error.

**Cause**: Missing dependency in `requirements.txt`.

**Solution**:
1. Add missing package to `requirements.txt`:
   ```txt
   packagename==1.0.0
   ```
2. Commit and push:
   ```bash
   git add backend/requirements.txt
   git commit -m "Add missing dependency"
   git push
   ```
3. Render will auto-redeploy.

---

### Build Fails: "Permission denied: './build.sh'"

**Symptom**: Build script not executable.

**Cause**: `build.sh` doesn't have execute permissions.

**Solution**:
```bash
chmod +x backend/build.sh
git add backend/build.sh
git commit -m "Make build script executable"
git push
```

---

### Service Won't Start: "Application startup failed"

**Symptom**: Render shows "Live" but health check fails or immediate restart loop.

**Cause**: Python error in `settings.py` or `wsgi.py`.

**Solution**:
1. Check Render **Logs** tab
2. Look for Python tracebacks
3. Common causes:
   - Missing `SECRET_KEY` env var
   - Database connection failed
   - Import error
   - Syntax error

**Check locally**:
```bash
cd backend
gunicorn card_tracker.wsgi:application --bind 127.0.0.1:8000
```

---

### Health Check Failing

**Symptom**: Render shows "Service Unhealthy" or frequent restarts.

**Cause**: `/api/health/` endpoint not responding.

**Solution**:

1. Verify health check endpoint exists:
   ```python
   # cards/views.py
   @api_view(['GET'])
   @permission_classes([AllowAny])
   def health_check(request):
       return Response({"status": "ok"})
   ```

2. Verify URL routing:
   ```python
   # card_tracker/urls.py
   urlpatterns = [
       path('api/health/', health_check),
       # ...
   ]
   ```

3. Test manually:
   ```bash
   curl https://your-backend.onrender.com/api/health/
   ```

---

### "This site can't be reached"

**Symptom**: Backend URL returns connection timeout.

**Cause**: Service is sleeping (Render free tier sleeps after 15 minutes of inactivity).

**Solution**:
- **Wait 30-60 seconds** for cold start (first request wakes it up)
- Set up uptime monitor (UptimeRobot) to ping every 10 minutes
- Upgrade to Render Starter plan ($7/month) for no sleep

---

## Frontend Issues (Vercel)

### Build Fails: "Type error: Cannot find module 'X'"

**Symptom**: Vercel build logs show TypeScript error.

**Cause**: Missing dependency or incorrect import.

**Solution**:
1. Check build locally:
   ```bash
   cd frontend
   npm run build
   ```
2. Fix TypeScript errors
3. Ensure all dependencies in `package.json`
4. Commit and push

---

### Build Fails: "NEXT_PUBLIC_API_URL is not defined"

**Symptom**: Build fails with environment variable error.

**Cause**: Required env var not set in Vercel.

**Solution**:
1. Go to Vercel dashboard → Project Settings → Environment Variables
2. Add `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api`
3. **Redeploy** (go to Deployments → Redeploy)

---

### Page Loads But Shows Blank Screen

**Symptom**: Frontend loads but nothing renders, console shows React errors.

**Cause**: Runtime JavaScript error.

**Solution**:
1. Check browser console for errors
2. Check Vercel **Functions** logs (for server-side errors)
3. Common causes:
   - Undefined variable
   - API request failing
   - Invalid data format

---

### "Hydration failed" Error

**Symptom**: React error about server/client mismatch.

**Cause**: Server-rendered HTML doesn't match client-rendered HTML.

**Solution**:
- Don't use browser-only APIs during SSR (e.g., `localStorage`, `window`)
- Use `useEffect` for client-only code:
  ```tsx
  useEffect(() => {
    // Safe to use window here
    const token = localStorage.getItem('token');
  }, []);
  ```

---

## Database Issues (Supabase)

### "FATAL: no pg_hba.conf entry for host"

**Symptom**: Backend can't connect to Supabase.

**Cause**: SSL not enabled or wrong connection settings.

**Solution**:

**Option 1**: Add `?sslmode=require` to `DATABASE_URL`:
```env
DATABASE_URL=postgresql://user:pass@host:6543/postgres?sslmode=require
```

**Option 2**: Update `settings.py`:
```python
DATABASES = {
    'default': {
        # ...
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}
```

---

### "FATAL: remaining connection slots are reserved"

**Symptom**: "Too many connections" error.

**Cause**: Hitting Supabase connection limit on free tier.

**Solution**:
1. **Use connection pooler**: Port **6543** (not 5432)
   ```
   postgresql://user:pass@host:6543/postgres
   ```
2. Set connection lifetime in Django:
   ```python
   DATABASES = {
       'default': dj_database_url.parse(
           DATABASE_URL,
           conn_max_age=600  # Reuse connections for 10 minutes
       )
   }
   ```
3. Reduce Gunicorn workers (in Render start command):
   ```
   gunicorn card_tracker.wsgi:application --workers 2 --bind 0.0.0.0:$PORT
   ```

---

### "could not connect to server: Operation timed out"

**Symptom**: Timeout when connecting to database.

**Cause**: Network issue or Supabase project paused.

**Solution**:
1. Check Supabase dashboard - **free tier pauses after 7 days of inactivity**
2. If paused, click project to wake it up (takes 1-2 minutes)
3. Verify `DATABASE_URL` is correct
4. Test connection locally:
   ```bash
   psql "postgresql://user:pass@host:6543/postgres?sslmode=require"
   ```

---

### Migrations Fail: "relation already exists"

**Symptom**: `python manage.py migrate` fails with duplicate table error.

**Cause**: Database state doesn't match migration history.

**Solution**:

**Option 1 - Fake migrations** (if tables already exist):
```bash
python manage.py migrate --fake
```

**Option 2 - Reset migrations** (DESTRUCTIVE - loses all data):
```bash
# Drop all tables
python manage.py flush

# Re-run migrations
python manage.py migrate
```

**Option 3 - Fresh database**:
1. Create new Supabase project
2. Update `DATABASE_URL`
3. Run migrations

---

## CORS Errors

### "Access-Control-Allow-Origin header is missing"

**Symptom**: Browser console shows CORS error when calling API.

**Cause**: Backend doesn't allow frontend domain.

**Solution**:

1. Update backend `CORS_ALLOWED_ORIGINS`:
   ```env
   # Render environment variable
   CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
   ```

2. Include protocol (`https://`) and NO trailing slash

3. For multiple domains (dev + prod):
   ```env
   CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
   ```

4. **Redeploy backend** (Render auto-redeploys when env vars change)

---

### CORS Error Only on Production, Not Local

**Symptom**: CORS works locally but not in production.

**Cause**: `CORS_ALLOWED_ORIGINS` doesn't include production frontend URL.

**Solution**:
1. Check exact Vercel URL (with `https://`)
2. Update Render env var: `CORS_ALLOWED_ORIGINS=https://exact-vercel-url.vercel.app`
3. Wait for redeploy

**Debug**: Check backend response headers in browser DevTools → Network:
```
Access-Control-Allow-Origin: https://your-frontend.vercel.app
```

---

### "Request header field X-Requested-With is not allowed"

**Symptom**: Custom headers blocked by CORS.

**Cause**: `CORS_ALLOW_HEADERS` doesn't include custom headers.

**Solution**: Add to `settings.py`:
```python
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-custom-header',  # Add your custom headers
]
```

---

## OAuth Issues

### "redirect_uri_mismatch"

**Symptom**: Google/Apple OAuth shows error after clicking "Sign in".

**Cause**: Redirect URI not whitelisted in OAuth provider.

**Solution**:

**Google**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Credentials
2. Click your OAuth 2.0 Client ID
3. Add **Authorized redirect URIs**:
   ```
   https://your-frontend.vercel.app/api/auth/callback/google
   https://your-backend.onrender.com/accounts/google/login/callback/
   ```
4. Save

**Apple**:
1. Go to [Apple Developer Portal](https://developer.apple.com/)
2. Certificates, Identifiers & Profiles → Identifiers
3. Select your Service ID
4. Add **Return URLs**:
   ```
   https://your-frontend.vercel.app/api/auth/callback/apple
   https://your-backend.onrender.com/accounts/apple/login/callback/
   ```
5. Save

---

### OAuth Works Locally But Not in Production

**Symptom**: Sign in works on `localhost:3000` but fails on Vercel.

**Cause**: Production redirect URIs not added to OAuth app.

**Solution**:
1. Add production URLs to Google/Apple OAuth config (see above)
2. Verify env vars in Vercel match Google Console:
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`
3. **Redeploy frontend**

---

### "invalid_client" Error

**Symptom**: OAuth fails with "invalid_client".

**Cause**: Client ID or secret is wrong.

**Solution**:
1. Double-check `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in Render and Vercel
2. Ensure no extra spaces or line breaks
3. Verify client ID format:
   ```
   123456789-abcdefghijklmnop.apps.googleusercontent.com
   ```
4. Regenerate secret if needed (Google Console)

---

### "Access blocked: This app's request is invalid"

**Symptom**: Google consent screen shows error.

**Cause**: OAuth app not verified or redirect URI invalid.

**Solution**:
1. Go to Google Cloud Console → OAuth consent screen
2. Add yourself as a **Test user**
3. Or submit app for verification (required for >100 users)

---

## Performance Issues

### Backend First Request Takes 30+ Seconds

**Symptom**: Cold start delay on Render free tier.

**Cause**: Service sleeps after 15 minutes of inactivity.

**Solution**:
- **Expected behavior** on Render free tier
- **Keep alive**: Use UptimeRobot to ping `/api/health/` every 10 minutes
- **Upgrade**: Render Starter plan ($7/month) has no sleep
- **Optimize**: Reduce dependencies, lazy-load modules

---

### API Requests Slow (500ms+)

**Symptom**: API calls take 500-2000ms.

**Cause**: Database queries or N+1 problem.

**Solution**:
1. Enable Django Debug Toolbar locally:
   ```bash
   pip install django-debug-toolbar
   ```
2. Identify slow queries
3. Add database indexes:
   ```python
   class Meta:
       indexes = [
           models.Index(fields=['user', 'is_active']),
       ]
   ```
4. Use `select_related()` and `prefetch_related()`:
   ```python
   UserCard.objects.select_related('card_template').prefetch_related('benefits')
   ```

---

### Frontend Loads Slowly

**Symptom**: Page takes 3+ seconds to load.

**Cause**: Large bundle size or unnecessary re-renders.

**Solution**:
1. Analyze bundle size:
   ```bash
   npm run build
   # Check .next/analyze output
   ```
2. Code-split large components:
   ```tsx
   const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
     loading: () => <p>Loading...</p>,
   });
   ```
3. Optimize images (use Next.js `Image` component)
4. Lazy-load off-screen content

---

## Environment Variable Issues

### "Environment variable not found"

**Symptom**: Runtime error about missing env var.

**Cause**: Variable not set or typo.

**Solution**:

**Backend (Render)**:
1. Go to Render dashboard → Your service → Environment
2. Verify variable name (case-sensitive)
3. Click "Save Changes" (triggers redeploy)

**Frontend (Vercel)**:
1. Go to Vercel dashboard → Project Settings → Environment Variables
2. Add variable
3. **Must redeploy** after adding env vars (Vercel doesn't auto-redeploy)

---

### Changes to .env Not Reflected

**Symptom**: Updated env var but app still uses old value.

**Cause**: Env vars cached or not redeployed.

**Solution**:

**Local development**:
```bash
# Restart dev servers
# Backend
cd backend
python manage.py runserver

# Frontend
cd frontend
npm run dev
```

**Production**:
- Render: Auto-redeploys when env vars change (wait 2-3 minutes)
- Vercel: **Manual redeploy required** (go to Deployments → Redeploy)

---

### "NEXT_PUBLIC_API_URL is undefined"

**Symptom**: API calls fail with undefined URL.

**Cause**: Missing `NEXT_PUBLIC_` prefix or not set.

**Solution**:
1. Ensure variable starts with `NEXT_PUBLIC_`:
   ```env
   NEXT_PUBLIC_API_URL=https://backend.onrender.com/api
   ```
2. In Vercel, add to environment variables
3. **Redeploy** (env vars only apply to new builds)

---

## Common Error Messages

### "Mixed Content" Warning

**Symptom**: Browser blocks HTTP requests from HTTPS page.

**Cause**: Trying to call HTTP backend from HTTPS frontend.

**Solution**:
- Ensure `NEXT_PUBLIC_API_URL` uses `https://`:
  ```env
  NEXT_PUBLIC_API_URL=https://backend.onrender.com/api
  ```

---

### "Failed to fetch" or "Network error"

**Symptom**: API calls fail with generic network error.

**Possible Causes**:
1. **Backend down**: Check Render dashboard
2. **CORS error**: Check browser console for CORS message
3. **Wrong API URL**: Verify `NEXT_PUBLIC_API_URL`
4. **Cold start**: Wait 30 seconds and retry

**Debug**:
```bash
# Test backend directly
curl https://your-backend.onrender.com/api/health/

# Check from frontend
# Open browser console → Network tab → See failed request details
```

---

### "CSRF token missing or incorrect"

**Symptom**: POST/PUT/DELETE requests fail with 403.

**Cause**: CSRF protection enabled but token not sent.

**Solution**:

**Option 1**: Disable CSRF for API (if using JWT):
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# Exempt API endpoints from CSRF
from django.views.decorators.csrf import csrf_exempt
```

**Option 2**: Send CSRF token from frontend:
```tsx
// Get CSRF token from cookie
const csrfToken = document.cookie
  .split('; ')
  .find(row => row.startsWith('csrftoken='))
  ?.split('=')[1];

// Include in request headers
axios.post('/api/endpoint/', data, {
  headers: {
    'X-CSRFToken': csrfToken,
  },
});
```

---

## Getting Help

If you're still stuck:

1. **Check logs**:
   - Render: Dashboard → Logs
   - Vercel: Dashboard → Deployments → Click deployment → Logs
   - Browser: DevTools → Console + Network tabs

2. **Search errors**:
   - Copy exact error message
   - Search on Stack Overflow, GitHub Issues

3. **Community**:
   - [Django Forum](https://forum.djangoproject.com/)
   - [Next.js Discussions](https://github.com/vercel/next.js/discussions)
   - [Render Community](https://community.render.com/)

4. **Documentation**:
   - [Django Docs](https://docs.djangoproject.com/)
   - [Next.js Docs](https://nextjs.org/docs)
   - [Render Docs](https://render.com/docs)
   - [Vercel Docs](https://vercel.com/docs)

---

## Debug Checklist

When something isn't working:

- [ ] Check all logs (Render, Vercel, Browser console)
- [ ] Verify environment variables are set correctly
- [ ] Test backend API directly with `curl` or Postman
- [ ] Check network tab in browser DevTools
- [ ] Ensure services are deployed and running (not paused/asleep)
- [ ] Verify CORS settings
- [ ] Check OAuth redirect URIs match production URLs
- [ ] Try in incognito/private browsing (rules out cache issues)
- [ ] Compare working local setup vs production config

---

## Prevention Tips

- **Always test locally before deploying**
- **Use .env.example files** to document required variables
- **Version control**: Commit working state before major changes
- **Monitor logs** after each deployment
- **Set up alerts**: UptimeRobot, Sentry for error tracking
- **Document custom configurations** for future reference
