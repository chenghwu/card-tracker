'use client';

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

  return (
    <div className="space-y-8">
      {banks.map((bank) => (
        <div key={bank}>
          <h2 className="text-xl font-semibold mb-4">{bank}</h2>
          <div className="grid gap-4 sm:gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
            {cardsByBank[bank].map((card) => (
              <CardItem key={card.id} card={card} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
