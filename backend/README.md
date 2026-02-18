# Card Tracker Backend

Django REST API backend for the Credit Card Benefits Tracker application.

## Tech Stack

- Python 3.10+
- Django 5.2
- Django REST Framework 3.16
- PostgreSQL (Supabase) / SQLite (local dev)
- django-allauth + dj-rest-auth (OAuth & JWT)
- Google Gemini 2.5 Flash (AI card lookup)

## Project Structure

```
backend/
├── card_tracker/          # Django project settings
│   ├── settings.py        # Main settings with DB, CORS, Auth config
│   └── urls.py            # Root URL routing
├── cards/                 # Main application
│   ├── models.py          # 5 core models (CardTemplate, BenefitTemplate, etc.)
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views and viewsets
│   ├── urls.py            # App URL routing
│   ├── admin.py           # Django admin configuration
│   ├── services/          # Business logic
│   │   ├── periods.py     # Period calculation (calendar/membership year)
│   │   ├── tracking.py    # Benefit usage tracking
│   │   ├── deadlines.py   # Urgency and expiration logic
│   │   └── card_lookup.py # Gemini AI integration
│   ├── data/              # Seed data
│   │   └── card_seeds.py  # 19 popular credit cards with benefits
│   └── management/
│       └── commands/
│           └── seed_cards.py  # Management command to seed database
├── .env                   # Environment variables (not in git)
├── .env.example           # Environment variables template
└── requirements.txt       # Python dependencies
```

## Setup Instructions

### 1. Install Dependencies

Using uv (recommended):
```bash
cd backend
uv sync
```

**Note:** Always use `uv` for dependency management. Do not use `pip` directly.

If you don't have `uv` installed:
```bash
# Install uv (one-time setup)
curl -LsSf https://astral.sh/uv/install.sh | sh
# Then restart your terminal
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

**For local development with SQLite:**
- Leave `DB_NAME` empty in `.env`
- No database setup needed!

**For PostgreSQL/Supabase:**
- Set `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

**For OAuth (optional):**
- Set `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`
- Set `APPLE_CLIENT_ID` and `APPLE_CLIENT_SECRET`

**For Gemini AI lookup (optional):**
- Set `GEMINI_API_KEY`

### 3. Run Migrations

```bash
uv run python manage.py migrate
```

### 4. Seed Card Data

Populate database with 19 popular credit cards:

```bash
uv run python manage.py seed_cards
```

### 5. Create Superuser (optional)

```bash
uv run python manage.py createsuperuser
```

### 6. Run Development Server

```bash
uv run python manage.py runserver 8000
```

API will be available at: `http://localhost:8000/api/`

Admin panel: `http://localhost:8000/admin/`

## Database Models

### CardTemplate
Shared card definitions (one per card product).
- `bank`, `name`, `annual_fee_cents`, `image_url`, `is_verified`

### BenefitTemplate
Benefits tied to card templates.
- `card_template`, `name`, `description`, `amount_cents`
- `frequency` (monthly/quarterly/semi_annual/annual)
- `period_type` (calendar_year/membership_year)
- `category` (travel/dining/entertainment/shopping/transportation/other)

### UserCard
A card owned by a specific user.
- `user`, `card_template`, `open_date`, `nickname`, `is_active`

### UserBenefit
User's benefit instance (allows per-user overrides).
- `user_card`, `benefit_template`, `custom_amount_cents`, `custom_name`

### BenefitUsage
Usage record for a benefit within a specific period.
- `user_benefit`, `amount_cents`, `used_at`, `period_start`, `period_end`, `note`

## API Endpoints

### Authentication
- `POST /api/auth/google/` - Google OAuth login
- `POST /api/auth/apple/` - Apple OAuth login
- `POST /api/auth/registration/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### Card Templates
- `GET /api/card-templates/` - List all card templates
- `GET /api/card-templates/?q=platinum` - Search card templates
- `GET /api/card-templates/{id}/` - Get card template details

### Card Management
- `GET /api/cards/` - List user's cards
- `POST /api/cards/` - Add a new card (auto-creates UserBenefits)
- `GET /api/cards/{id}/` - Get card detail with benefits and status
- `PATCH /api/cards/{id}/` - Update card (open_date, nickname)
- `DELETE /api/cards/{id}/` - Deactivate card (soft delete)

### Benefit Tracking
- `POST /api/benefits/{id}/use/` - Record benefit usage
  ```json
  {
    "amount_cents": 5000,
    "used_at": "2024-02-15T10:30:00Z",
    "note": "Used at hotel"
  }
  ```
- `DELETE /api/benefits/{id}/usage/{uid}/` - Undo usage

### Dashboard
- `GET /api/dashboard/summary/` - Get summary statistics
  - Total cards, benefits, credits available/used
  - Critical and warning benefit counts
  - Utilization rate

- `GET /api/dashboard/deadlines/?days=30` - Get expiring benefits
  - Benefits with remaining value expiring within N days
  - Sorted by urgency (critical → warning → upcoming)

### AI Card Lookup (Optional)
- `POST /api/card-lookup/` - Lookup card using Gemini AI
  ```json
  {
    "card_name": "Platinum Card",
    "bank": "American Express",
    "create": true
  }
  ```

## API Conventions

- **All amounts in cents** (integers): `annual_fee_cents`, `amount_cents`
- **Period types**: `calendar_year`, `membership_year`
- **Frequencies**: `monthly`, `quarterly`, `semi_annual`, `annual`
- **Categories**: `travel`, `dining`, `entertainment`, `shopping`, `transportation`, `other`
- **Soft delete**: Cards are deactivated via `is_active=False`, not deleted

## Business Logic Services

### periods.py
Calculates benefit periods based on:
- **Calendar Year**: Jan 1 - Dec 31
- **Membership Year**: Based on card open date anniversary

Handles monthly, quarterly, semi-annual, and annual frequencies.

### tracking.py
- Calculates used/remaining amounts for benefits
- Records benefit usage with period validation
- Prevents overuse (checks remaining amount)
- Supports undo functionality

### deadlines.py
Calculates urgency levels:
- **Critical**: ≤7 days until expiry
- **Warning**: 8-14 days
- **Upcoming**: 15-30 days
- **OK**: 31+ days

### card_lookup.py
Uses Gemini 2.5 Flash to:
- Extract card and benefit information from natural language
- Parse structured data from AI responses
- Create CardTemplate and BenefitTemplate instances
- Mark AI-generated cards as unverified

## Testing

Run tests:
```bash
uv run python manage.py test
```

## Admin Panel

Access Django admin at `/admin/` to:
- View and edit card templates
- Manage benefits
- View user cards and usage
- Moderate AI-generated cards (verify accuracy)

## Production Deployment

### Prerequisites

1. **PostgreSQL Database** (Supabase recommended)
   - Create a new project on [Supabase](https://supabase.com/)
   - Note your connection details (host, database name, password)
   - Supabase provides connection pooling by default

2. **OAuth Credentials**
   - Google OAuth: [Google Cloud Console](https://console.developers.google.com/)
   - Apple OAuth: [Apple Developer Portal](https://developer.apple.com/)

3. **Email Service** (for benefit reminders)
   - Gmail with App Password
   - SendGrid, Mailgun, or other SMTP provider

### Deployment Steps

#### 1. Environment Configuration

Copy `.env.example` to `.env` and configure all production values:

```bash
cp .env.example .env
```

**Critical Settings:**
```env
# Generate a strong secret key (use: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
SECRET_KEY=your-super-secret-key-here

# Production mode
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# PostgreSQL (Supabase)
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-supabase-password
DB_HOST=db.your-project.supabase.co
DB_PORT=5432
DB_CONN_MAX_AGE=600

# OAuth
GOOGLE_CLIENT_ID=your-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-secret
APPLE_CLIENT_ID=com.yourapp.cardtracker
APPLE_CLIENT_SECRET=your-apple-key

# Email
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Security
SECURE_SSL_REDIRECT=True
```

#### 2. Install Dependencies

**IMPORTANT: Always use `uv`, never `pip` directly**

```bash
uv sync
```

#### 3. Run Migrations

```bash
uv run python manage.py migrate
```

#### 4. Seed Card Data

```bash
uv run python manage.py seed_cards
```

#### 5. Collect Static Files

```bash
python manage.py collectstatic --no-input
```

#### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

#### 7. Run with Gunicorn

```bash
gunicorn card_tracker.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

**Recommended Gunicorn Configuration:**
```bash
gunicorn card_tracker.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --threads 2 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
```

### Setting Up Email Reminders

The reminder system sends emails to users about expiring benefits.

#### 1. Test the Reminder Command

Dry run to preview emails without sending:
```bash
uv run python manage.py send_reminders --dry-run
```

Send test email:
```bash
uv run python manage.py send_reminders --test-email your-email@example.com
```

#### 2. Set Up Cron Job

Add to crontab (`crontab -e`):

```cron
# Send benefit reminders daily at 9 AM
0 9 * * * cd /path/to/backend && /path/to/uv run python manage.py send_reminders >> /var/log/card-reminders.log 2>&1
```

**Alternative: Using systemd timer (Linux)**

Create `/etc/systemd/system/card-reminders.service`:
```ini
[Unit]
Description=Send card benefit reminders
After=network.target

[Service]
Type=oneshot
User=youruser
WorkingDirectory=/path/to/backend
ExecStart=/path/to/uv run python manage.py send_reminders
StandardOutput=journal
StandardError=journal
```

Create `/etc/systemd/system/card-reminders.timer`:
```ini
[Unit]
Description=Send card benefit reminders daily

[Timer]
OnCalendar=daily
OnCalendar=09:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start:
```bash
sudo systemctl enable card-reminders.timer
sudo systemctl start card-reminders.timer
```

### OAuth Configuration

#### Google OAuth

1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `https://yourdomain.com/api/auth/google/callback/`
   - `http://localhost:3000/auth/callback` (for local testing)
6. Copy Client ID and Client Secret to `.env`

#### Apple OAuth

Apple OAuth requires more setup:

1. Go to [Apple Developer Portal](https://developer.apple.com/)
2. Create an App ID (e.g., `com.yourapp.cardtracker`)
3. Enable "Sign in with Apple" capability
4. Create a Service ID
5. Configure domains and redirect URLs:
   - Domain: `yourdomain.com`
   - Redirect URL: `https://yourdomain.com/api/auth/apple/callback/`
6. Create a Key for "Sign in with Apple"
7. Download the key file (.p8)

**Generate Client Secret:**

Apple requires generating a JWT token as the client secret. Use this Python script:

```python
import jwt
import time

# Your Apple credentials
team_id = "YOUR_TEAM_ID"
client_id = "com.yourapp.cardtracker"  # Your Service ID
key_id = "YOUR_KEY_ID"  # Key ID from Apple
key_file = "AuthKey_YOUR_KEY_ID.p8"  # Downloaded .p8 file

# Read private key
with open(key_file, 'r') as f:
    key = f.read()

# Generate JWT
headers = {
    "kid": key_id,
    "alg": "ES256"
}

payload = {
    "iss": team_id,
    "iat": int(time.time()),
    "exp": int(time.time()) + 86400 * 180,  # 180 days
    "aud": "https://appleid.apple.com",
    "sub": client_id
}

client_secret = jwt.encode(payload, key, algorithm="ES256", headers=headers)
print(client_secret)
```

Add the generated secret to `.env` as `APPLE_CLIENT_SECRET`.

### API Rate Limiting

The API implements throttling to prevent abuse:

- **Anonymous users**: 20 requests/hour
- **Authenticated users**: 100 requests/hour

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1612345678
```

When rate limited, the API returns `429 Too Many Requests`.

### Health Check Endpoint

Use the health check endpoint for monitoring:

```bash
curl https://yourdomain.com/api/health/
```

Response:
```json
{
  "status": "ok",
  "database": "connected",
  "version": "1.0.0"
}
```

Configure your monitoring service (e.g., UptimeRobot, Pingdom) to check this endpoint every 5 minutes.

### Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` (50+ random characters)
- [ ] HTTPS enabled (`SECURE_SSL_REDIRECT=True`)
- [ ] Secure cookies enabled (automatic when `DEBUG=False`)
- [ ] `ALLOWED_HOSTS` configured with your domain
- [ ] Database credentials stored securely
- [ ] OAuth credentials not committed to git
- [ ] Email credentials stored securely
- [ ] CORS configured for your frontend domain only
- [ ] Regular database backups enabled (Supabase provides automatic backups)
- [ ] Firewall configured (allow only ports 80, 443)
- [ ] Rate limiting enabled (automatic)

### Database Configuration

#### Using Supabase

Supabase provides:
- Automatic backups
- Connection pooling
- SSL connections
- Database monitoring

Connection string format:
```
postgresql://postgres:password@db.project.supabase.co:5432/postgres
```

#### Connection Pooling

The app uses `CONN_MAX_AGE=600` (10 minutes) for connection pooling. This reduces database connection overhead.

For high-traffic deployments, consider using PgBouncer or Supabase's pooler URL.

### Static Files

Static files are served using WhiteNoise middleware. This allows serving static files efficiently without needing a separate web server (nginx/Apache) for static content.

To update static files:
```bash
python manage.py collectstatic --no-input
```

### Logging

Logs are written to:
- Console: INFO level (all requests)
- File: ERROR level (`logs/error.log`)

View logs:
```bash
tail -f logs/error.log
```

Configure log level via environment:
```env
DJANGO_LOG_LEVEL=DEBUG  # For development
DJANGO_LOG_LEVEL=INFO   # For production
```

## Troubleshooting

### Issue: Database connection fails

**Symptoms:**
- `FATAL: password authentication failed`
- `could not connect to server`

**Solutions:**
1. Verify database credentials in `.env`
2. Check if database host is accessible (firewall/network)
3. Test connection manually:
   ```bash
   psql -h your-host -U postgres -d postgres
   ```
4. For Supabase, ensure you're using the correct host (check Supabase dashboard)

### Issue: OAuth login fails

**Symptoms:**
- `invalid_client` error
- `redirect_uri_mismatch` error

**Solutions:**
1. Verify OAuth credentials in `.env`
2. Check authorized redirect URIs in OAuth provider:
   - Google: Should match `https://yourdomain.com/api/auth/google/callback/`
   - Apple: Should match `https://yourdomain.com/api/auth/apple/callback/`
3. Ensure HTTPS is enabled in production
4. Check CORS settings allow your frontend domain

### Issue: Static files not loading

**Symptoms:**
- 404 errors for CSS/JS files
- Admin panel has no styling

**Solutions:**
1. Run `python manage.py collectstatic --no-input`
2. Verify WhiteNoise is installed: `pip install whitenoise`
3. Check `STATIC_ROOT` and `STATIC_URL` settings
4. Ensure WhiteNoise middleware is enabled

### Issue: Email reminders not sending

**Symptoms:**
- `send_reminders` command completes but no emails
- SMTP authentication errors

**Solutions:**
1. Verify email settings in `.env`
2. For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833)
3. Test email configuration:
   ```bash
   python manage.py send_reminders --test-email your-email@example.com
   ```
4. Check email service logs
5. Ensure `EMAIL_USE_TLS=True` for Gmail

### Issue: Rate limiting too restrictive

**Symptoms:**
- Users getting `429 Too Many Requests` errors

**Solutions:**
1. Increase throttle rates in `settings.py`:
   ```python
   'DEFAULT_THROTTLE_RATES': {
       'anon': '50/hour',
       'user': '200/hour',
   }
   ```
2. Consider per-endpoint throttling for expensive operations
3. Implement caching for frequently accessed data

### Issue: High database connection count

**Symptoms:**
- "too many connections" errors
- Slow database queries

**Solutions:**
1. Verify `CONN_MAX_AGE` is set (default: 600 seconds)
2. Use Supabase's connection pooler URL
3. Reduce number of Gunicorn workers if needed
4. Monitor connection usage in Supabase dashboard

### Issue: Slow API responses

**Symptoms:**
- Requests taking >2 seconds
- Timeout errors

**Solutions:**
1. Enable database query logging to identify slow queries
2. Add database indexes for frequently queried fields
3. Implement Redis caching for dashboard stats
4. Increase Gunicorn workers: `--workers 4 --threads 2`
5. Use Supabase's read replicas for read-heavy workloads

## Environment Variables

See `.env.example` for full list. Key variables:

### Django Core
- `SECRET_KEY` - Django secret key (required, 50+ chars)
- `DEBUG` - Debug mode (True/False, default: True)
- `ALLOWED_HOSTS` - Comma-separated hostnames (required in production)
- `DJANGO_LOG_LEVEL` - Logging level (DEBUG/INFO/WARNING/ERROR)

### Database
- `DB_NAME` - Database name (empty for SQLite)
- `DB_USER` - Database user (default: postgres)
- `DB_PASSWORD` - Database password (required for PostgreSQL)
- `DB_HOST` - Database host (required for PostgreSQL)
- `DB_PORT` - Database port (default: 5432)
- `DB_CONN_MAX_AGE` - Connection pooling timeout in seconds (default: 600)

### OAuth
- `GOOGLE_CLIENT_ID` - Google OAuth client ID
- `GOOGLE_CLIENT_SECRET` - Google OAuth client secret
- `APPLE_CLIENT_ID` - Apple Service ID (e.g., com.yourapp.cardtracker)
- `APPLE_CLIENT_SECRET` - Apple client secret (JWT token)

### Email
- `DEFAULT_FROM_EMAIL` - From address for system emails
- `EMAIL_HOST` - SMTP host (default: smtp.gmail.com)
- `EMAIL_PORT` - SMTP port (default: 587)
- `EMAIL_HOST_USER` - SMTP username
- `EMAIL_HOST_PASSWORD` - SMTP password/app password

### Features
- `GEMINI_API_KEY` - Google Gemini API key (optional, for card lookup)

### Security
- `SECURE_SSL_REDIRECT` - Force HTTPS redirect (default: True in production)

## Management Commands

### seed_cards
Populate database with card templates:
```bash
python manage.py seed_cards
```

### send_reminders
Send email reminders about expiring benefits:
```bash
# Dry run (preview only)
python manage.py send_reminders --dry-run

# Send test email
python manage.py send_reminders --test-email your@email.com

# Send real emails
python manage.py send_reminders
```

### Other useful commands
```bash
# Create superuser
python manage.py createsuperuser

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Django shell
python manage.py shell

# Check for issues
python manage.py check
```

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the main project README
- Open an issue on GitHub
