// TypeScript interfaces matching backend API responses

// Card Templates
export interface CardTemplate {
  id: number;
  bank: string;
  name: string;
  annual_fee_cents: number;
  image_url: string | null;
  is_verified: boolean;
  benefit_count?: number;
  benefits?: BenefitTemplate[];
  created_at?: string;
  updated_at?: string;
}

// Benefit Templates
export type Frequency = 'monthly' | 'quarterly' | 'semi_annual' | 'annual';
export type PeriodType = 'calendar_year' | 'membership_year';
export type BenefitCategory = 'travel' | 'dining' | 'entertainment' | 'shopping' | 'transportation' | 'other';

export interface BenefitTemplate {
  id: number;
  card_template: number;
  name: string;
  description: string;
  amount_cents: number;
  frequency: Frequency;
  period_type: PeriodType;
  category: BenefitCategory;
  created_at: string;
  updated_at: string;
}

// User Cards
export interface UserCard {
  id: number;
  user: number;
  card_template: CardTemplate;
  open_date: string; // ISO date string
  nickname: string | null;
  card_type: 'personal' | 'business';
  credit_limit_cents: number | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// User Benefits
export interface UserBenefit {
  id: number;
  user_card: number;
  benefit_template: BenefitTemplate;
  custom_amount_cents: number | null;
  custom_name: string | null;
  effective_name?: string;
  effective_amount_cents?: number;
  usage_records?: BenefitUsage[];
  created_at?: string;
  updated_at?: string;
  // Computed fields from API
  remaining_amount_cents?: number;
  used_amount_cents?: number;
  progress_percentage?: number;
  current_period_start?: string;
  current_period_end?: string;
  days_until_deadline?: number;
  deadline_urgency?: 'critical' | 'warning' | 'upcoming' | 'ok';
}

// Benefit Usage
export interface BenefitUsage {
  id: number;
  user_benefit: number;
  amount_cents: number;
  used_at: string; // ISO datetime string
  period_start: string; // ISO date string
  period_end: string; // ISO date string
  note: string | null;
  created_at: string;
}

// API Request/Response types

export interface CardSearchParams {
  q?: string;
  limit?: number;
}

export interface AddCardRequest {
  card_template_id: number;
  open_date: string; // ISO date string
  nickname?: string;
  card_type?: 'personal' | 'business';
  credit_limit_cents?: number;
}

export interface UpdateCardRequest {
  open_date?: string;
  nickname?: string;
  card_type?: 'personal' | 'business';
  credit_limit_cents?: number | null;
  is_active?: boolean;
}

export interface RecordUsageRequest {
  amount_cents: number;
  used_at?: string; // ISO datetime string, defaults to now
  note?: string;
}

// Dashboard Summary
export interface DashboardSummary {
  total_cards: number;
  personal_cards: number;
  business_cards: number;
  total_benefits: number;
  total_annual_fee_cents: number;
  total_credits_available_cents: number;
  total_credits_used_cents: number;
  total_credits_total_cents: number;
  critical_benefits: number;
  warning_benefits: number;
  utilization_rate: number;
}

// Dashboard Deadline
// The backend serializes urgency as `deadline_urgency` (source='urgency') and
// days remaining as `days_until_deadline` (source='days_until_expiry') via
// UserBenefitSerializer.
export interface DashboardDeadline extends UserBenefit {
  card_name: string;
  card_issuer: string;
}

// Card Detail Response
export interface CardDetailResponse extends UserCard {
  benefits: UserBenefit[];
}

// Monthly Overview
export interface MonthlyOverviewBenefit {
  id: number;
  name: string;
  card_name: string;
  frequency: Frequency;
  amount_cents: number;
  used_amount_cents: number;
  remaining_amount_cents: number;
  current_period_start: string;
  current_period_end: string;
  is_fully_used: boolean;
}

// Error Response
export interface ErrorResponse {
  detail?: string;
  [key: string]: any;
}

// Auth
export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  profile_picture?: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
  user: User;
}
