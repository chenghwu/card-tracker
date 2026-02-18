"""
URL configuration for card_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from card_tracker.views import google_oauth_done, debug_oauth, debug_google_login

urlpatterns = [
    path('admin/', admin.site.urls),

    # dj-rest-auth: login/logout/password endpoints + JWT token endpoints
    # e.g. POST /api/auth/login/, POST /api/auth/token/refresh/
    path('api/auth/', include('dj_rest_auth.urls')),

    # dj-rest-auth registration: POST /api/auth/registration/
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    # dj-rest-auth social login (SPA code-exchange approach):
    # POST /api/auth/social/google/  — send the Google auth code, receive JWT
    path('api/auth/social/', include('allauth.socialaccount.urls')),

    # django-allauth: full server-side OAuth flow (browser redirect approach)
    # GET /accounts/google/login/  — kicks off the Google OAuth redirect
    # GET /accounts/google/login/callback/  — Google redirects here after consent
    path('accounts/', include('allauth.urls')),

    # After allauth finishes the OAuth flow and logs the user in via session,
    # this view mints JWT tokens and redirects to the Next.js frontend.
    path('api/auth/google/done/', google_oauth_done, name='google_oauth_done'),
    path('api/debug/oauth/', debug_oauth, name='debug_oauth'),
    path('api/debug/google-login/', debug_google_login, name='debug_google_login'),

    # Application API routes
    path('api/', include('cards.urls')),
]
