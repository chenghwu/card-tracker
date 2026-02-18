import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Format cents to currency string
export function formatCurrency(cents: number): string {
  const dollars = cents / 100;
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(dollars);
}

// Calculate deadline urgency based on days remaining
export function getDeadlineUrgency(daysRemaining: number): 'critical' | 'warning' | 'upcoming' | 'ok' {
  if (daysRemaining <= 3) return 'critical';
  if (daysRemaining <= 7) return 'warning';
  if (daysRemaining <= 14) return 'upcoming';
  return 'ok';
}

// Get badge color variant based on urgency
export function getUrgencyColor(urgency: 'critical' | 'warning' | 'upcoming' | 'ok'): string {
  switch (urgency) {
    case 'critical':
      return 'destructive';
    case 'warning':
      return 'default'; // orange-ish
    case 'upcoming':
      return 'secondary';
    case 'ok':
      return 'outline';
    default:
      return 'outline';
  }
}

// Format date to readable string
// Parses YYYY-MM-DD as local date to avoid UTC timezone shift (e.g. 2026-02-01 showing as Jan 31)
export function formatDate(dateString: string): string {
  const [year, month, day] = dateString.split('-').map(Number);
  const date = new Date(year, month - 1, day);
  return new Intl.DateTimeFormat('en-US', {
    month: 'numeric',
    day: 'numeric',
    year: 'numeric',
  }).format(date);
}

// Format datetime to readable string
export function formatDateTime(dateTimeString: string): string {
  const date = new Date(dateTimeString);
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  }).format(date);
}

// Calculate progress percentage
export function calculateProgress(used: number, total: number): number {
  if (total === 0) return 0;
  return Math.min(Math.round((used / total) * 100), 100);
}

// Get benefit category display name
export function getCategoryDisplayName(category: string): string {
  const categoryMap: Record<string, string> = {
    travel: 'Travel',
    dining: 'Dining',
    rideshare: 'Rideshare',
    streaming: 'Streaming',
    wireless: 'Wireless',
    other: 'Other',
  };
  return categoryMap[category] || category;
}

// Get frequency display name
export function getFrequencyDisplayName(frequency: string, periodType?: string): string {
  if (frequency === 'annual' && periodType) {
    return periodType === 'membership_year' ? 'Annual (Membership Year)' : 'Annual (Calendar Year)';
  }
  const frequencyMap: Record<string, string> = {
    monthly: 'Monthly',
    quarterly: 'Quarterly',
    semi_annual: 'Semi-Annual',
    annual: 'Annual',
  };
  return frequencyMap[frequency] || frequency;
}
