# Card Tracker — Backend (Django REST Framework)

## Overview
Python API backend for the Credit Card Benefits Tracker app.
Serves REST API consumed by the Next.js frontend.

## Tech Stack
- Python 3.12, Django 5, Django REST Framework
- django-allauth + dj-rest-auth (Google/Apple OAuth, JWT)
- Supabase PostgreSQL
- Gemini 2.5 Flash (card data lookup)

## Project Structure
- card_tracker/ — Django project settings, urls, wsgi
- cards/ — Main app: models, serializers, views, urls
- cards/services/ — Business logic (periods, tracking, deadlines, card_lookup)
- cards/data/ — Curated card seed data
- cards/management/commands/ — seed_cards, send_reminders

## Key Commands
**IMPORTANT: Always use `uv` for dependency management, never use `pip` directly**

- uv sync                           # Install/update dependencies
- uv run python manage.py migrate   # Run migrations
- uv run python manage.py seed_cards  # Populate card templates
- uv run python manage.py runserver 8000  # Start dev server
- uv run python manage.py test      # Run tests

## API Contract
All endpoints under /api/. Returns JSON. Auth via JWT Bearer token.
Frontend runs on localhost:3000 — CORS configured for it.

## Conventions
- All monetary values in cents (integers)
- Amounts: annual_fee_cents, amount_cents, etc.
- Period types: calendar_year, membership_year
- Frequencies: monthly, quarterly, semi_annual, annual
- Soft delete cards via is_active=False

## Database Models

### CardTemplate
Shared card definitions — one per card product.
Fields: bank, name, annual_fee_cents, image_url, is_verified

### BenefitTemplate
Benefit tied to a card template.
Fields: card_template, name, description, amount_cents, frequency, period_type, category

### UserCard
A card owned by a specific user.
Fields: user, card_template, open_date, nickname, is_active

### UserBenefit
User's benefit instance (allows per-user overrides).
Fields: user_card, benefit_template, custom_amount_cents, custom_name

### BenefitUsage
Usage record for a benefit within a specific period.
Fields: user_benefit, amount_cents, used_at, period_start, period_end, note

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/google/` | Google OAuth login, returns JWT |
| POST | `/api/auth/apple/` | Apple OAuth login, returns JWT |
| GET | `/api/card-templates/?q=platinum` | Search card templates |
| POST | `/api/card-lookup/` | Gemini AI lookup for unknown cards |
| GET | `/api/cards/` | List user's cards with benefit summaries |
| POST | `/api/cards/` | Add a card (creates UserCard + UserBenefits) |
| GET | `/api/cards/{id}/` | Card detail with benefits + usage status |
| PATCH | `/api/cards/{id}/` | Update card (open date, nickname) |
| DELETE | `/api/cards/{id}/` | Deactivate card |
| POST | `/api/benefits/{id}/use/` | Record benefit usage |
| DELETE | `/api/benefits/{id}/usage/{uid}/` | Undo usage |
| GET | `/api/dashboard/summary/` | Aggregated stats |
| GET | `/api/dashboard/deadlines/` | Expiring benefits |
