"""
Benefit tracking service.
Calculates used and remaining amounts for benefits.
"""
from datetime import date
from django.db.models import Sum
from .periods import get_current_period


def get_benefit_status(user_benefit, reference_date: date = None):
    """
    Calculate the current status of a user benefit including:
    - Current period start/end dates
    - Used amount in current period
    - Remaining amount in current period

    Args:
        user_benefit: UserBenefit instance
        reference_date: Date to calculate status for (defaults to today)

    Returns:
        Dictionary with status information
    """
    if reference_date is None:
        reference_date = date.today()

    benefit_template = user_benefit.benefit_template
    user_card = user_benefit.user_card

    # Get current period
    period_start, period_end = get_current_period(
        open_date=user_card.open_date,
        period_type=benefit_template.period_type,
        frequency=benefit_template.frequency,
        reference_date=reference_date
    )

    # Calculate used amount in current period
    used_amount = user_benefit.usage_records.filter(
        period_start=period_start,
        period_end=period_end
    ).aggregate(total=Sum('amount_cents'))['total'] or 0

    # Get effective benefit amount
    effective_amount = user_benefit.effective_amount_cents

    # Calculate remaining amount
    remaining_amount = max(0, effective_amount - used_amount)

    return {
        'period_start': period_start,
        'period_end': period_end,
        'used_amount_cents': used_amount,
        'remaining_amount_cents': remaining_amount,
        'effective_amount_cents': effective_amount,
        'is_fully_used': remaining_amount == 0,
    }


def get_benefits_with_status(user_card, reference_date: date = None):
    """
    Get all benefits for a user card with their current status.

    Args:
        user_card: UserCard instance
        reference_date: Date to calculate status for (defaults to today)

    Returns:
        List of benefits with status information attached
    """
    benefits = []

    for user_benefit in user_card.benefits.select_related('benefit_template').all():
        status = get_benefit_status(user_benefit, reference_date)

        # Attach status to benefit
        user_benefit.used_amount_cents = status['used_amount_cents']
        user_benefit.remaining_amount_cents = status['remaining_amount_cents']
        user_benefit.current_period_start = status['period_start']
        user_benefit.current_period_end = status['period_end']
        user_benefit.is_fully_used = status['is_fully_used']

        # Attach urgency (local import avoids circular dependency)
        from .deadlines import calculate_urgency
        urgency, days_until_expiry = calculate_urgency(status['period_end'], reference_date)
        user_benefit.urgency = urgency
        user_benefit.days_until_expiry = days_until_expiry

        benefits.append(user_benefit)

    return benefits


def record_usage(user_benefit, amount_cents: int, used_at: date = None, note: str = ''):
    """
    Record a benefit usage.

    Args:
        user_benefit: UserBenefit instance
        amount_cents: Amount used in cents
        used_at: Date of usage (defaults to today)
        note: Optional note about the usage

    Returns:
        Created BenefitUsage instance

    Raises:
        ValueError: If amount exceeds remaining amount
    """
    from ..models import BenefitUsage

    if used_at is None:
        used_at = date.today()

    # Get current period
    benefit_template = user_benefit.benefit_template
    user_card = user_benefit.user_card

    period_start, period_end = get_current_period(
        open_date=user_card.open_date,
        period_type=benefit_template.period_type,
        frequency=benefit_template.frequency,
        reference_date=used_at
    )

    # Check if usage would exceed benefit amount
    status = get_benefit_status(user_benefit, used_at)
    if amount_cents > status['remaining_amount_cents']:
        raise ValueError(
            f"Amount {amount_cents/100:.2f} exceeds remaining benefit "
            f"amount {status['remaining_amount_cents']/100:.2f}"
        )

    # Create usage record
    usage = BenefitUsage.objects.create(
        user_benefit=user_benefit,
        amount_cents=amount_cents,
        used_at=used_at,
        period_start=period_start,
        period_end=period_end,
        note=note
    )

    return usage


def delete_usage(usage_id: int, user):
    """
    Delete (undo) a benefit usage.

    Args:
        usage_id: ID of the BenefitUsage to delete
        user: User making the request (for permission check)

    Raises:
        PermissionError: If usage doesn't belong to user
    """
    from ..models import BenefitUsage

    try:
        usage = BenefitUsage.objects.select_related(
            'user_benefit__user_card__user'
        ).get(id=usage_id)
    except BenefitUsage.DoesNotExist:
        raise ValueError(f"Usage with id {usage_id} not found")

    # Check permission
    if usage.user_benefit.user_card.user != user:
        raise PermissionError("You don't have permission to delete this usage")

    usage.delete()
