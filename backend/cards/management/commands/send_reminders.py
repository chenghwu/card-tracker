from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import date, timedelta
from collections import defaultdict

from cards.services.deadlines import get_expiring_benefits, calculate_urgency


class Command(BaseCommand):
    help = 'Send email reminders to users about expiring benefits'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview emails without sending',
        )
        parser.add_argument(
            '--test-email',
            type=str,
            help='Send test email to specified address',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        test_email = options['test_email']

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No emails will be sent'))

        # Define reminder thresholds
        thresholds = [3, 7, 14]  # Days before expiration
        today = date.today()

        # Get all users with active cards
        users = User.objects.filter(
            cards__is_active=True
        ).distinct()

        total_emails = 0
        total_benefits = 0

        for user in users:
            # Get expiring benefits for this user (within 14 days)
            expiring_benefits = get_expiring_benefits(user, today, max_days=14)

            if not expiring_benefits:
                continue

            # Group benefits by urgency threshold
            benefits_by_threshold = defaultdict(list)

            for benefit in expiring_benefits:
                days_left = benefit.days_until_expiry

                # Categorize by threshold
                if days_left <= 3:
                    benefits_by_threshold['critical'].append(benefit)
                elif days_left <= 7:
                    benefits_by_threshold['warning_7'].append(benefit)
                elif days_left <= 14:
                    benefits_by_threshold['warning_14'].append(benefit)

            # Only send if there are benefits in our thresholds
            if benefits_by_threshold:
                email_sent = self.send_reminder_email(
                    user,
                    benefits_by_threshold,
                    dry_run=dry_run,
                    test_email=test_email
                )

                if email_sent:
                    total_emails += 1
                    total_benefits += len(expiring_benefits)

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nDRY RUN: Would have sent {total_emails} emails '
                    f'for {total_benefits} expiring benefits'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nSuccessfully sent {total_emails} reminder emails '
                    f'for {total_benefits} expiring benefits'
                )
            )

    def send_reminder_email(self, user, benefits_by_threshold, dry_run=False, test_email=None):
        """
        Send reminder email to user about expiring benefits.
        """
        # Prepare email context
        critical_benefits = benefits_by_threshold.get('critical', [])
        warning_7_benefits = benefits_by_threshold.get('warning_7', [])
        warning_14_benefits = benefits_by_threshold.get('warning_14', [])

        total_at_risk_cents = sum(
            b.remaining_amount_cents
            for benefits_list in benefits_by_threshold.values()
            for b in benefits_list
        )

        context = {
            'user': user,
            'critical_benefits': critical_benefits,
            'warning_7_benefits': warning_7_benefits,
            'warning_14_benefits': warning_14_benefits,
            'total_at_risk': total_at_risk_cents / 100,
            'total_benefits_count': sum(len(b) for b in benefits_by_threshold.values()),
        }

        # Create email subject
        if critical_benefits:
            subject = f'⚠️ Urgent: {len(critical_benefits)} credit card benefit(s) expiring in 3 days!'
        elif warning_7_benefits:
            subject = f'Reminder: {len(warning_7_benefits)} credit card benefit(s) expiring this week'
        else:
            subject = f'Reminder: {len(warning_14_benefits)} credit card benefit(s) expiring soon'

        # Generate email body
        html_message = self.generate_html_email(context)
        plain_message = self.generate_plain_email(context)

        # Determine recipient
        recipient_email = test_email if test_email else user.email

        if not recipient_email:
            self.stdout.write(
                self.style.WARNING(f'User {user.username} has no email address')
            )
            return False

        # Send email
        if dry_run:
            self.stdout.write(f'\n{"-" * 80}')
            self.stdout.write(self.style.SUCCESS(f'TO: {recipient_email}'))
            self.stdout.write(self.style.SUCCESS(f'SUBJECT: {subject}'))
            self.stdout.write(f'\n{plain_message}\n')
            self.stdout.write(f'{"-" * 80}\n')
            return True

        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@cardtracker.com',
                recipient_list=[recipient_email],
                html_message=html_message,
                fail_silently=False,
            )
            self.stdout.write(
                self.style.SUCCESS(f'Sent reminder to {recipient_email}')
            )
            return True
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to send email to {recipient_email}: {str(e)}')
            )
            return False

    def generate_html_email(self, context):
        """Generate HTML email content."""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }}
        .header {{ background-color: #4F46E5; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; background-color: #f9fafb; }}
        .benefit-group {{ margin-bottom: 30px; }}
        .benefit-card {{ background: white; border-left: 4px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 4px; }}
        .critical {{ border-left-color: #DC2626; }}
        .warning {{ border-left-color: #F59E0B; }}
        .benefit-header {{ font-weight: bold; margin-bottom: 5px; }}
        .benefit-meta {{ font-size: 14px; color: #666; }}
        .amount {{ font-weight: bold; color: #059669; }}
        .footer {{ padding: 20px; text-align: center; color: #666; font-size: 12px; }}
        .summary {{ background: #FEF3C7; border: 1px solid #F59E0B; padding: 15px; border-radius: 4px; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Credit Card Benefits Reminder</h1>
    </div>
    <div class="content">
        <div class="summary">
            <strong>Total at risk:</strong> ${context['total_at_risk']:.2f} in {context['total_benefits_count']} benefit(s)
        </div>

        {self._render_benefit_section(
            context.get('critical_benefits', []),
            'Critical: Expiring in 3 days or less!',
            'critical',
            '🚨'
        )}

        {self._render_benefit_section(
            context.get('warning_7_benefits', []),
            'Expiring this week (4-7 days)',
            'warning',
            '⚠️'
        )}

        {self._render_benefit_section(
            context.get('warning_14_benefits', []),
            'Expiring soon (8-14 days)',
            'warning',
            '📅'
        )}

        <p>Log in to your Card Tracker dashboard to use these benefits before they expire!</p>
    </div>
    <div class="footer">
        <p>This is an automated reminder from Card Tracker</p>
        <p>You're receiving this because you have credit card benefits expiring soon</p>
    </div>
</body>
</html>
"""

    def _render_benefit_section(self, benefits, title, css_class, icon):
        """Render a section of benefits in HTML."""
        if not benefits:
            return ''

        cards_html = ''
        for benefit in benefits:
            card_name = benefit.user_card.nickname or benefit.user_card.card_template.name
            benefit_name = benefit.effective_name
            remaining = benefit.remaining_amount_cents / 100
            days_left = benefit.days_until_expiry
            period_end = benefit.current_period_end.strftime('%b %d, %Y')

            cards_html += f"""
        <div class="benefit-card {css_class}">
            <div class="benefit-header">{benefit_name}</div>
            <div class="benefit-meta">
                Card: {card_name}<br>
                Remaining: <span class="amount">${remaining:.2f}</span><br>
                Expires: {period_end} ({days_left} day{'s' if days_left != 1 else ''} left)
            </div>
        </div>
"""

        return f"""
        <div class="benefit-group">
            <h2>{icon} {title}</h2>
            {cards_html}
        </div>
"""

    def generate_plain_email(self, context):
        """Generate plain text email content."""
        message = f"""
Credit Card Benefits Reminder
{'=' * 50}

Hi {context['user'].first_name or context['user'].username},

You have ${context['total_at_risk']:.2f} in credit card benefits expiring soon!

"""

        if context.get('critical_benefits'):
            message += "\n🚨 CRITICAL: Expiring in 3 days or less!\n"
            message += "-" * 50 + "\n"
            for benefit in context['critical_benefits']:
                card_name = benefit.user_card.nickname or benefit.user_card.card_template.name
                remaining = benefit.remaining_amount_cents / 100
                days_left = benefit.days_until_expiry
                message += f"• {benefit.effective_name}\n"
                message += f"  Card: {card_name}\n"
                message += f"  Remaining: ${remaining:.2f}\n"
                message += f"  Expires in: {days_left} day{'s' if days_left != 1 else ''}\n\n"

        if context.get('warning_7_benefits'):
            message += "\n⚠️  Expiring this week (4-7 days)\n"
            message += "-" * 50 + "\n"
            for benefit in context['warning_7_benefits']:
                card_name = benefit.user_card.nickname or benefit.user_card.card_template.name
                remaining = benefit.remaining_amount_cents / 100
                days_left = benefit.days_until_expiry
                message += f"• {benefit.effective_name}\n"
                message += f"  Card: {card_name}\n"
                message += f"  Remaining: ${remaining:.2f}\n"
                message += f"  Expires in: {days_left} days\n\n"

        if context.get('warning_14_benefits'):
            message += "\n📅 Expiring soon (8-14 days)\n"
            message += "-" * 50 + "\n"
            for benefit in context['warning_14_benefits']:
                card_name = benefit.user_card.nickname or benefit.user_card.card_template.name
                remaining = benefit.remaining_amount_cents / 100
                days_left = benefit.days_until_expiry
                message += f"• {benefit.effective_name}\n"
                message += f"  Card: {card_name}\n"
                message += f"  Remaining: ${remaining:.2f}\n"
                message += f"  Expires in: {days_left} days\n\n"

        message += """
Log in to your Card Tracker dashboard to use these benefits!

---
This is an automated reminder from Card Tracker
"""
        return message
