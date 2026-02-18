"""
Management command to update card benefits using Gemini AI.

Usage:
    python manage.py update_benefits                  # Update all verified cards
    python manage.py update_benefits --bank "Chase"   # Update one bank only
    python manage.py update_benefits --card-id 5      # Update one card only
    python manage.py update_benefits --dry-run        # Preview without saving

Schedule this command to run weekly (e.g. via cron or Render cron job):
    0 3 * * 1  python manage.py update_benefits  >> /var/log/update_benefits.log 2>&1
"""
import json
import time
from django.core.management.base import BaseCommand
from cards.models import CardTemplate, BenefitTemplate
from cards.services.card_lookup import lookup_card_benefits


class Command(BaseCommand):
    help = 'Update card benefits using Gemini AI to stay current'

    def add_arguments(self, parser):
        parser.add_argument('--bank', type=str, help='Only update cards from this bank')
        parser.add_argument('--card-id', type=int, help='Only update this specific card template ID')
        parser.add_argument('--dry-run', action='store_true', help='Preview changes without saving')
        parser.add_argument('--delay', type=float, default=2.0,
                            help='Seconds to wait between Gemini API calls (default: 2)')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        delay = options['delay']

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN — no changes will be saved\n'))

        # Build queryset
        cards = CardTemplate.objects.filter(is_verified=True)
        if options['card_id']:
            cards = cards.filter(id=options['card_id'])
        elif options['bank']:
            cards = cards.filter(bank__iexact=options['bank'])

        total = cards.count()
        self.stdout.write(f'Updating {total} card(s) via Gemini AI...\n')

        updated = 0
        skipped = 0
        errors = 0

        for card in cards:
            self.stdout.write(f'\n[{card.bank}] {card.name}')

            result = lookup_card_benefits(card.name, card.bank)

            if not result['success']:
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Gemini error: {result["error"]}')
                )
                errors += 1
                time.sleep(delay)
                continue

            card_data = result['card_data']
            ai_benefits = card_data.get('benefits', [])

            if not ai_benefits:
                self.stdout.write(self.style.WARNING('  - No benefits returned, skipping'))
                skipped += 1
                time.sleep(delay)
                continue

            changes = self._compute_changes(card, ai_benefits)

            if not changes['has_changes']:
                self.stdout.write('  ✓ Already up to date')
                skipped += 1
                time.sleep(delay)
                continue

            # Report changes
            for b in changes['to_add']:
                self.stdout.write(
                    self.style.SUCCESS(f'  + ADD: {b["name"]} (${b["amount_cents"]/100:.0f} {b["frequency"]})')
                )
            for name, diff in changes['to_update']:
                self.stdout.write(
                    self.style.WARNING(f'  ~ UPDATE: {name} — {diff}')
                )
            for name in changes['to_remove']:
                self.stdout.write(
                    self.style.ERROR(f'  - REMOVE: {name}')
                )

            if not dry_run:
                self._apply_changes(card, ai_benefits, changes)
                # Mark card as recently verified
                card.is_verified = True
                card.save(update_fields=['updated_at'])
                updated += 1
            else:
                updated += 1  # count as would-be updated in dry run

            time.sleep(delay)

        self.stdout.write('\n' + '─' * 50)
        if dry_run:
            self.stdout.write(self.style.WARNING(
                f'DRY RUN complete: {updated} would update, {skipped} unchanged, {errors} errors'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Done: {updated} updated, {skipped} unchanged, {errors} errors'
            ))

    def _compute_changes(self, card, ai_benefits):
        """Compare AI benefits against DB and return what needs to change."""
        existing = {b.name: b for b in card.benefits.all()}
        ai_names = {b['name'] for b in ai_benefits}

        to_add = []
        to_update = []
        to_remove = []

        for ai_b in ai_benefits:
            name = ai_b['name']
            amount = ai_b.get('amount_cents', 0)
            freq = ai_b.get('frequency', '')
            period = ai_b.get('period_type', '')

            if name not in existing:
                to_add.append(ai_b)
            else:
                db_b = existing[name]
                diffs = []
                if db_b.amount_cents != amount:
                    diffs.append(f'amount ${db_b.amount_cents/100:.0f}→${amount/100:.0f}')
                if db_b.frequency != freq:
                    diffs.append(f'frequency {db_b.frequency}→{freq}')
                if db_b.period_type != period:
                    diffs.append(f'period_type {db_b.period_type}→{period}')
                if diffs:
                    to_update.append((name, ', '.join(diffs)))

        # Benefits in DB but not in AI response — flag but don't auto-remove
        # (AI might just not know about a benefit; safer to flag only)
        for name in existing:
            if name not in ai_names:
                to_remove.append(name)

        return {
            'has_changes': bool(to_add or to_update),
            'to_add': to_add,
            'to_update': to_update,
            'to_remove': to_remove,  # flagged only, not auto-deleted
        }

    def _apply_changes(self, card, ai_benefits, changes):
        """Save the computed changes to the database."""
        existing = {b.name: b for b in card.benefits.all()}

        # Add new benefits
        for b_data in changes['to_add']:
            BenefitTemplate.objects.create(
                card_template=card,
                name=b_data['name'],
                description=b_data.get('description', ''),
                amount_cents=b_data.get('amount_cents', 0),
                frequency=b_data.get('frequency', 'annual'),
                period_type=b_data.get('period_type', 'calendar_year'),
                category=b_data.get('category', 'other'),
            )

        # Update changed benefits
        for name, _ in changes['to_update']:
            ai_b = next(b for b in ai_benefits if b['name'] == name)
            db_b = existing[name]
            db_b.amount_cents = ai_b.get('amount_cents', db_b.amount_cents)
            db_b.frequency = ai_b.get('frequency', db_b.frequency)
            db_b.period_type = ai_b.get('period_type', db_b.period_type)
            db_b.description = ai_b.get('description', db_b.description)
            db_b.category = ai_b.get('category', db_b.category)
            db_b.save()
