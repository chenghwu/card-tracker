from django.core.management.base import BaseCommand
from cards.models import CardTemplate, BenefitTemplate
from cards.data.card_seeds import CARD_SEEDS


class Command(BaseCommand):
    help = 'Populate database with seed card templates and their benefits'

    def handle(self, *args, **options):
        self.stdout.write('Seeding card templates...')

        created_cards = 0
        updated_cards = 0
        created_benefits = 0

        for card_data in CARD_SEEDS:
            # Extract benefits from card data
            benefits_data = card_data.pop('benefits', [])

            # Create or update card template
            card_template, created = CardTemplate.objects.update_or_create(
                bank=card_data['bank'],
                name=card_data['name'],
                defaults=card_data
            )

            if created:
                created_cards += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {card_template}')
                )
            else:
                updated_cards += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated: {card_template}')
                )

            # Create benefit templates
            for benefit_data in benefits_data:
                benefit, created = BenefitTemplate.objects.get_or_create(
                    card_template=card_template,
                    name=benefit_data['name'],
                    defaults=benefit_data
                )

                if created:
                    created_benefits += 1
                    self.stdout.write(f'  - Added benefit: {benefit.name}')
                else:
                    # Update existing benefit with new data
                    for key, value in benefit_data.items():
                        setattr(benefit, key, value)
                    benefit.save()
                    self.stdout.write(f'  - Updated benefit: {benefit.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSeeding complete! Created {created_cards} cards, '
                f'updated {updated_cards} cards, created {created_benefits} benefits.'
            )
        )
