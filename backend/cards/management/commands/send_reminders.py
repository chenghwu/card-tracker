from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from datetime import date
from collections import defaultdict

from cards.services.deadlines import get_expiring_benefits


# Only send reminders on these exact days-remaining thresholds
REMINDER_THRESHOLDS = {7, 3, 1}


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

        today = date.today()

        users = User.objects.filter(cards__is_active=True).distinct()

        total_emails = 0
        total_benefits = 0

        for user in users:
            # Fetch all benefits expiring within 7 days that still have value
            expiring_benefits = get_expiring_benefits(user, today, max_days=7)

            # Keep only benefits whose days_left exactly matches a reminder threshold
            benefits_by_threshold = defaultdict(list)
            for benefit in expiring_benefits:
                days_left = benefit.days_until_expiry
                if days_left not in REMINDER_THRESHOLDS:
                    continue
                if days_left == 1:
                    benefits_by_threshold['day_1'].append(benefit)
                elif days_left == 3:
                    benefits_by_threshold['day_3'].append(benefit)
                else:
                    benefits_by_threshold['day_7'].append(benefit)

            if not benefits_by_threshold:
                continue

            email_sent = self.send_reminder_email(
                user,
                benefits_by_threshold,
                dry_run=dry_run,
                test_email=test_email,
            )

            if email_sent:
                total_emails += 1
                total_benefits += sum(len(v) for v in benefits_by_threshold.values())

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
        day_1 = benefits_by_threshold.get('day_1', [])
        day_3 = benefits_by_threshold.get('day_3', [])
        day_7 = benefits_by_threshold.get('day_7', [])

        all_benefits = day_1 + day_3 + day_7
        total_unused_cents = sum(b.remaining_amount_cents for b in all_benefits)

        context = {
            'user': user,
            'day_1_benefits': day_1,
            'day_3_benefits': day_3,
            'day_7_benefits': day_7,
            'total_unused': total_unused_cents / 100,
            'total_benefits_count': len(all_benefits),
        }

        # Subject reflects the most urgent bucket present
        if day_1:
            subject = f'Card Tracker ⚠️ Last chance: {len(day_1)} benefit(s) expiring tomorrow!'
        elif day_3:
            subject = f'Card Tracker ⚠️ Urgent: {len(day_3)} benefit(s) expiring in 3 days!'
        else:
            subject = f'Card Tracker Reminder: {len(day_7)} benefit(s) expiring in 7 days'

        html_message = self.generate_html_email(context)
        plain_message = self.generate_plain_email(context)

        recipient_email = test_email if test_email else user.email

        if not recipient_email:
            self.stdout.write(self.style.WARNING(f'User {user.username} has no email address'))
            return False

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
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                html_message=html_message,
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Sent reminder to {recipient_email}'))
            return True
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send email to {recipient_email}: {str(e)}'))
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
        .upcoming {{ border-left-color: #3B82F6; }}
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
            <strong>Total unused:</strong> ${context['total_unused']:.2f} in {context['total_benefits_count']} benefit(s)
        </div>

        {self._render_benefit_section(context.get('day_1_benefits', []), 'Expiring tomorrow — last chance!', 'critical', '🚨')}
        {self._render_benefit_section(context.get('day_3_benefits', []), 'Expiring in 3 days', 'warning', '⚠️')}
        {self._render_benefit_section(context.get('day_7_benefits', []), 'Expiring in 7 days', 'upcoming', '📅')}

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
            bank = benefit.user_card.card_template.bank
            benefit_name = benefit.effective_name
            remaining = benefit.remaining_amount_cents / 100
            days_left = benefit.days_until_expiry
            period_end = benefit.current_period_end.strftime('%b %d, %Y')

            cards_html += f"""
        <div class="benefit-card {css_class}">
            <div class="benefit-header">{benefit_name}</div>
            <div class="benefit-meta">
                Card: {bank} {card_name}<br>
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

You have ${context['total_unused']:.2f} in unused credit card benefits expiring soon!

"""

        def write_section(benefits, header):
            out = header + '\n' + '-' * 50 + '\n'
            for benefit in benefits:
                card_name = benefit.user_card.nickname or benefit.user_card.card_template.name
                bank = benefit.user_card.card_template.bank
                remaining = benefit.remaining_amount_cents / 100
                days_left = benefit.days_until_expiry
                out += f"• {benefit.effective_name}\n"
                out += f"  Card: {bank} {card_name}\n"
                out += f"  Remaining: ${remaining:.2f}\n"
                out += f"  Expires in: {days_left} day{'s' if days_left != 1 else ''}\n\n"
            return out

        if context.get('day_1_benefits'):
            message += write_section(context['day_1_benefits'], '🚨 Expiring tomorrow — last chance!')
        if context.get('day_3_benefits'):
            message += write_section(context['day_3_benefits'], '⚠️  Expiring in 3 days')
        if context.get('day_7_benefits'):
            message += write_section(context['day_7_benefits'], '📅 Expiring in 7 days')

        message += """
Log in to your Card Tracker dashboard to use these benefits!

---
This is an automated reminder from Card Tracker
"""
        return message
