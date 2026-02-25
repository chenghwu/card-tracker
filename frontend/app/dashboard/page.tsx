'use client';

import { useQuery } from '@tanstack/react-query';
import { MainLayout } from '@/components/layout/main-layout';
import { SummaryCards } from '@/components/dashboard/summary-cards';
import { SummaryCardsSkeleton } from '@/components/dashboard/summary-cards-skeleton';
import { DeadlineList } from '@/components/dashboard/deadline-list';
import { DashboardBenefits } from '@/components/dashboard/dashboard-benefits';
import { getDashboardSummary, getDashboardDeadlines } from '@/lib/api';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';

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

  const isLoading = summaryLoading || deadlinesLoading;
  const error = summaryError || deadlinesError;

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
                <Skeleton className="h-6 w-48" />
                {[1, 2, 3].map((i) => (
                  <Skeleton key={i} className="h-16 w-full" />
                ))}
              </div>
              <div className="space-y-4">
                <Skeleton className="h-6 w-48" />
                {[1, 2, 3].map((i) => (
                  <Skeleton key={i} className="h-16 w-full" />
                ))}
              </div>
            </div>
          </>
        ) : (
          <>
            {summary && <SummaryCards summary={summary} />}
            <div className="grid gap-8 lg:grid-cols-2">
              {deadlines && <DeadlineList deadlines={deadlines} />}
              <DashboardBenefits />
            </div>
          </>
        )}
      </div>
    </MainLayout>
  );
}
