# Card Tracker — Frontend (Next.js + TypeScript)

## Overview
React/TypeScript frontend for the Credit Card Benefits Tracker app.
Consumes REST API from the Django backend.

## Tech Stack
- Next.js 15 (App Router), TypeScript, React 19
- Tailwind CSS + shadcn/ui
- NextAuth.js v5 (Google/Apple OAuth)
- TanStack Query (mutations, optimistic updates)
- Axios or fetch for API calls

## Project Structure
- src/app/ — Pages and layouts (App Router)
- src/components/ui/ — shadcn/ui primitives
- src/components/layout/ — Sidebar, Topbar
- src/components/cards/ — CardGrid, CardItem, AddCardDialog
- src/components/benefits/ — BenefitRow, ProgressBar, DeadlineBadge
- src/components/dashboard/ — SummaryCards, DeadlineList, MonthlyOverview
- src/lib/ — api.ts, auth.ts, utils.ts
- src/types/ — TypeScript interfaces matching API responses

## Key Commands
- npm install
- npm run dev  (runs on localhost:3000)
- npm run build
- npm run lint

## API Contract
Backend runs on localhost:8000. All API calls go to NEXT_PUBLIC_API_URL.
Auth: JWT token stored after OAuth flow, sent as Bearer header.

## Conventions
- All amounts from API are in cents — display with formatCurrency() util
- Deadline urgency: critical (≤3 days), warning (≤7), upcoming (≤14), ok (>14)
- Use shadcn/ui components for all UI primitives
- Use TanStack Query for all API mutations (mark usage, add/remove cards)
- Server Components for initial data loading where possible

## Pages

### Landing (`/`)
Marketing page with feature highlights and sign-in CTAs.

### Login (`/login`)
Google/Apple OAuth sign-in buttons.

### Dashboard (`/dashboard`)
Summary cards (total fees, benefit value, net value).
Action-needed deadlines with color-coded badges.
Current month benefits grid with checkmarks.

### My Cards (`/cards`)
Card grid grouped by bank.
"Add Card" button with search.

### Add Card (`/cards/add`)
Search autocomplete for card templates.
Select card → enter open date → save.

### Card Detail (`/cards/[id]`)
Card info header (bank, name, open date, fee).
Benefits table with progress bars.
"Use" button for each benefit.
Usage history with undo.

### All Benefits (`/benefits`)
Filterable/sortable table of all benefits across cards.
Filter by card, category, status.

### Settings (`/settings`)
User preferences and notifications.

## TypeScript Interfaces

Match the backend API responses:
- CardTemplate: bank, name, annual_fee_cents, image_url
- BenefitTemplate: name, amount_cents, frequency, period_type, category
- UserCard: card_template data, open_date, nickname, is_active
- UserBenefit: benefit_template data, custom overrides, remaining amount
- BenefitUsage: amount_cents, used_at, period_start, period_end, note
