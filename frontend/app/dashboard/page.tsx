'use client';

import { useQuery } from '@tanstack/react-query';
import { MainLayout } from '@/components/layout/main-layout';
import { SummaryCards } from '@/components/dashboard/summary-cards';
import { SummaryCardsSkeleton } from '@/components/dashboard/summary-cards-skeleton';
import { DeadlineList } from '@/components/dashboard/deadline-list';
import { MonthlyOverview } from '@/components/dashboard/monthly-overview';
import { getDashboardSummary, getDashboardDeadlines, getMonthlyOverview } from '@/lib/api';
import { Alert, AlertDescription } from '@/components/ui/alert';

export default function DashboardPage() {
  const {
    data: summary,
    isLoading: summaryLoading,
    error: summaryError,
  } = useQuery({
    queryKey: ['dashboard-summary'],
    queryFn: getDashboardSummary,
  });

  const {
    data: deadlines,
    isLoading: deadlinesLoading,
    error: deadlinesError,
  } = useQuery({
    queryKey: ['dashboard-deadlines'],
    queryFn: getDashboardDeadlines,
  });

  const {
    data: monthlyData,
    isLoading: monthlyLoading,
    error: monthlyError,
  } = useQuery({
    queryKey: ['monthly-overview'],
    queryFn: getMonthlyOverview,
  });

  const isLoading = summaryLoading || deadlinesLoading;
  const error = summaryError || deadlinesError || monthlyError;

  return (
    <MainLayout>
      <div className="space-y-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground">
            Overview of your credit card benefits and upcoming deadlines
          </p>
        </div>

        {error && (
          <Alert variant="destructive">
            <AlertDescription>
              Failed to load dashboard data. Please try again later.
            </AlertDescription>
          </Alert>
        )}

        {isLoading ? (
          <>
            <SummaryCardsSkeleton />
            <div className="grid gap-8 lg:grid-cols-2">
              <div className="space-y-4">
                <div className="h-6 w-48 bg-accent animate-pulse rounded" />
                <div className="space-y-2">
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="h-16 bg-accent animate-pulse rounded" />
                  ))}
                </div>
              </div>
              <div className="space-y-4">
                <div className="h-6 w-48 bg-accent animate-pulse rounded" />
                <div className="space-y-2">
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="h-16 bg-accent animate-pulse rounded" />
                  ))}
                </div>
              </div>
            </div>
          </>
        ) : (
          <>
            {summary && <SummaryCards summary={summary} />}
            <div className="grid gap-8 lg:grid-cols-2">
              {deadlines && <DeadlineList deadlines={deadlines} />}
              <MonthlyOverview benefits={monthlyData ?? []} isLoading={monthlyLoading} />
            </div>
          </>
        )}
      </div>
    </MainLayout>
  );
}
