# Deployment Checklist

Use this checklist to ensure successful deployment of the Credit Card Benefits Tracker to production.

---

## Pre-Deployment Preparation

### Code Quality
- [ ] All tests passing locally (`pytest` for backend, `npm test` for frontend)
- [ ] No console errors in development
- [ ] Code linted and formatted
- [ ] Git working tree clean (all changes committed)
- [ ] Main/master branch up to date

### Documentation
- [ ] `README.md` updated with project info
- [ ] API endpoints documented
- [ ] Environment variables documented
- [ ] Deployment guides reviewed

---

## Phase 1: Database Setup (Supabase)

See: `DEPLOYMENT_SUPABASE.md`

- [ ] Supabase account created
- [ ] New project created (name: `card-tracker`)
- [ ] Database password saved securely
- [ ] Connection string copied (use port 6543 for pooler)
- [ ] Connection string added to password manager
- [ ] `dj-database-url` added to `requirements.txt`
- [ ] `settings.py` updated to support `DATABASE_URL`
- [ ] SSL mode configured (`sslmode=require`)
- [ ] Database connection tested locally
- [ ] Migrations applied to production database
- [ ] Seed data loaded (`python manage.py seed_cards`)
- [ ] Superuser created (optional, for Django admin)

**Verify**:
```bash
# Test connection
python manage.py dbshell
# Should connect to Supabase PostgreSQL
```

---

## Phase 2: Backend Deployment (Render)

See: `DEPLOYMENT_RENDER.md`

### Prepare Backend
- [ ] `gunicorn` in `requirements.txt`
- [ ] `whitenoise` in `requirements.txt`
- [ ] `dj-database-url` in `requirements.txt`
- [ ] `build.sh` created and executable (`chmod +x backend/build.sh`)
- [ ] `settings.py` configured for production:
  - [ ] `DEBUG=False` by default
  - [ ] `ALLOWED_HOSTS` from env
  - [ ] `STATIC_ROOT` configured
  - [ ] `WhiteNoiseMiddleware` added
  - [ ] `DATABASE_URL` support
  - [ ] Production security settings (SSL redirect, secure cookies)
- [ ] Health check endpoint created (`/api/health/`)
- [ ] Changes committed and pushed to GitHub

### Deploy to Render
- [ ] Render account created (sign up with GitHub)
- [ ] GitHub repository connected
- [ ] New Web Service created
- [ ] Service configured:
  - [ ] Name: `card-tracker-backend`
  - [ ] Root Directory: `backend`
  - [ ] Build Command: `./build.sh`
  - [ ] Start Command: `gunicorn card_tracker.wsgi:application --bind 0.0.0.0:$PORT`
  - [ ] Plan: **Free**
- [ ] Environment variables set:
  - [ ] `SECRET_KEY` (auto-generated)
  - [ ] `DEBUG=False`
  - [ ] `ALLOWED_HOSTS=<render-service-url>`
  - [ ] `DATABASE_URL=<supabase-connection-string>`
  - [ ] `CORS_ALLOWED_ORIGINS=http://localhost:3000` (update after frontend deploy)
  - [ ] `GOOGLE_CLIENT_ID` (if using OAuth)
  - [ ] `GOOGLE_CLIENT_SECRET` (if using OAuth)
  - [ ] `GEMINI_API_KEY` (if using AI lookup)
- [ ] First deployment successful (watch logs)
- [ ] Health check endpoint responding:
  ```
  curl https://your-backend.onrender.com/api/health/
  ```
- [ ] API endpoints accessible:
  ```
  curl https://your-backend.onrender.com/api/card-templates/
  ```

**Service URL**: `https://______________________.onrender.com`

---

## Phase 3: Frontend Deployment (Vercel)

See: `DEPLOYMENT_VERCEL.md`

### Prepare Frontend
- [ ] `NEXT_PUBLIC_API_URL` used in API client
- [ ] `.env.production.example` created with template
- [ ] Production build tested locally (`npm run build`)
- [ ] No build errors or warnings
- [ ] Changes committed and pushed to GitHub

### Deploy to Vercel
- [ ] Vercel account created (sign up with GitHub)
- [ ] GitHub repository imported
- [ ] Project configured:
  - [ ] Framework: `Next.js` (auto-detected)
  - [ ] Root Directory: `frontend`
  - [ ] Build Command: `npm run build`
- [ ] Environment variables set:
  - [ ] `NEXT_PUBLIC_API_URL=https://<render-backend-url>/api`
  - [ ] `NEXTAUTH_URL=https://<vercel-url>` (update after first deploy)
  - [ ] `NEXTAUTH_SECRET` (auto-generated)
  - [ ] `GOOGLE_CLIENT_ID` (if using OAuth)
  - [ ] `GOOGLE_CLIENT_SECRET` (if using OAuth)
- [ ] First deployment successful (watch build logs)
- [ ] Frontend accessible at Vercel URL
- [ ] No console errors in browser

**Frontend URL**: `https://______________________.vercel.app`

---

## Phase 4: Connect Frontend & Backend

### Update Backend CORS
- [ ] Go to Render dashboard → Environment
- [ ] Update `CORS_ALLOWED_ORIGINS` to include Vercel URL:
  ```
  CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
  ```
- [ ] Save changes (triggers redeploy)
- [ ] Wait for redeploy to complete

### Update Frontend NEXTAUTH_URL
- [ ] Go to Vercel dashboard → Project Settings → Environment Variables
- [ ] Update `NEXTAUTH_URL` to actual Vercel URL:
  ```
  NEXTAUTH_URL=https://your-frontend.vercel.app
  ```
- [ ] Save changes
- [ ] Redeploy frontend (Deployments → Redeploy)

### Update ALLOWED_HOSTS
- [ ] Go to Render dashboard → Environment
- [ ] Update `ALLOWED_HOSTS` to Render service URL:
  ```
  ALLOWED_HOSTS=your-backend.onrender.com
  ```
- [ ] Save and redeploy

---

## Phase 5: OAuth Configuration

See: `ENVIRONMENT_VARIABLES.md` → OAuth Setup

### Google OAuth
- [ ] Google Cloud project created
- [ ] OAuth consent screen configured:
  - [ ] App name: Credit Card Benefits Tracker
  - [ ] Support email set
  - [ ] Scopes: `email`, `profile`, `openid`
- [ ] OAuth 2.0 Client ID created
- [ ] Authorized redirect URIs added:
  - [ ] `https://<vercel-url>/api/auth/callback/google`
  - [ ] `https://<render-url>/accounts/google/login/callback/`
  - [ ] `http://localhost:3000/api/auth/callback/google` (dev)
  - [ ] `http://localhost:8000/accounts/google/login/callback/` (dev)
- [ ] Client ID and Secret copied
- [ ] Added to both Render and Vercel environment variables
- [ ] Both services redeployed

### Apple OAuth (Optional)
- [ ] Apple Developer account ($99/year)
- [ ] App ID created
- [ ] Service ID created
- [ ] "Sign in with Apple" enabled
- [ ] Return URLs configured:
  - [ ] `https://<vercel-url>/api/auth/callback/apple`
  - [ ] `https://<render-url>/accounts/apple/login/callback/`
- [ ] Private key downloaded
- [ ] JWT client secret generated
- [ ] Added to both Render and Vercel environment variables
- [ ] Both services redeployed

---

## Phase 6: End-to-End Testing

### Basic Connectivity
- [ ] Frontend loads without errors
- [ ] Backend health check responds
- [ ] No CORS errors in browser console

### Authentication Flow
- [ ] Login page accessible
- [ ] Google OAuth button works
- [ ] Redirects to Google consent screen
- [ ] Redirects back to app after consent
- [ ] JWT token stored in browser
- [ ] User sees authenticated state (e.g., name/email displayed)
- [ ] Logout works
- [ ] Protected routes require authentication

### Core Features
- [ ] Dashboard loads with summary cards
- [ ] "Add Card" flow works:
  - [ ] Search for card (autocomplete)
  - [ ] Select card from results
  - [ ] Enter open date
  - [ ] Save card
  - [ ] Card appears in "My Cards"
- [ ] Card detail page loads:
  - [ ] Shows card info
  - [ ] Lists benefits with progress bars
  - [ ] "Use Benefit" button works
- [ ] Track benefit usage:
  - [ ] Click "Use Benefit"
  - [ ] Enter amount and date
  - [ ] Usage records saved
  - [ ] Progress bar updates
  - [ ] Remaining amount calculated correctly
- [ ] Usage history displayed
- [ ] "Undo" usage works
- [ ] Deadline alerts show (if benefits expiring soon)

### Edge Cases
- [ ] Cold start handled gracefully (backend sleeps after 15 min on Render free tier)
- [ ] Loading states show during API calls
- [ ] Error messages display for failed requests
- [ ] Form validation works (required fields, date formats)
- [ ] Empty states show (no cards, no benefits)

---

## Phase 7: Performance & Monitoring

### Performance
- [ ] Page load time < 3 seconds (after cold start)
- [ ] API response time < 500ms (for warm backend)
- [ ] Images optimized and loading fast
- [ ] No unnecessary re-renders

### Monitoring
- [ ] Render logs show no errors
- [ ] Vercel deployment logs clean
- [ ] Browser console clean (no warnings/errors)
- [ ] Set up uptime monitor (UptimeRobot):
  - [ ] Monitor created
  - [ ] URL: `https://<backend>/api/health/`
  - [ ] Interval: Every 10 minutes (keeps backend warm)
  - [ ] Email alerts enabled

---

## Phase 8: Security Review

### Backend
- [ ] `DEBUG=False` in production
- [ ] `SECRET_KEY` is strong and unique (not the default)
- [ ] `ALLOWED_HOSTS` restricts to production domain only
- [ ] Database uses SSL (`sslmode=require`)
- [ ] CORS only allows frontend domain
- [ ] CSRF protection enabled
- [ ] Secure cookies enabled (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`)
- [ ] XSS protection enabled
- [ ] No sensitive data in logs
- [ ] No `.env` files committed to git

### Frontend
- [ ] `NEXTAUTH_SECRET` is strong and unique
- [ ] No API keys exposed in client-side code
- [ ] OAuth scopes minimal (only `email`, `profile`)
- [ ] No console.log() statements with sensitive data
- [ ] Environment variables properly scoped (public vs server-only)

### OAuth
- [ ] Redirect URIs whitelist only production domains
- [ ] OAuth apps in "Production" mode (not "Testing")
- [ ] Test users removed (if Google OAuth in production)

---

## Phase 9: Documentation & Handoff

- [ ] Update main `README.md`:
  - [ ] Add production URLs
  - [ ] Add "Live Demo" section
  - [ ] Update architecture diagram with deployed services
- [ ] Create user guide (optional):
  - [ ] How to add a card
  - [ ] How to track benefits
  - [ ] How to set reminders
- [ ] Document admin tasks:
  - [ ] How to add new card templates
  - [ ] How to view logs
  - [ ] How to run database backups

---

## Phase 10: Post-Deployment Tasks

### Immediate (Day 1)
- [ ] Monitor logs for errors (Render + Vercel)
- [ ] Test all features again
- [ ] Share with beta users (if applicable)
- [ ] Collect feedback

### Short-term (Week 1)
- [ ] Monitor uptime (should be 99%+)
- [ ] Check Supabase usage (should stay under 500MB)
- [ ] Optimize slow queries (if any)
- [ ] Fix any reported bugs

### Long-term (Monthly)
- [ ] Review Render/Vercel usage (should stay in free tier)
- [ ] Backup database manually (Supabase free tier has no auto-backups)
- [ ] Update dependencies (security patches)
- [ ] Rotate secrets (every 90 days)

---

## Rollback Plan

If something goes wrong:

### Backend Issues
1. Check Render logs for errors
2. Revert to previous deployment:
   - Go to Render dashboard → Deployments
   - Find last working deployment
   - Click "Redeploy"
3. Or fix and push new commit (auto-redeploys)

### Frontend Issues
1. Check Vercel logs for build/runtime errors
2. Revert to previous deployment:
   - Go to Vercel dashboard → Deployments
   - Find last working deployment
   - Click "Promote to Production"
3. Or fix and push new commit (auto-redeploys)

### Database Issues
1. Check Supabase dashboard for connection issues
2. Verify `DATABASE_URL` in Render is correct
3. Check Supabase project is not paused (free tier pauses after 7 days inactivity)
4. Restore from backup if data corrupted

---

## Success Criteria

✅ **Backend**:
- Health check returns `200 OK`
- API endpoints accessible and returning correct data
- Database connected and migrations applied
- Seed data loaded
- No errors in logs

✅ **Frontend**:
- Site loads without errors
- OAuth login works
- All pages accessible
- API calls succeed (no CORS errors)
- No console errors

✅ **Integration**:
- Full user flow works (signup → add card → track benefit)
- Data persists across sessions
- Real-time updates work

✅ **Performance**:
- Page loads < 3 seconds (after cold start)
- API responses < 500ms (warm backend)
- Uptime > 99%

✅ **Security**:
- HTTPS enabled on both frontend and backend
- OAuth properly configured
- No sensitive data exposed
- Environment variables secure

---

## Troubleshooting Quick Reference

| Issue | Check | Solution |
|-------|-------|----------|
| Backend won't start | Render logs | Verify `DATABASE_URL`, `SECRET_KEY`, `ALLOWED_HOSTS` |
| Frontend won't build | Vercel logs | Check TypeScript errors, missing dependencies |
| CORS error | Browser console | Update `CORS_ALLOWED_ORIGINS` in Render |
| OAuth redirect error | OAuth provider | Add redirect URI to Google/Apple OAuth app |
| Database connection fails | Supabase dashboard | Check project is not paused, verify credentials |
| Slow first request | Expected behavior | Render free tier cold starts (~30s). Use uptime monitor. |
| API 404 errors | API client config | Verify `NEXT_PUBLIC_API_URL` matches Render URL |

---

## Resources

- `DEPLOYMENT_SUPABASE.md` - Database setup
- `DEPLOYMENT_RENDER.md` - Backend deployment
- `DEPLOYMENT_VERCEL.md` - Frontend deployment
- `ENVIRONMENT_VARIABLES.md` - All env vars explained
- `OPERATIONS.md` - Day-to-day maintenance
- `TROUBLESHOOTING.md` - Common issues and solutions

---

## Deployment Complete! 🎉

Once all items are checked:

1. Share your live app URL
2. Add to portfolio/resume
3. Consider upgrades if scaling:
   - Render Starter ($7/month) - No cold starts
   - Vercel Pro ($20/month) - More bandwidth
   - Supabase Pro ($25/month) - Backups & more storage

**Your app is now live at**:
- Frontend: `https://______________________.vercel.app`
- Backend: `https://______________________.onrender.com`

Enjoy your Credit Card Benefits Tracker!
