# Card Tracker - Integration Testing Guide

**Quick Start Guide for Testing the Frontend ↔ Backend Integration**

---

## Prerequisites

Before testing, ensure both servers are running:

```bash
# Terminal 1 - Backend
cd /Users/CWU/Documents/card_tracker/backend
uv run python manage.py runserver 8000

# Terminal 2 - Frontend
cd /Users/CWU/Documents/card_tracker/frontend
npm run dev
```

Verify servers are up:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

---

## 1. Quick Health Check

### Test Backend is Running

```bash
curl http://localhost:8000/api/health/
```

**Expected Response:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "database": "connected"
}
```

### Test Frontend is Running

Open browser to http://localhost:3000

**Expected:** Landing page with "Card Tracker" branding

---

## 2. Test CORS Configuration

### Check CORS Headers

```bash
curl -I -X GET http://localhost:8000/api/card-templates/ \
  -H "Origin: http://localhost:3000"
```

**Expected Headers:**
```
access-control-allow-origin: http://localhost:3000
access-control-allow-credentials: true
```

If these headers are missing, the frontend cannot communicate with the backend.

---

## 3. Test Public Endpoints (No Auth)

### 3.1 List All Card Templates

```bash
curl -s http://localhost:8000/api/card-templates/ | python3 -m json.tool
```

**Expected:** JSON response with 19 card templates

**Verify:**
- Count: 19
- Each card has: id, bank, name, annual_fee_cents, benefit_count
- Cards include: AmEx Platinum, Chase Sapphire Reserve, etc.

### 3.2 Search Card Templates

```bash
curl -s "http://localhost:8000/api/card-templates/?q=platinum" | python3 -m json.tool
```

**Expected:** Filtered results containing "platinum" in bank or name

### 3.3 Get Single Card Template

```bash
curl -s http://localhost:8000/api/card-templates/1/ | python3 -m json.tool
```

**Expected:** Full details for AmEx Platinum Card with benefits array

---

## 4. Test Authentication Flow

### 4.1 Create Test User & Get Token

```bash
cd /Users/CWU/Documents/card_tracker/backend

uv run python manage.py shell << 'PYTHON'
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# Create or get test user
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'testuser@example.com'}
)

if created:
    user.set_password('testpass123')
    user.save()

# Generate tokens
refresh = RefreshToken.for_user(user)
print(f"Access Token: {refresh.access_token}")
print(f"Refresh Token: {refresh}")
PYTHON
```

**Copy the access token** - you'll need it for the next steps.

### 4.2 Test Protected Endpoint (Without Token)

```bash
curl -s http://localhost:8000/api/cards/
```

**Expected:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

Status: 401 Unauthorized ✅

### 4.3 Test Protected Endpoint (With Token)

Replace `YOUR_TOKEN_HERE` with the token from step 4.1:

```bash
TOKEN="YOUR_TOKEN_HERE"

curl -s -X GET http://localhost:8000/api/cards/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" | python3 -m json.tool
```

**Expected:** List of user's cards (may be empty initially)

Status: 200 OK ✅

---

## 5. Test Card Management Flow

### 5.1 Add a Card

```bash
TOKEN="YOUR_TOKEN_HERE"

curl -s -X POST http://localhost:8000/api/cards/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "card_template_id": 1,
    "open_date": "2025-01-01",
    "nickname": "My Test Card"
  }' | python3 -m json.tool
```

**Expected Response:**
- Status: 201 Created
- Returns full card object with ID
- Includes `benefits` array (5 items for AmEx Platinum)
- Each benefit has: id, benefit_template, effective_amount_cents, usage_records

**Verify:**
- Card created with correct open_date
- 5 UserBenefit instances auto-created
- Each benefit starts with 0 usage

### 5.2 List Cards (After Adding)

```bash
TOKEN="YOUR_TOKEN_HERE"

curl -s -X GET http://localhost:8000/api/cards/ \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

**Expected:**
- Status: 200 OK
- Results array contains newly added card
- Benefit summary shows total credits

### 5.3 Get Card Detail

```bash
TOKEN="YOUR_TOKEN_HERE"
CARD_ID=1  # Use ID from previous response

curl -s -X GET http://localhost:8000/api/cards/$CARD_ID/ \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

**Expected:**
- Full card details with expanded benefits array
- Each benefit shows:
  - remaining_amount_cents
  - current_period_start/end
  - days_until_deadline
  - deadline_urgency (critical/warning/upcoming/ok)

---

## 6. Test Dashboard Endpoints

### 6.1 Dashboard Summary

```bash
TOKEN="YOUR_TOKEN_HERE"

curl -s -X GET http://localhost:8000/api/dashboard/summary/ \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

**Expected Fields:**
```json
{
  "total_cards": 1,
  "total_benefits": 5,
  "total_credits_available_cents": 48500,
  "total_credits_used_cents": 0,
  "total_credits_total_cents": 48500,
  "critical_benefits": 0,
  "warning_benefits": 2,
  "utilization_rate": 0.0
}
```

### 6.2 Dashboard Deadlines

```bash
TOKEN="YOUR_TOKEN_HERE"

curl -s -X GET http://localhost:8000/api/dashboard/deadlines/ \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

**Expected:**
- List of benefits expiring soon
- Each benefit has urgency level
- Sorted by days_until_expiry (ascending)

---

## 7. Test Frontend Integration

### 7.1 Test Landing Page

1. Open: http://localhost:3000
2. Verify: Page loads with branding
3. Click: "Sign In" button
4. Verify: Redirects to /login

### 7.2 Test Login (Mock Auth)

1. Open: http://localhost:3000/login
2. Click: "Continue with Google" button
3. Verify: Sets mock token in localStorage
4. Verify: Redirects to /dashboard

**Check localStorage:**
```javascript
// Open browser console
localStorage.getItem('access_token')
// Should return: "mock_token"
```

### 7.3 Test Cards Page (Without Auth)

1. Clear localStorage: `localStorage.clear()`
2. Open: http://localhost:3000/cards
3. Open browser DevTools → Console
4. Look for error: "Authentication credentials were not provided"

**This is expected** - the page tries to call the API without a valid token.

### 7.4 Test Cards Page (With Real Token)

1. Get a real JWT token (from Section 4.1)
2. Set in localStorage:
   ```javascript
   localStorage.setItem('access_token', 'YOUR_TOKEN_HERE')
   ```
3. Refresh: http://localhost:3000/cards
4. Verify: Page loads without errors
5. Verify: Shows "No cards yet" or lists existing cards

### 7.5 Test Card Search

1. On /cards page, click "Add Card"
2. Type in search box: "platinum"
3. Verify: Search results appear after 300ms delay
4. Verify: Shows AmEx Platinum, Chase Platinum, etc.

**Check Network Tab:**
- Request: `GET /api/card-templates/?q=platinum&limit=10`
- Status: 200 OK
- Response: Array of matching cards

### 7.6 Test Add Card Flow

1. Search for "Platinum"
2. Click on "American Express Platinum Card"
3. Enter open date: 2025-01-01
4. Enter nickname: "My Test Card" (optional)
5. Click "Add Card"

**Expected:**
- Toast notification: "Card added successfully"
- Dialog closes
- Cards page refreshes
- New card appears in list

**Check Network Tab:**
- Request: `POST /api/cards/`
- Body: `{"card_template_id":1,"open_date":"2025-01-01","nickname":"My Test Card"}`
- Status: 201 Created
- Response: Full card object with benefits

### 7.7 Test Dashboard

1. Navigate to: http://localhost:3000/dashboard
2. Verify: Summary cards load with stats
3. Verify: Deadline list shows expiring benefits
4. Verify: Loading skeletons appear briefly

**Check Network Tab (2 parallel requests):**
- `GET /api/dashboard/summary/` - Status: 200
- `GET /api/dashboard/deadlines/` - Status: 200

---

## 8. Test Error Handling

### 8.1 Test Network Error

1. Stop the backend server
2. Refresh /dashboard page
3. Verify: Error alert appears: "Failed to load dashboard data"

### 8.2 Test Invalid Token

1. Set invalid token:
   ```javascript
   localStorage.setItem('access_token', 'invalid_token_123')
   ```
2. Refresh /cards page
3. Verify: API returns 401
4. Verify: Error alert or redirect to login

### 8.3 Test Token Refresh (Advanced)

This requires a real OAuth flow, which isn't implemented yet.

---

## 9. Browser DevTools Checklist

### 9.1 Console Tab

Check for errors:
- ❌ No CORS errors
- ❌ No 404 errors
- ❌ No TypeScript errors
- ✅ API requests succeed

### 9.2 Network Tab

For each API request, verify:
- Request URL: starts with `http://localhost:8000/api/`
- Request Headers: includes `Authorization: Bearer <token>`
- Response Status: 200, 201, or expected error
- Response Headers: includes CORS headers

### 9.3 Application Tab → Local Storage

Verify stored keys:
- `access_token` - JWT token
- `refresh_token` - (if using OAuth)

---

## 10. Integration Test Checklist

Use this checklist to verify the integration:

### Backend API
- [ ] Health check endpoint responds
- [ ] Card templates endpoint returns 19 cards
- [ ] Search works with query parameter
- [ ] Protected endpoints require authentication
- [ ] JWT tokens are accepted
- [ ] CORS headers present for localhost:3000

### Frontend
- [ ] Landing page loads
- [ ] Login page redirects after mock login
- [ ] Cards page fetches data from API
- [ ] Card search calls API with debouncing
- [ ] Add card dialog works end-to-end
- [ ] Dashboard loads summary and deadlines
- [ ] Error alerts appear on failures
- [ ] Loading skeletons shown while fetching

### Integration
- [ ] Frontend can reach backend API
- [ ] CORS allows requests from frontend
- [ ] JWT authentication works
- [ ] API responses match TypeScript types
- [ ] React Query caching works
- [ ] Mutations invalidate cache correctly

---

## 11. Common Issues & Solutions

### Issue: CORS Error

**Symptoms:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
1. Check `CORS_ALLOWED_ORIGINS` in backend settings.py
2. Should include: `http://localhost:3000`
3. Restart backend server after changes

### Issue: 401 Unauthorized

**Symptoms:**
```json
{"detail": "Authentication credentials were not provided."}
```

**Solution:**
1. Check token in localStorage: `localStorage.getItem('access_token')`
2. Get fresh token from backend (Section 4.1)
3. Verify token is being sent in request headers

### Issue: "Cannot connect to backend"

**Symptoms:**
```
Failed to fetch
Network error
```

**Solution:**
1. Verify backend is running on port 8000
2. Check: `curl http://localhost:8000/api/health/`
3. Restart backend if needed

### Issue: "Card templates not loading"

**Symptoms:**
- Empty search results
- "No cards found" message

**Solution:**
1. Check if data is seeded:
   ```bash
   cd backend
   uv run python manage.py seed_cards
   ```
2. Verify 19 cards exist:
   ```bash
   curl http://localhost:8000/api/card-templates/ | grep count
   ```

---

## 12. Manual End-to-End Test Script

Run this complete flow to verify everything works:

```bash
#!/bin/bash

# 1. Check health
echo "1. Testing health endpoint..."
curl -s http://localhost:8000/api/health/ | grep -q "ok" && echo "✅ Backend healthy" || echo "❌ Backend down"

# 2. Check card templates
echo -e "\n2. Testing card templates..."
COUNT=$(curl -s http://localhost:8000/api/card-templates/ | python3 -c "import sys, json; print(json.load(sys.stdin)['count'])")
[ "$COUNT" -eq 19 ] && echo "✅ $COUNT cards seeded" || echo "⚠️  Only $COUNT cards found"

# 3. Create test user and get token
echo -e "\n3. Creating test user and token..."
cd /Users/CWU/Documents/card_tracker/backend
TOKEN=$(uv run python manage.py shell -c "
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
user, _ = User.objects.get_or_create(username='testuser', defaults={'email':'test@example.com'})
print(RefreshToken.for_user(user).access_token)
" 2>/dev/null | tail -1)
echo "✅ Token generated"

# 4. Test authenticated endpoint
echo -e "\n4. Testing authenticated API call..."
RESULT=$(curl -s -w "%{http_code}" -X GET http://localhost:8000/api/cards/ \
  -H "Authorization: Bearer $TOKEN" -o /dev/null)
[ "$RESULT" -eq 200 ] && echo "✅ Authentication works" || echo "❌ Auth failed (HTTP $RESULT)"

# 5. Add a card
echo -e "\n5. Adding test card..."
RESULT=$(curl -s -w "%{http_code}" -X POST http://localhost:8000/api/cards/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"card_template_id":1,"open_date":"2025-01-01"}' -o /dev/null)
[ "$RESULT" -eq 201 ] && echo "✅ Card added" || echo "❌ Add card failed (HTTP $RESULT)"

# 6. Get dashboard
echo -e "\n6. Testing dashboard..."
RESULT=$(curl -s -w "%{http_code}" -X GET http://localhost:8000/api/dashboard/summary/ \
  -H "Authorization: Bearer $TOKEN" -o /dev/null)
[ "$RESULT" -eq 200 ] && echo "✅ Dashboard works" || echo "❌ Dashboard failed (HTTP $RESULT)"

echo -e "\n✅ Integration test complete!"
```

Save as `test_integration.sh` and run:
```bash
chmod +x test_integration.sh
./test_integration.sh
```

---

## 13. Next Steps

After verifying the integration works:

1. **Implement Real OAuth:**
   - Add Google/Apple OAuth credentials
   - Replace mock token with real OAuth flow
   - Test token refresh mechanism

2. **Add E2E Tests:**
   - Install Playwright or Cypress
   - Write automated tests for critical flows
   - Run in CI/CD pipeline

3. **Deploy to Production:**
   - Follow DEPLOYMENT_GUIDE.md
   - Configure production environment variables
   - Test production deployment

4. **Monitor in Production:**
   - Add error tracking (Sentry)
   - Monitor API response times
   - Track user flows

---

## Support

If you encounter issues not covered in this guide:

1. Check backend logs: Terminal running `python manage.py runserver 8000`
2. Check frontend logs: Terminal running `npm run dev`
3. Check browser console: DevTools → Console tab
4. Check network requests: DevTools → Network tab

For specific errors, refer to **TROUBLESHOOTING.md** in the project root.

---

**Last Updated:** February 17, 2026
