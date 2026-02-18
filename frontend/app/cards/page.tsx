'use client';

import { useQuery } from '@tanstack/react-query';
import { MainLayout } from '@/components/layout/main-layout';
import { CardGrid } from '@/components/cards/card-grid';
import { CardGridSkeleton } from '@/components/cards/card-grid-skeleton';
import { AddCardDialog } from '@/components/cards/add-card-dialog';
import { getUserCards } from '@/lib/api';
import { CreditCard } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';

export default function CardsPage() {
  const {
    data: cards,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['user-cards'],
    queryFn: getUserCards,
  });

  return (
    <MainLayout>
      <div className="space-y-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">My Cards</h1>
            <p className="text-muted-foreground">
              Manage your credit cards and their benefits
            </p>
          </div>
          <AddCardDialog />
        </div>

        {error && (
          <Alert variant="destructive">
            <AlertDescription>
              Failed to load your cards. Please try again later.
            </AlertDescription>
          </Alert>
        )}

        {isLoading ? (
          <CardGridSkeleton />
        ) : cards && cards.length > 0 ? (
          <CardGrid cards={cards} />
        ) : (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <div className="rounded-full bg-accent p-6 mb-4">
              <CreditCard className="h-12 w-12 text-muted-foreground" />
            </div>
            <h3 className="text-lg font-semibold mb-2">No cards yet</h3>
            <p className="text-sm text-muted-foreground mb-6 max-w-sm">
              Add your first credit card to start tracking benefits and maximizing your rewards.
            </p>
            <AddCardDialog />
          </div>
        )}
      </div>
    </MainLayout>
  );
}
