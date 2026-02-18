from datetime import date
import calendar

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db import connection
from .models import CardTemplate, UserCard, UserBenefit, BenefitUsage
from .serializers import (
    CardTemplateSerializer,
    CardTemplateListSerializer,
    UserCardSerializer,
    UserCardListSerializer,
    UserBenefitSerializer,
    RecordUsageSerializer,
)
from .services.tracking import get_benefit_status, get_benefits_with_status, record_usage, delete_usage
from .services.deadlines import get_expiring_benefits, get_dashboard_summary
from .services.card_lookup import lookup_card_benefits, create_card_from_lookup


class CardTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for searching and retrieving card templates.
    GET /api/card-templates/?q=platinum
    GET /api/card-templates/{id}/
    """
    queryset = CardTemplate.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return CardTemplateListSerializer
        return CardTemplateSerializer

    def get_queryset(self):
        queryset = CardTemplate.objects.all()
        search_query = self.request.query_params.get('q', None)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(bank__icontains=search_query)
            )

        return queryset.order_by('bank', 'name')


class UserCardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user's cards.
    GET /api/cards/ - List user's cards
    POST /api/cards/ - Add a new card
    GET /api/cards/{id}/ - Get card detail
    PATCH /api/cards/{id}/ - Update card
    DELETE /api/cards/{id}/ - Deactivate card
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserCardListSerializer
        return UserCardSerializer

    def get_queryset(self):
        return UserCard.objects.filter(
            user=self.request.user,
            is_active=True
        ).select_related('card_template').prefetch_related('benefits__benefit_template')

    def perform_create(self, serializer):
        """Create UserCard and auto-create UserBenefit instances"""
        user_card = serializer.save(user=self.request.user)

        # Auto-create UserBenefit instances for each BenefitTemplate
        benefit_templates = user_card.card_template.benefits.all()
        for benefit_template in benefit_templates:
            UserBenefit.objects.create(
                user_card=user_card,
                benefit_template=benefit_template
            )

    def perform_destroy(self, instance):
        """Soft delete by setting is_active to False"""
        instance.is_active = False
        instance.save()

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to include benefit status"""
        instance = self.get_object()

        # Get benefits with status information
        benefits_with_status = get_benefits_with_status(instance)

        # Update the instance's benefits for serialization
        instance._benefits_with_status = benefits_with_status

        serializer = self.get_serializer(instance)
        data = serializer.data

        # Replace benefits with status-enhanced benefits
        benefit_serializer = UserBenefitSerializer(benefits_with_status, many=True)
        data['benefits'] = benefit_serializer.data

        return Response(data)


class UserBenefitViewSet(viewsets.GenericViewSet):
    """
    ViewSet for benefit tracking operations.
    POST /api/benefits/{id}/use/ - Record benefit usage
    DELETE /api/benefits/{id}/usage/{uid}/ - Undo usage
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserBenefitSerializer

    def get_queryset(self):
        return UserBenefit.objects.filter(
            user_card__user=self.request.user,
            user_card__is_active=True
        ).select_related('benefit_template', 'user_card')

    @action(detail=True, methods=['post'], url_path='use')
    def record_use(self, request, pk=None):
        """Record benefit usage"""
        user_benefit = self.get_object()
        serializer = RecordUsageSerializer(data=request.data)

        if serializer.is_valid():
            try:
                usage = record_usage(
                    user_benefit=user_benefit,
                    amount_cents=serializer.validated_data['amount_cents'],
                    used_at=serializer.validated_data.get('used_at'),
                    note=serializer.validated_data.get('note', '')
                )

                return Response({
                    'success': True,
                    'message': 'Usage recorded successfully',
                    'usage_id': usage.id,
                    'amount_cents': usage.amount_cents,
                    'used_at': usage.used_at,
                    'period_start': usage.period_start,
                    'period_end': usage.period_end,
                }, status=status.HTTP_201_CREATED)

            except ValueError as e:
                return Response({
                    'success': False,
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='usage/(?P<usage_id>[0-9]+)')
    def delete_usage(self, request, pk=None, usage_id=None):
        """Undo a benefit usage"""
        try:
            delete_usage(usage_id, request.user)
            return Response({
                'success': True,
                'message': 'Usage deleted successfully'
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_404_NOT_FOUND)

        except PermissionError as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_summary(request):
    """
    Get dashboard summary statistics.
    GET /api/dashboard/summary/
    """
    # Demo mode: return sample data if not authenticated
    if not request.user.is_authenticated:
        return Response({
            'total_annual_fees_cents': 69500,  # $695 (e.g., one Amex Platinum)
            'total_benefit_value_cents': 75000,  # $750 in benefits
            'net_value_cents': 5500,  # $55 net positive
            'total_benefits': 5,
            'benefits_used': 2,
            'benefits_fully_used': 1,
            'utilization_rate': 0.40,  # 40% utilization
        })

    summary = get_dashboard_summary(request.user)
    return Response(summary)


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_deadlines(request):
    """
    Get expiring benefits (benefits with value remaining that expire soon).
    GET /api/dashboard/deadlines/?days=30
    """
    # Demo mode: return sample deadline data if not authenticated
    if not request.user.is_authenticated:
        return Response({
            'count': 2,
            'benefits': [
                {
                    'id': 1,
                    'name': 'Uber Cash',
                    'amount_cents': 1500,
                    'remaining_cents': 1500,
                    'used_cents': 0,
                    'percent_used': 0,
                    'urgency': 'warning',
                    'days_remaining': 5,
                    'period_end': '2026-02-28',
                    'card_name': 'Amex Platinum',
                },
                {
                    'id': 2,
                    'name': 'Entertainment Credit',
                    'amount_cents': 2000,
                    'remaining_cents': 1000,
                    'used_cents': 1000,
                    'percent_used': 50,
                    'urgency': 'upcoming',
                    'days_remaining': 12,
                    'period_end': '2026-02-28',
                    'card_name': 'Amex Platinum',
                }
            ]
        })

    max_days = int(request.query_params.get('days', 30))
    expiring_benefits = get_expiring_benefits(request.user, max_days=max_days)

    # Serialize the benefits with urgency info
    serializer = UserBenefitSerializer(expiring_benefits, many=True)

    return Response({
        'count': len(expiring_benefits),
        'benefits': serializer.data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def card_lookup(request):
    """
    Lookup card information using Gemini AI.
    POST /api/card-lookup/
    Body: {"card_name": "Platinum Card", "bank": "American Express", "create": true}
    """
    card_name = request.data.get('card_name')
    bank = request.data.get('bank', None)
    create = request.data.get('create', False)

    if not card_name:
        return Response({
            'success': False,
            'error': 'card_name is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Lookup card benefits using Gemini
    result = lookup_card_benefits(card_name, bank)

    if not result['success']:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    # Optionally create the card in the database
    if create:
        create_result = create_card_from_lookup(result['card_data'])
        result.update(create_result)

    return Response(result)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_monthly_overview(request):
    """
    Get monthly overview of active benefits for the current calendar month.
    Includes monthly, quarterly, and semi_annual benefits whose current period
    overlaps with the current calendar month. Annual benefits are excluded.
    GET /api/dashboard/monthly-overview/
    """
    today = date.today()
    # First and last day of the current calendar month
    month_start = date(today.year, today.month, 1)
    month_end = date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])

    included_frequencies = {'monthly', 'quarterly', 'semi_annual'}

    user_cards = UserCard.objects.filter(
        user=request.user,
        is_active=True,
    ).prefetch_related('benefits__benefit_template', 'benefits__usage_records')

    results = []

    for user_card in user_cards:
        card_name = user_card.nickname or user_card.card_template.name

        for user_benefit in user_card.benefits.all():
            frequency = user_benefit.benefit_template.frequency

            # Skip annual benefits
            if frequency not in included_frequencies:
                continue

            benefit_status = get_benefit_status(user_benefit, today)
            period_start = benefit_status['period_start']
            period_end = benefit_status['period_end']

            # Check whether the benefit's current period overlaps with the current calendar month
            # Overlap condition: period_start <= month_end AND period_end >= month_start
            if period_start > month_end or period_end < month_start:
                continue

            results.append({
                'id': user_benefit.id,
                'name': user_benefit.effective_name,
                'card_name': card_name,
                'frequency': frequency,
                'amount_cents': user_benefit.effective_amount_cents,
                'used_amount_cents': benefit_status['used_amount_cents'],
                'remaining_amount_cents': benefit_status['remaining_amount_cents'],
                'current_period_start': period_start.isoformat(),
                'current_period_end': period_end.isoformat(),
                'is_fully_used': benefit_status['is_fully_used'],
            })

    # Sort: not-fully-used first, then fully used
    results.sort(key=lambda b: (1 if b['is_fully_used'] else 0, b['name']))

    return Response(results)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for monitoring.
    GET /api/health/

    Returns:
        - status: 'ok' if service is healthy
        - database: 'connected' if database is accessible
        - version: API version
    """
    health_status = {
        'status': 'ok',
        'version': '1.0.0',
    }

    # Check database connectivity
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        health_status['database'] = 'connected'
    except Exception as e:
        health_status['status'] = 'degraded'
        health_status['database'] = 'disconnected'
        health_status['error'] = str(e)
        return Response(health_status, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(health_status, status=status.HTTP_200_OK)
