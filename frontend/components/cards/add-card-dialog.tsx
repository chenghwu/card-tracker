'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { CardSearch } from './card-search';
import { addCard, lookupCardWithAI } from '@/lib/api';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import type { CardTemplate } from '@/types';
import { Plus, Loader2, CreditCard, Sparkles } from 'lucide-react';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog';
import { formatCurrency } from '@/lib/utils';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';

// Known bank name fragments to extract from a free-text query
const KNOWN_BANKS = [
  'chase',
  'amex',
  'american express',
  'citi',
  'citibank',
  'capital one',
  'discover',
  'wells fargo',
  'bank of america',
  'us bank',
  'barclays',
  'synchrony',
];

/** Best-effort extraction of a bank name from a free-text search query */
function parseBankFromQuery(query: string): { bank: string; cardName: string } {
  const lower = query.toLowerCase();
  for (const bank of KNOWN_BANKS) {
    if (lower.includes(bank)) {
      // Normalise "amex" → "American Express" for the API, keep others as-is
      const normalisedBank =
        bank === 'amex' ? 'American Express' : bank
          .split(' ')
          .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
          .join(' ');
      // Strip the bank token from the card name so we don't duplicate it
      const cardName = query.replace(new RegExp(bank, 'i'), '').trim() || query;
      return { bank: normalisedBank, cardName };
    }
  }
  return { bank: '', cardName: query };
}

export function AddCardDialog() {
  const [open, setOpen] = useState(false);
  const [step, setStep] = useState<'search' | 'ai-preview' | 'details'>('search');
  const [selectedCard, setSelectedCard] = useState<CardTemplate | null>(null);
  const [openDate, setOpenDate] = useState('');
  const [nickname, setNickname] = useState('');
  const [cardType, setCardType] = useState<'personal' | 'business'>('personal');
  const [autoDetectedType, setAutoDetectedType] = useState<'personal' | 'business'>('personal');
  const [pendingCardType, setPendingCardType] = useState<'personal' | 'business' | null>(null);
  const [creditLimit, setCreditLimit] = useState('');

  // AI lookup state
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState<string | null>(null);
  const [aiCard, setAiCard] = useState<CardTemplate | null>(null);

  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: addCard,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user-cards'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-summary'] });
      setOpen(false);
      resetForm();
      toast.success('Card added successfully', {
        description: `${selectedCard?.name} has been added to your wallet`,
      });
    },
    onError: () => {
      toast.error('Failed to add card', {
        description: 'Please try again or contact support',
      });
    },
  });

  const resetForm = () => {
    setStep('search');
    setSelectedCard(null);
    setOpenDate('');
    setNickname('');
    setCardType('personal');
    setAutoDetectedType('personal');
    setPendingCardType(null);
    setCreditLimit('');
    setAiLoading(false);
    setAiError(null);
    setAiCard(null);
  };

  const detectCardType = (card: CardTemplate): 'personal' | 'business' =>
    /business/i.test(card.name) || /business/i.test(card.bank) ? 'business' : 'personal';

  const handleSelectCard = (card: CardTemplate) => {
    setSelectedCard(card);
    const detected = detectCardType(card);
    setCardType(detected);
    setAutoDetectedType(detected);
    setStep('details');
  };

  /** Called by CardSearch when the user clicks "Search with AI" */
  const handleAIRequest = async (query: string) => {
    setAiError(null);
    setAiLoading(true);

    const { bank, cardName } = parseBankFromQuery(query);

    try {
      const result = await lookupCardWithAI(bank, cardName);
      setAiCard(result);
      setStep('ai-preview');
    } catch {
      setAiError("Couldn't find that card. Try a different search.");
    } finally {
      setAiLoading(false);
    }
  };

  const handleConfirmAICard = () => {
    if (!aiCard) return;
    setSelectedCard(aiCard);
    const detected = detectCardType(aiCard);
    setCardType(detected);
    setAutoDetectedType(detected);
    setAiCard(null);
    setStep('details');
  };

  const handleCancelAIPreview = () => {
    setAiCard(null);
    setAiError(null);
    setStep('search');
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCard || !openDate) return;

    mutation.mutate({
      card_template_id: selectedCard.id,
      open_date: openDate,
      nickname: nickname || undefined,
      card_type: cardType,
      credit_limit_cents: creditLimit ? Math.round(parseFloat(creditLimit) * 100) : undefined,
    });
  };

  const handleOpenChange = (newOpen: boolean) => {
    setOpen(newOpen);
    if (!newOpen) {
      resetForm();
    }
  };

  // Dialog title + description per step
  const dialogTitle =
    step === 'search'
      ? 'Search for a Card'
      : step === 'ai-preview'
      ? 'AI Card Result'
      : 'Card Details';

  const dialogDescription =
    step === 'search'
      ? 'Search for your credit card to get started'
      : step === 'ai-preview'
      ? 'Review the card found by AI before adding it'
      : 'Enter the details for your card';

  return (
    <>
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Add Card
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto top-[15%] translate-y-0">
        <DialogHeader>
          <DialogTitle>{dialogTitle}</DialogTitle>
          <DialogDescription>{dialogDescription}</DialogDescription>
        </DialogHeader>

        {mutation.error && (
          <Alert variant="destructive">
            <AlertDescription>
              Failed to add card. Please try again.
            </AlertDescription>
          </Alert>
        )}

        {/* ── Step: search ───────────────────────────────────────────── */}
        {step === 'search' && (
          <>
            <CardSearch
              onSelect={handleSelectCard}
              onAIRequest={handleAIRequest}
              aiLoading={aiLoading}
            />
            {aiError && (
              <Alert variant="destructive" className="mt-2">
                <AlertDescription>{aiError}</AlertDescription>
              </Alert>
            )}
          </>
        )}

        {/* ── Step: ai-preview ──────────────────────────────────────── */}
        {step === 'ai-preview' && aiCard && (
          <div className="space-y-4">
            <div className="rounded-lg border p-4 bg-muted/50 space-y-3">
              {/* Header row */}
              <div className="flex items-center gap-3">
                {aiCard.image_url ? (
                  <img
                    src={aiCard.image_url}
                    alt={aiCard.name}
                    className="h-10 w-16 rounded object-cover"
                  />
                ) : (
                  <CreditCard className="h-8 w-8 text-muted-foreground shrink-0" />
                )}
                <div className="min-w-0">
                  <p className="font-semibold truncate">{aiCard.name}</p>
                  <p className="text-sm text-muted-foreground">{aiCard.bank}</p>
                </div>
                <Badge variant="secondary" className="ml-auto shrink-0">
                  <Sparkles className="h-3 w-3 mr-1" />
                  AI Result
                </Badge>
              </div>

              {/* Annual fee */}
              <p className="text-sm">
                Annual Fee:{' '}
                <span className="font-medium">{formatCurrency(aiCard.annual_fee_cents)}</span>
              </p>

              {/* Benefits list */}
              {aiCard.benefits && aiCard.benefits.length > 0 && (
                <div className="space-y-1">
                  <p className="text-sm font-medium">Benefits</p>
                  <ul className="text-sm text-muted-foreground space-y-1 list-disc list-inside">
                    {aiCard.benefits.map((b) => (
                      <li key={b.id}>
                        {b.name}
                        {b.amount_cents > 0 && (
                          <span className="ml-1 text-foreground font-medium">
                            ({formatCurrency(b.amount_cents)})
                          </span>
                        )}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <div className="flex gap-2">
              <Button
                type="button"
                variant="outline"
                onClick={handleCancelAIPreview}
              >
                Cancel
              </Button>
              <Button className="flex-1" onClick={handleConfirmAICard}>
                Add this card
              </Button>
            </div>
          </div>
        )}

        {/* ── Step: details ─────────────────────────────────────────── */}
        {step === 'details' && selectedCard && (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="rounded-lg border p-4 bg-muted/50">
              <div className="flex items-center gap-3 mb-2">
                {selectedCard.image_url && (
                  <img
                    src={selectedCard.image_url}
                    alt={selectedCard.name}
                    className="h-10 w-16 rounded object-cover"
                  />
                )}
                <div>
                  <p className="font-semibold">{selectedCard.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {selectedCard.bank}
                  </p>
                </div>
              </div>
              <p className="text-sm">
                Annual Fee: {formatCurrency(selectedCard.annual_fee_cents)}
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="open-date">Card Open Date *</Label>
              <Input
                id="open-date"
                type="date"
                value={openDate}
                onChange={(e) => setOpenDate(e.target.value)}
                required
                max={new Date().toISOString().split('T')[0]}
              />
              <p className="text-xs text-muted-foreground">
                This is used to calculate benefit periods
              </p>
            </div>

            <div className="space-y-2">
              <Label>Card Type</Label>
              <div className="flex gap-2">
                <Button
                  type="button"
                  variant={cardType === 'personal' ? 'default' : 'outline'}
                  size="sm"
                  className="flex-1"
                  onClick={() => {
                    if (cardType !== 'personal') {
                      'personal' === autoDetectedType ? setCardType('personal') : setPendingCardType('personal');
                    }
                  }}
                >
                  Personal
                </Button>
                <Button
                  type="button"
                  variant={cardType === 'business' ? 'default' : 'outline'}
                  size="sm"
                  className="flex-1"
                  onClick={() => {
                    if (cardType !== 'business') {
                      'business' === autoDetectedType ? setCardType('business') : setPendingCardType('business');
                    }
                  }}
                >
                  Business
                </Button>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="nickname">Nickname (optional)</Label>
              <Input
                id="nickname"
                type="text"
                placeholder="e.g., My travel card"
                value={nickname}
                onChange={(e) => setNickname(e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="credit-limit">Credit Limit (optional)</Label>
              <div className="relative">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground text-sm">$</span>
                <Input
                  id="credit-limit"
                  type="number"
                  step="1"
                  min="0"
                  placeholder="e.g., 10000"
                  value={creditLimit}
                  onChange={(e) => setCreditLimit(e.target.value)}
                  className="pl-7"
                />
              </div>
            </div>

            <div className="flex gap-2">
              <Button
                type="button"
                variant="outline"
                onClick={() => setStep('search')}
                disabled={mutation.isPending}
              >
                Back
              </Button>
              <Button type="submit" disabled={mutation.isPending} className="flex-1">
                {mutation.isPending ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Adding...
                  </>
                ) : (
                  'Add Card'
                )}
              </Button>
            </div>
          </form>
        )}
      </DialogContent>
    </Dialog>

    <AlertDialog open={!!pendingCardType} onOpenChange={(open) => !open && setPendingCardType(null)}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Change card type?</AlertDialogTitle>
          <AlertDialogDescription>
            This card was automatically detected as <strong>{cardType}</strong>. Are you sure you want to change it to <strong>{pendingCardType}</strong>?
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction onClick={() => { setCardType(pendingCardType!); setPendingCardType(null); }}>
            Change to {pendingCardType}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
    </>
  );
}
