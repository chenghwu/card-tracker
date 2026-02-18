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
    try:
        from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView
        return OAuth2LoginView.adapter_view(
            __import__('allauth.socialaccount.providers.google.views', fromlist=['GoogleOAuth2Adapter']).GoogleOAuth2Adapter
        )(request)
    except Exception:
        from allauth.socialaccount.models import SocialApp
        apps = list(SocialApp.objects.filter(provider='google').values())
        return JsonResponse({'error': traceback.format_exc(), 'db_apps': apps})


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
