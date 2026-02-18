'use client';

import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { searchCardTemplates } from '@/lib/api';
import { formatCurrency } from '@/lib/utils';
import type { CardTemplate } from '@/types';
import { Search, Loader2, CreditCard, Sparkles } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';

interface CardSearchProps {
  onSelect: (card: CardTemplate) => void;
  /** Called when the user wants to try the AI lookup; receives the current raw query */
  onAIRequest?: (query: string) => void;
  /** When true, the "Search with AI" button shows a loading spinner */
  aiLoading?: boolean;
}

export function CardSearch({ onSelect, onAIRequest, aiLoading = false }: CardSearchProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [debouncedQuery, setDebouncedQuery] = useState('');

  // Debounce search
  const handleSearch = (value: string) => {
    setSearchQuery(value);
    const timer = setTimeout(() => {
      setDebouncedQuery(value);
    }, 300);
    return () => clearTimeout(timer);
  };

  const { data: results, isLoading } = useQuery({
    queryKey: ['card-search', debouncedQuery],
    queryFn: () => searchCardTemplates({ q: debouncedQuery, limit: 10 }),
    enabled: debouncedQuery.length >= 2,
  });

  const showAIFallback =
    !!onAIRequest &&
    results !== undefined &&
    results.length === 0 &&
    debouncedQuery.length >= 3;

  return (
    <div className="space-y-4">
      <div className="relative">
        <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
        <Input
          type="text"
          placeholder="Search for a credit card (e.g., Chase Sapphire)"
          value={searchQuery}
          onChange={(e) => handleSearch(e.target.value)}
          className="pl-9"
        />
      </div>

      {isLoading && (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
        </div>
      )}

      {results && results.length > 0 && (
        <div className="space-y-2">
          {results.map((card) => (
            <Card
              key={card.id}
              className="cursor-pointer hover:bg-accent transition-colors"
              onClick={() => onSelect(card)}
            >
              <CardContent className="flex items-center justify-between p-4">
                <div className="flex items-center gap-3">
                  {card.image_url ? (
                    <img
                      src={card.image_url}
                      alt={card.name}
                      className="h-10 w-16 rounded object-cover"
                    />
                  ) : (
                    <CreditCard className="h-8 w-8 text-muted-foreground" />
                  )}
                  <div>
                    <p className="font-medium">{card.name}</p>
                    <p className="text-sm text-muted-foreground">{card.bank}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">
                    {formatCurrency(card.annual_fee_cents)} fee
                  </Badge>
                  {card.is_verified && (
                    <Badge variant="default">Verified</Badge>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {results && results.length === 0 && debouncedQuery.length >= 2 && !showAIFallback && (
        <div className="text-center py-8 text-muted-foreground">
          <p>No cards found for &ldquo;{debouncedQuery}&rdquo;</p>
          <p className="text-sm mt-2">Try a different search term</p>
        </div>
      )}

      {showAIFallback && (
        <div className="text-center py-6 space-y-3">
          <p className="text-muted-foreground text-sm">
            No cards found for &ldquo;{debouncedQuery}&rdquo;
          </p>
          <Button
            variant="outline"
            onClick={() => onAIRequest(debouncedQuery)}
            disabled={aiLoading}
          >
            {aiLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Searching with AI&hellip;
              </>
            ) : (
              <>
                <Sparkles className="mr-2 h-4 w-4" />
                Search with AI
              </>
            )}
          </Button>
        </div>
      )}
    </div>
  );
}
