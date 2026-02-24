'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { MainLayout } from '@/components/layout/main-layout';
import { CardGrid } from '@/components/cards/card-grid';
import { CardGridSkeleton } from '@/components/cards/card-grid-skeleton';
import { CardTable } from '@/components/cards/card-table';
import { AddCardDialog } from '@/components/cards/add-card-dialog';
import { getUserCards } from '@/lib/api';
import { CreditCard, LayoutGrid, List } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';

type FilterType = 'all' | 'personal' | 'business';
type ViewType = 'grid' | 'table';

export default function CardsPage() {
  const [filter, setFilter] = useState<FilterType>('all');
  const [view, setView] = useState<ViewType>('grid');

  const {
    data: cards,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['user-cards'],
    queryFn: getUserCards,
  });

  const filteredCards = cards?.filter((card) => {
    if (filter === 'all') return true;
    return card.card_type === filter;
  });

  const personalCount = cards?.filter((c) => c.card_type === 'personal').length ?? 0;
  const businessCount = cards?.filter((c) => c.card_type === 'business').length ?? 0;

  return (
    <MainLayout>
      <div className="space-y-8">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
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

        {!isLoading && cards && cards.length > 0 && (
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex flex-wrap gap-2">
              <Button
                variant={filter === 'all' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setFilter('all')}
              >
                All ({cards.length})
              </Button>
              <Button
                variant={filter === 'personal' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setFilter('personal')}
              >
                Personal ({personalCount})
              </Button>
              <Button
                variant={filter === 'business' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setFilter('business')}
              >
                Business ({businessCount})
              </Button>
            </div>
            <div className="flex gap-1 border rounded-md p-0.5">
              <Button
                variant={view === 'grid' ? 'secondary' : 'ghost'}
                size="icon"
                className="h-7 w-7"
                onClick={() => setView('grid')}
              >
                <LayoutGrid className="h-4 w-4" />
              </Button>
              <Button
                variant={view === 'table' ? 'secondary' : 'ghost'}
                size="icon"
                className="h-7 w-7"
                onClick={() => setView('table')}
              >
                <List className="h-4 w-4" />
              </Button>
            </div>
          </div>
        )}

        {isLoading ? (
          <CardGridSkeleton />
        ) : filteredCards && filteredCards.length > 0 ? (
          view === 'table' ? <CardTable cards={filteredCards} /> : <CardGrid cards={filteredCards} />
        ) : cards && cards.length > 0 ? (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <div className="rounded-full bg-accent p-6 mb-4">
              <CreditCard className="h-12 w-12 text-muted-foreground" />
            </div>
            <h3 className="text-lg font-semibold mb-2">No {filter} cards</h3>
            <p className="text-sm text-muted-foreground">
              You don&apos;t have any {filter} cards yet.
            </p>
          </div>
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
