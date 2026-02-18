"""
Gemini AI integration for card data lookup.
Uses Gemini 2.5 Flash to extract card and benefit information.
"""
from google import genai
from django.conf import settings


def get_gemini_client():
    """Get configured Gemini client"""
    if settings.GEMINI_API_KEY:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        return client
    return None


def lookup_card_benefits(card_name: str, bank: str = None) -> dict:
    """
    Use Gemini AI to lookup card benefits.

    Args:
        card_name: Name of the credit card
        bank: Optional bank/issuer name

    Returns:
        Dictionary with card information and benefits, or error message
    """
    client = get_gemini_client()
    if not client:
        return {
            'success': False,
            'error': 'Gemini API key not configured'
        }

    try:

        # Construct the prompt
        full_name = f"{bank} {card_name}" if bank else card_name

        prompt = f"""
Please provide detailed information about the {full_name} credit card, including:

1. Official card name
2. Issuing bank
3. Annual fee (in USD)
4. All recurring credit benefits (e.g., travel credits, dining credits, shopping credits)

For each benefit, include:
- Benefit name
- Description
- Amount (in USD)
- Frequency (monthly, quarterly, semi-annual, or annual)
- Period type (calendar year or membership year)
- Category (travel, dining, entertainment, shopping, transportation, or other)

Format your response as JSON with this structure:
{{
    "bank": "Bank Name",
    "name": "Card Name",
    "annual_fee_usd": 695,
    "benefits": [
        {{
            "name": "Benefit Name",
            "description": "Description of the benefit",
            "amount_usd": 200,
            "frequency": "annual",
            "period_type": "calendar_year",
            "category": "travel"
        }}
    ]
}}

Only include benefits that are:
- Recurring credits (not one-time bonuses)
- Have a fixed dollar amount
- Are automatically available to all cardholders

If the card doesn't exist or you're not confident about the information, return:
{{
    "error": "Card not found or information unavailable"
}}
"""

        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt
        )
        result_text = response.text

        # Try to parse JSON from the response
        import json
        import re

        # Extract JSON from markdown code blocks if present
        json_match = re.search(r'```json\s*(.*?)\s*```', result_text, re.DOTALL)
        if json_match:
            result_text = json_match.group(1)
        else:
            # Try to find JSON object in the text
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(0)

        card_data = json.loads(result_text)

        # Check for error in response
        if 'error' in card_data:
            return {
                'success': False,
                'error': card_data['error']
            }

        # Convert USD to cents
        if 'annual_fee_usd' in card_data:
            card_data['annual_fee_cents'] = int(card_data['annual_fee_usd'] * 100)
            del card_data['annual_fee_usd']

        for benefit in card_data.get('benefits', []):
            if 'amount_usd' in benefit:
                benefit['amount_cents'] = int(benefit['amount_usd'] * 100)
                del benefit['amount_usd']

        return {
            'success': True,
            'card_data': card_data
        }

    except json.JSONDecodeError as e:
        return {
            'success': False,
            'error': f'Failed to parse AI response: {str(e)}',
            'raw_response': result_text
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Gemini API error: {str(e)}'
        }


def create_card_from_lookup(card_data: dict) -> dict:
    """
    Create a CardTemplate and BenefitTemplates from lookup data.

    Args:
        card_data: Card data dictionary from lookup_card_benefits

    Returns:
        Dictionary with created card information
    """
    from ..models import CardTemplate, BenefitTemplate

    try:
        # Create CardTemplate
        card_template, created = CardTemplate.objects.get_or_create(
            bank=card_data['bank'],
            name=card_data['name'],
            defaults={
                'annual_fee_cents': card_data.get('annual_fee_cents', 0),
                'is_verified': False  # Mark as unverified since it came from AI
            }
        )

        if not created:
            # Update existing card
            card_template.annual_fee_cents = card_data.get('annual_fee_cents', 0)
            card_template.save()

        # Create BenefitTemplates
        benefits_created = 0
        for benefit_data in card_data.get('benefits', []):
            benefit, benefit_created = BenefitTemplate.objects.get_or_create(
                card_template=card_template,
                name=benefit_data['name'],
                defaults={
                    'description': benefit_data.get('description', ''),
                    'amount_cents': benefit_data['amount_cents'],
                    'frequency': benefit_data['frequency'],
                    'period_type': benefit_data['period_type'],
                    'category': benefit_data.get('category', 'other'),
                }
            )

            if benefit_created:
                benefits_created += 1

        return {
            'success': True,
            'card_id': card_template.id,
            'card_created': created,
            'benefits_created': benefits_created,
            'message': f"{'Created' if created else 'Updated'} card with {benefits_created} new benefits"
        }

    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to create card: {str(e)}'
        }
