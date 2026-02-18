"""
Period calculation service for benefit tracking.
Handles calendar year vs membership year period calculations.
"""
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


def get_current_period(open_date: date, period_type: str, frequency: str, reference_date: date = None) -> tuple[date, date]:
    """
    Calculate the current benefit period based on card open date, period type, and frequency.

    Period rules:
    - monthly:     always 1st to last day of calendar month
    - quarterly:   always Jan-Mar, Apr-Jun, Jul-Sep, Oct-Dec
    - semi_annual: always Jan-Jun, Jul-Dec
    - annual:      calendar_year = Jan 1 - Dec 31
                   membership_year = card open date anniversary

    Args:
        open_date: The date the card was opened
        period_type: 'calendar_year' or 'membership_year'
        frequency: 'monthly', 'quarterly', 'semi_annual', or 'annual'
        reference_date: Date to calculate period for (defaults to today)

    Returns:
        Tuple of (period_start, period_end)
    """
    if reference_date is None:
        reference_date = date.today()

    # Monthly, quarterly, and semi-annual always follow calendar periods
    if frequency in ('monthly', 'quarterly', 'semi_annual'):
        return _get_calendar_year_period(reference_date, frequency)

    # Annual can be either calendar or membership year
    if period_type == 'calendar_year':
        return _get_calendar_year_period(reference_date, frequency)
    elif period_type == 'membership_year':
        return _get_membership_year_period(open_date, reference_date, frequency)
    else:
        raise ValueError(f"Invalid period_type: {period_type}")


def _get_calendar_year_period(reference_date: date, frequency: str) -> tuple[date, date]:
    """Calculate period based on calendar year"""
    year = reference_date.year

    if frequency == 'annual':
        period_start = date(year, 1, 1)
        period_end = date(year, 12, 31)

    elif frequency == 'semi_annual':
        # Two 6-month periods: Jan-Jun, Jul-Dec
        if reference_date.month <= 6:
            period_start = date(year, 1, 1)
            period_end = date(year, 6, 30)
        else:
            period_start = date(year, 7, 1)
            period_end = date(year, 12, 31)

    elif frequency == 'quarterly':
        # Four 3-month periods
        quarter = (reference_date.month - 1) // 3
        start_month = quarter * 3 + 1
        period_start = date(year, start_month, 1)

        # Calculate end of quarter
        end_month = start_month + 2
        if end_month == 12:
            period_end = date(year, 12, 31)
        else:
            period_end = date(year, end_month + 1, 1) - timedelta(days=1)

    elif frequency == 'monthly':
        period_start = date(year, reference_date.month, 1)
        # Last day of month
        if reference_date.month == 12:
            period_end = date(year, 12, 31)
        else:
            period_end = date(year, reference_date.month + 1, 1) - timedelta(days=1)

    else:
        raise ValueError(f"Invalid frequency: {frequency}")

    return period_start, period_end


def _get_membership_year_period(open_date: date, reference_date: date, frequency: str) -> tuple[date, date]:
    """Calculate period based on membership year (anniversary of card opening)"""

    if frequency == 'annual':
        # Find the most recent anniversary
        years_diff = reference_date.year - open_date.year
        period_start = date(reference_date.year, open_date.month, open_date.day)

        # If we haven't reached this year's anniversary yet, use last year's
        if reference_date < period_start:
            period_start = date(reference_date.year - 1, open_date.month, open_date.day)

        period_end = period_start + relativedelta(years=1) - timedelta(days=1)

    elif frequency == 'semi_annual':
        # Two 6-month periods per membership year
        months_since_open = (reference_date.year - open_date.year) * 12 + (reference_date.month - open_date.month)
        periods_since_open = months_since_open // 6

        period_start = open_date + relativedelta(months=periods_since_open * 6)
        period_end = period_start + relativedelta(months=6) - timedelta(days=1)

    elif frequency == 'quarterly':
        # Four 3-month periods per membership year
        months_since_open = (reference_date.year - open_date.year) * 12 + (reference_date.month - open_date.month)
        periods_since_open = months_since_open // 3

        period_start = open_date + relativedelta(months=periods_since_open * 3)
        period_end = period_start + relativedelta(months=3) - timedelta(days=1)

    elif frequency == 'monthly':
        # Monthly periods based on card open day
        months_since_open = (reference_date.year - open_date.year) * 12 + (reference_date.month - open_date.month)

        period_start = open_date + relativedelta(months=months_since_open)
        period_end = period_start + relativedelta(months=1) - timedelta(days=1)

    else:
        raise ValueError(f"Invalid frequency: {frequency}")

    return period_start, period_end


def get_next_period(period_end: date, frequency: str) -> tuple[date, date]:
    """
    Get the next period after a given period end date.

    Args:
        period_end: End date of the current period
        frequency: 'monthly', 'quarterly', 'semi_annual', or 'annual'

    Returns:
        Tuple of (next_period_start, next_period_end)
    """
    next_period_start = period_end + timedelta(days=1)

    if frequency == 'annual':
        next_period_end = next_period_start + relativedelta(years=1) - timedelta(days=1)
    elif frequency == 'semi_annual':
        next_period_end = next_period_start + relativedelta(months=6) - timedelta(days=1)
    elif frequency == 'quarterly':
        next_period_end = next_period_start + relativedelta(months=3) - timedelta(days=1)
    elif frequency == 'monthly':
        next_period_end = next_period_start + relativedelta(months=1) - timedelta(days=1)
    else:
        raise ValueError(f"Invalid frequency: {frequency}")

    return next_period_start, next_period_end
