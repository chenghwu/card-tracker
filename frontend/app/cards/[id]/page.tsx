'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { MainLayout } from '@/components/layout/main-layout';
import { BenefitRow } from '@/components/benefits/benefit-row';
import { UsageHistory } from '@/components/benefits/usage-history';
import { UseBenefitDialog } from '@/components/benefits/use-benefit-dialog';
import { getCardDetail, undoBenefitUsage } from '@/lib/api';
import { formatCurrency, formatDate } from '@/lib/utils';
import { CreditCard, ArrowLeft } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import Link from 'next/link';
import type { UserBenefit } from '@/types';
import { useParams } from 'next/navigation';

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
    bg: 'bg-violet-50 dark:bg-violet-950/20',
    border: 'border border-violet-200 dark:border-violet-800',
    title: 'text-violet-700 dark:text-violet-300',
  },
  {
    key: 'semi_annual' as const,
    label: 'Semi-Annual',
    bg: 'bg-amber-50 dark:bg-amber-950/20',
    border: 'border border-amber-200 dark:border-amber-800',
    title: 'text-amber-700 dark:text-amber-300',
  },
  {
    key: 'annual' as const,
    label: 'Annual',
    bg: 'bg-emerald-50 dark:bg-emerald-950/20',
    border: 'border border-emerald-200 dark:border-emerald-800',
    title: 'text-emerald-700 dark:text-emerald-300',
  },
];

export default function CardDetailPage() {
  const params = useParams();
  const cardId = parseInt(params.id as string);
  const [selectedBenefit, setSelectedBenefit] = useState<UserBenefit | null>(null);
  const queryClient = useQueryClient();

  const {
    data: card,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['card-detail', cardId],
    queryFn: () => getCardDetail(cardId),
    enabled: !isNaN(cardId),
  });

  const undoMutation = useMutation({
    mutationFn: ({ benefitId, usageId }: { benefitId: number; usageId: number }) =>
      undoBenefitUsage(benefitId, usageId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['card-detail', cardId] });
    },
  });

  return (
    <MainLayout>
      <div className="space-y-8">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" asChild>
            <Link href="/cards">
              <ArrowLeft className="h-5 w-5" />
            </Link>
          </Button>
          <div className="flex-1">
            <h1 className="text-3xl font-bold tracking-tight">Card Details</h1>
          </div>
        </div>

        {error && (
          <Alert variant="destructive">
            <AlertDescription>
              Failed to load card details. Please try again later.
            </AlertDescription>
          </Alert>
        )}

        {isLoading ? (
          <>
            <div className="rounded-lg border bg-card p-4 sm:p-6">
              <div className="flex flex-col sm:flex-row gap-4">
                <Skeleton className="h-16 w-24 flex-shrink-0" />
                <div className="flex-1 space-y-3">
                  <Skeleton className="h-8 w-48" />
                  <Skeleton className="h-5 w-32" />
                  <div className="flex gap-2">
                    <Skeleton className="h-5 w-24" />
                    <Skeleton className="h-5 w-20" />
                  </div>
                </div>
                <Skeleton className="h-16 w-32" />
              </div>
            </div>
            <div className="space-y-4">
              <Skeleton className="h-8 w-32" />
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-32 w-full" />
              ))}
            </div>
          </>
        ) : card ? (
          <>
            {/* Card Info Header */}
            <div className="rounded-lg border bg-card p-4 sm:p-6">
              <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
                <div className="flex flex-col sm:flex-row items-start gap-4">
                  {card.card_template.image_url ? (
                    <img
                      src={card.card_template.image_url}
                      alt={card.card_template.name}
                      className="h-16 w-24 rounded object-cover flex-shrink-0"
                    />
                  ) : (
                    <CreditCard className="h-12 w-12 text-muted-foreground flex-shrink-0" />
                  )}
                  <div>
                    <h2 className="text-xl sm:text-2xl font-bold mb-1">
                      {card.nickname || card.card_template.name}
                    </h2>
                    <p className="text-base sm:text-lg text-muted-foreground mb-2">
                      {card.card_template.bank}
                    </p>
                    <div className="flex flex-wrap gap-2">
                      <Badge variant="outline">
                        Opened {formatDate(card.open_date)}
                      </Badge>
                      {card.card_template.is_verified && (
                        <Badge variant="secondary">Verified</Badge>
                      )}
                    </div>
                  </div>
                </div>
                <div className="text-left sm:text-right">
                  <p className="text-sm text-muted-foreground mb-1">Annual Fee</p>
                  <p className="text-xl sm:text-2xl font-bold">
                    {formatCurrency(card.card_template.annual_fee_cents)}
                  </p>
                </div>
              </div>
            </div>

            {/* Benefits Section */}
            <div>
              <div className="mb-4">
                <h2 className="text-2xl font-bold">Benefits</h2>
                <p className="text-muted-foreground">
                  {card.benefits.length} {card.benefits.length === 1 ? 'benefit' : 'benefits'} available
                </p>
              </div>

              {card.benefits.length > 0 ? (
                <div className="space-y-6">
                  {FREQUENCY_SECTIONS.map(({ key, label, bg, border, title }) => {
                    const group = card.benefits.filter(
                      (b) => b.benefit_template.frequency === key
                    );
                    if (group.length === 0) return null;
                    return (
                      <div key={key} className={`rounded-xl p-4 sm:p-5 ${bg} ${border}`}>
                        <h3 className={`text-sm font-semibold uppercase tracking-wide mb-4 ${title}`}>
                          {label}
                        </h3>
                        <div className="space-y-3">
                          {group.map((benefit) => (
                            <div key={benefit.id}>
                              <BenefitRow
                                benefit={benefit}
                                onUse={() => setSelectedBenefit(benefit)}
                              />
                              <UsageHistory
                                usageRecords={benefit.usage_records ?? []}
                                benefitId={benefit.id}
                                onUndo={(usageId) =>
                                  undoMutation.mutate({ benefitId: benefit.id, usageId })
                                }
                              />
                            </div>
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="text-center py-12 text-muted-foreground">
                  <p>No benefits configured for this card</p>
                </div>
              )}
            </div>
          </>
        ) : null}

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
