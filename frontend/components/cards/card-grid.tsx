'use client';

import { useState } from 'react';
import { ChevronDown, ChevronRight } from 'lucide-react';
import { CardItem } from './card-item';
import type { UserCard } from '@/types';

interface CardGridProps {
  cards: UserCard[];
}

export function CardGrid({ cards }: CardGridProps) {
  // Group cards by bank
  const cardsByBank = cards.reduce((acc, card) => {
    const bank = card.card_template.bank;
    if (!acc[bank]) {
      acc[bank] = [];
    }
    acc[bank].push(card);
    return acc;
  }, {} as Record<string, UserCard[]>);

  const banks = Object.keys(cardsByBank).sort();
  const [collapsed, setCollapsed] = useState<Set<string>>(new Set());

  const toggle = (bank: string) =>
    setCollapsed((prev) => {
      const next = new Set(prev);
      next.has(bank) ? next.delete(bank) : next.add(bank);
      return next;
    });

  return (
    <div className="space-y-4">
      {banks.map((bank, index) => {
        const isCollapsed = collapsed.has(bank);
        return (
          <div key={bank}>
            {index > 0 && <div className="border-t mb-4" />}
            <button
              onClick={() => toggle(bank)}
              className="flex items-center gap-3 mb-5 w-full text-left group"
            >
              {isCollapsed
                ? <ChevronRight className="h-4 w-4 text-muted-foreground" />
                : <ChevronDown className="h-4 w-4 text-muted-foreground" />
              }
              <h2 className="text-xl font-semibold group-hover:text-foreground/80 transition-colors">{bank}</h2>
              <span className="text-xs text-muted-foreground bg-muted px-2 py-0.5 rounded-full">
                {cardsByBank[bank].length} {cardsByBank[bank].length === 1 ? 'card' : 'cards'}
              </span>
            </button>
            {!isCollapsed && (
              <div className="grid gap-4 sm:gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
                {cardsByBank[bank].map((card) => (
                  <CardItem key={card.id} card={card} />
                ))}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
