from django.contrib import admin
from .models import CardTemplate, BenefitTemplate, UserCard, UserBenefit, BenefitUsage


class BenefitTemplateInline(admin.TabularInline):
    model = BenefitTemplate
    extra = 1


@admin.register(CardTemplate)
class CardTemplateAdmin(admin.ModelAdmin):
    list_display = ['bank', 'name', 'annual_fee_cents', 'is_verified', 'created_at']
    list_filter = ['bank', 'is_verified']
    search_fields = ['bank', 'name']
    inlines = [BenefitTemplateInline]


@admin.register(BenefitTemplate)
class BenefitTemplateAdmin(admin.ModelAdmin):
    list_display = ['card_template', 'name', 'amount_cents', 'frequency', 'period_type', 'category']
    list_filter = ['frequency', 'period_type', 'category']
    search_fields = ['name', 'card_template__name']


class UserBenefitInline(admin.TabularInline):
    model = UserBenefit
    extra = 0


@admin.register(UserCard)
class UserCardAdmin(admin.ModelAdmin):
    list_display = ['user', 'card_template', 'nickname', 'open_date', 'is_active', 'created_at']
    list_filter = ['is_active', 'card_template__bank']
    search_fields = ['user__username', 'user__email', 'card_template__name', 'nickname']
    inlines = [UserBenefitInline]


class BenefitUsageInline(admin.TabularInline):
    model = BenefitUsage
    extra = 0


@admin.register(UserBenefit)
class UserBenefitAdmin(admin.ModelAdmin):
    list_display = ['user_card', 'benefit_template', 'effective_name', 'effective_amount_cents']
    search_fields = ['user_card__user__username', 'benefit_template__name']
    inlines = [BenefitUsageInline]


@admin.register(BenefitUsage)
class BenefitUsageAdmin(admin.ModelAdmin):
    list_display = ['user_benefit', 'amount_cents', 'used_at', 'period_start', 'period_end']
    list_filter = ['used_at']
    search_fields = ['user_benefit__benefit_template__name', 'note']
    date_hierarchy = 'used_at'
