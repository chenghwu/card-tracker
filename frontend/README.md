# Card Tracker Frontend

A modern, mobile-responsive React/Next.js application for tracking credit card benefits and deadlines.

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **UI Components**: shadcn/ui
- **State Management**: TanStack Query (React Query)
- **Authentication**: NextAuth.js v5 (OAuth)
- **Icons**: Lucide React
- **Notifications**: Sonner (Toast notifications)
- **Theme**: next-themes (Light/Dark mode support)

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000` (or configure `NEXT_PUBLIC_API_URL`)

### Installation

```bash
npm install
```

### Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key-here

# OAuth Providers (optional for development)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
APPLE_CLIENT_ID=your-apple-client-id
APPLE_CLIENT_SECRET=your-apple-client-secret
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm run start
```

### Linting

```bash
npm run lint
```

## Features Implemented

### ✓ Phase 1-5: Core Functionality
- Next.js 15 with TypeScript and Tailwind CSS
- Authentication flow with mock OAuth
- Dashboard with summary cards and deadline alerts
- Card management (add, view, delete)
- Benefit tracking with usage recording
- All pages working with proper layouts

### ✓ Phase 6: Polish & UX Enhancements
- **Mobile Responsive**: Collapsible sidebar, responsive grids, optimized layouts
- **Loading States**: Skeleton loaders for all data-heavy components
- **Toast Notifications**: Success/error feedback using Sonner
- **Error Handling**: Custom 404 and error pages, user-friendly messages
- **Settings Page**: Theme toggle, account management, notification preferences
- **Accessibility**: ARIA labels, keyboard navigation, focus states
- **Animations**: Smooth transitions, hover effects, fade-in animations
- **SEO**: Meta tags, OpenGraph, Twitter cards

## Project Structure

```
frontend/
├── app/                      # Next.js App Router pages
│   ├── dashboard/           # Dashboard with loading states
│   ├── cards/               # Card management
│   │   ├── [id]/           # Card detail page
│   │   └── loading.tsx     # Cards loading skeleton
│   ├── benefits/           # All benefits view
│   ├── settings/           # User settings with theme toggle
│   ├── layout.tsx          # Root layout with SEO meta
│   ├── not-found.tsx       # Custom 404 page
│   ├── error.tsx           # Global error boundary
│   └── globals.css         # Global styles with animations
├── components/
│   ├── ui/                 # shadcn/ui components
│   ├── layout/             # Layout components
│   │   ├── main-layout.tsx
│   │   ├── sidebar.tsx     # Desktop & mobile responsive
│   │   └── topbar.tsx      # With mobile menu trigger
│   ├── cards/              # Card components
│   │   ├── card-grid-skeleton.tsx
│   │   └── ...
│   ├── benefits/           # Benefit components
│   └── dashboard/          # Dashboard components
│       ├── summary-cards-skeleton.tsx
│       └── ...
├── lib/
│   ├── api.ts              # API client
│   ├── utils.ts            # Utility functions
│   └── providers.tsx       # Query & Theme providers
└── types/
    └── index.ts            # TypeScript types
```

## Key Features

### Mobile Responsive Design
- Hamburger menu with slide-out sidebar on mobile
- Single-column layouts on small screens
- Touch-friendly 44px minimum tap targets
- Responsive typography and spacing

### Loading States
- Skeleton loaders for cards, dashboard, and lists
- Page-level loading with `loading.tsx` files
- Inline spinners for mutations

### Toast Notifications
```tsx
import { toast } from 'sonner';

toast.success('Card added successfully');
toast.error('Failed to add card');
```

### Theme Support
```tsx
import { useTheme } from 'next-themes';

const { theme, setTheme } = useTheme();
setTheme('light' | 'dark' | 'system');
```

### Accessibility
- Proper ARIA labels
- Keyboard navigation
- Focus indicators
- WCAG AA color contrast

## API Integration

Using TanStack Query for data fetching:

```tsx
import { useQuery, useMutation } from '@tanstack/react-query';

const { data, isLoading, error } = useQuery({
  queryKey: ['user-cards'],
  queryFn: getUserCards,
});

const mutation = useMutation({
  mutationFn: addCard,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['user-cards'] });
    toast.success('Card added!');
  },
});
```

## Deployment

### Vercel (Recommended)

```bash
vercel
```

Set environment variables in Vercel dashboard.

### Docker

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
EXPOSE 3000
CMD ["npm", "start"]
```

## Testing Checklist

- [ ] Test on mobile (320px, 375px, 768px)
- [ ] Test on desktop (1024px, 1440px)
- [ ] Test light and dark themes
- [ ] Test all CRUD operations
- [ ] Test error states
- [ ] Test loading states
- [ ] Test keyboard navigation
- [ ] Run Lighthouse audit

## Troubleshooting

### API Connection Issues
```bash
curl http://localhost:8000/health/
```

### Build Errors
```bash
rm -rf .next node_modules
npm install
npm run build
```

## Contributing

1. Follow existing code structure
2. Use TypeScript for all files
3. Add loading and error states
4. Test mobile responsiveness
5. Ensure accessibility

See [CLAUDE.md](./CLAUDE.md) for detailed development guide.

## License

MIT
