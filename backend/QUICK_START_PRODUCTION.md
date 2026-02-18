# Quick Start: Production Deployment

This is a condensed checklist for deploying the Card Tracker backend to production. For detailed instructions, see `README.md`.

## Pre-Deployment Checklist

- [ ] PostgreSQL database ready (Supabase recommended)
- [ ] Domain name configured with SSL certificate
- [ ] Google OAuth credentials obtained
- [ ] Apple OAuth credentials obtained (optional)
- [ ] Email service configured (Gmail, SendGrid, etc.)
- [ ] Server/hosting ready (VPS, cloud instance, etc.)

## 5-Minute Setup

### 1. Clone and Setup
```bash
git clone <your-repo>
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
nano .env  # Edit with your production values
```

**Critical variables to set:**
```env
SECRET_KEY=<generate-random-50-char-string>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=postgres
DB_HOST=db.your-project.supabase.co
DB_PASSWORD=<your-db-password>
GOOGLE_CLIENT_ID=<your-google-client-id>
GOOGLE_CLIENT_SECRET=<your-google-secret>
EMAIL_HOST_USER=<your-email>
EMAIL_HOST_PASSWORD=<your-email-password>
```

### 3. Initialize Database
```bash
python manage.py migrate
python manage.py seed_cards
python manage.py createsuperuser  # Optional
```

### 4. Collect Static Files
```bash
python manage.py collectstatic --no-input
```

### 5. Test Configuration
```bash
python manage.py check --deploy
python manage.py send_reminders --dry-run
```

### 6. Start Server
```bash
gunicorn card_tracker.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --threads 2 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile -
```

## Post-Deployment

### Setup Monitoring
1. Configure uptime monitor for `https://yourdomain.com/api/health/`
2. Monitor error logs: `tail -f logs/error.log`

### Setup Email Reminders
Add to crontab (`crontab -e`):
```cron
0 9 * * * cd /path/to/backend && python manage.py send_reminders
```

### Verify Everything Works
```bash
# Test health check
curl https://yourdomain.com/api/health/

# Test API
curl https://yourdomain.com/api/card-templates/

# Check logs
tail -f logs/error.log
```

## Common Issues

### Database connection fails
- Verify database credentials in `.env`
- Check firewall allows connection to database
- Test: `psql -h your-host -U postgres -d postgres`

### OAuth not working
- Check redirect URIs in OAuth provider settings
- Verify HTTPS is enabled
- Check CORS settings allow your frontend domain

### Emails not sending
- Use App Password for Gmail (not regular password)
- Test: `python manage.py send_reminders --test-email your@email.com`

### Static files 404
- Run: `python manage.py collectstatic --no-input`
- Verify WhiteNoise is in MIDDLEWARE

## Security Quick Check

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` (50+ characters)
- [ ] HTTPS enabled (SSL certificate)
- [ ] `ALLOWED_HOSTS` set correctly
- [ ] Database password secure
- [ ] OAuth credentials not in git
- [ ] Email credentials secure
- [ ] Firewall configured (ports 80, 443 only)

## Generate Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Systemd Service (Linux)

Create `/etc/systemd/system/cardtracker.service`:
```ini
[Unit]
Description=Card Tracker API
After=network.target

[Service]
Type=notify
User=youruser
WorkingDirectory=/path/to/backend
ExecStart=/path/to/gunicorn card_tracker.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --threads 2
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl enable cardtracker
sudo systemctl start cardtracker
sudo systemctl status cardtracker
```

## Nginx Reverse Proxy

Create `/etc/nginx/sites-available/cardtracker`:
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/cardtracker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Resource Requirements

**Minimum:**
- 1 vCPU
- 1 GB RAM
- 10 GB disk

**Recommended:**
- 2 vCPU
- 2 GB RAM
- 20 GB disk
- PostgreSQL managed service (Supabase)

## Support

For detailed documentation, see:
- `README.md` - Complete documentation
- `PHASE6_POLISH_SUMMARY.md` - Implementation details
- `.env.example` - Environment variable reference

## Quick Commands Reference

```bash
# Management Commands
python manage.py migrate              # Run database migrations
python manage.py seed_cards           # Populate card data
python manage.py send_reminders       # Send email reminders
python manage.py collectstatic        # Collect static files
python manage.py createsuperuser      # Create admin user

# Testing
python manage.py check                # Check for issues
python manage.py check --deploy       # Production readiness check
python manage.py test                 # Run tests

# Utility
python manage.py shell                # Django shell
python manage.py dbshell              # Database shell

# Server
python manage.py runserver            # Development server
gunicorn card_tracker.wsgi:application  # Production server
```

---

**Ready to deploy!** Follow these steps and you'll have a production-ready backend in minutes.
