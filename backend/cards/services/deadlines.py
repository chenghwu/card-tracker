"""
Deadline and urgency calculation service.
Determines urgency levels for expiring benefits.
"""
from datetime import date, timedelta
from .tracking import get_benefit_status


def calculate_urgency(period_end: date, reference_date: date = None) -> tuple[str, int]:
    """
    Calculate urgency level based on days until period end.

    Args:
        period_end: End date of the benefit period
        reference_date: Date to calculate from (defaults to today)

    Returns:
        Tuple of (urgency_level, days_until_expiry)

    Urgency levels:
        - 'critical': 7 days or less
        - 'warning': 8-14 days
        - 'upcoming': 15-30 days
        - 'ok': 31+ days
    """
    if reference_date is None:
        reference_date = date.today()

    days_until_expiry = (period_end - reference_date).days

    if days_until_expiry < 0:
        urgency = 'expired'
    elif days_until_expiry <= 7:
        urgency = 'critical'
    elif days_until_expiry <= 14:
        urgency = 'warning'
    elif days_until_expiry <= 30:
        urgency = 'upcoming'
    else:
        urgency = 'ok'

    return urgency, days_until_expiry


def get_expiring_benefits(user, reference_date: date = None, max_days: int = 30):
    """
    Get all benefits that are expiring within the specified number of days,
    with remaining value.

    Args:
        user: User to get benefits for
        reference_date: Date to calculate from (defaults to today)
        max_days: Maximum days until expiry to include (default 30)

    Returns:
        List of benefits with urgency information, sorted by urgency
    """
    from ..models import UserCard

    if reference_date is None:
        reference_date = date.today()

    expiring_benefits = []

    # Get all active user cards
    user_cards = UserCard.objects.filter(
        user=user,
        is_active=True
    ).prefetch_related('benefits__benefit_template')

    for user_card in user_cards:
        for user_benefit in user_card.benefits.all():
            # Get benefit status
            status = get_benefit_status(user_benefit, reference_date)

            # Only include if there's remaining value
            if status['remaining_amount_cents'] > 0:
                urgency, days_until_expiry = calculate_urgency(
                    status['period_end'],
                    reference_date
                )

                # Only include if expiring within max_days
                if days_until_expiry <= max_days and days_until_expiry >= 0:
                    # Attach urgency info to benefit
                    user_benefit.urgency = urgency
                    user_benefit.days_until_expiry = days_until_expiry
                    user_benefit.used_amount_cents = status['used_amount_cents']
                    user_benefit.remaining_amount_cents = status['remaining_amount_cents']
                    user_benefit.current_period_start = status['period_start']
                    user_benefit.current_period_end = status['period_end']

                    expiring_benefits.append(user_benefit)

    # Sort by urgency (critical first) then by days until expiry
    urgency_order = {'critical': 0, 'warning': 1, 'upcoming': 2}
    expiring_benefits.sort(
        key=lambda b: (urgency_order.get(b.urgency, 3), b.days_until_expiry)
    )

    return expiring_benefits


def get_dashboard_summary(user, reference_date: date = None):
    """
    Get dashboard summary statistics for a user.

    Args:
        user: User to get summary for
        reference_date: Date to calculate from (defaults to today)

    Returns:
        Dictionary with summary statistics
    """
    from ..models import UserCard

    if reference_date is None:
        reference_date = date.today()

    # Get all active user cards
    user_cards = UserCard.objects.filter(
        user=user,
        is_active=True
    ).prefetch_related('benefits__benefit_template', 'benefits__usage_records')

    total_cards = user_cards.count()
    total_benefits = 0
    total_credits_available_cents = 0
    total_credits_used_cents = 0
    total_annual_fee_cents = 0
    critical_benefits = 0
    warning_benefits = 0

    for user_card in user_cards:
        total_annual_fee_cents += user_card.card_template.annual_fee_cents
        for user_benefit in user_card.benefits.all():
            total_benefits += 1

            # Get benefit status
            status = get_benefit_status(user_benefit, reference_date)

            total_credits_available_cents += status['remaining_amount_cents']
            total_credits_used_cents += status['used_amount_cents']

            # Check urgency
            if status['remaining_amount_cents'] > 0:
                urgency, _ = calculate_urgency(status['period_end'], reference_date)
                if urgency == 'critical':
                    critical_benefits += 1
                elif urgency == 'warning':
                    warning_benefits += 1

    return {
        'total_cards': total_cards,
        'total_benefits': total_benefits,
        'total_annual_fee_cents': total_annual_fee_cents,
        'total_credits_available_cents': total_credits_available_cents,
        'total_credits_used_cents': total_credits_used_cents,
        'total_credits_total_cents': total_credits_available_cents + total_credits_used_cents,
        'critical_benefits': critical_benefits,
        'warning_benefits': warning_benefits,
        'utilization_rate': round(
            (total_credits_used_cents / (total_credits_available_cents + total_credits_used_cents) * 100)
            if (total_credits_available_cents + total_credits_used_cents) > 0 else 0,
            1
        )
    }
