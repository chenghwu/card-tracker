'use client';

import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { formatCurrency, formatDate, getUrgencyColor, getCategoryDisplayName, getFrequencyDisplayName } from '@/lib/utils';
import type { UserBenefit } from '@/types';
import { Clock } from 'lucide-react';

interface BenefitRowProps {
  benefit: UserBenefit;
  onUse: () => void;
  cardName?: string;
}

export function BenefitRow({ benefit, onUse, cardName }: BenefitRowProps) {
  const template = benefit.benefit_template;
  const amount = benefit.custom_amount_cents || template.amount_cents;
  const name = benefit.custom_name || template.name;
  const remaining = benefit.remaining_amount_cents ?? amount;
  const used = benefit.used_amount_cents ?? 0;
  const progress = amount > 0 ? Math.min(Math.round((used / amount) * 100), 100) : 0;
  const urgency = benefit.deadline_urgency || 'ok';
  const daysUntilDeadline = benefit.days_until_deadline;

  const isFullyUsed = remaining === 0;


  return (
    <div className="border rounded-lg p-3 sm:p-4 space-y-3 transition-shadow hover:shadow-md">
      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <div className="flex flex-wrap items-center gap-2 mb-1">
            <h3 className="font-semibold text-sm sm:text-base">{name}</h3>
            {cardName && (
              <Badge variant="outline" className="text-xs font-normal text-muted-foreground">
                {cardName}
              </Badge>
            )}
            <Badge variant="outline" className="text-xs">
              {getCategoryDisplayName(template.category)}
            </Badge>
            <Badge variant="secondary" className="text-xs">
              {getFrequencyDisplayName(template.frequency, template.period_type)}
            </Badge>
          </div>
          {template.description && (
            <p className="text-xs sm:text-sm text-muted-foreground mb-2">
              {template.description}
            </p>
          )}
        </div>
        {daysUntilDeadline !== undefined && daysUntilDeadline <= 14 && (
          <Badge variant={getUrgencyColor(urgency) as any} className="self-start">
            <Clock className="h-3 w-3 mr-1" />
            {daysUntilDeadline}d left
          </Badge>
        )}
      </div>

      <div className="space-y-2">
        <div className="flex flex-col sm:flex-row sm:justify-between gap-1 text-xs sm:text-sm">
          <span className="text-muted-foreground">
            {formatCurrency(used)} used of {formatCurrency(amount)}
          </span>
          <span className="font-medium">
            {formatCurrency(remaining)} remaining
          </span>
        </div>
        <Progress value={progress} className="h-2" indicatorClassName="bg-green-500" />
      </div>

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        <div className="text-xs text-muted-foreground order-2 sm:order-1">
          {benefit.current_period_start && benefit.current_period_end && (
            <span className="block sm:inline">
              Period: {formatDate(benefit.current_period_start)} - {formatDate(benefit.current_period_end)}
            </span>
          )}
        </div>
        <Button
          size="sm"
          onClick={onUse}
          disabled={isFullyUsed}
          className="w-full sm:w-auto order-1 sm:order-2"
        >
          {isFullyUsed ? 'Fully Used' : 'Mark as Used'}
        </Button>
      </div>
    </div>
  );
}
