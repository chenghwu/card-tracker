'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { ChevronDown, ChevronUp, Undo2 } from 'lucide-react';
import { formatDate, formatCurrency } from '@/lib/utils';
import type { BenefitUsage } from '@/types';

interface UsageHistoryProps {
  usageRecords: BenefitUsage[];
  benefitId: number;
  onUndo: (usageId: number) => void;
}

export function UsageHistory({ usageRecords, benefitId, onUndo }: UsageHistoryProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!usageRecords || usageRecords.length === 0) {
    return null;
  }

  return (
    <div className="mt-1">
      <button
        onClick={() => setIsExpanded((prev) => !prev)}
        className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors py-1"
        aria-expanded={isExpanded}
      >
        {isExpanded ? (
          <ChevronUp className="h-3.5 w-3.5" />
        ) : (
          <ChevronDown className="h-3.5 w-3.5" />
        )}
        Usage History ({usageRecords.length})
      </button>

      {isExpanded && (
        <div className="mt-2 space-y-1 border-t pt-2">
          {usageRecords.map((record) => (
            <div
              key={record.id}
              className="flex items-center justify-between gap-2 rounded-md px-2 py-1.5 text-xs hover:bg-muted/50"
            >
              <div className="flex flex-wrap items-center gap-x-3 gap-y-0.5 min-w-0">
                <span className="text-muted-foreground shrink-0">
                  {formatDate(record.used_at.split('T')[0])}
                </span>
                <span className="font-medium shrink-0">
                  {formatCurrency(record.amount_cents)}
                </span>
                {record.note && (
                  <span className="text-muted-foreground truncate">{record.note}</span>
                )}
              </div>
              <Button
                variant="ghost"
                size="sm"
                className="h-6 px-2 text-muted-foreground hover:text-destructive shrink-0"
                onClick={() => onUndo(record.id)}
                aria-label="Undo this usage"
              >
                <Undo2 className="h-3.5 w-3.5 mr-1" />
                Undo
              </Button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
