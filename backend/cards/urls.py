from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CardTemplateViewSet,
    UserCardViewSet,
    UserBenefitViewSet,
    dashboard_summary,
    dashboard_deadlines,
    dashboard_monthly_overview,
    card_lookup,
    health_check,
    cron_send_reminders,
)

router = DefaultRouter()
router.register(r'card-templates', CardTemplateViewSet, basename='card-template')
router.register(r'cards', UserCardViewSet, basename='card')
router.register(r'benefits', UserBenefitViewSet, basename='benefit')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/summary/', dashboard_summary, name='dashboard-summary'),
    path('dashboard/deadlines/', dashboard_deadlines, name='dashboard-deadlines'),
    path('dashboard/monthly-overview/', dashboard_monthly_overview, name='dashboard-monthly-overview'),
    path('card-lookup/', card_lookup, name='card-lookup'),
    path('health/', health_check, name='health-check'),
    path('cron/send-reminders/', cron_send_reminders, name='cron-send-reminders'),
]
