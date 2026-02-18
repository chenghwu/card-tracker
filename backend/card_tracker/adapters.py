"""
Custom django-allauth adapters for social authentication.

After a successful Google OAuth flow (initiated via /accounts/google/login/),
allauth redirects to LOGIN_REDIRECT_URL. We override the social account adapter
so that, instead of staying on the Django side, the user is sent back to the
Next.js frontend with JWT access/refresh tokens as query parameters:

    http://localhost:3000/auth/callback?access=TOKEN&refresh=REFRESH_TOKEN
"""

from urllib.parse import urlencode

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """Return a dict with JWT access and refresh tokens for the given user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Extend allauth's DefaultSocialAccountAdapter to redirect back to the
    Next.js frontend with JWT tokens after a successful social login.

    This is called by allauth after the OAuth callback has been processed
    and the user has been logged in (or created).
    """

    def get_connect_redirect_url(self, request, socialaccount):
        """
        Return the URL to redirect to after a *connection* (i.e. linking a
        social account to an existing account).  Not typically used in our
        flow but included for completeness.
        """
        return self._frontend_callback_url(request.user)

    def save_user(self, request, sociallogin, form=None):
        """
        Call the parent implementation to persist the user, then stash the
        user on the sociallogin so we can pick it up in the redirect hook.
        """
        user = super().save_user(request, sociallogin, form=form)
        return user

    def authentication_error(self, request, provider_id, error=None, exception=None, extra_context=None):
        """
        Redirect to the frontend login page with an error flag when OAuth
        authentication fails (e.g. user denied permission, invalid code).
        """
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        error_url = f"{frontend_url}/login?error=oauth_failed"
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(error_url)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _frontend_callback_url(self, user):
        """Build the frontend callback URL with JWT tokens as query params."""
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        tokens = get_tokens_for_user(user)
        params = urlencode({
            'access': tokens['access'],
            'refresh': tokens['refresh'],
        })
        return f"{frontend_url}/auth/callback?{params}"
