'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { AlertCircle, Clock } from 'lucide-react';
import { formatCurrency, getUrgencyColor } from '@/lib/utils';
import { UseBenefitDialog } from '@/components/benefits/use-benefit-dialog';
import type { DashboardDeadline, UserBenefit } from '@/types';

interface DeadlineListProps {
  deadlines: DashboardDeadline[];
}

export function DeadlineList({ deadlines }: DeadlineListProps) {
  const [selectedBenefit, setSelectedBenefit] = useState<UserBenefit | null>(null);

  if (deadlines.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Upcoming Deadlines</CardTitle>
          <CardDescription>No urgent benefits requiring attention</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <Clock className="h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-sm text-muted-foreground">
              All your benefits are either used or have plenty of time remaining.
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <AlertCircle className="h-5 w-5" />
            Upcoming Deadlines
          </CardTitle>
          <CardDescription>
            Benefits that need attention ({deadlines.length})
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {deadlines.map((deadline) => {
              const benefit = deadline.benefit_template;
              const remaining = deadline.remaining_amount_cents || 0;

              return (
                <div
                  key={deadline.id}
                  className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b pb-4 last:border-0 last:pb-0"
                >
                  <div className="space-y-1 min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <p className="font-medium text-sm sm:text-base">{deadline.effective_name}</p>
                      <Badge variant={getUrgencyColor(deadline.deadline_urgency ?? 'ok') as any}>
                        {deadline.days_until_deadline}d left
                      </Badge>
                    </div>
                    <p className="text-xs sm:text-sm text-muted-foreground truncate">
                      {deadline.card_name} · {benefit.category || 'Benefit'}
                    </p>
                    <p className="text-sm font-medium">
                      {formatCurrency(remaining)} remaining
                    </p>
                  </div>
                  <Button
                    size="sm"
                    className="w-full sm:w-auto flex-shrink-0"
                    onClick={() => setSelectedBenefit(deadline)}
                  >
                    Use Now
                  </Button>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {selectedBenefit && (
        <UseBenefitDialog
          benefit={selectedBenefit}
          open={!!selectedBenefit}
          onOpenChange={(open) => !open && setSelectedBenefit(null)}
        />
      )}
    </>
  );
}
