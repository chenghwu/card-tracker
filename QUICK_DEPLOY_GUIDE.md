# Quick Deploy Guide

Fast-track deployment reference for the Credit Card Benefits Tracker.

---

## Prerequisites

- [ ] GitHub account with code pushed
- [ ] Working local development environment
- [ ] ~2 hours available
- [ ] Access to email for account verifications

---

## Step 1: Database (Supabase) - 15 min

### Actions
1. Sign up at [supabase.com](https://supabase.com) with GitHub
2. Create new project (name: `card-tracker`)
3. Copy **DATABASE_URL** from Settings → Database
4. Save password securely

### Command
```bash
# Test connection locally (optional)
cd backend
# Add DATABASE_URL to .env
python manage.py migrate
python manage.py seed_cards
```

**Details**: See `DEPLOYMENT_SUPABASE.md`

---

## Step 2: Backend (Render) - 30 min

### Actions
1. Sign up at [render.com](https://render.com) with GitHub
2. New Web Service → Connect `card_tracker` repo
3. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn card_tracker.wsgi:application --bind 0.0.0.0:$PORT`

### Environment Variables
```
SECRET_KEY=<auto-generate>
DEBUG=False
ALLOWED_HOSTS=<your-render-url>.onrender.com
DATABASE_URL=<paste-from-supabase>
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Verify
```bash
curl https://<your-backend>.onrender.com/api/health/
# Should return: {"status":"ok","database":"connected"}
```

**Details**: See `DEPLOYMENT_RENDER.md`

---

## Step 3: Frontend (Vercel) - 20 min

### Actions
1. Sign up at [vercel.com](https://vercel.com) with GitHub
2. Import project → Select `card_tracker` repo
3. Configure:
   - **Root Directory**: `frontend`
   - **Framework**: Next.js (auto-detected)

### Environment Variables
```
NEXT_PUBLIC_API_URL=https://<your-backend>.onrender.com/api
NEXTAUTH_URL=https://<your-frontend>.vercel.app
NEXTAUTH_SECRET=<auto-generate or: openssl rand -base64 32>
```

### Verify
Open `https://<your-frontend>.vercel.app` in browser

**Details**: See `DEPLOYMENT_VERCEL.md`

---

## Step 4: Connect Services - 15 min

### Update Backend CORS
In Render dashboard → Environment:
```
CORS_ALLOWED_ORIGINS=https://<your-frontend>.vercel.app
```
Save → Wait for redeploy (~2 min)

### Update Frontend URL
In Vercel dashboard → Environment Variables:
```
NEXTAUTH_URL=https://<your-frontend>.vercel.app
```
Save → Redeploy

### Update Backend ALLOWED_HOSTS
In Render dashboard → Environment:
```
ALLOWED_HOSTS=<your-backend>.onrender.com
```
Save → Redeploy

---

## Step 5: Test Everything - 30 min

### Quick Tests
- [ ] Frontend loads without errors
- [ ] No CORS errors in browser console
- [ ] Health check: `curl https://<backend>/api/health/`
- [ ] API list cards: `curl https://<backend>/api/card-templates/`

### Full User Flow (without OAuth)
Since OAuth requires additional setup, test these first:
- [ ] Frontend displays (even if login doesn't work yet)
- [ ] Backend API responds
- [ ] Database connected

### OAuth Setup (Optional - do later)
Follow `ENVIRONMENT_VARIABLES.md` → OAuth Setup section to configure Google/Apple login.

**Details**: See `DEPLOYMENT_CHECKLIST.md`

---

## Optional: Configure OAuth - 30 min

### Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth 2.0 Client ID
3. Add redirect URIs:
   - `https://<frontend>.vercel.app/api/auth/callback/google`
   - `https://<backend>.onrender.com/accounts/google/login/callback/`
4. Copy Client ID and Secret
5. Add to both Render and Vercel environment variables
6. Redeploy both services

**Details**: See `ENVIRONMENT_VARIABLES.md` → OAuth Setup

---

## Quick Troubleshooting

### Backend Won't Start
- Check Render logs for errors
- Verify `DATABASE_URL` is correct
- Ensure `SECRET_KEY` is set

### Frontend Shows CORS Error
- Update `CORS_ALLOWED_ORIGINS` in Render
- Include full URL with `https://`
- Wait for backend to redeploy

### "This site can't be reached"
- Backend is sleeping (Render free tier)
- Wait 30 seconds for cold start
- Set up UptimeRobot to keep it awake

### OAuth "redirect_uri_mismatch"
- Add production URLs to Google OAuth app
- Format: `https://domain.com/api/auth/callback/google`
- No trailing slash

**Details**: See `TROUBLESHOOTING.md`

---

## Monitoring Setup (After Deployment)

### UptimeRobot (Free)
1. Sign up at [uptimerobot.com](https://uptimerobot.com)
2. Create HTTP(s) monitor
3. URL: `https://<backend>.onrender.com/api/health/`
4. Interval: Every 10 minutes
5. Keeps backend awake on free tier

**Details**: See `OPERATIONS.md` → Monitoring

---

## Cost Optimization

**Free Tier Limits:**
- Supabase: 500MB database (plenty for personal use)
- Render: 750 hours/month (enough for 1 service)
- Vercel: 100GB bandwidth (20K+ page views)

**Stay Free:**
- Monitor usage in dashboards
- Delete old benefit usage records periodically
- Use uptime monitor to prevent excessive cold starts

**When to Upgrade:**
- Render Starter ($7/month): No cold starts
- Supabase Pro ($25/month): Automated backups
- Vercel Pro ($20/month): More bandwidth

---

## Deployment Checklist Summary

### Pre-Deployment
- [ ] Code pushed to GitHub
- [ ] Local tests passing
- [ ] `.env.example` files reviewed

### Supabase
- [ ] Account created
- [ ] Project created
- [ ] Database URL saved

### Render
- [ ] Account created
- [ ] Service created
- [ ] Environment variables set
- [ ] First deploy successful
- [ ] Health check responding

### Vercel
- [ ] Account created
- [ ] Project imported
- [ ] Environment variables set
- [ ] First deploy successful
- [ ] Frontend loads

### Integration
- [ ] CORS configured
- [ ] URLs updated (NEXTAUTH_URL, ALLOWED_HOSTS)
- [ ] Services connected
- [ ] API calls working

### Testing
- [ ] Health check OK
- [ ] API endpoints accessible
- [ ] Frontend loads
- [ ] No console errors
- [ ] OAuth working (if configured)

---

## File Reference

| File | Purpose |
|------|---------|
| `DEPLOYMENT_SUMMARY.md` | Complete overview |
| `DEPLOYMENT_SUPABASE.md` | Database setup (detailed) |
| `DEPLOYMENT_RENDER.md` | Backend deployment (detailed) |
| `DEPLOYMENT_VERCEL.md` | Frontend deployment (detailed) |
| `ENVIRONMENT_VARIABLES.md` | All env vars explained |
| `DEPLOYMENT_CHECKLIST.md` | Full verification steps |
| `TROUBLESHOOTING.md` | Common issues |
| `OPERATIONS.md` | Daily maintenance |
| `QUICK_DEPLOY_GUIDE.md` | This file |

---

## Commands Reference

### Local Development
```bash
# Backend
cd backend
python manage.py runserver

# Frontend
cd frontend
npm run dev
```

### Testing
```bash
# Backend API
curl http://localhost:8000/api/health/

# Frontend build
cd frontend
npm run build
```

### Production Health Check
```bash
# Backend
curl https://<your-backend>.onrender.com/api/health/

# Frontend
curl https://<your-frontend>.vercel.app/
```

### Database
```bash
# Connect to production database
psql "<DATABASE_URL>"

# Backup
pg_dump "<DATABASE_URL>" > backup.sql
```

---

## Support

### Documentation
Start with `DEPLOYMENT_SUMMARY.md` for a complete overview.

### Stuck?
1. Check `TROUBLESHOOTING.md` for your specific error
2. Review deployment guide for the failing service
3. Check service logs (Render/Vercel dashboard)
4. Verify environment variables

### Communities
- [Render Community](https://community.render.com/)
- [Vercel Discord](https://discord.gg/vercel)
- [Supabase Discord](https://discord.supabase.com/)

---

## Timeline

**First-Time Deployment**: ~2 hours
- Database: 15 min
- Backend: 30 min
- Frontend: 20 min
- Integration: 15 min
- Testing: 30 min
- OAuth (optional): +30 min

**Future Deploys**: Automatic
- Push to GitHub → Auto-deploys in ~5 minutes

---

## Success Indicators

You know deployment is successful when:
- ✅ Backend health check returns `{"status":"ok"}`
- ✅ Frontend loads in browser without errors
- ✅ No CORS errors in console
- ✅ API calls work (even if auth fails without OAuth)
- ✅ Uptime monitor shows "Up"
- ✅ All services show "Live" in dashboards

---

## Next Actions After Deploy

1. **Set up monitoring** (UptimeRobot)
2. **Configure OAuth** (Google/Apple)
3. **Add custom domain** (optional)
4. **Test full user flow**
5. **Monitor logs** for first 24 hours
6. **Share with users**

---

**Ready to deploy?** Start with `DEPLOYMENT_SUPABASE.md`

**Questions?** Check `TROUBLESHOOTING.md` or `DEPLOYMENT_SUMMARY.md`
