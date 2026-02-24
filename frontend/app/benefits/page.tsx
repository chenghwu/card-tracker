'use client';

import { useState } from 'react';
import { useQuery, useQueries } from '@tanstack/react-query';
import { MainLayout } from '@/components/layout/main-layout';
import { BenefitRow } from '@/components/benefits/benefit-row';
import { UseBenefitDialog } from '@/components/benefits/use-benefit-dialog';
import { getUserCards, getCardDetail } from '@/lib/api';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { ChevronDown, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import type { UserBenefit } from '@/types';

const FREQUENCY_SECTIONS = [
  {
    key: 'monthly' as const,
    label: 'Monthly',
    bg: 'bg-blue-50 dark:bg-blue-950/20',
    border: 'border border-blue-200 dark:border-blue-800',
    title: 'text-blue-700 dark:text-blue-300',
  },
  {
    key: 'quarterly' as const,
    label: 'Quarterly',
    bg: 'bg-amber-50 dark:bg-amber-950/20',
    border: 'border border-amber-200 dark:border-amber-800',
    title: 'text-amber-700 dark:text-amber-300',
  },
  {
    key: 'semi_annual' as const,
    label: 'Semi-Annual',
    bg: 'bg-violet-50 dark:bg-violet-950/20',
    border: 'border border-violet-200 dark:border-violet-800',
    title: 'text-violet-700 dark:text-violet-300',
  },
  {
    key: 'annual' as const,
    label: 'Annual',
    bg: 'bg-emerald-50 dark:bg-emerald-950/20',
    border: 'border border-emerald-200 dark:border-emerald-800',
    title: 'text-emerald-700 dark:text-emerald-300',
  },
];

interface BenefitWithCard extends UserBenefit {
  cardDisplayName: string;
}

export default function BenefitsPage() {
  const [selectedBenefit, setSelectedBenefit] = useState<UserBenefit | null>(null);
  const [filter, setFilter] = useState<'all' | 'unused' | 'used'>('all');
  const [collapsedSections, setCollapsedSections] = useState<Set<string>>(new Set());

  const toggleSection = (key: string) =>
    setCollapsedSections((prev) => {
      const next = new Set(prev);
      next.has(key) ? next.delete(key) : next.add(key);
      return next;
    });

  const { data: cards, isLoading: cardsLoading, error: cardsError } = useQuery({
    queryKey: ['cards'],
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
  const hasError = cardsError || cardDetailQueries.some((q) => q.isError);

  // Flatten all benefits across all cards, attaching a display name
  const allBenefits: BenefitWithCard[] = cardDetailQueries.flatMap((q, i) => {
    if (!q.data) return [];
    const card = q.data;
    const displayName = card.nickname || `${card.card_template.bank} ${card.card_template.name}`;
    return card.benefits.map((b) => ({ ...b, cardDisplayName: displayName }));
  });

  const totalBenefits = allBenefits.length;

  return (
    <MainLayout>
      <div className="space-y-8">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">All Benefits</h1>
            <p className="text-muted-foreground">
              {isLoading ? 'Loading…' : `${totalBenefits} benefits across ${cards?.length ?? 0} cards`}
            </p>
          </div>
          {!isLoading && totalBenefits > 0 && (
            <div className="flex gap-2">
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

        {hasError && (
          <Alert variant="destructive">
            <AlertDescription>Failed to load benefits. Please try again later.</AlertDescription>
          </Alert>
        )}

        {isLoading ? (
          <div className="space-y-6">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="rounded-xl border p-5 space-y-3">
                <Skeleton className="h-4 w-24" />
                <Skeleton className="h-28 w-full" />
                <Skeleton className="h-28 w-full" />
              </div>
            ))}
          </div>
        ) : totalBenefits === 0 ? (
          <div className="text-center py-16 text-muted-foreground">
            <p className="text-lg font-medium mb-1">No benefits yet</p>
            <p className="text-sm">Add a card to start tracking your benefits.</p>
          </div>
        ) : (
          <div className="space-y-6">
            {FREQUENCY_SECTIONS.map(({ key, label, bg, border, title }) => {
              const group = allBenefits.filter((b) => {
                if (b.benefit_template.frequency !== key) return false;
                const isFullyUsed = (b.remaining_amount_cents ?? b.effective_amount_cents ?? 0) === 0;
                if (filter === 'used') return isFullyUsed;
                if (filter === 'unused') return !isFullyUsed;
                return true;
              });
              if (group.length === 0) return null;
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
                      {group.map((benefit) => (
                        <BenefitRow
                          key={benefit.id}
                          benefit={benefit}
                          cardName={benefit.cardDisplayName}
                          onUse={() => setSelectedBenefit(benefit)}
                          hideFrequency
                        />
                      ))}
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
            onOpenChange={(open) => !open && setSelectedBenefit(null)}
          />
        )}
      </div>
    </MainLayout>
  );
}
