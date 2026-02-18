# Render Backend Deployment Guide

This guide walks you through deploying the Django REST API backend to Render (free tier).

## Why Render?

- **Free Tier**: $0/month for web services (with limitations)
- **Automatic Deploys**: Deploys on every git push
- **HTTPS Built-in**: Free SSL certificates
- **Persistent Storage**: Use external database (Supabase)
- **Easy Setup**: No Docker knowledge required

**Free Tier Limitations**:
- Services spin down after 15 minutes of inactivity
- Cold start takes ~30 seconds (first request after idle)
- 750 hours/month free (enough for 1 service)

---

## Prerequisites

Before you begin:

✅ Supabase database configured (see `DEPLOYMENT_SUPABASE.md`)
✅ Backend code pushed to GitHub
✅ GitHub account connected to Render

---

## Step 1: Prepare Backend for Production

### 1.1 Update `requirements.txt`

Ensure all production dependencies are included:

```bash
cd backend
```

Add/verify these dependencies in `requirements.txt`:

```txt
Django==5.0.1
djangorestframework==3.14.0
django-allauth==0.61.1
dj-rest-auth==5.0.2
djangorestframework-simplejwt==5.3.1
psycopg2-binary==2.9.9
python-decouple==3.8
django-cors-headers==4.3.1
gunicorn==21.2.0
dj-database-url==2.1.0
whitenoise==6.6.0
google-generativeai==0.3.2
```

### 1.2 Update `settings.py`

Add production settings. Edit `backend/card_tracker/settings.py`:

```python
import os
import dj_database_url
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=lambda v: [s.strip() for s in v.split(',')])

# Static files (WhiteNoise)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# WhiteNoise settings
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Database
DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)
    }
else:
    # Fallback to SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# CORS Configuration
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# Production Security Settings
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'
```

---

## Step 2: Create Build Script

Create `backend/build.sh`:

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Optional: Load seed data (uncomment for first deploy)
# python manage.py seed_cards
```

Make it executable:

```bash
chmod +x backend/build.sh
```

---

## Step 3: Create Render Blueprint (Optional)

Create `backend/render.yaml` for infrastructure-as-code:

```yaml
services:
  - type: web
    name: card-tracker-backend
    env: python
    region: oregon
    plan: free
    branch: main
    buildCommand: "./build.sh"
    startCommand: "gunicorn card_tracker.wsgi:application --bind 0.0.0.0:$PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: DATABASE_URL
        sync: false  # Set this manually from Supabase
      - key: ALLOWED_HOSTS
        sync: false  # Will be auto-filled with Render URL
      - key: CORS_ALLOWED_ORIGINS
        sync: false  # Add your Vercel frontend URL
      - key: GOOGLE_CLIENT_ID
        sync: false
      - key: GOOGLE_CLIENT_SECRET
        sync: false
      - key: GEMINI_API_KEY
        sync: false
```

---

## Step 4: Create Render Account

1. Go to [https://render.com](https://render.com)
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (recommended)
4. Authorize Render to access your repositories

---

## Step 5: Create New Web Service

### 5.1 Connect Repository

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository:
   - If not listed, click **"Configure account"** to grant access
3. Select your `card_tracker` repository
4. Click **"Connect"**

### 5.2 Configure Service

Fill in the form:

| Field | Value |
|-------|-------|
| **Name** | `card-tracker-backend` (or any unique name) |
| **Region** | Choose closest to you (e.g., Oregon) |
| **Branch** | `main` (or your default branch) |
| **Root Directory** | `backend` |
| **Environment** | `Python 3` |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn card_tracker.wsgi:application --bind 0.0.0.0:$PORT` |
| **Plan** | **Free** |

### 5.3 Advanced Settings (Click "Advanced")

**Environment Variables** - Add these:

```
SECRET_KEY=<click "Generate" to auto-generate>
DEBUG=False
ALLOWED_HOSTS=card-tracker-backend.onrender.com
DATABASE_URL=<your-supabase-connection-string>
CORS_ALLOWED_ORIGINS=https://your-app.vercel.app
GOOGLE_CLIENT_ID=<your-google-client-id>
GOOGLE_CLIENT_SECRET=<your-google-client-secret>
GEMINI_API_KEY=<your-gemini-api-key>
```

**Important Notes**:
- **ALLOWED_HOSTS**: Replace with your actual Render service URL (you'll see it after creation)
- **DATABASE_URL**: Copy from Supabase (see `DEPLOYMENT_SUPABASE.md`)
- **CORS_ALLOWED_ORIGINS**: Add your Vercel frontend URL (deploy frontend first, then update this)

### 5.4 Create Service

Click **"Create Web Service"**

Render will:
1. Clone your repository
2. Run `build.sh` (install deps, migrate DB, collect static files)
3. Start gunicorn server
4. Assign a URL: `https://card-tracker-backend.onrender.com`

**First deploy takes ~5 minutes**. Watch the logs in real-time.

---

## Step 6: Verify Deployment

### 6.1 Check Build Logs

You should see:
```
==> Installing dependencies...
Collecting Django==5.0.1...
Successfully installed Django-5.0.1 ...

==> Collecting static files...
Copying '/opt/render/...'
120 static files copied to '/opt/render/project/src/staticfiles'.

==> Running migrations...
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, cards
Running migrations:
  No migrations to apply.

==> Starting gunicorn...
[INFO] Listening at: http://0.0.0.0:10000
```

### 6.2 Test API Health Check

Visit your service URL:
```
https://card-tracker-backend.onrender.com/api/health/
```

Expected response:
```json
{
  "status": "ok",
  "database": "connected"
}
```

*(If you haven't added a health check endpoint, see Step 9)*

### 6.3 Test API Endpoints

```bash
# List card templates
curl https://card-tracker-backend.onrender.com/api/card-templates/

# Search cards
curl "https://card-tracker-backend.onrender.com/api/card-templates/?q=sapphire"
```

---

## Step 7: Update ALLOWED_HOSTS

After first deploy, update `ALLOWED_HOSTS`:

1. Go to Render dashboard → Your service → **Environment**
2. Edit `ALLOWED_HOSTS` variable:
   ```
   ALLOWED_HOSTS=card-tracker-backend.onrender.com
   ```
3. **Save Changes** (triggers auto-redeploy)

---

## Step 8: Load Seed Data (First Deploy Only)

If you didn't run `seed_cards` in `build.sh`:

1. Go to Render dashboard → Your service
2. Click **"Shell"** tab (opens interactive terminal)
3. Run:
   ```bash
   python manage.py seed_cards
   ```

Or add to `build.sh` and redeploy:
```bash
# In build.sh
python manage.py seed_cards
```

---

## Step 9: Add Health Check Endpoint (Recommended)

Create a simple health check for monitoring.

**File**: `backend/cards/views.py`

Add this view:
```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection

@api_view(['GET'])
@permission_classes([AllowAny])  # No auth required
def health_check(request):
    """Health check endpoint for monitoring"""
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return Response({
        "status": "ok",
        "database": db_status,
    })
```

**File**: `backend/card_tracker/urls.py`

Add to urlpatterns:
```python
from cards.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check),  # Add this
    path('api/', include('cards.urls')),
]
```

Commit and push to trigger auto-deploy.

---

## Step 10: Configure Custom Domain (Optional)

If you have a custom domain:

1. Go to **Settings** → **Custom Domain**
2. Click **"Add Custom Domain"**
3. Enter your domain: `api.yoursite.com`
4. Add CNAME record to your DNS:
   ```
   CNAME   api   card-tracker-backend.onrender.com
   ```
5. Wait for SSL certificate provisioning (~5 minutes)

---

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Auto-generated by Render |
| `DEBUG` | Debug mode (always False in prod) | `False` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `card-tracker-backend.onrender.com` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated frontend URLs | `https://yourapp.vercel.app` |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | Get from Google Console |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret | Get from Google Console |
| `GEMINI_API_KEY` | Gemini API key (optional) | Get from Google AI Studio |

---

## Auto-Deploy on Git Push

Render automatically deploys when you push to your branch:

```bash
git add .
git commit -m "Update API endpoints"
git push origin main
```

Watch deployment in Render dashboard **"Logs"** tab.

---

## Troubleshooting

### Build Fails: "ModuleNotFoundError"

**Cause**: Missing dependency in `requirements.txt`

**Solution**:
1. Add the missing package to `requirements.txt`
2. Commit and push
3. Render will auto-redeploy

### Service Won't Start: "Application startup failed"

**Cause**: Likely a `settings.py` error

**Solution**:
1. Check logs in Render dashboard
2. Look for Python tracebacks
3. Common issues:
   - Missing environment variable
   - Database connection failed
   - Import error

### Database Connection Failed

**Error**: `FATAL: no pg_hba.conf entry for host`

**Solution**:
- Verify `DATABASE_URL` in Render environment variables
- Ensure Supabase allows connections from Render IPs
- Check SSL settings: `ssl_require=True` in database config

### Static Files Not Loading

**Error**: 404 on `/static/admin/...`

**Solution**:
1. Verify `whitenoise` is installed
2. Check `build.sh` runs `collectstatic`
3. Ensure `WhiteNoiseMiddleware` is in `MIDDLEWARE`

### Cold Start Too Slow

**Issue**: First request after idle takes 30+ seconds

**Solutions**:
- **Upgrade to Starter Plan** ($7/month): No cold starts
- **Keep-alive ping**: Use a free uptime monitor (UptimeRobot) to ping every 10 minutes
- **Optimize startup**: Reduce dependencies, lazy-load modules

### "This site can't be reached"

**Cause**: Service might be asleep or crashed

**Solution**:
1. Check Render dashboard for service status
2. If sleeping, first request will wake it (wait 30 seconds)
3. If crashed, check logs for errors

---

## Monitoring & Maintenance

### 1. View Logs

Go to Render dashboard → Your service → **Logs**

Filter by:
- **Build Logs**: Deployment process
- **Deploy Logs**: Application startup
- **Application Logs**: Runtime logs (Django output)

### 2. Set Up Uptime Monitoring

Use [UptimeRobot](https://uptimerobot.com) (free tier):

1. Create a monitor
2. Monitor type: **HTTP(s)**
3. URL: `https://card-tracker-backend.onrender.com/api/health/`
4. Interval: **Every 10 minutes** (keeps service awake)
5. Get alerts if service goes down

### 3. Scale Up (If Needed)

Free tier limitations:
- 512 MB RAM
- 0.1 CPU
- Sleeps after 15 minutes inactivity

**Upgrade to Starter Plan ($7/month)**:
- 512 MB RAM (same)
- 0.5 CPU (5x faster)
- **No sleep** (always on)
- **Custom domain**

---

## Deployment Checklist

- [ ] `requirements.txt` includes all production dependencies
- [ ] `build.sh` created and executable
- [ ] `settings.py` configured for production (WhiteNoise, database, CORS)
- [ ] GitHub repository connected to Render
- [ ] Web service created on Render
- [ ] Environment variables configured
- [ ] First deployment successful
- [ ] Health check endpoint working
- [ ] API endpoints return expected responses
- [ ] Seed data loaded
- [ ] ALLOWED_HOSTS updated with Render URL
- [ ] CORS configured with frontend URL (after deploying frontend)

---

## Next Steps

✅ Backend deployed to Render
✅ API accessible via HTTPS
✅ Database connected to Supabase

**Continue to**: `DEPLOYMENT_VERCEL.md` to deploy your frontend.

**Then**: Update `CORS_ALLOWED_ORIGINS` in Render with your Vercel URL.

---

## Resources

- [Render Documentation](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)
