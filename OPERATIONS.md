# Operations & Maintenance Guide

Day-to-day operations, monitoring, and maintenance for the Credit Card Benefits Tracker.

---

## Table of Contents

1. [Monitoring](#monitoring)
2. [Viewing Logs](#viewing-logs)
3. [Database Operations](#database-operations)
4. [Adding New Card Templates](#adding-new-card-templates)
5. [Managing Users](#managing-users)
6. [Backup & Recovery](#backup--recovery)
7. [Scaling & Performance](#scaling--performance)
8. [Cost Monitoring](#cost-monitoring)
9. [Security Maintenance](#security-maintenance)
10. [Routine Tasks](#routine-tasks)

---

## Monitoring

### Service Health

**Check all services are up**:
- Backend: `https://your-backend.onrender.com/api/health/`
- Frontend: `https://your-frontend.vercel.app`
- Database: Supabase dashboard

**Expected responses**:
```json
// Backend health check
{
  "status": "ok",
  "database": "connected"
}
```

---

### Uptime Monitoring

**Set up UptimeRobot** (free):

1. Go to [UptimeRobot.com](https://uptimerobot.com)
2. Sign up (free plan: 50 monitors, 5-minute intervals)
3. Create monitors:

**Backend Monitor**:
- Monitor Type: HTTP(s)
- URL: `https://your-backend.onrender.com/api/health/`
- Monitoring Interval: **Every 10 minutes** (keeps Render alive)
- Alert When: Down for 2 minutes
- Alert Contacts: Your email

**Frontend Monitor**:
- Monitor Type: HTTP(s)
- URL: `https://your-frontend.vercel.app`
- Monitoring Interval: Every 5 minutes
- Expected Status Code: 200

**Database Monitor** (via backend):
- Already covered by backend health check (includes DB connection test)

---

### Performance Monitoring

**Vercel Analytics** (free):
1. Go to Vercel dashboard → Your project → Analytics
2. Click "Enable Analytics"
3. View:
   - Page load times
   - Core Web Vitals
   - Real User Monitoring (RUM)
   - Top pages by traffic

**Render Metrics**:
- Go to Render dashboard → Your service → Metrics
- View:
   - CPU usage
   - Memory usage
   - Response times
   - Request count

---

### Error Tracking (Optional)

**Sentry** for production error monitoring:

1. Sign up at [Sentry.io](https://sentry.io) (free tier: 5K errors/month)
2. Create projects for backend and frontend
3. Install:
   ```bash
   # Backend
   pip install sentry-sdk

   # Frontend
   npm install @sentry/nextjs
   ```
4. Configure (see Sentry docs for setup)

---

## Viewing Logs

### Backend Logs (Render)

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Select your backend service
3. Click **Logs** tab
4. Filter by:
   - **Build Logs**: Deployment process
   - **Deploy Logs**: Service startup
   - **Application Logs**: Runtime logs

**Search logs**:
- Use search bar to filter by keyword (e.g., "ERROR", "500")
- Click **Download Logs** to save locally

**Common log patterns**:
```
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Using worker: sync
[INFO] Booting worker with pid: 123

# Good request
GET /api/cards/ 200 OK

# Error (investigate)
ERROR django.request: Internal Server Error
```

---

### Frontend Logs (Vercel)

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Click **Deployments** tab
4. Click on a deployment
5. View:
   - **Build Logs**: `npm install`, `npm run build`
   - **Function Logs**: Server-side runtime logs (API routes, SSR)

**Real-time logs**:
```bash
# Install Vercel CLI
npm i -g vercel

# View logs
vercel logs https://your-frontend.vercel.app --follow
```

---

### Database Logs (Supabase)

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Select your project
3. Go to **Database** → **Logs**
4. View:
   - Query logs
   - Connection errors
   - Slow queries

**Database metrics**:
- Go to **Database** → **Reports**
- View:
  - Storage usage
  - Active connections
  - Query performance

---

### Browser Console Logs

**Development**:
```javascript
// Frontend logs (browser console)
console.log('API Response:', data);
console.error('Failed to fetch:', error);
```

**Production debugging**:
1. Open browser DevTools (F12)
2. **Console** tab: JavaScript errors
3. **Network** tab: API requests/responses
4. **Application** tab: Cookies, localStorage (JWT tokens)

---

## Database Operations

### Running Migrations

**Production**:

**Option 1 - Render Shell**:
1. Go to Render dashboard → Your service
2. Click **Shell** tab (opens terminal)
3. Run migration:
   ```bash
   python manage.py migrate
   ```

**Option 2 - Build script** (automatic on deploy):
```bash
# backend/build.sh already includes:
python manage.py migrate
```

**Local testing first**:
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations  # Verify
```

---

### Viewing Database Data

**Django Admin**:

1. Create superuser (if not done):
   ```bash
   # In Render Shell
   python manage.py createsuperuser
   ```

2. Access admin:
   ```
   https://your-backend.onrender.com/admin/
   ```

3. View/edit:
   - Card Templates
   - Benefits
   - User Cards
   - Benefit Usage

**Supabase Table Editor**:
1. Go to Supabase dashboard → **Table Editor**
2. View/query tables directly
3. ⚠️ **Be careful editing production data**

**psql (PostgreSQL CLI)**:
```bash
psql "postgresql://user:pass@host:6543/postgres?sslmode=require"

# List tables
\dt

# Query
SELECT * FROM cards_cardtemplate LIMIT 10;

# Exit
\q
```

---

### Database Backups

See [Backup & Recovery](#backup--recovery) section below.

---

## Adding New Card Templates

### Method 1: Django Admin (Recommended)

1. Go to `https://your-backend.onrender.com/admin/`
2. Log in with superuser credentials
3. Click **Card Templates** → **Add Card Template**
4. Fill in:
   - Bank name
   - Card name
   - Annual fee (in cents, e.g., 55000 for $550)
   - Image URL (optional)
   - Is verified: ✓
5. Click **Save and add another** (to add benefits)
6. Click **Benefit Templates** → **Add Benefit Template**
7. Fill in:
   - Card template (select the card just created)
   - Benefit name (e.g., "Annual Uber Credit")
   - Description
   - Amount (in cents, e.g., 20000 for $200)
   - Frequency (monthly, quarterly, semi_annual, annual)
   - Period type (calendar_year or membership_year)
   - Category
8. Click **Save**
9. Repeat for all benefits

---

### Method 2: Management Command

**Create/update seed data**:

Edit `backend/cards/data/seed_cards.py` (or create new file):

```python
# cards/data/new_cards.py
CARD_DATA = [
    {
        "bank": "Chase",
        "name": "Sapphire Preferred",
        "annual_fee_cents": 9500,
        "image_url": "https://example.com/sapphire-preferred.png",
        "is_verified": True,
        "benefits": [
            {
                "name": "Annual Travel Credit",
                "description": "$50 annual hotel credit",
                "amount_cents": 5000,
                "frequency": "annual",
                "period_type": "membership_year",
                "category": "travel",
            },
        ],
    },
]
```

Run:
```bash
# In Render Shell
python manage.py seed_cards
```

---

### Method 3: API (Programmatic)

**POST to admin API**:

```bash
curl -X POST https://your-backend.onrender.com/admin/api/cards/ \
  -H "Authorization: Bearer YOUR_ADMIN_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "bank": "Chase",
    "name": "Freedom Flex",
    "annual_fee_cents": 0,
    "is_verified": true
  }'
```

*(Requires implementing admin API endpoints)*

---

## Managing Users

### View Users

**Django Admin**:
1. Go to `/admin/` → **Users**
2. View all registered users
3. See:
   - Email
   - Join date
   - Last login
   - Active status

**Database query**:
```sql
-- In psql or Supabase SQL Editor
SELECT id, email, date_joined, last_login, is_active
FROM auth_user
ORDER BY date_joined DESC
LIMIT 20;
```

---

### Deactivate User

**Django Admin**:
1. Go to `/admin/` → **Users**
2. Click user
3. Uncheck **Active**
4. Click **Save**

**Shell**:
```bash
# In Render Shell
python manage.py shell

>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.get(email='user@example.com')
>>> user.is_active = False
>>> user.save()
```

---

### Delete User Data (GDPR)

**Script**:
```bash
# In Render Shell
python manage.py shell

>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.get(email='user@example.com')

# Delete all user data
>>> user.cards.all().delete()  # Deletes UserCards (cascade deletes benefits/usage)
>>> user.delete()  # Deletes user account
```

---

## Backup & Recovery

### Database Backups

**Manual backup** (recommended weekly):

```bash
# Export database to SQL file
pg_dump "postgresql://user:pass@host:6543/postgres?sslmode=require" \
  --no-owner --no-acl \
  > backup_$(date +%Y%m%d).sql

# Or using Supabase CLI
supabase db dump -p your-db-password > backup.sql
```

**Store backups**:
- Local drive
- Cloud storage (Google Drive, Dropbox)
- GitHub (if no sensitive data)

---

### Restore from Backup

**Restore database**:

```bash
# Drop existing data (⚠️ DESTRUCTIVE)
psql "postgresql://..." -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Restore from backup
psql "postgresql://..." < backup_20260215.sql

# Or using Supabase CLI
supabase db push backup.sql
```

---

### Code Backups

**Git is your backup**:
- All code is version-controlled
- GitHub serves as remote backup
- Can rollback to any commit

**Restore previous version**:
```bash
# View history
git log --oneline

# Rollback to commit
git revert <commit-hash>
git push

# Or reset (⚠️ rewrites history)
git reset --hard <commit-hash>
git push --force
```

---

### Deployment Rollback

**Render**:
1. Go to Render dashboard → Deployments
2. Find last working deployment
3. Click **Redeploy**

**Vercel**:
1. Go to Vercel dashboard → Deployments
2. Find last working deployment
3. Click **⋯** → **Promote to Production**

---

## Scaling & Performance

### When to Scale

**Indicators**:
- Backend cold starts affecting UX (>30s)
- Running out of Supabase storage (>500MB)
- High traffic (>1,000 daily active users)
- Frequent 429 rate limit errors

---

### Backend Scaling

**Render Free → Starter ($7/month)**:
- ✅ No cold starts (always on)
- ✅ 512 MB RAM (same)
- ✅ 0.5 CPU (5x faster)

**Upgrade**:
1. Go to Render dashboard → Your service → Settings
2. Change Plan to **Starter**
3. Save (takes effect immediately)

**Horizontal scaling** (multiple instances):
- Available on paid plans
- Configure in Render dashboard → Settings → Scaling

---

### Frontend Scaling

**Vercel Free → Pro ($20/month)**:
- ✅ 1TB bandwidth (vs 100GB)
- ✅ Unlimited team members
- ✅ Password-protected previews
- ✅ Advanced analytics

**Auto-scales**:
- Vercel automatically scales frontend (edge network)
- No configuration needed

---

### Database Scaling

**Supabase Free → Pro ($25/month)**:
- ✅ 8GB storage (vs 500MB)
- ✅ 50GB bandwidth (vs 2GB)
- ✅ Daily automated backups
- ✅ 7-day PITR (Point-in-Time Recovery)

**Upgrade**:
1. Go to Supabase dashboard → Settings → Billing
2. Select **Pro Plan**
3. Confirm

---

### Performance Optimization

**Backend**:
- Add database indexes on frequently queried fields
- Use `select_related()` and `prefetch_related()`
- Enable query caching (Redis)
- Optimize serializers (only return needed fields)

**Frontend**:
- Code splitting (dynamic imports)
- Image optimization (Next.js Image component)
- Lazy loading (React.lazy, Suspense)
- Minimize bundle size (analyze with webpack-bundle-analyzer)

**Database**:
- Create indexes:
  ```python
  class Meta:
      indexes = [
          models.Index(fields=['user', 'is_active']),
          models.Index(fields=['user_card', 'period_start']),
      ]
  ```
- VACUUM (PostgreSQL maintenance):
  ```sql
  VACUUM ANALYZE;
  ```

---

## Cost Monitoring

### Current Costs (Free Tier)

| Service | Plan | Cost | Usage Limit |
|---------|------|------|-------------|
| Render | Free | $0 | 750 hours/month, sleeps after 15min |
| Vercel | Hobby | $0 | 100GB bandwidth, 6000 build min/month |
| Supabase | Free | $0 | 500MB database, 2GB bandwidth |
| **Total** | | **$0** | |

---

### Monitor Usage

**Render**:
- Dashboard → Your service → Metrics
- View hours used (should stay under 750/month for free tier)

**Vercel**:
- Dashboard → Usage
- View bandwidth, builds, function executions

**Supabase**:
- Dashboard → Database → Reports
- View storage used (alert at 400MB)

---

### Cost Alerts

**Set up alerts**:

1. **Supabase**: Settings → Billing → Set up alerts at 80% usage
2. **Render**: Enable email notifications for quota limits
3. **Vercel**: Usage tab → Notifications

---

### Projected Costs (if scaling)

**Low traffic** (~100 users):
- Render: Free or Starter ($7/month)
- Vercel: Free
- Supabase: Free
- **Total: $0-7/month**

**Medium traffic** (~1,000 users):
- Render Starter: $7/month
- Vercel Pro: $20/month
- Supabase Pro: $25/month
- **Total: $52/month**

**High traffic** (~10,000 users):
- Render Standard: $25/month
- Vercel Pro: $20/month
- Supabase Pro: $25/month
- CDN/Redis: $10/month
- **Total: $80/month**

---

## Security Maintenance

### Regular Security Tasks

**Monthly**:
- [ ] Review access logs for suspicious activity
- [ ] Check for failed login attempts (Django admin logs)
- [ ] Review OAuth app permissions (Google Cloud Console)

**Quarterly** (every 3 months):
- [ ] Rotate `SECRET_KEY` and `NEXTAUTH_SECRET`
- [ ] Update dependencies (security patches)
- [ ] Review user accounts (deactivate inactive users)

**Annually**:
- [ ] Rotate database password
- [ ] Regenerate OAuth client secrets
- [ ] Review and update security policies

---

### Update Dependencies

**Backend**:
```bash
cd backend

# Check for outdated packages
pip list --outdated

# Update all
pip install --upgrade -r requirements.txt

# Or update specific package
pip install --upgrade django

# Update requirements.txt
pip freeze > requirements.txt

# Test locally, then commit and push
git add requirements.txt
git commit -m "Update dependencies"
git push
```

**Frontend**:
```bash
cd frontend

# Check for outdated packages
npm outdated

# Update all
npm update

# Or update specific package
npm install next@latest

# Test locally, then commit and push
git add package.json package-lock.json
git commit -m "Update dependencies"
git push
```

---

### Security Audits

**Django**:
```bash
python manage.py check --deploy
```

**Node.js**:
```bash
npm audit
npm audit fix  # Fix vulnerabilities
```

---

## Routine Tasks

### Daily
- [ ] Check uptime monitor (should be 99%+)
- [ ] Review error logs (any new errors?)
- [ ] Monitor Render/Vercel dashboards for issues

### Weekly
- [ ] Review analytics (page views, user signups)
- [ ] Check database storage usage
- [ ] Backup database manually

### Monthly
- [ ] Update dependencies (security patches)
- [ ] Review cost/usage (staying in free tier?)
- [ ] Check for slow queries (optimize if needed)

### Quarterly
- [ ] Rotate secrets (SECRET_KEY, NEXTAUTH_SECRET)
- [ ] Review user feedback/feature requests
- [ ] Performance audit (load times, optimize)

### Annually
- [ ] Security audit (penetration testing)
- [ ] Review architecture (any major changes needed?)
- [ ] Update documentation

---

## Deployment Workflow

### For Regular Updates

1. **Develop locally**:
   ```bash
   git checkout -b feature/new-feature
   # Make changes
   npm run dev  # Test frontend
   python manage.py runserver  # Test backend
   ```

2. **Test**:
   ```bash
   # Backend tests
   pytest

   # Frontend build
   npm run build
   ```

3. **Commit and push**:
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin feature/new-feature
   ```

4. **Create PR**:
   - GitHub → Pull Request
   - Vercel automatically creates preview deployment
   - Review preview before merging

5. **Merge to main**:
   - Merge PR on GitHub
   - Render auto-deploys backend
   - Vercel auto-deploys frontend

---

### For Hotfixes

**Fast-track deployment** (skip PR):

```bash
git checkout main
git pull
# Fix issue
git add .
git commit -m "Hotfix: Fix critical bug"
git push origin main
# Both services auto-deploy
```

---

## Checklists

### Pre-Deployment Checklist
- [ ] All tests passing locally
- [ ] No console errors
- [ ] Environment variables documented
- [ ] Backup database before major changes

### Post-Deployment Checklist
- [ ] Monitor logs for errors (first 30 minutes)
- [ ] Test critical user flows
- [ ] Check uptime monitor
- [ ] Notify users if major changes

---

## Getting Help

**Service Issues**:
- Render: [Community Forum](https://community.render.com/)
- Vercel: [Support](https://vercel.com/support)
- Supabase: [Discord](https://discord.supabase.com/)

**Code Issues**:
- Django: [Forum](https://forum.djangoproject.com/)
- Next.js: [GitHub Discussions](https://github.com/vercel/next.js/discussions)

**Emergency**:
- Check `TROUBLESHOOTING.md` for common issues
- Review logs (Render, Vercel, Supabase, browser console)
- Rollback to previous deployment if needed

---

## Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Next.js Production Best Practices](https://nextjs.org/docs/deployment)
- [PostgreSQL Maintenance](https://www.postgresql.org/docs/current/maintenance.html)
