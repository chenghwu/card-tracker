from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class CardTemplate(models.Model):
    """Shared card definitions - one per card product"""
    bank = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    annual_fee_cents = models.IntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['bank', 'name']
        unique_together = ['bank', 'name']

    def __str__(self):
        return f"{self.bank} {self.name}"


class BenefitTemplate(models.Model):
    """Benefit tied to a card template"""
    PERIOD_TYPE_CHOICES = [
        ('calendar_year', 'Calendar Year'),
        ('membership_year', 'Membership Year'),
    ]

    FREQUENCY_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annual', 'Semi-Annual'),
        ('annual', 'Annual'),
    ]

    CATEGORY_CHOICES = [
        ('travel', 'Travel'),
        ('dining', 'Dining'),
        ('entertainment', 'Entertainment'),
        ('shopping', 'Shopping'),
        ('transportation', 'Transportation'),
        ('other', 'Other'),
    ]

    card_template = models.ForeignKey(
        CardTemplate,
        on_delete=models.CASCADE,
        related_name='benefits'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    amount_cents = models.IntegerField()
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    period_type = models.CharField(max_length=20, choices=PERIOD_TYPE_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['card_template', 'name']

    def __str__(self):
        return f"{self.card_template.name} - {self.name}"


class UserCard(models.Model):
    """A card owned by a specific user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    card_template = models.ForeignKey(
        CardTemplate,
        on_delete=models.CASCADE,
        related_name='user_cards'
    )
    CARD_TYPE_CHOICES = [
        ('personal', 'Personal'),
        ('business', 'Business'),
    ]

    open_date = models.DateField()
    nickname = models.CharField(max_length=100, blank=True)
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES, default='personal')
    credit_limit_cents = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.nickname or self.card_template.name}"


class UserBenefit(models.Model):
    """User's benefit instance (allows per-user overrides)"""
    user_card = models.ForeignKey(
        UserCard,
        on_delete=models.CASCADE,
        related_name='benefits'
    )
    benefit_template = models.ForeignKey(
        BenefitTemplate,
        on_delete=models.CASCADE,
        related_name='user_benefits'
    )
    custom_amount_cents = models.IntegerField(null=True, blank=True)
    custom_name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user_card', 'benefit_template']

    def __str__(self):
        return f"{self.user_card} - {self.custom_name or self.benefit_template.name}"

    @property
    def effective_amount_cents(self):
        """Return custom amount if set, otherwise template amount"""
        return self.custom_amount_cents if self.custom_amount_cents is not None else self.benefit_template.amount_cents

    @property
    def effective_name(self):
        """Return custom name if set, otherwise template name"""
        return self.custom_name or self.benefit_template.name


class BenefitUsage(models.Model):
    """Usage record for a benefit within a specific period"""
    user_benefit = models.ForeignKey(
        UserBenefit,
        on_delete=models.CASCADE,
        related_name='usage_records'
    )
    amount_cents = models.IntegerField()
    used_at = models.DateTimeField(default=timezone.now)
    period_start = models.DateField()
    period_end = models.DateField()
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-used_at']

    def __str__(self):
        return f"{self.user_benefit} - {self.amount_cents/100:.2f} on {self.used_at.date()}"
