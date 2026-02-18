"""
Management command to configure Google OAuth SocialApp in the database.

Idempotent: safe to run on every deploy. Ensures exactly one Google SocialApp
exists in the DB linked to the current site, using credentials from env vars.
"""
import os

from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Configure Google OAuth SocialApp in the database'

    def handle(self, *args, **options):
        from allauth.socialaccount.models import SocialApp

        client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
        secret = os.environ.get('GOOGLE_CLIENT_SECRET', '')

        if not client_id or not secret:
            self.stdout.write(self.style.WARNING(
                'GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not set — skipping OAuth setup'
            ))
            return

        site = Site.objects.get_or_create(id=1, defaults={'domain': 'example.com', 'name': 'example.com'})[0]

        # Delete any existing Google SocialApps to avoid MultipleObjectsReturned
        deleted_count = SocialApp.objects.filter(provider='google').delete()[0]
        if deleted_count:
            self.stdout.write(f'Removed {deleted_count} existing Google SocialApp(s)')

        app = SocialApp.objects.create(
            provider='google',
            name='Google',
            client_id=client_id,
            secret=secret,
        )
        app.sites.add(site)

        self.stdout.write(self.style.SUCCESS(
            f'Google SocialApp created (client_id: {client_id[:20]}...) and linked to site id={site.id}'
        ))
