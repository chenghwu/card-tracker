# Environment Variables Reference

Complete guide to all environment variables used in the Credit Card Benefits Tracker.

---

## Table of Contents

1. [Backend Variables (Django)](#backend-variables-django)
2. [Frontend Variables (Next.js)](#frontend-variables-nextjs)
3. [How to Generate Secrets](#how-to-generate-secrets)
4. [OAuth Setup](#oauth-setup)
5. [Environment-Specific Configs](#environment-specific-configs)

---

## Backend Variables (Django)

Location: `backend/.env`

### Core Django Settings

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Django secret key for cryptography | `django-insecure-...` | ✅ Yes |
| `DEBUG` | Enable debug mode (NEVER true in production) | `False` | ✅ Yes |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `localhost,myapp.onrender.com` | ✅ Yes |

**Generate SECRET_KEY**:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

### Database Configuration

**Option A: DATABASE_URL (Recommended)**

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db?sslmode=require` | ✅ Yes (prod) |

**Option B: Individual Parameters**

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `DB_NAME` | Database name | `postgres` | ✅ Yes (if not using DATABASE_URL) |
| `DB_USER` | Database user | `postgres.xxxxx` | ✅ Yes |
| `DB_PASSWORD` | Database password | `your-supabase-password` | ✅ Yes |
| `DB_HOST` | Database host | `aws-0-us-west-1.pooler.supabase.com` | ✅ Yes |
| `DB_PORT` | Database port | `6543` (Supabase pooler) or `5432` | ✅ Yes |

**Supabase Example**:
```env
DATABASE_URL=postgresql://postgres.abcdefghij:mypassword@aws-0-us-west-1.pooler.supabase.com:6543/postgres?sslmode=require
```

---

### CORS Configuration

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `CORS_ALLOWED_ORIGINS` | Comma-separated frontend URLs | `http://localhost:3000,https://myapp.vercel.app` | ✅ Yes |

**Development**:
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Production**:
```env
CORS_ALLOWED_ORIGINS=https://myapp.vercel.app
```

**Both**:
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://myapp.vercel.app
```

---

### Google OAuth

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `GOOGLE_CLIENT_ID` | Google OAuth 2.0 Client ID | `123456789-abc.apps.googleusercontent.com` | Optional |
| `GOOGLE_CLIENT_SECRET` | Google OAuth 2.0 Client Secret | `GOCSPX-...` | Optional |

**Where to get**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable OAuth
3. Create OAuth 2.0 Client ID (Web application)
4. Add redirect URIs:
   - `http://localhost:8000/accounts/google/login/callback/` (dev)
   - `https://your-backend.onrender.com/accounts/google/login/callback/` (prod)

---

### Apple OAuth (Optional)

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `APPLE_CLIENT_ID` | Apple Service ID | `com.yourcompany.cardtracker` | Optional |
| `APPLE_CLIENT_SECRET` | Apple Client Secret (JWT) | `eyJhbGciOi...` | Optional |

**Where to get**:
1. Go to [Apple Developer Portal](https://developer.apple.com/)
2. Create App ID and Service ID
3. Configure Sign in with Apple
4. Generate JWT secret (requires private key)

---

### Gemini AI (Optional)

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | `AIzaSy...` | Optional |

**Where to get**:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key
3. Free tier: 60 requests/minute

**Used for**: Auto-populating unknown card benefits via AI lookup.

---

### Email Configuration (Optional)

For production email (password reset, notifications):

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `EMAIL_HOST` | SMTP server | `smtp.gmail.com` | Optional |
| `EMAIL_PORT` | SMTP port | `587` | Optional |
| `EMAIL_HOST_USER` | SMTP username | `your-email@gmail.com` | Optional |
| `EMAIL_HOST_PASSWORD` | SMTP password | App-specific password | Optional |

**Gmail Setup**:
1. Enable 2-factor authentication
2. Generate [App Password](https://myaccount.google.com/apppasswords)
3. Use app password (not your regular password)

---

## Frontend Variables (Next.js)

Location: `frontend/.env.local` (development) or Vercel Environment Variables (production)

### API Configuration

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000/api` (dev)<br>`https://backend.onrender.com/api` (prod) | ✅ Yes |

**Important**: `NEXT_PUBLIC_` prefix makes it available to browser (client-side).

---

### NextAuth.js Configuration

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `NEXTAUTH_URL` | Canonical URL of your app | `http://localhost:3000` (dev)<br>`https://myapp.vercel.app` (prod) | ✅ Yes |
| `NEXTAUTH_SECRET` | Secret for JWT encryption | Random 32-character string | ✅ Yes |

**Generate NEXTAUTH_SECRET**:
```bash
openssl rand -base64 32
```

---

### Google OAuth (Frontend)

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `GOOGLE_CLIENT_ID` | Same as backend | `123456789-abc.apps.googleusercontent.com` | Optional |
| `GOOGLE_CLIENT_SECRET` | Same as backend | `GOCSPX-...` | Optional |

**Must match** backend configuration. Add redirect URI:
- `http://localhost:3000/api/auth/callback/google` (dev)
- `https://myapp.vercel.app/api/auth/callback/google` (prod)

---

### Apple OAuth (Frontend)

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `APPLE_CLIENT_ID` | Same as backend | `com.yourcompany.cardtracker` | Optional |
| `APPLE_CLIENT_SECRET` | Same as backend | JWT token | Optional |

**Must match** backend configuration. Add redirect URI:
- `http://localhost:3000/api/auth/callback/apple` (dev)
- `https://myapp.vercel.app/api/auth/callback/apple` (prod)

---

## How to Generate Secrets

### Django SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### NEXTAUTH_SECRET

```bash
openssl rand -base64 32
```

### Or use Render/Vercel auto-generation

Both Render and Vercel can auto-generate secrets when you create environment variables.

---

## OAuth Setup

### Google OAuth Configuration

#### Step 1: Create Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Project name: `Card Tracker`

#### Step 2: Enable OAuth

1. Go to **APIs & Services** → **OAuth consent screen**
2. User Type: **External** (unless you have Google Workspace)
3. Fill in:
   - **App name**: Credit Card Benefits Tracker
   - **User support email**: Your email
   - **Developer contact**: Your email
4. Scopes: Add `email`, `profile`, `openid`
5. Test users: Add your email (for development)

#### Step 3: Create Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth 2.0 Client ID**
3. Application type: **Web application**
4. Name: `Card Tracker Web`
5. **Authorized redirect URIs**:
   ```
   http://localhost:3000/api/auth/callback/google
   http://localhost:8000/accounts/google/login/callback/
   https://your-frontend.vercel.app/api/auth/callback/google
   https://your-backend.onrender.com/accounts/google/login/callback/
   ```
6. Click **Create**
7. Copy **Client ID** and **Client Secret**

#### Step 4: Add to Environment Variables

**Backend** (`backend/.env`):
```env
GOOGLE_CLIENT_ID=123456789-abc.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnop
```

**Frontend** (`frontend/.env.local` or Vercel):
```env
GOOGLE_CLIENT_ID=123456789-abc.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnop
```

---

### Apple OAuth Configuration (Optional)

Apple OAuth is more complex and requires:
- Apple Developer Account ($99/year)
- App ID
- Service ID
- Private key for JWT signing

**Steps**:
1. [Apple Developer Portal](https://developer.apple.com/)
2. Create App ID
3. Create Service ID
4. Enable "Sign in with Apple"
5. Configure redirect URIs
6. Download private key
7. Generate JWT client secret

**Due to complexity**, consider implementing only Google OAuth initially.

---

## Environment-Specific Configs

### Local Development

**Backend** (`backend/.env`):
```env
SECRET_KEY=django-insecure-local-dev-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Use SQLite (no database config needed)
# Or use Supabase for testing

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

GEMINI_API_KEY=your-gemini-api-key
```

**Frontend** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api

NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-local-secret

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

---

### Production (Render + Vercel)

**Backend** (Render Environment Variables):
```env
SECRET_KEY=<auto-generated-by-render>
DEBUG=False
ALLOWED_HOSTS=card-tracker-backend.onrender.com

DATABASE_URL=postgresql://postgres.xxx:pass@aws-0-us-west-1.pooler.supabase.com:6543/postgres?sslmode=require

CORS_ALLOWED_ORIGINS=https://card-tracker-frontend.vercel.app

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

GEMINI_API_KEY=your-gemini-api-key
```

**Frontend** (Vercel Environment Variables):
```env
NEXT_PUBLIC_API_URL=https://card-tracker-backend.onrender.com/api

NEXTAUTH_URL=https://card-tracker-frontend.vercel.app
NEXTAUTH_SECRET=<auto-generated-by-vercel>

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

---

## Security Best Practices

### 1. Never Commit Secrets

Add to `.gitignore`:
```
# Environment files
.env
.env.local
.env.production
*.env
```

### 2. Use Different Secrets for Each Environment

- **Development**: Simple, memorable secrets
- **Production**: Strong, auto-generated secrets

### 3. Rotate Secrets Regularly

Change production secrets every 90 days:
1. Generate new secret
2. Update in Render/Vercel
3. Redeploy
4. Invalidate old secret

### 4. Restrict OAuth Scopes

Only request necessary permissions:
- ✅ `email`, `profile`, `openid`
- ❌ Don't request calendar, drive, etc.

### 5. Use Environment-Specific OAuth Credentials

Consider separate OAuth apps for dev vs. prod:
- `Card Tracker (Development)`
- `Card Tracker (Production)`

---

## Troubleshooting

### "Environment variable not found"

**Cause**: Variable not set or typo

**Solution**:
1. Check variable name matches exactly (case-sensitive)
2. For Next.js public vars, ensure `NEXT_PUBLIC_` prefix
3. For Vercel, redeploy after adding variables

### "CORS policy: No 'Access-Control-Allow-Origin' header"

**Cause**: Frontend URL not in `CORS_ALLOWED_ORIGINS`

**Solution**:
1. Add frontend URL to backend's `CORS_ALLOWED_ORIGINS`
2. Include protocol (`https://`) and no trailing slash
3. Redeploy backend

### "Invalid OAuth redirect URI"

**Cause**: OAuth provider doesn't have your URL

**Solution**:
1. Add all redirect URIs to Google/Apple OAuth app
2. Format: `https://domain.com/api/auth/callback/google`
3. Include both frontend and backend URLs

### Database connection fails

**Cause**: `DATABASE_URL` is malformed or Supabase credentials wrong

**Solution**:
1. Copy `DATABASE_URL` directly from Supabase dashboard
2. Ensure `?sslmode=require` is appended
3. Use port `6543` (pooler) not `5432`

---

## Quick Reference

### Backend .env Template

```env
# Core
SECRET_KEY=your-django-secret-key
DEBUG=False
ALLOWED_HOSTS=your-backend.onrender.com

# Database
DATABASE_URL=postgresql://user:pass@host:6543/postgres?sslmode=require

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app

# OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Optional
GEMINI_API_KEY=your-gemini-api-key
```

### Frontend .env Template

```env
# API
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api

# Auth
NEXTAUTH_URL=https://your-frontend.vercel.app
NEXTAUTH_SECRET=your-nextauth-secret

# OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

---

## Resources

- [Django Settings Reference](https://docs.djangoproject.com/en/5.0/ref/settings/)
- [Next.js Environment Variables](https://nextjs.org/docs/basic-features/environment-variables)
- [Google OAuth Setup](https://developers.google.com/identity/protocols/oauth2)
- [Supabase Connection Strings](https://supabase.com/docs/guides/database/connecting-to-postgres)
