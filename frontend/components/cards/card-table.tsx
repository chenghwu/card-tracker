'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { formatCurrency, formatDate } from '@/lib/utils';
import type { UserCard } from '@/types';
import { ArrowUpDown, ArrowUp, ArrowDown } from 'lucide-react';

type SortColumn = 'bank' | 'name' | 'credit_limit' | 'open_date' | 'card_type';
type SortDir = 'asc' | 'desc';

interface CardTableProps {
  cards: UserCard[];
}

function SortIcon({ column, sortCol, sortDir }: { column: SortColumn; sortCol: SortColumn; sortDir: SortDir }) {
  if (column !== sortCol) return <ArrowUpDown className="ml-1 h-3 w-3 text-muted-foreground/50" />;
  return sortDir === 'asc'
    ? <ArrowUp className="ml-1 h-3 w-3" />
    : <ArrowDown className="ml-1 h-3 w-3" />;
}

export function CardTable({ cards }: CardTableProps) {
  const [sortCol, setSortCol] = useState<SortColumn>('bank');
  const [sortDir, setSortDir] = useState<SortDir>('asc');

  const handleSort = (col: SortColumn) => {
    if (sortCol === col) {
      setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortCol(col);
      setSortDir('asc');
    }
  };

  const sorted = [...cards].sort((a, b) => {
    let aVal: string | number = '';
    let bVal: string | number = '';

    switch (sortCol) {
      case 'bank':
        aVal = a.card_template.bank.toLowerCase();
        bVal = b.card_template.bank.toLowerCase();
        break;
      case 'name':
        aVal = (a.nickname || a.card_template.name).toLowerCase();
        bVal = (b.nickname || b.card_template.name).toLowerCase();
        break;
      case 'credit_limit':
        aVal = a.credit_limit_cents ?? -1;
        bVal = b.credit_limit_cents ?? -1;
        break;
      case 'open_date':
        aVal = a.open_date;
        bVal = b.open_date;
        break;
      case 'card_type':
        aVal = a.card_type;
        bVal = b.card_type;
        break;
    }

    if (aVal < bVal) return sortDir === 'asc' ? -1 : 1;
    if (aVal > bVal) return sortDir === 'asc' ? 1 : -1;
    return 0;
  });

  const thClass = 'text-left text-xs font-medium text-muted-foreground uppercase tracking-wide whitespace-nowrap';
  const colBtn = 'inline-flex items-center hover:text-foreground transition-colors';

  return (
    <div className="rounded-lg border overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b bg-muted/50">
            <th className={`${thClass} px-4 py-3`}>
              <button className={colBtn} onClick={() => handleSort('bank')}>
                Bank / Issuer <SortIcon column="bank" sortCol={sortCol} sortDir={sortDir} />
              </button>
            </th>
            <th className={`${thClass} px-4 py-3`}>
              <button className={colBtn} onClick={() => handleSort('name')}>
                Card Name <SortIcon column="name" sortCol={sortCol} sortDir={sortDir} />
              </button>
            </th>
            <th className={`${thClass} px-4 py-3`}>
              <button className={colBtn} onClick={() => handleSort('credit_limit')}>
                Credit Limit <SortIcon column="credit_limit" sortCol={sortCol} sortDir={sortDir} />
              </button>
            </th>
            <th className={`${thClass} px-4 py-3`}>
              <button className={colBtn} onClick={() => handleSort('open_date')}>
                Open Date <SortIcon column="open_date" sortCol={sortCol} sortDir={sortDir} />
              </button>
            </th>
            <th className={`${thClass} px-4 py-3`}>
              <button className={colBtn} onClick={() => handleSort('card_type')}>
                Type <SortIcon column="card_type" sortCol={sortCol} sortDir={sortDir} />
              </button>
            </th>
            <th className={`${thClass} px-4 py-3`} />
          </tr>
        </thead>
        <tbody>
          {sorted.map((card, i) => (
            <tr
              key={card.id}
              className={`border-b last:border-0 hover:bg-muted/30 transition-colors ${i % 2 === 0 ? '' : 'bg-muted/10'}`}
            >
              <td className="px-4 py-3 text-muted-foreground">{card.card_template.bank}</td>
              <td className="px-4 py-3 font-medium">
                {card.nickname || card.card_template.name}
                {card.nickname && card.nickname.toLowerCase() !== card.card_template.name.toLowerCase() && (
                  <span className="ml-1.5 text-xs text-muted-foreground font-normal">
                    ({card.card_template.name})
                  </span>
                )}
              </td>
              <td className="px-4 py-3 text-muted-foreground">
                {card.credit_limit_cents ? formatCurrency(card.credit_limit_cents) : '—'}
              </td>
              <td className="px-4 py-3 text-muted-foreground whitespace-nowrap">{formatDate(card.open_date)}</td>
              <td className="px-4 py-3">
                <Badge
                  variant="outline"
                  className={card.card_type === 'business'
                    ? 'border-amber-500 text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/30'
                    : 'border-blue-500 text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/30'}
                >
                  {card.card_type === 'business' ? 'Business' : 'Personal'}
                </Badge>
              </td>
              <td className="px-4 py-3">
                <Button variant="ghost" size="sm" asChild>
                  <Link href={`/cards/${card.id}`}>View</Link>
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
