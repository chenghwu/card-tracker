# Supabase PostgreSQL Setup Guide

This guide walks you through setting up Supabase PostgreSQL for the Credit Card Benefits Tracker backend.

## Why Supabase?

- **Free Tier**: 500MB database, 2GB bandwidth, enough for personal use
- **PostgreSQL**: Production-grade database (not SQLite)
- **SSL by Default**: Secure connections out of the box
- **No Credit Card Required**: Start free, upgrade if needed

---

## Step 1: Create Supabase Account

1. Go to [https://supabase.com](https://supabase.com)
2. Click **"Start your project"**
3. Sign up with GitHub (recommended) or email
4. Verify your email if required

---

## Step 2: Create a New Project

1. Click **"New Project"** from your dashboard
2. Fill in project details:
   - **Name**: `card-tracker` (or any name you prefer)
   - **Database Password**: Generate a strong password (save this!)
   - **Region**: Choose closest to you (e.g., `us-west-1`)
   - **Pricing Plan**: Select **Free tier**
3. Click **"Create new project"**
4. Wait 2-3 minutes for provisioning

---

## Step 3: Get Database Credentials

Once your project is ready:

1. Go to **Project Settings** (gear icon in bottom left)
2. Click **Database** in the left sidebar
3. Scroll to **Connection string** section
4. You'll see two formats:

### URI Format (Recommended for Django)
```
postgresql://postgres.xxxxxxxxxxxxx:[YOUR-PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres
```

### Individual Parameters Format
```
Host: aws-0-us-west-1.pooler.supabase.com
Database: postgres
Port: 6543 (use this for connection pooling)
User: postgres.xxxxxxxxxxxxx
Password: [YOUR-PASSWORD]
```

> **Important**: Use Port **6543** (connection pooler) NOT 5432 (direct) for better performance on free tier.

---

## Step 4: Configure Backend Environment Variables

### Option A: Using Database URL (Recommended)

Update your `backend/.env` file:

```env
# Django Configuration
SECRET_KEY=your-django-secret-key-change-this
DEBUG=False
ALLOWED_HOSTS=your-render-app.onrender.com

# Database Configuration (Supabase)
DATABASE_URL=postgresql://postgres.xxxxxxxxxxxxx:[YOUR-PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres

# Social Authentication
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Gemini AI (Optional)
GEMINI_API_KEY=your-gemini-api-key
```

### Option B: Using Individual Parameters

```env
# Database Configuration (Supabase)
DB_NAME=postgres
DB_USER=postgres.xxxxxxxxxxxxx
DB_PASSWORD=your-supabase-password
DB_HOST=aws-0-us-west-1.pooler.supabase.com
DB_PORT=6543
```

---

## Step 5: Update Django Settings for DATABASE_URL

The backend's `settings.py` needs to support `DATABASE_URL` parsing.

Add `dj-database-url` to `backend/requirements.txt`:

```txt
dj-database-url==2.1.0
```

Update `backend/card_tracker/settings.py`:

```python
import dj_database_url

# Database Configuration
DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    # Use DATABASE_URL (Render, Supabase)
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
elif DB_NAME := config('DB_NAME', default=''):
    # Use individual parameters (Supabase)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': DB_NAME,
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
            'OPTIONS': {
                'sslmode': 'require',  # Required for Supabase
            }
        }
    }
else:
    # Use SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

---

## Step 6: Test Connection Locally

1. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Test connection:
   ```bash
   python manage.py dbshell
   ```

   You should see:
   ```
   psql (version)
   SSL connection (protocol: TLSv1.3, cipher: ...)
   Type "help" for help.

   postgres=>
   ```

3. Exit with `\q`

---

## Step 7: Run Migrations

Create all database tables:

```bash
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, cards, account, socialaccount
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying cards.0001_initial... OK
  ...
```

---

## Step 8: Load Seed Data

Populate the database with popular credit card templates:

```bash
python manage.py seed_cards
```

Expected output:
```
Seeding card templates...
Created: Chase Sapphire Reserve
Created: American Express Platinum
...
Successfully seeded X card templates with Y benefits.
```

---

## Step 9: Create Admin User (Optional)

To access Django admin:

```bash
python manage.py createsuperuser
```

Follow prompts to set email and password.

---

## Security Best Practices

### 1. Enable SSL Mode
Always use `sslmode=require` in your database connection for Supabase.

### 2. Use Environment Variables
NEVER commit your database password to git. Always use `.env` files.

### 3. Connection Pooling
Use port **6543** (not 5432) for Supabase's connection pooler. This prevents hitting connection limits on free tier.

### 4. Restrict Database Access

In Supabase dashboard:

1. Go to **Project Settings → Database**
2. Scroll to **Connection Pooling**
3. Set **Pool Mode**: `Transaction` (best for Django)
4. Set **Pool Size**: `15` (default, adequate for free tier)

### 5. IP Whitelisting (Optional)

If deploying to Render, add Render's IP ranges:

1. Go to **Project Settings → Database**
2. Scroll to **Restrictions**
3. Add Render's outbound IPs (check Render docs)

---

## Monitoring Database Usage

Check your database usage:

1. Go to Supabase dashboard
2. Click **Database** in left sidebar
3. View:
   - **Storage Used**: Should stay under 500MB on free tier
   - **Active Connections**: Monitor for connection pooling issues

---

## Backup Strategy

### Automated Backups (Paid Plans)
Supabase free tier does NOT include automated backups.

### Manual Backups

1. Export via SQL:
   ```bash
   pg_dump -h aws-0-us-west-1.pooler.supabase.com \
           -U postgres.xxxxxxxxxxxxx \
           -d postgres \
           -p 6543 \
           --no-owner --no-acl \
           > backup_$(date +%Y%m%d).sql
   ```

2. Or use Supabase CLI:
   ```bash
   supabase db dump > backup.sql
   ```

### Recommended Backup Schedule
- **Manual backups**: Weekly for personal use
- **Before major changes**: Always backup before migrations

---

## Troubleshooting

### Connection Timeout
**Error**: `could not connect to server: Operation timed out`

**Solutions**:
- Check your internet connection
- Verify the host URL is correct
- Try using port 6543 (pooler) instead of 5432
- Check Supabase project is not paused (free tier pauses after 1 week inactivity)

### SSL Required
**Error**: `FATAL: no pg_hba.conf entry for host`

**Solution**: Add `sslmode=require` to your connection:
```python
'OPTIONS': {
    'sslmode': 'require',
}
```

### Too Many Connections
**Error**: `FATAL: remaining connection slots are reserved`

**Solutions**:
- Use port 6543 (connection pooler) NOT 5432
- Set `conn_max_age=600` in database config
- Reduce concurrent workers in production

### Project Paused
Supabase free tier pauses projects after 1 week of inactivity.

**Solution**: Visit your project dashboard to wake it up (takes 1-2 minutes).

---

## Cost Optimization

Free tier limits:
- **500MB Database Storage**: Should be plenty for personal use
- **2GB Bandwidth**: ~20K API requests/month
- **Unlimited API Requests**: No hard limit on queries

**Tips to stay within limits**:
- Delete old benefit usage records periodically
- Optimize images (use CDN for card logos)
- Enable database connection pooling

---

## Upgrading to Supabase Pro (Optional)

If you exceed free tier limits:

- **Pro Plan**: $25/month
  - 8GB database
  - 50GB bandwidth
  - Daily automated backups
  - 1 week PITR (Point-in-Time Recovery)

---

## Next Steps

✅ Supabase database configured
✅ Backend connected to PostgreSQL
✅ Migrations applied
✅ Seed data loaded

**Continue to**: `DEPLOYMENT_RENDER.md` to deploy your backend to Render.

---

## Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Django PostgreSQL Settings](https://docs.djangoproject.com/en/5.0/ref/settings/#databases)
- [Connection Pooling Guide](https://supabase.com/docs/guides/database/connection-pooling)
