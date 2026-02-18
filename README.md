# Credit Card Benefits Tracker

A web application to track credit card benefits and credits (Uber, dining, travel credits, etc.) with smart deadline tracking and usage monitoring.

## Features

- **Card Management**: Add and manage multiple credit cards
- **Benefit Tracking**: Track monthly/quarterly/semi-annual/annual benefits
- **Smart Deadlines**: Color-coded alerts for expiring benefits (red ≤3 days, orange ≤7 days, yellow ≤14 days)
- **Period Types**: Supports both calendar year and membership year tracking
- **Usage History**: Record partial usage and see remaining amounts with progress bars
- **AI-Powered**: Gemini 2.5 Flash integration for auto-populating unknown card benefits
- **OAuth Login**: Secure Google and Apple sign-in

## Architecture

- **Backend**: Django 5 + Django REST Framework (Python)
- **Frontend**: Next.js 15 + TypeScript + Tailwind CSS
- **Database**: Supabase PostgreSQL
- **Auth**: django-allauth + NextAuth.js
- **Hosting**: Render (backend) + Vercel (frontend) — **100% free tier**

## Project Structure

```
card_tracker/
├── backend/          # Django REST API
│   ├── card_tracker/ # Project settings
│   ├── cards/        # Main app (models, views, services)
│   └── CLAUDE.md     # Backend development guide
├── frontend/         # Next.js frontend
│   ├── src/
│   │   ├── app/      # Pages (App Router)
│   │   ├── components/
│   │   └── lib/
│   └── CLAUDE.md     # Frontend development guide
└── README.md
```

## Getting Started

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_cards  # Load popular card data
python manage.py runserver 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev  # Runs on localhost:3000
```

## Tech Stack

| Component | Technology | Cost |
|-----------|-----------|------|
| Backend | Django 5 + DRF | Free |
| Frontend | Next.js 15 + TypeScript | Free |
| Database | Supabase PostgreSQL | Free (500MB) |
| Auth | django-allauth + NextAuth.js | Free |
| AI | Gemini 2.5 Flash | Free tier |
| Backend Hosting | Render | Free tier |
| Frontend Hosting | Vercel | Free tier |
| **Total** | | **$0** |

## Deployment

The app is ready for production deployment to **100% free tier** hosting:

### Quick Start Deployment

1. **Database** (Supabase): See `DEPLOYMENT_SUPABASE.md`
2. **Backend** (Render): See `DEPLOYMENT_RENDER.md`
3. **Frontend** (Vercel): See `DEPLOYMENT_VERCEL.md`
4. **Verify**: Follow `DEPLOYMENT_CHECKLIST.md`

### Deployment Documentation

| Guide | Description |
|-------|-------------|
| `DEPLOYMENT_SUPABASE.md` | Set up PostgreSQL database on Supabase |
| `DEPLOYMENT_RENDER.md` | Deploy Django backend to Render |
| `DEPLOYMENT_VERCEL.md` | Deploy Next.js frontend to Vercel |
| `ENVIRONMENT_VARIABLES.md` | Complete reference for all env vars |
| `DEPLOYMENT_CHECKLIST.md` | Step-by-step deployment verification |
| `TROUBLESHOOTING.md` | Common issues and solutions |
| `OPERATIONS.md` | Day-to-day maintenance and monitoring |

### Production Architecture

```
┌─────────────────┐
│   Vercel CDN    │  Next.js Frontend (Free Tier)
│  (Global Edge)  │  - Instant loading
└────────┬────────┘  - Auto-scaling
         │
         │ HTTPS/API
         ▼
┌─────────────────┐
│  Render.com     │  Django REST API (Free Tier)
│  Web Service    │  - JWT authentication
└────────┬────────┘  - Auto-deploy on push
         │
         │ PostgreSQL
         ▼
┌─────────────────┐
│   Supabase      │  PostgreSQL Database (Free Tier)
│   PostgreSQL    │  - 500MB storage
└─────────────────┘  - Connection pooling
```

**Estimated Costs**: $0/month (free tier for personal use)

---

## Future: iOS App

The architecture is designed for future iOS app development via **React Native (Expo)**, which will consume the same Django API with no backend changes needed.

## Development

See `backend/CLAUDE.md` and `frontend/CLAUDE.md` for detailed development guidelines and conventions.

## Operations & Monitoring

After deployment, see `OPERATIONS.md` for:
- Monitoring service health
- Viewing logs
- Database maintenance
- Adding new cards
- Backup strategies
- Performance optimization
