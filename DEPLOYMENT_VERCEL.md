# Vercel Frontend Deployment Guide

This guide walks you through deploying the Next.js frontend to Vercel (free tier).

## Why Vercel?

- **Free Tier**: $0/month for personal projects
- **Built for Next.js**: Created by Next.js team, optimized performance
- **Automatic Deploys**: Deploy on every git push
- **Edge Network**: Fast global CDN
- **Preview Deployments**: Every PR gets a preview URL
- **No Sleep**: Unlike Render, always instant (no cold starts)

**Free Tier Limits**:
- 100GB bandwidth/month
- 100 deployments/day
- More than enough for personal use

---

## Prerequisites

Before you begin:

✅ Backend deployed to Render (see `DEPLOYMENT_RENDER.md`)
✅ Frontend code pushed to GitHub
✅ Render backend URL available

---

## Step 1: Prepare Frontend for Production

### 1.1 Create Production Environment File

Create `frontend/.env.production.example`:

```env
# API Configuration
NEXT_PUBLIC_API_URL=https://card-tracker-backend.onrender.com/api

# NextAuth Configuration
NEXTAUTH_URL=https://your-app.vercel.app
NEXTAUTH_SECRET=your-nextauth-secret-change-this

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Apple OAuth (optional)
APPLE_CLIENT_ID=your-apple-client-id
APPLE_CLIENT_SECRET=your-apple-client-secret
```

### 1.2 Verify API Client Configuration

Ensure your API client uses `NEXT_PUBLIC_API_URL`.

**File**: `frontend/lib/api.ts` (or similar)

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### 1.3 Test Production Build Locally

```bash
cd frontend
npm run build
```

Expected output:
```
✓ Compiled successfully
✓ Linting and checking validity of types
✓ Collecting page data
✓ Generating static pages (5/5)
✓ Finalizing page optimization

Route (app)                              Size
┌ ○ /                                    1.2 kB
├ ○ /cards                               850 B
├ ○ /dashboard                           2.4 kB
└ ○ /login                               800 B
```

If build succeeds, you're ready to deploy!

---

## Step 2: Create Vercel Account

1. Go to [https://vercel.com](https://vercel.com)
2. Click **"Sign Up"**
3. Sign up with **GitHub** (recommended)
4. Authorize Vercel to access your repositories

---

## Step 3: Import Project

### 3.1 Connect Repository

1. Click **"Add New..."** → **"Project"**
2. Select **"Import Git Repository"**
3. Find your `card_tracker` repository
4. Click **"Import"**

### 3.2 Configure Project

Fill in the form:

| Field | Value |
|-------|-------|
| **Framework Preset** | `Next.js` (auto-detected) |
| **Root Directory** | `frontend` ⚠️ **Important**: Click "Edit" and set this |
| **Build Command** | `npm run build` (default) |
| **Output Directory** | `.next` (default) |
| **Install Command** | `npm install` (default) |

### 3.3 Environment Variables

Click **"Environment Variables"** and add these:

**Required Variables:**

```
NEXT_PUBLIC_API_URL=https://card-tracker-backend.onrender.com/api
NEXTAUTH_URL=https://your-app.vercel.app
NEXTAUTH_SECRET=<click "Generate" or use: openssl rand -base64 32>
```

**OAuth Variables (if configured):**

```
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
APPLE_CLIENT_ID=your-apple-client-id
APPLE_CLIENT_SECRET=your-apple-client-secret
```

**Important Notes**:
- **NEXT_PUBLIC_API_URL**: Use your Render backend URL
- **NEXTAUTH_URL**: Will be updated after first deploy with actual Vercel URL
- **NEXTAUTH_SECRET**: Generate with `openssl rand -base64 32` or use Vercel's generator

### 3.4 Deploy

Click **"Deploy"**

Vercel will:
1. Clone your repository
2. Install dependencies (`npm install`)
3. Build the project (`npm run build`)
4. Deploy to global edge network
5. Assign a URL: `https://card-tracker-frontend.vercel.app`

**First deploy takes ~2 minutes**. Watch the build logs in real-time.

---

## Step 4: Update NEXTAUTH_URL

After first deploy:

1. Copy your Vercel URL (e.g., `https://card-tracker-frontend.vercel.app`)
2. Go to **Project Settings** → **Environment Variables**
3. Edit `NEXTAUTH_URL` variable:
   ```
   NEXTAUTH_URL=https://card-tracker-frontend.vercel.app
   ```
4. Click **"Save"**
5. Go to **Deployments** tab
6. Click **"Redeploy"** on the latest deployment

---

## Step 5: Update Backend CORS Settings

Now that frontend is deployed, update backend to allow requests:

1. Go to Render dashboard → Your backend service
2. Go to **Environment** tab
3. Edit `CORS_ALLOWED_ORIGINS`:
   ```
   CORS_ALLOWED_ORIGINS=https://card-tracker-frontend.vercel.app
   ```
4. Click **"Save Changes"** (triggers auto-redeploy)

**For multiple domains** (development + production):
```
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://card-tracker-frontend.vercel.app
```

---

## Step 6: Configure OAuth Providers

### 6.1 Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create new one)
3. Go to **APIs & Services** → **Credentials**
4. Click existing OAuth 2.0 Client ID (or create new)
5. Add **Authorized redirect URIs**:
   ```
   https://card-tracker-frontend.vercel.app/api/auth/callback/google
   https://card-tracker-backend.onrender.com/accounts/google/login/callback/
   ```
6. Save changes

### 6.2 Apple OAuth Setup (Optional)

1. Go to [Apple Developer Portal](https://developer.apple.com/)
2. Go to **Certificates, Identifiers & Profiles**
3. Select your Service ID
4. Add **Return URLs**:
   ```
   https://card-tracker-frontend.vercel.app/api/auth/callback/apple
   https://card-tracker-backend.onrender.com/accounts/apple/login/callback/
   ```
5. Save changes

---

## Step 7: Verify Deployment

### 7.1 Visit Your Site

Open: `https://card-tracker-frontend.vercel.app`

You should see your landing page with no errors.

### 7.2 Test API Connection

Open browser console and check for:
- ✅ No CORS errors
- ✅ API requests to backend succeed
- ✅ 401/403 responses for protected endpoints (expected before login)

### 7.3 Test Authentication Flow

1. Click **"Sign In"**
2. Try Google OAuth login
3. Should redirect to Google → back to your app
4. Check that JWT token is stored

### 7.4 Test Full User Flow

1. Log in
2. Add a card
3. Record benefit usage
4. View dashboard

If all works, deployment is successful!

---

## Step 8: Configure Custom Domain (Optional)

If you have a custom domain:

### 8.1 Add Domain in Vercel

1. Go to **Project Settings** → **Domains**
2. Click **"Add"**
3. Enter your domain: `cards.yoursite.com`
4. Vercel will show DNS records to add

### 8.2 Update DNS Records

Add these records to your DNS provider:

**Option A: CNAME (Subdomain)**
```
Type    Name    Value
CNAME   cards   cname.vercel-dns.com
```

**Option B: A Record (Apex Domain)**
```
Type    Name    Value
A       @       76.76.21.21
```

### 8.3 Wait for SSL

Vercel automatically provisions SSL certificates (~5 minutes).

### 8.4 Update Environment Variables

Update `NEXTAUTH_URL` to use your custom domain:
```
NEXTAUTH_URL=https://cards.yoursite.com
```

And update backend CORS:
```
CORS_ALLOWED_ORIGINS=https://cards.yoursite.com
```

Redeploy both services.

---

## Environment Variables Reference

| Variable | Description | Example | Scope |
|----------|-------------|---------|-------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `https://backend.onrender.com/api` | Public (client-side) |
| `NEXTAUTH_URL` | Frontend canonical URL | `https://yourapp.vercel.app` | Server-only |
| `NEXTAUTH_SECRET` | NextAuth.js encryption secret | Random 32-char string | Server-only |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | Get from Google Console | Server-only |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret | Get from Google Console | Server-only |
| `APPLE_CLIENT_ID` | Apple OAuth client ID | Get from Apple Developer | Server-only |
| `APPLE_CLIENT_SECRET` | Apple OAuth secret | Get from Apple Developer | Server-only |

**Important**:
- Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser
- Other variables are server-only (not exposed)

---

## Auto-Deploy on Git Push

Vercel automatically deploys when you push to your branch:

```bash
git add .
git commit -m "Update dashboard UI"
git push origin main
```

**Production Deployment**: Triggered by pushes to `main` branch

**Preview Deployments**: Every PR gets a unique preview URL (e.g., `card-tracker-git-feature-branch.vercel.app`)

### Disable Auto-Deploy (Optional)

If you want manual control:

1. Go to **Project Settings** → **Git**
2. Toggle off **"Production Branch"** or **"Preview Deployments"**

---

## Preview Deployments

Every pull request gets a preview deployment:

1. Create a new branch:
   ```bash
   git checkout -b feature/new-dashboard
   ```

2. Make changes and push:
   ```bash
   git add .
   git commit -m "New dashboard design"
   git push origin feature/new-dashboard
   ```

3. Create a PR on GitHub

4. Vercel automatically:
   - Builds the PR branch
   - Creates a preview URL: `https://card-tracker-git-feature-new-dashboard.vercel.app`
   - Comments on the PR with the preview link

5. Test the preview before merging

---

## Troubleshooting

### Build Fails: "Module not found"

**Cause**: Missing dependency

**Solution**:
1. Check `package.json` has all dependencies
2. Run `npm install` locally to verify
3. Commit and push `package-lock.json`

### "NEXT_PUBLIC_API_URL is not defined"

**Cause**: Environment variable not set

**Solution**:
1. Go to **Project Settings** → **Environment Variables**
2. Verify `NEXT_PUBLIC_API_URL` is set
3. Redeploy

### CORS Error: "Access-Control-Allow-Origin"

**Cause**: Backend doesn't allow your frontend domain

**Solution**:
1. Update `CORS_ALLOWED_ORIGINS` in Render
2. Include your Vercel URL
3. Redeploy backend

### OAuth Redirect URL Mismatch

**Error**: `redirect_uri_mismatch`

**Cause**: OAuth provider doesn't have your Vercel URL

**Solution**:
1. Add Vercel URL to Google/Apple OAuth allowed redirect URIs
2. Format: `https://your-app.vercel.app/api/auth/callback/google`

### 404 on API Requests

**Cause**: `NEXT_PUBLIC_API_URL` is incorrect

**Solution**:
1. Verify Render backend URL is correct
2. Ensure URL ends with `/api` (no trailing slash)
3. Test backend URL in browser first

### Slow Page Loads

**Issue**: Pages take 10+ seconds to load

**Cause**: Backend cold start on Render free tier

**Solutions**:
- **Keep backend warm**: Use UptimeRobot to ping every 10 minutes
- **Upgrade backend**: Render Starter plan ($7/month) has no cold starts
- **Loading states**: Add skeleton loaders to improve UX

---

## Performance Optimization

### 1. Enable Image Optimization

Vercel automatically optimizes images. Use Next.js `Image` component:

```tsx
import Image from 'next/image';

<Image
  src="/card-image.png"
  alt="Card"
  width={300}
  height={200}
/>
```

### 2. Static Generation

Use `generateStaticParams` for public pages:

```tsx
// app/cards/[id]/page.tsx
export async function generateStaticParams() {
  const cards = await fetchPopularCards();
  return cards.map((card) => ({ id: card.id }));
}
```

### 3. Edge Middleware

Use Edge Middleware for auth checks (ultra-fast):

```tsx
// middleware.ts
import { NextResponse } from 'next/server';

export function middleware(request) {
  // Auth logic here
}

export const config = {
  matcher: ['/dashboard/:path*', '/cards/:path*'],
};
```

### 4. Analytics

Enable Vercel Analytics (free):

1. Go to **Project Settings** → **Analytics**
2. Click **"Enable"**
3. Adds performance tracking with zero config

---

## Monitoring

### 1. View Deployment Logs

Go to **Deployments** → Click deployment → View **Build Logs** and **Function Logs**

### 2. Check Performance

**Vercel Analytics Dashboard**:
- Page load times
- Core Web Vitals
- Real user data

**Vercel Speed Insights**:
- Identifies slow pages
- Optimization suggestions

### 3. Error Tracking (Optional)

Integrate Sentry for error monitoring:

```bash
npm install @sentry/nextjs
```

Add to `next.config.ts`:
```typescript
const { withSentryConfig } = require('@sentry/nextjs');

module.exports = withSentryConfig(nextConfig, {
  // Sentry config
});
```

---

## Deployment Checklist

- [ ] `frontend/.env.production.example` created
- [ ] API client uses `NEXT_PUBLIC_API_URL`
- [ ] Local production build succeeds (`npm run build`)
- [ ] Vercel account created and GitHub connected
- [ ] Project imported with correct root directory (`frontend`)
- [ ] Environment variables configured
- [ ] First deployment successful
- [ ] `NEXTAUTH_URL` updated with actual Vercel URL
- [ ] Backend CORS updated with Vercel URL
- [ ] OAuth providers configured with Vercel redirect URIs
- [ ] Login flow tested and working
- [ ] Full user flow tested (add card, track usage, view dashboard)

---

## Cost & Scaling

**Free Tier Limits**:
- **Bandwidth**: 100GB/month
- **Builds**: 100 deployments/day (6,000 build minutes/month)
- **Serverless Function Execution**: 100GB-hours
- **Edge Middleware**: Unlimited

**Estimations** (personal use):
- **Monthly Visits**: ~1,000 users = ~10GB bandwidth
- **Builds**: ~5-10 per day = well under limit

**Upgrade to Pro ($20/month)** if you need:
- 1TB bandwidth
- Unlimited team members
- Password-protected deployments
- Advanced analytics

---

## Next Steps

✅ Frontend deployed to Vercel
✅ Backend and frontend connected
✅ OAuth configured
✅ Full app accessible via HTTPS

**Continue to**:
- `ENVIRONMENT_VARIABLES.md` - Complete reference of all env vars
- `DEPLOYMENT_CHECKLIST.md` - Final deployment verification
- `OPERATIONS.md` - Day-to-day operations and monitoring

---

## Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment Guide](https://nextjs.org/docs/deployment)
- [Environment Variables in Next.js](https://nextjs.org/docs/basic-features/environment-variables)
