import axios, { AxiosError } from 'axios';
import type {
  CardTemplate,
  UserCard,
  CardDetailResponse,
  UserBenefit,
  BenefitUsage,
  DashboardSummary,
  DashboardDeadline,
  MonthlyOverviewBenefit,
  CardSearchParams,
  AddCardRequest,
  UpdateCardRequest,
  RecordUsageRequest,
  ErrorResponse,
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Create axios instance
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use(
  (config) => {
    // Get token from localStorage (set after OAuth)
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle token refresh on 401
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<ErrorResponse>) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && originalRequest) {
      // Try to refresh token
      const refreshToken = localStorage.getItem('refresh_token');

      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
            refresh: refreshToken,
          });

          const { access } = response.data;
          localStorage.setItem('access_token', access);

          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return apiClient(originalRequest);
        } catch (refreshError) {
          // Refresh failed, clear tokens and redirect to login
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          if (typeof window !== 'undefined') {
            window.location.href = '/login';
          }
          return Promise.reject(refreshError);
        }
      }
    }

    return Promise.reject(error);
  }
);

// API functions

// Card Templates
export const searchCardTemplates = async (params: CardSearchParams): Promise<CardTemplate[]> => {
  const response = await apiClient.get<{ results: CardTemplate[] }>('/card-templates/', { params });
  return response.data.results;
};

export const lookupCardWithAI = async (bank: string, cardName: string): Promise<CardTemplate> => {
  // Pass create:true so the backend persists the CardTemplate and returns a real `card_id`.
  // Response shape: { success, card_id, card_data: { bank, name, annual_fee_cents, benefits } }
  const response = await apiClient.post<{
    success: boolean;
    card_id: number;
    card_data: {
      bank: string;
      name: string;
      annual_fee_cents: number;
      benefits?: Array<{
        id?: number;
        name: string;
        description: string;
        amount_cents: number;
        frequency: string;
        period_type: string;
        category: string;
      }>;
    };
  }>('/card-lookup/', { bank, card_name: cardName, create: true });

  const { card_id, card_data } = response.data;

  // Map to CardTemplate shape so the rest of the UI can treat it uniformly.
  return {
    id: card_id,
    bank: card_data.bank,
    name: card_data.name,
    annual_fee_cents: card_data.annual_fee_cents,
    image_url: null,
    is_verified: false,
    benefits: (card_data.benefits ?? []).map((b, idx) => ({
      id: b.id ?? idx,
      card_template: card_id,
      name: b.name,
      description: b.description,
      amount_cents: b.amount_cents,
      frequency: b.frequency as import('@/types').Frequency,
      period_type: b.period_type as import('@/types').PeriodType,
      category: b.category as import('@/types').BenefitCategory,
      created_at: '',
      updated_at: '',
    })),
  };
};

// User Cards
export const getUserCards = async (): Promise<UserCard[]> => {
  const response = await apiClient.get<{ results: UserCard[] }>('/cards/');
  return response.data.results;
};

export const getCardDetail = async (cardId: number): Promise<CardDetailResponse> => {
  const response = await apiClient.get<CardDetailResponse>(`/cards/${cardId}/`);
  return response.data;
};

export const addCard = async (data: AddCardRequest): Promise<UserCard> => {
  const response = await apiClient.post<UserCard>('/cards/', data);
  return response.data;
};

export const updateCard = async (cardId: number, data: UpdateCardRequest): Promise<UserCard> => {
  const response = await apiClient.patch<UserCard>(`/cards/${cardId}/`, data);
  return response.data;
};

export const deleteCard = async (cardId: number): Promise<void> => {
  await apiClient.delete(`/cards/${cardId}/`);
};

// Benefits
export const recordBenefitUsage = async (
  benefitId: number,
  data: RecordUsageRequest
): Promise<BenefitUsage> => {
  const response = await apiClient.post<BenefitUsage>(`/benefits/${benefitId}/use/`, data);
  return response.data;
};

export const undoBenefitUsage = async (benefitId: number, usageId: number): Promise<void> => {
  await apiClient.delete(`/benefits/${benefitId}/usage/${usageId}/`);
};

// Dashboard
export const getDashboardSummary = async (): Promise<DashboardSummary> => {
  const response = await apiClient.get<DashboardSummary>('/dashboard/summary/');
  return response.data;
};

export const getDashboardDeadlines = async (): Promise<DashboardDeadline[]> => {
  const response = await apiClient.get<{ benefits: DashboardDeadline[] }>('/dashboard/deadlines/');
  return response.data.benefits || [];
};

export const getMonthlyOverview = async (): Promise<MonthlyOverviewBenefit[]> => {
  const response = await apiClient.get<MonthlyOverviewBenefit[]>('/dashboard/monthly-overview/');
  return response.data;
};
