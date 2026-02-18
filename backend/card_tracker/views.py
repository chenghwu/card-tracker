"""
Views for the card_tracker Django project (not the cards app).

Provides the OAuth → JWT handoff view that bridges allauth's server-side
Google OAuth flow with the Next.js frontend SPA.

Flow:
  1. User clicks "Continue with Google" on the frontend.
  2. Frontend redirects to /accounts/google/login/?next=/api/auth/google/done/
  3. allauth handles the Google OAuth dance (redirects to Google, handles callback).
  4. allauth redirects the authenticated session to /api/auth/google/done/
  5. This view picks up the authenticated session user, mints JWT tokens, then
     redirects to FRONTEND_URL/auth/callback?access=TOKEN&refresh=REFRESH_TOKEN.
  6. The frontend /auth/callback page stores the tokens and navigates to /dashboard.
"""

import traceback
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_GET
from rest_framework_simplejwt.tokens import RefreshToken


def _get_tokens_for_user(user):
    """Mint a JWT access/refresh token pair for the given user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@require_GET
def debug_google_login(request):
    """Wraps allauth's Google login view to expose the actual exception."""
    try:
        from allauth.socialaccount.providers.google.views import oauth2_login
        return oauth2_login(request)
    except Exception:
        return JsonResponse({'error': traceback.format_exc()}, status=200)


@require_GET
def debug_oauth(request):
    """Temporary diagnostic endpoint — remove after OAuth is confirmed working."""
    try:
        from allauth.socialaccount.models import SocialApp
        from django.contrib.sites.models import Site
        apps_in_db = list(SocialApp.objects.filter(provider='google').values('id', 'name', 'client_id'))
        sites = list(Site.objects.values('id', 'domain'))
    except Exception as e:
        apps_in_db = str(e)
        sites = []

    try:
        from allauth.socialaccount import app_settings as sa_settings
        provider_config = sa_settings.PROVIDERS.get('google', {})
        has_app_key = 'APP' in provider_config
        has_apps_key = 'APPS' in provider_config
        client_id_from_settings = (provider_config.get('APP') or {}).get('client_id', '')
    except Exception as e:
        has_app_key = has_apps_key = False
        client_id_from_settings = str(e)

    try:
        import os
        google_client_id_env = bool(os.environ.get('GOOGLE_CLIENT_ID'))
    except Exception:
        google_client_id_env = False

    try:
        from allauth.socialaccount.providers.google.provider import GoogleProvider
        from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
        error_detail = 'provider import ok'
    except Exception as e:
        error_detail = traceback.format_exc()

    return JsonResponse({
        'google_client_id_env_set': google_client_id_env,
        'client_id_from_settings': bool(client_id_from_settings),
        'has_app_key': has_app_key,
        'has_apps_key': has_apps_key,
        'socialapps_in_db': apps_in_db,
        'sites': sites,
        'provider_import': error_detail,
        'site_id': settings.SITE_ID,
    })


@login_required
def google_oauth_done(request):
    """
    Landing view after allauth completes the Google OAuth flow.

    allauth logs the user in via Django's session backend, so by the time
    this view runs `request.user` is the authenticated user.  We mint JWT
    tokens and redirect to the Next.js frontend callback route.
    """
    tokens = _get_tokens_for_user(request.user)
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
    params = urlencode({
        'access': tokens['access'],
        'refresh': tokens['refresh'],
    })
    redirect_url = f"{frontend_url}/auth/callback?{params}"
    return HttpResponseRedirect(redirect_url)
