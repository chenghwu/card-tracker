'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { MainLayout } from '@/components/layout/main-layout';
import { BenefitRow } from '@/components/benefits/benefit-row';
import { UsageHistory } from '@/components/benefits/usage-history';
import { UseBenefitDialog } from '@/components/benefits/use-benefit-dialog';
import { getCardDetail, undoBenefitUsage, updateCard } from '@/lib/api';
import { formatCurrency, formatDate } from '@/lib/utils';
import { CreditCard, ArrowLeft, Pencil, ChevronDown, ChevronRight } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';
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

export default function CardDetailPage() {
  const params = useParams();
  const cardId = parseInt(params.id as string);
  const [selectedBenefit, setSelectedBenefit] = useState<UserBenefit | null>(null);
  const [benefitFilter, setBenefitFilter] = useState<'all' | 'unused' | 'used'>('all');
  const [collapsedSections, setCollapsedSections] = useState<Set<string>>(new Set());

  const toggleSection = (key: string) =>
    setCollapsedSections((prev) => {
      const next = new Set(prev);
      next.has(key) ? next.delete(key) : next.add(key);
      return next;
    });
  const [editOpen, setEditOpen] = useState(false);
  const [editNickname, setEditNickname] = useState('');
  const [editCardType, setEditCardType] = useState<'personal' | 'business'>('personal');
  const [editCreditLimit, setEditCreditLimit] = useState('');
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

  const editMutation = useMutation({
    mutationFn: (data: { nickname?: string; card_type?: 'personal' | 'business'; credit_limit_cents?: number | null }) =>
      updateCard(cardId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['card-detail', cardId] });
      queryClient.invalidateQueries({ queryKey: ['user-cards'] });
      setEditOpen(false);
      toast.success('Card updated');
    },
    onError: () => toast.error('Failed to update card'),
  });

  const handleEditOpen = () => {
    setEditNickname(card?.nickname || '');
    setEditCardType(card?.card_type || 'personal');
    setEditCreditLimit(card?.credit_limit_cents ? (card.credit_limit_cents / 100).toString() : '');
    setEditOpen(true);
  };

  const handleEditSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    editMutation.mutate({
      nickname: editNickname,
      card_type: editCardType,
      credit_limit_cents: editCreditLimit ? Math.round(parseFloat(editCreditLimit) * 100) : null,
    });
  };

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
                    <div className="flex items-center gap-2 mb-1">
                      <h2 className="text-xl sm:text-2xl font-bold">
                        {card.nickname || card.card_template.name}
                      </h2>
                      <Button variant="ghost" size="icon" className="h-7 w-7" onClick={handleEditOpen}>
                        <Pencil className="h-4 w-4 text-muted-foreground" />
                      </Button>
                    </div>
                    {card.nickname && (
                      <p className="text-sm text-muted-foreground -mt-0.5 mb-0.5">
                        {card.card_template.name}
                      </p>
                    )}
                    <p className="text-base sm:text-lg text-muted-foreground mb-2">
                      {card.card_template.bank}
                    </p>
                    <div className="flex flex-wrap gap-2">
                      <Badge
                        variant="outline"
                        className={card.card_type === 'business'
                          ? 'border-amber-500 text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/30'
                          : 'border-blue-500 text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/30'}
                      >
                        {card.card_type === 'business' ? 'Business' : 'Personal'}
                      </Badge>
                      <Badge variant="outline">
                        Opened {formatDate(card.open_date)}
                      </Badge>
                      {card.card_template.is_verified && (
                        <Badge variant="secondary">Verified</Badge>
                      )}
                    </div>
                  </div>
                </div>
                <div className="text-left sm:text-right space-y-2">
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">Annual Fee</p>
                    <p className="text-xl sm:text-2xl font-bold">
                      {formatCurrency(card.card_template.annual_fee_cents)}
                    </p>
                  </div>
                  {card.credit_limit_cents && (
                    <div>
                      <p className="text-sm text-muted-foreground mb-1">Credit Limit</p>
                      <p className="text-lg font-semibold">
                        {formatCurrency(card.credit_limit_cents)}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Benefits Section */}
            <div>
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4">
                <div>
                  <h2 className="text-2xl font-bold">Benefits</h2>
                  <p className="text-muted-foreground">
                    {card.benefits.length} {card.benefits.length === 1 ? 'benefit' : 'benefits'} available
                  </p>
                </div>
                {card.benefits.length > 0 && (
                  <div className="flex gap-2">
                    {(['all', 'unused', 'used'] as const).map((f) => (
                      <Button
                        key={f}
                        variant={benefitFilter === f ? 'default' : 'outline'}
                        size="sm"
                        onClick={() => setBenefitFilter(f)}
                        className="capitalize"
                      >
                        {f}
                      </Button>
                    ))}
                  </div>
                )}
              </div>

              {card.benefits.length > 0 ? (
                <div className="space-y-6">
                  {FREQUENCY_SECTIONS.map(({ key, label, bg, border, title }) => {
                    const group = card.benefits.filter((b) => {
                      if (b.benefit_template.frequency !== key) return false;
                      const isFullyUsed = (b.remaining_amount_cents ?? b.effective_amount_cents ?? 0) === 0;
                      if (benefitFilter === 'used') return isFullyUsed;
                      if (benefitFilter === 'unused') return !isFullyUsed;
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
                        )}
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

        <Dialog open={editOpen} onOpenChange={setEditOpen}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Edit Card</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleEditSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label>Card Type</Label>
                <div className="flex gap-2">
                  <Button
                    type="button"
                    variant={editCardType === 'personal' ? 'default' : 'outline'}
                    size="sm"
                    className="flex-1"
                    onClick={() => setEditCardType('personal')}
                  >
                    Personal
                  </Button>
                  <Button
                    type="button"
                    variant={editCardType === 'business' ? 'default' : 'outline'}
                    size="sm"
                    className="flex-1"
                    onClick={() => setEditCardType('business')}
                  >
                    Business
                  </Button>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="edit-nickname">Nickname</Label>
                <Input
                  id="edit-nickname"
                  placeholder={card?.card_template.name}
                  value={editNickname}
                  onChange={(e) => setEditNickname(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit-credit-limit">Credit Limit</Label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground text-sm">$</span>
                  <Input
                    id="edit-credit-limit"
                    type="number"
                    step="1"
                    min="0"
                    placeholder="e.g., 10000"
                    value={editCreditLimit}
                    onChange={(e) => setEditCreditLimit(e.target.value)}
                    className="pl-7"
                  />
                </div>
              </div>
              <div className="flex gap-2">
                <Button type="button" variant="outline" onClick={() => setEditOpen(false)} className="flex-1">
                  Cancel
                </Button>
                <Button type="submit" disabled={editMutation.isPending} className="flex-1">
                  Save
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>
    </MainLayout>
  );
}
