# Integration Quick Reference

**Last Updated:** February 17, 2026

---

## 🚀 Quick Start

### Start Servers

```bash
# Terminal 1 - Backend
cd /Users/CWU/Documents/card_tracker/backend
uv run python manage.py runserver 8000

# Terminal 2 - Frontend  
cd /Users/CWU/Documents/card_tracker/frontend
npm run dev
```

### Verify Integration

```bash
# Backend health check
curl http://localhost:8000/api/health/

# Frontend
open http://localhost:3000
```

---

## 🔑 Generate Test Token

```bash
cd backend

uv run python manage.py shell << 'PYTHON'
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

user, _ = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
user.set_password('testpass123')
user.save()

refresh = RefreshToken.for_user(user)
print(f"Access Token: {refresh.access_token}")
PYTHON
```

---

## 🧪 Test API Endpoints

```bash
# Set your token
TOKEN="your_token_here"

# List cards (authenticated)
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/cards/

# Add card
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"card_template_id": 1, "open_date": "2025-01-01"}' \
  http://localhost:8000/api/cards/

# Dashboard summary
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/dashboard/summary/
```

---

## 🌐 Frontend Testing

### Set Token in Browser

```javascript
// Open browser console on localhost:3000
localStorage.setItem('access_token', 'YOUR_TOKEN_HERE')
```

### Test Pages

- Landing: http://localhost:3000
- Login: http://localhost:3000/login
- Dashboard: http://localhost:3000/dashboard
- Cards: http://localhost:3000/cards

---

## 📡 API Endpoints Reference

### Public (No Auth)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health/` | GET | Health check |
| `/api/card-templates/` | GET | List cards |
| `/api/card-templates/?q=search` | GET | Search cards |
| `/api/card-templates/{id}/` | GET | Card detail |

### Protected (JWT Required)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/cards/` | GET | User's cards |
| `/api/cards/` | POST | Add card |
| `/api/cards/{id}/` | GET | Card detail |
| `/api/cards/{id}/` | PATCH | Update card |
| `/api/cards/{id}/` | DELETE | Remove card |
| `/api/dashboard/summary/` | GET | Dashboard stats |
| `/api/dashboard/deadlines/` | GET | Expiring benefits |
| `/api/benefits/{id}/use/` | POST | Record usage |

---

## 🔍 Check CORS

```bash
curl -I \
  -H "Origin: http://localhost:3000" \
  http://localhost:8000/api/card-templates/

# Should see:
# access-control-allow-origin: http://localhost:3000
# access-control-allow-credentials: true
```

---

## 🐛 Quick Troubleshooting

### Backend Not Responding

```bash
# Check if running
lsof -i:8000

# Restart
cd backend
uv run python manage.py runserver 8000
```

### Frontend Not Loading

```bash
# Check if running
lsof -i:3000

# Restart
cd frontend
npm run dev
```

### CORS Errors

Check `backend/card_tracker/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000'
]
```

### 401 Unauthorized

1. Generate new token (see above)
2. Set in localStorage
3. Refresh page

---

## 📊 Integration Status

| Component | Status |
|-----------|--------|
| Backend API | ✅ Working |
| Frontend UI | ✅ Working |
| CORS | ✅ Configured |
| JWT Auth | ✅ Functional |
| Data Flow | ✅ Complete |
| OAuth | ⚠️ Pending |

---

## 📚 Full Documentation

- **TESTING_GUIDE.md** - Complete testing instructions
- **INTEGRATION_STATUS.md** - Detailed status report
- **TROUBLESHOOTING.md** - Common issues
- **README.md** - Project overview

---

## 🎯 Common Tasks

### Seed More Cards

```bash
cd backend
uv run python manage.py seed_cards
```

### Reset Database

```bash
cd backend
rm db.sqlite3
uv run python manage.py migrate
uv run python manage.py seed_cards
```

### View Logs

```bash
# Backend logs - in terminal running runserver
# Frontend logs - in terminal running npm run dev
# Browser logs - DevTools Console
```

### Run Tests

```bash
# Backend
cd backend
uv run python manage.py test

# Frontend (if tests exist)
cd frontend
npm test
```

---

## 🔗 URLs

- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8000
- **API Root:** http://localhost:8000/api/
- **Admin:** http://localhost:8000/admin/

---

## 📞 Need Help?

1. Check browser console for errors
2. Check terminal logs for server errors
3. Check Network tab for API issues
4. Refer to TROUBLESHOOTING.md

---

**Status:** ✅ Fully Integrated and Operational
