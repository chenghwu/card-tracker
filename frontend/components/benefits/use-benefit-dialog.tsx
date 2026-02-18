'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { recordBenefitUsage } from '@/lib/api';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import type { UserBenefit } from '@/types';
import { Loader2 } from 'lucide-react';
import { formatCurrency } from '@/lib/utils';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { toast } from 'sonner';

interface UseBenefitDialogProps {
  benefit: UserBenefit;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function UseBenefitDialog({ benefit, open, onOpenChange }: UseBenefitDialogProps) {
  const template = benefit.benefit_template;
  const totalAmount = benefit.custom_amount_cents || template.amount_cents;
  const remaining = benefit.remaining_amount_cents || totalAmount;

  const [amountDollars, setAmountDollars] = useState<string>((remaining / 100).toFixed(2));
  const [note, setNote] = useState('');

  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (amountCents: number) =>
      recordBenefitUsage(benefit.id, {
        amount_cents: amountCents,
        note: note || undefined,
      }),
    onSuccess: (data, amountCents) => {
      queryClient.invalidateQueries({ queryKey: ['card-detail'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-summary'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-deadlines'] });
      onOpenChange(false);
      setAmountDollars((remaining / 100).toFixed(2));
      setNote('');
      toast.success('Benefit usage recorded', {
        description: `${formatCurrency(amountCents)} used successfully`,
      });
    },
    onError: () => {
      toast.error('Failed to record usage', {
        description: 'Please try again or contact support',
      });
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const amount = parseFloat(amountDollars);
    if (isNaN(amount) || amount <= 0) return;

    const amountCents = Math.round(amount * 100);
    if (amountCents > remaining) {
      toast.error('Invalid amount', {
        description: 'Amount cannot exceed remaining balance',
      });
      return;
    }

    mutation.mutate(amountCents);
  };

  const handleUseFull = () => {
    mutation.mutate(remaining);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Record Benefit Usage</DialogTitle>
          <DialogDescription>
            {benefit.custom_name || template.name} - {formatCurrency(remaining)} remaining
          </DialogDescription>
        </DialogHeader>

        {mutation.error && (
          <Alert variant="destructive">
            <AlertDescription>
              Failed to record usage. Please try again.
            </AlertDescription>
          </Alert>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="amount">Amount Used ($)</Label>
            <Input
              id="amount"
              type="number"
              step="0.01"
              min="0.01"
              max={(remaining / 100).toFixed(2)}
              value={amountDollars}
              onChange={(e) => setAmountDollars(e.target.value)}
              required
            />
            <p className="text-xs text-muted-foreground">
              Maximum: {formatCurrency(remaining)}
            </p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="note">Note (optional)</Label>
            <Input
              id="note"
              type="text"
              placeholder="e.g., Uber rides for December"
              value={note}
              onChange={(e) => setNote(e.target.value)}
            />
          </div>

          <div className="flex gap-2">
            <Button
              type="button"
              variant="outline"
              onClick={handleUseFull}
              disabled={mutation.isPending}
            >
              Use Full Amount
            </Button>
            <Button type="submit" disabled={mutation.isPending} className="flex-1">
              {mutation.isPending ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Recording...
                </>
              ) : (
                'Record Usage'
              )}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
