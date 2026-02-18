from rest_framework import serializers
from .models import CardTemplate, BenefitTemplate, UserCard, UserBenefit, BenefitUsage


class BenefitTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BenefitTemplate
        fields = [
            'id', 'name', 'description', 'amount_cents',
            'frequency', 'period_type', 'category'
        ]


class CardTemplateSerializer(serializers.ModelSerializer):
    benefits = BenefitTemplateSerializer(many=True, read_only=True)
    benefit_count = serializers.SerializerMethodField()

    class Meta:
        model = CardTemplate
        fields = [
            'id', 'bank', 'name', 'annual_fee_cents',
            'image_url', 'is_verified', 'benefit_count', 'benefits'
        ]

    def get_benefit_count(self, obj):
        return obj.benefits.count()


class CardTemplateListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views (without full benefits)"""
    benefit_count = serializers.SerializerMethodField()

    class Meta:
        model = CardTemplate
        fields = [
            'id', 'bank', 'name', 'annual_fee_cents',
            'image_url', 'is_verified', 'benefit_count'
        ]

    def get_benefit_count(self, obj):
        return obj.benefits.count()


class BenefitUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BenefitUsage
        fields = [
            'id', 'amount_cents', 'used_at',
            'period_start', 'period_end', 'note', 'created_at'
        ]


class UserBenefitSerializer(serializers.ModelSerializer):
    benefit_template = BenefitTemplateSerializer(read_only=True)
    effective_name = serializers.ReadOnlyField()
    effective_amount_cents = serializers.ReadOnlyField()
    usage_records = BenefitUsageSerializer(many=True, read_only=True)
    card_name = serializers.SerializerMethodField()

    # These will be populated by tracking service
    used_amount_cents = serializers.IntegerField(read_only=True, required=False)
    remaining_amount_cents = serializers.IntegerField(read_only=True, required=False)
    current_period_start = serializers.DateField(read_only=True, required=False)
    current_period_end = serializers.DateField(read_only=True, required=False)
    deadline_urgency = serializers.CharField(source='urgency', read_only=True, required=False)
    days_until_deadline = serializers.IntegerField(source='days_until_expiry', read_only=True, required=False)

    def get_card_name(self, obj):
        return obj.user_card.nickname or obj.user_card.card_template.name

    class Meta:
        model = UserBenefit
        fields = [
            'id', 'benefit_template', 'custom_amount_cents', 'custom_name',
            'effective_name', 'effective_amount_cents', 'usage_records',
            'used_amount_cents', 'remaining_amount_cents',
            'current_period_start', 'current_period_end',
            'deadline_urgency', 'days_until_deadline', 'card_name',
        ]


class UserCardSerializer(serializers.ModelSerializer):
    card_template = CardTemplateSerializer(read_only=True)
    card_template_id = serializers.PrimaryKeyRelatedField(
        queryset=CardTemplate.objects.all(),
        source='card_template',
        write_only=True
    )
    benefits = UserBenefitSerializer(many=True, read_only=True)

    class Meta:
        model = UserCard
        fields = [
            'id', 'card_template', 'card_template_id', 'open_date',
            'nickname', 'is_active', 'benefits', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserCardListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    card_template = CardTemplateListSerializer(read_only=True)
    benefit_summary = serializers.SerializerMethodField()

    class Meta:
        model = UserCard
        fields = [
            'id', 'card_template', 'open_date', 'nickname',
            'is_active', 'benefit_summary', 'created_at'
        ]

    def get_benefit_summary(self, obj):
        """Returns count of benefits and total available credits"""
        benefits = obj.benefits.all()
        total_credits = sum(b.effective_amount_cents for b in benefits)
        return {
            'count': len(benefits),
            'total_credits_cents': total_credits
        }


class RecordUsageSerializer(serializers.Serializer):
    """Serializer for recording benefit usage"""
    amount_cents = serializers.IntegerField(min_value=1)
    used_at = serializers.DateTimeField(required=False)
    note = serializers.CharField(max_length=500, required=False, allow_blank=True)
