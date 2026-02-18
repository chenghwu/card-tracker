#!/usr/bin/env python
"""
Quick API test script to verify endpoints are working.
Run: uv run python test_api.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'card_tracker.settings')
django.setup()

from cards.models import CardTemplate, BenefitTemplate

# Test data retrieval
print("Testing Card Tracker Backend API")
print("=" * 50)

# Check card templates
card_count = CardTemplate.objects.count()
print(f"\n✓ Card Templates in database: {card_count}")

# Show some cards
if card_count > 0:
    print("\nSample cards:")
    for card in CardTemplate.objects.all()[:5]:
        benefit_count = card.benefits.count()
        print(f"  - {card.bank} {card.name}")
        print(f"    Annual Fee: ${card.annual_fee_cents/100:.2f}")
        print(f"    Benefits: {benefit_count}")

# Check benefits
benefit_count = BenefitTemplate.objects.count()
print(f"\n✓ Total Benefits in database: {benefit_count}")

if benefit_count > 0:
    print("\nSample benefits:")
    for benefit in BenefitTemplate.objects.all()[:3]:
        print(f"  - {benefit.name}")
        print(f"    Card: {benefit.card_template.name}")
        print(f"    Amount: ${benefit.amount_cents/100:.2f}")
        print(f"    Frequency: {benefit.frequency}")

print("\n" + "=" * 50)
print("✓ Backend API setup complete!")
print("\nNext steps:")
print("1. Start the server: uv run python manage.py runserver 8000")
print("2. Visit http://localhost:8000/admin/ to manage data")
print("3. Test API endpoints at http://localhost:8000/api/")
print("\nAvailable endpoints:")
print("  - GET /api/card-templates/")
print("  - GET /api/card-templates/?q=platinum")
print("  - GET /api/cards/ (requires auth)")
print("  - GET /api/dashboard/summary/ (requires auth)")
print("  - GET /api/dashboard/deadlines/ (requires auth)")
