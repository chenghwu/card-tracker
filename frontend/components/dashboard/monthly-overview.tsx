'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Skeleton } from '@/components/ui/skeleton';
import { CheckCircle2, CalendarDays } from 'lucide-react';
import { formatCurrency, calculateProgress, getFrequencyDisplayName } from '@/lib/utils';
import type { MonthlyOverviewBenefit } from '@/types';

interface MonthlyOverviewProps {
  benefits: MonthlyOverviewBenefit[];
  isLoading?: boolean;
}

function MonthlyOverviewSkeleton() {
  return (
    <Card>
      <CardHeader>
        <Skeleton className="h-6 w-32" />
        <Skeleton className="h-4 w-48 mt-1" />
      </CardHeader>
      <CardContent className="space-y-4">
        <Skeleton className="h-2 w-full rounded-full" />
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="flex items-center justify-between gap-3 border-b pb-3 last:border-0 last:pb-0">
              <div className="space-y-1.5 flex-1">
                <Skeleton className="h-4 w-40" />
                <Skeleton className="h-3 w-24" />
                <Skeleton className="h-1.5 w-full rounded-full" />
              </div>
              <Skeleton className="h-4 w-16" />
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

export function MonthlyOverview({ benefits, isLoading = false }: MonthlyOverviewProps) {
  if (isLoading) {
    return <MonthlyOverviewSkeleton />;
  }

  const now = new Date();
  const monthYear = now.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });

  const usedCount = benefits.filter((b) => b.is_fully_used).length;
  const totalCount = benefits.length;
  const overallProgress = calculateProgress(usedCount, totalCount);

  if (totalCount === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <CalendarDays className="h-5 w-5" />
            This Month
          </CardTitle>
          <CardDescription>{monthYear}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <CalendarDays className="h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-sm text-muted-foreground">
              No monthly or periodic benefits this month
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <CalendarDays className="h-5 w-5" />
          This Month
        </CardTitle>
        <CardDescription>
          {monthYear} &mdash; {usedCount} of {totalCount} benefits used
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Overall utilisation progress bar */}
        <div className="space-y-1">
          <Progress value={overallProgress} className="h-2" />
          <p className="text-xs text-muted-foreground text-right">
            {overallProgress}% complete
          </p>
        </div>

        {/* Scrollable list of benefit rows */}
        <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
          {benefits.map((benefit) => {
            const benefitProgress = calculateProgress(
              benefit.used_amount_cents,
              benefit.amount_cents
            );

            return (
              <div
                key={benefit.id}
                className="flex items-center justify-between gap-3 border-b pb-3 last:border-0 last:pb-0"
              >
                {/* Left: name, card, progress */}
                <div className="space-y-1 min-w-0 flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <p className="font-medium text-sm truncate">{benefit.name}</p>
                    <Badge variant="outline" className="text-xs shrink-0">
                      {getFrequencyDisplayName(benefit.frequency)}
                    </Badge>
                  </div>
                  <p className="text-xs text-muted-foreground truncate">{benefit.card_name}</p>
                  {!benefit.is_fully_used && (
                    <Progress value={benefitProgress} className="h-1.5 mt-1" />
                  )}
                </div>

                {/* Right: remaining amount or checkmark */}
                <div className="flex flex-col items-end shrink-0 gap-1">
                  {benefit.is_fully_used ? (
                    <CheckCircle2 className="h-5 w-5 text-green-500" />
                  ) : (
                    <span className="text-sm font-medium whitespace-nowrap">
                      {formatCurrency(benefit.remaining_amount_cents)} left
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
