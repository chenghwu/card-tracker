'use client';

import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
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

  // Group by issuer → card name
  const byIssuer = deadlines.reduce<Record<string, Record<string, DashboardDeadline[]>>>((acc, d) => {
    const issuer = d.card_issuer || d.card_name.split(' ')[0];
    const card = d.card_name;
    if (!acc[issuer]) acc[issuer] = {};
    if (!acc[issuer][card]) acc[issuer][card] = [];
    acc[issuer][card].push(d);
    return acc;
  }, {});
  const issuers = Object.keys(byIssuer).sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }));

  if (deadlines.length === 0) {
    return (
      <div className="space-y-3">
        <div>
          <h2 className="text-2xl font-bold">Upcoming Deadlines</h2>
          <p className="text-sm text-muted-foreground">No urgent benefits requiring attention</p>
        </div>
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-8 text-center">
            <Clock className="h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-sm text-muted-foreground">
              All your benefits are either used or have plenty of time remaining.
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-3">
        <div>
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <AlertCircle className="h-5 w-5" />
            Upcoming Deadlines
          </h2>
          <p className="text-sm text-muted-foreground">
            Benefits that need attention ({deadlines.length})
          </p>
        </div>
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-6">
              {issuers.map((issuer, issuerIdx) => (
                <div key={issuer}>
                  {issuerIdx > 0 && <div className="border-t mb-4" />}
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-sm font-bold text-foreground">{issuer}</span>
                    <div className="flex-1 h-px bg-border" />
                  </div>
                  <div className="space-y-5">
                    {Object.keys(byIssuer[issuer]).sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' })).map((cardName) => {
                      const shortName = cardName.startsWith(issuer + ' ')
                        ? cardName.slice(issuer.length + 1)
                        : cardName;
                      return (
                        <div key={cardName}>
                          <p className="text-xs font-semibold text-muted-foreground mb-2 ml-0.5">
                            {shortName}
                          </p>
                          <div className="space-y-3">
                            {byIssuer[issuer][cardName].map((deadline) => {
                              const benefit = deadline.benefit_template;
                              const remaining = deadline.remaining_amount_cents || 0;
                              return (
                                <div
                                  key={deadline.id}
                                  className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pl-2 border-l-2 border-muted"
                                >
                                  <div className="space-y-1 min-w-0 flex-1">
                                    <div className="flex flex-wrap items-center gap-2">
                                      <p className="font-medium text-sm">{deadline.effective_name}</p>
                                      <Badge variant="secondary" className="text-xs capitalize">
                                        {benefit.category || 'Benefit'}
                                      </Badge>
                                      <Badge variant={getUrgencyColor(deadline.deadline_urgency ?? 'ok') as any}>
                                        {deadline.days_until_deadline}d left
                                      </Badge>
                                    </div>
                                    <p className="text-sm font-medium">
                                      {formatCurrency(remaining)} remaining
                                    </p>
                                  </div>
                                  <Button
                                    size="sm"
                                    className="w-full sm:w-auto flex-shrink-0"
                                    onClick={() => setSelectedBenefit(deadline)}
                                  >
                                    Record Usage
                                  </Button>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

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
