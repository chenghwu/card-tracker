'use client';

import { useState } from 'react';
import { useQuery, useQueries, useQueryClient } from '@tanstack/react-query';
import { UseBenefitDialog } from '@/components/benefits/use-benefit-dialog';
import { getUserCards, getCardDetail } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Skeleton } from '@/components/ui/skeleton';
import { ChevronDown, ChevronRight, CheckCircle2 } from 'lucide-react';
import { formatCurrency, calculateProgress, getFrequencyDisplayName } from '@/lib/utils';
import type { UserBenefit } from '@/types';

const PERIOD_SECTIONS = [
  {
    key: 'monthly' as const,
    label: 'This Month',
    bg: 'bg-blue-50 dark:bg-blue-950/20',
    border: 'border border-blue-200 dark:border-blue-800',
    title: 'text-blue-700 dark:text-blue-300',
  },
  {
    key: 'quarterly' as const,
    label: 'This Quarter',
    bg: 'bg-amber-50 dark:bg-amber-950/20',
    border: 'border border-amber-200 dark:border-amber-800',
    title: 'text-amber-700 dark:text-amber-300',
  },
  {
    key: 'semi_annual' as const,
    label: 'This Half Year',
    bg: 'bg-violet-50 dark:bg-violet-950/20',
    border: 'border border-violet-200 dark:border-violet-800',
    title: 'text-violet-700 dark:text-violet-300',
  },
  {
    key: 'annual' as const,
    label: 'This Year',
    bg: 'bg-emerald-50 dark:bg-emerald-950/20',
    border: 'border border-emerald-200 dark:border-emerald-800',
    title: 'text-emerald-700 dark:text-emerald-300',
  },
];

interface BenefitWithCard extends UserBenefit {
  cardDisplayName: string;
  cardId: number;
}

export function DashboardBenefits() {
  const queryClient = useQueryClient();
  const [selectedBenefit, setSelectedBenefit] = useState<UserBenefit | null>(null);
  const [filter, setFilter] = useState<'all' | 'unused' | 'used'>('all');
  const [collapsedSections, setCollapsedSections] = useState<Set<string>>(new Set(['quarterly', 'semi_annual', 'annual']));

  const toggleSection = (key: string) =>
    setCollapsedSections((prev) => {
      const next = new Set(prev);
      next.has(key) ? next.delete(key) : next.add(key);
      return next;
    });

  const { data: cards, isLoading: cardsLoading } = useQuery({
    queryKey: ['user-cards'],
    queryFn: getUserCards,
  });

  const cardDetailQueries = useQueries({
    queries: (cards ?? []).map((card) => ({
      queryKey: ['card-detail', card.id],
      queryFn: () => getCardDetail(card.id),
      enabled: !!cards,
    })),
  });

  const isLoading = cardsLoading || cardDetailQueries.some((q) => q.isLoading);

  const allBenefits: BenefitWithCard[] = cardDetailQueries.flatMap((q) => {
    if (!q.data) return [];
    const card = q.data;
    const displayName = card.nickname || `${card.card_template.bank} ${card.card_template.name}`;
    return card.benefits.map((b) => ({ ...b, cardDisplayName: displayName, cardId: card.id }));
  });

  const handleBenefitUsed = (cardId: number) => {
    queryClient.invalidateQueries({ queryKey: ['card-detail', cardId] });
    queryClient.invalidateQueries({ queryKey: ['dashboard-summary'] });
    queryClient.invalidateQueries({ queryKey: ['dashboard-deadlines'] });
  };

  if (isLoading) {
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <Skeleton className="h-7 w-32" />
          <div className="flex gap-2">
            <Skeleton className="h-8 w-12" />
            <Skeleton className="h-8 w-16" />
            <Skeleton className="h-8 w-12" />
          </div>
        </div>
        {[1, 2, 3].map((i) => (
          <div key={i} className="rounded-xl border p-5 space-y-3">
            <Skeleton className="h-4 w-24" />
            <Skeleton className="h-2 w-full rounded-full" />
            <Skeleton className="h-16 w-full" />
            <Skeleton className="h-16 w-full" />
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h2 className="text-2xl font-bold">Benefits</h2>
          <p className="text-sm text-muted-foreground">
            {allBenefits.length} benefits across {cards?.length ?? 0} cards
          </p>
        </div>
        {allBenefits.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {(['all', 'unused', 'used'] as const).map((f) => (
              <Button
                key={f}
                variant={filter === f ? 'default' : 'outline'}
                size="sm"
                onClick={() => setFilter(f)}
                className="capitalize"
              >
                {f}
              </Button>
            ))}
          </div>
        )}
      </div>

      {allBenefits.length === 0 ? (
        <div className="text-center py-12 text-muted-foreground">
          <p>No benefits yet. Add a card to start tracking.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {PERIOD_SECTIONS.map(({ key, label, bg, border, title }) => {
            const group = allBenefits.filter((b) => {
              if (b.benefit_template.frequency !== key) return false;
              const isFullyUsed = (b.remaining_amount_cents ?? b.effective_amount_cents ?? 0) === 0;
              if (filter === 'used') return isFullyUsed;
              if (filter === 'unused') return !isFullyUsed;
              return true;
            });
            if (group.length === 0) return null;

            const usedCount = group.filter((b) => (b.remaining_amount_cents ?? b.effective_amount_cents ?? 0) === 0).length;
            const overallProgress = calculateProgress(usedCount, group.length);
            const isCollapsed = collapsedSections.has(key);

            return (
              <div key={key} className={`rounded-xl ${bg} ${border}`}>
                <button
                  onClick={() => toggleSection(key)}
                  className={`w-full flex items-center justify-between p-4 sm:p-5 ${isCollapsed ? '' : 'pb-2 sm:pb-3'}`}
                >
                  <h3 className={`text-sm font-semibold uppercase tracking-wide ${title}`}>
                    {label} <span className="font-normal opacity-70">({group.length})</span>
                  </h3>
                  {isCollapsed
                    ? <ChevronRight className={`h-4 w-4 ${title}`} />
                    : <ChevronDown className={`h-4 w-4 ${title}`} />
                  }
                </button>

                {!isCollapsed && (
                  <div className="px-4 sm:px-5 pb-4 sm:pb-5 space-y-3">
                    {/* Section progress */}
                    <div className="space-y-1">
                      <p className="text-xs text-muted-foreground">
                        {usedCount} of {group.length} benefits used
                      </p>
                      <Progress value={overallProgress} className="h-1.5" />
                      <p className="text-xs text-muted-foreground text-right">{overallProgress}% complete</p>
                    </div>

                    {/* Compact benefit rows */}
                    <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
                      {group.map((benefit) => {
                        const amount = benefit.effective_amount_cents ?? 0;
                        const used = benefit.used_amount_cents ?? 0;
                        const remaining = benefit.remaining_amount_cents ?? amount;
                        const isFullyUsed = remaining === 0;
                        const progress = calculateProgress(used, amount);

                        return (
                          <div
                            key={benefit.id}
                            className="flex items-center justify-between gap-3 border-b pb-3 last:border-0 last:pb-0 cursor-pointer"
                            onClick={() => !isFullyUsed && setSelectedBenefit(benefit)}
                          >
                            <div className="space-y-1 min-w-0 flex-1">
                              <div className="flex flex-wrap items-center gap-2">
                                <p className="font-medium text-sm truncate">{benefit.effective_name}</p>
                                <Badge variant="outline" className="text-xs shrink-0">
                                  {getFrequencyDisplayName(benefit.benefit_template.frequency)}
                                </Badge>
                              </div>
                              <p className="text-xs text-muted-foreground truncate">{benefit.cardDisplayName}</p>
                              {!isFullyUsed && (
                                <Progress value={progress} className="h-1.5 mt-1" />
                              )}
                            </div>
                            <div className="flex flex-col items-end shrink-0 gap-1">
                              {isFullyUsed ? (
                                <CheckCircle2 className="h-5 w-5 text-green-500" />
                              ) : (
                                <span className="text-sm font-medium whitespace-nowrap">
                                  {formatCurrency(remaining)} left
                                </span>
                              )}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {selectedBenefit && (
        <UseBenefitDialog
          benefit={selectedBenefit}
          open={!!selectedBenefit}
          onOpenChange={(open) => {
            if (!open) {
              const b = selectedBenefit as BenefitWithCard;
              handleBenefitUsed(b.cardId);
              setSelectedBenefit(null);
            }
          }}
        />
      )}
    </div>
  );
}
