# Quick Start Guide
## Credit Card Benefits Tracker

Get the application running in 5 minutes!

---

## Prerequisites

- **Backend:** Python 3.10+ with `uv` installed
- **Frontend:** Node.js 18+ with `npm` installed

---

## Step 1: Start the Backend (2 minutes)

```bash
# Navigate to backend directory
cd /Users/CWU/Documents/card_tracker/backend

# Start the Django server
uv run python manage.py runserver 8000
```

**Expected output:**
```
Starting development server at http://127.0.0.1:8000/
Django version 5.2.11
✓ 19 card templates loaded
✓ Database ready
```

**Verify:** Visit http://localhost:8000/admin/ in your browser

---

## Step 2: Start the Frontend (2 minutes)

```bash
# Open a new terminal
cd /Users/CWU/Documents/card_tracker/frontend

# Start the Next.js server
npm run dev
```

**Expected output:**
```
▲ Next.js 15.x
- Local: http://localhost:3000
✓ Ready in 2.3s
```

**Verify:** Visit http://localhost:3000 in your browser

---

## Step 3: Get a Test User Token (1 minute)

```bash
# In the backend directory
cd /Users/CWU/Documents/card_tracker/backend

# Get JWT token for test user
uv run python manage.py shell -c "
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
user, _ = User.objects.get_or_create(username='testuser', email='test@example.com')
user.set_password('testpass123')
user.save()
refresh = RefreshToken.for_user(user)
print(f'\nAccess Token: {refresh.access_token}\n')
"
```

**Copy the access token** and save it for the next step.

---

## Step 4: Login to Frontend (30 seconds)

1. Open http://localhost:3000 in your browser
2. Open browser DevTools (press F12)
3. Go to Console tab
4. Paste this code (replace YOUR_TOKEN with the token from Step 3):

```javascript
localStorage.setItem('access_token', 'YOUR_TOKEN_HERE');
window.location.href = '/dashboard';
```

5. You should now see the dashboard!

---

## Testing the Application

### Test Card Search
1. Go to http://localhost:3000/cards
2. Click "Add Card"
3. Search for "Platinum"
4. See 2 results (Amex Platinum cards)

### Test Adding a Card
1. Click on "American Express Platinum Card"
2. Enter open date: 2024-01-15
3. Enter nickname: "My Platinum"
4. Click "Save"
5. Card should appear in your collection

### Test Marking Benefit as Used
1. Click on your card to view details
2. Find the "Uber Cash" benefit ($15/month)
3. Click "Mark as Used"
4. Enter amount: $15.00
5. Click "Submit"
6. Progress bar should update

### Test Dashboard
1. Go to http://localhost:3000/dashboard
2. See summary cards:
   - Total Cards: 1
   - Total Benefits: 5
   - Total Available: $485.00
3. See deadline alerts (if any benefits are expiring soon)

---

## API Testing (Optional)

### Test with curl

```bash
# Get all card templates (no auth required)
curl http://localhost:8000/api/card-templates/

# Search for cards
curl "http://localhost:8000/api/card-templates/?q=platinum"

# Get user cards (auth required)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/cards/

# Get dashboard summary
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/dashboard/summary/
```

---

## Troubleshooting

### Backend won't start
```bash
cd backend
uv sync
uv run python manage.py migrate
uv run python manage.py runserver 8000
```

### Frontend won't start
```bash
cd frontend
npm install
npm run dev
```

### No cards showing up
```bash
cd backend
uv run python manage.py seed_cards
```

### Frontend can't connect to backend
Check that:
1. Backend is running on port 8000
2. Frontend .env.local has: `NEXT_PUBLIC_API_URL=http://localhost:8000/api`
3. No CORS errors in browser console

### Token expired
Generate a new token using Step 3 above.

---

## Project Structure

```
card_tracker/
├── backend/           # Django REST API (port 8000)
│   ├── cards/        # Main app with models, views, serializers
│   ├── manage.py     # Django management script
│   └── db.sqlite3    # SQLite database (19 cards seeded)
│
├── frontend/         # Next.js app (port 3000)
│   ├── app/         # Pages and layouts
│   ├── components/  # React components
│   ├── lib/         # API client
│   └── types/       # TypeScript types
│
└── README.md        # This file
```

---

## Key URLs

| Service | URL | Notes |
|---------|-----|-------|
| Frontend | http://localhost:3000 | Main application |
| Backend API | http://localhost:8000/api | REST API |
| Django Admin | http://localhost:8000/admin | Database management |
| Card Templates | http://localhost:8000/api/card-templates/ | Public endpoint |
| User Cards | http://localhost:8000/api/cards/ | Requires auth |
| Dashboard | http://localhost:8000/api/dashboard/summary/ | Requires auth |

---

## Test User Credentials

**Username:** testuser
**Password:** testpass123
**Email:** test@example.com

Note: OAuth (Google/Apple) not configured yet. Use JWT token method above.

---

## Features to Test

### Working Features
- ✅ Card template search
- ✅ Add card to collection
- ✅ View card details with benefits
- ✅ Mark benefit as used
- ✅ Dashboard summary
- ✅ Deadline tracking
- ✅ Period calculations (monthly, annual, etc.)
- ✅ Progress bars for benefit usage

### Not Yet Implemented
- ⏳ OAuth sign-in (Google/Apple)
- ⏳ User profile editing
- ⏳ Email notifications
- ⏳ Mobile app
- ⏳ AI card lookup (requires Gemini API key)

---

## Documentation

- **Backend README:** `/Users/CWU/Documents/card_tracker/backend/README.md`
- **Frontend README:** `/Users/CWU/Documents/card_tracker/frontend/README.md`
- **Integration Test Report:** `/Users/CWU/Documents/card_tracker/INTEGRATION_TEST_REPORT.md`
- **Fixes Applied:** `/Users/CWU/Documents/card_tracker/INTEGRATION_FIXES_APPLIED.md`

---

## Next Steps

1. ✅ Backend and frontend are running
2. ✅ Test user can login
3. ⏳ Complete the manual testing checklist above
4. ⏳ Configure OAuth credentials (optional)
5. ⏳ Deploy to production

---

## Support

For issues or questions:
1. Check the INTEGRATION_TEST_REPORT.md for detailed test results
2. Check browser console for errors
3. Check terminal output for server errors
4. Verify both servers are running

---

**Status:** ✅ Ready for testing
**Last Updated:** February 17, 2026
**Version:** 1.0
