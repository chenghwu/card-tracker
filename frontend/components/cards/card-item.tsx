'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from '@/components/ui/alert-dialog';
import { formatCurrency, formatDate } from '@/lib/utils';
import { deleteCard } from '@/lib/api';
import type { UserCard } from '@/types';
import Link from 'next/link';
import { CreditCard, Trash2 } from 'lucide-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';

interface CardItemProps {
  card: UserCard;
}

export function CardItem({ card }: CardItemProps) {
  const { card_template, open_date, nickname } = card;
  const queryClient = useQueryClient();

  const deleteMutation = useMutation({
    mutationFn: () => deleteCard(card.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user-cards'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-summary'] });
      toast.success('Card removed', {
        description: `${nickname || card_template.name} has been removed.`,
      });
    },
    onError: () => {
      toast.error('Failed to remove card');
    },
  });

  return (
    <Card className={`hover:shadow-lg transition-shadow duration-200 border-l-4 ${card.card_type === 'business' ? 'border-l-amber-500' : 'border-l-blue-500'}`}>
      <CardHeader>
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1 min-w-0">
            <CardTitle className="flex items-center gap-2 text-base sm:text-lg">
              {card_template.image_url ? (
                <img
                  src={card_template.image_url}
                  alt={card_template.name}
                  className="h-8 w-12 rounded object-cover flex-shrink-0"
                />
              ) : (
                <CreditCard className="h-6 w-6 text-muted-foreground flex-shrink-0" />
              )}
              <span className="truncate">{nickname || card_template.name}</span>
            </CardTitle>
            {card.nickname && (
              <p className="text-xs text-muted-foreground mt-0.5 truncate">{card_template.name}</p>
            )}
            <CardDescription className="mt-0.5 truncate">
              {card_template.bank}
            </CardDescription>
          </div>
          <div className="flex flex-wrap items-center gap-1 flex-shrink-0 justify-end">
            <Badge className={card.card_type === 'business' ? 'border-amber-500 text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/30' : 'border-blue-500 text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/30'} variant="outline">
              {card.card_type === 'business' ? 'Business' : 'Personal'}
            </Badge>
            {card_template.is_verified && (
              <Badge variant="secondary">Verified</Badge>
            )}
            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-destructive">
                  <Trash2 className="h-4 w-4" />
                </Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Remove card?</AlertDialogTitle>
                  <AlertDialogDescription>
                    This will remove <strong>{nickname || card_template.name}</strong> and all its benefit tracking history.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                  <AlertDialogAction
                    onClick={() => deleteMutation.mutate()}
                    className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                  >
                    Remove
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex justify-between text-sm">
          <span className="text-muted-foreground">Annual Fee</span>
          <span className="font-medium">
            {formatCurrency(card_template.annual_fee_cents)}
          </span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-muted-foreground">Opened</span>
          <span className="font-medium">{formatDate(open_date)}</span>
        </div>
        {card.credit_limit_cents && (
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">Credit Limit</span>
            <span className="font-medium">{formatCurrency(card.credit_limit_cents)}</span>
          </div>
        )}
        <Button asChild className="w-full">
          <Link href={`/cards/${card.id}`}>View Benefits</Link>
        </Button>
      </CardContent>
    </Card>
  );
}
