# Dashboard Error Fix

## ✅ Error Fixed!

**Error**: `Query data cannot be undefined. Affected query key: ["dashboard-deadlines"]`

**Root Cause**: API response structure mismatch

---

## 🔍 What Was Wrong

### The Problem

**Backend API returns:**
```json
{
  "count": 1,
  "benefits": [...]
}
```

**Frontend code expected:**
```json
{
  "results": [...]
}
```

**Result**: `response.data.results` was `undefined` → TanStack Query error

---

## ✅ The Fix

**File**: `/Users/CWU/Documents/card_tracker/frontend/lib/api.ts`

**Before:**
```typescript
export const getDashboardDeadlines = async (): Promise<DashboardDeadline[]> => {
  const response = await apiClient.get<{ results: DashboardDeadline[] }>('/dashboard/deadlines/');
  return response.data.results;  // ❌ undefined!
};
```

**After:**
```typescript
export const getDashboardDeadlines = async (): Promise<DashboardDeadline[]> => {
  const response = await apiClient.get<{ benefits: DashboardDeadline[] }>('/dashboard/deadlines/');
  return response.data.benefits || [];  // ✅ Returns array or empty array
};
```

**Changes:**
1. Changed `results` → `benefits` to match API response
2. Added `|| []` fallback for safety (returns empty array if null/undefined)

---

## 🧪 How to Verify the Fix

### Test 1: Check Dashboard (Browser)

```bash
# 1. Reload dashboard page
open http://localhost:3000/dashboard

# 2. Open DevTools Console (F12)
# ✅ Expected: No "Query data cannot be undefined" error

# 3. Check Network tab
# Click "deadlines" request
# ✅ Expected: See response with "benefits" array
```

### Test 2: Check API Directly (Terminal)

```bash
# Generate a token if needed
cd /Users/CWU/Documents/card_tracker/backend
TOKEN=$(uv run python manage.py shell -c "
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
user = User.objects.get(username='demo_user')
print(RefreshToken.for_user(user).access_token)
")

# Test deadlines endpoint
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/dashboard/deadlines/ | jq

# ✅ Expected: JSON with "count" and "benefits" array
```

### Test 3: Check Console (Browser DevTools)

```javascript
// In browser console:
localStorage.getItem('access_token')
// ✅ Should show your JWT token

// Try fetching deadlines manually:
fetch('http://localhost:8000/api/dashboard/deadlines/', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
})
.then(r => r.json())
.then(data => console.log('Deadlines:', data));

// ✅ Expected: Object with "benefits" array
```

---

## 🎯 What Should Happen Now

### Dashboard Page Behavior

**Before the fix:**
- ❌ Console error: "Query data cannot be undefined"
- ❌ Deadlines section might not render
- ❌ React Query shows warning

**After the fix:**
- ✅ No console errors
- ✅ Deadlines section renders (shows "No urgent deadlines" if empty)
- ✅ Shows 1 warning deadline if you have expiring benefits

---

## 📊 API Response Examples

### Deadlines Endpoint

**Request:**
```
GET /api/dashboard/deadlines/
Authorization: Bearer <token>
```

**Response:**
```json
{
  "count": 1,
  "benefits": [
    {
      "id": 14,
      "benefit_template": {
        "id": 5,
        "name": "Entertainment Credit",
        "description": "$20/month credit",
        "amount_cents": 2000,
        "frequency": "monthly",
        "period_type": "calendar_year",
        "category": "entertainment"
      },
      "effective_name": "Entertainment Credit",
      "effective_amount_cents": 2000,
      "usage_records": [],
      "used_amount_cents": 0,
      "remaining_amount_cents": 2000,
      "current_period_start": "2026-02-01",
      "current_period_end": "2026-02-28",
      "urgency": "warning",
      "days_until_expiry": 11
    }
  ]
}
```

### Summary Endpoint (No issues)

**Request:**
```
GET /api/dashboard/summary/
Authorization: Bearer <token>
```

**Response:**
```json
{
  "total_cards": 2,
  "total_benefits": 6,
  "total_credits_available_cents": 47000,
  "total_credits_used_cents": 6500,
  "total_credits_total_cents": 53500,
  "critical_benefits": 0,
  "warning_benefits": 1,
  "utilization_rate": 12.1
}
```

---

## 🔍 Related Queries to Check

While fixing this, I should verify other queries don't have the same issue:

### Check These Files:

**lib/api.ts - All API functions:**
- ✅ `getDashboardSummary` - Returns flat object (no wrapper)
- ✅ `getDashboardDeadlines` - **FIXED** - Now uses `benefits`
- ✅ `getCardTemplates` - Uses `results` (paginated)
- ✅ `getUserCards` - Uses `results` (paginated)

**Pagination Pattern:**
Some endpoints DO use `results` correctly:
```typescript
// This is correct for paginated endpoints
{
  count: 20,
  next: null,
  previous: null,
  results: [...]
}
```

**Non-paginated endpoints:**
The dashboard deadlines endpoint doesn't follow pagination pattern - it uses `benefits` directly.

---

## ✅ Verification Checklist

After applying the fix:

- [ ] Reload dashboard page (http://localhost:3000/dashboard)
- [ ] Open DevTools console (F12)
- [ ] Verify NO error: "Query data cannot be undefined"
- [ ] Check deadlines section renders
- [ ] Verify deadline badges show (if you have expiring benefits)
- [ ] Check Network tab shows successful API call
- [ ] Verify response has "benefits" array in it

---

## 🚀 Quick Test Script

Run this to verify everything works:

```bash
#!/bin/bash

echo "🧪 Testing Dashboard Deadlines Fix..."
echo ""

# Get token
cd /Users/CWU/Documents/card_tracker/backend
TOKEN=$(uv run python manage.py shell -c "
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
user = User.objects.get(username='demo_user')
print(RefreshToken.for_user(user).access_token)
" 2>/dev/null | tail -1)

echo "✅ Token generated"
echo ""

# Test API
echo "📡 Testing /api/dashboard/deadlines/ endpoint..."
RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/dashboard/deadlines/)

echo "$RESPONSE" | jq

# Check if benefits key exists
if echo "$RESPONSE" | jq -e '.benefits' > /dev/null 2>&1; then
  COUNT=$(echo "$RESPONSE" | jq '.benefits | length')
  echo ""
  echo "✅ API returns 'benefits' array with $COUNT items"
else
  echo ""
  echo "❌ ERROR: API doesn't return 'benefits' array"
  exit 1
fi

echo ""
echo "🎉 Fix verified! Dashboard should work now."
echo ""
echo "Next: Open http://localhost:3000/dashboard and check console"
```

Save as `test-dashboard-fix.sh`, make executable, and run:
```bash
chmod +x test-dashboard-fix.sh
./test-dashboard-fix.sh
```

---

## 💡 Why This Happened

**Root Cause**: Backend and frontend were developed by separate agents in parallel. The integration agent missed this specific API response structure mismatch.

**The backend** uses Django's custom response format for deadlines:
```python
# Backend returns:
return Response({
    'count': len(benefits),
    'benefits': serializer.data
})
```

**The frontend** assumed standard DRF pagination format:
```typescript
// Frontend expected standard DRF format:
{ results: [...] }
```

**Lesson**: Always verify API response structures match TypeScript interfaces, especially after parallel development.

---

## ✅ Status

**Error**: ✅ **FIXED**

**File Changed**: `frontend/lib/api.ts` (line 140-141)

**Testing**: ✅ **API verified working**

**Next Step**: Reload dashboard in browser to confirm fix

---

**The dashboard should now load without errors!** 🎉
