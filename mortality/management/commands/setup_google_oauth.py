from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Setup Google OAuth application'

    def add_arguments(self, parser):
        parser.add_argument('--client-id', type=str, help='Google OAuth Client ID')
        parser.add_argument('--client-secret', type=str, help='Google OAuth Client Secret')

    def handle(self, *args, **options):
        client_id = options.get('client_id')
        client_secret = options.get('client_secret')
        
        if not client_id or not client_secret:
            self.stdout.write(
                self.style.ERROR('Please provide both --client-id and --client-secret')
            )
            self.stdout.write('Usage: python manage.py setup_google_oauth --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET')
            return
        
        # Get or create the default site
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={'domain': 'localhost:8000', 'name': 'DeathClock Local'}
        )
        
        # Create or update Google OAuth app
        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google OAuth',
                'client_id': client_id,
                'secret': client_secret,
            }
        )
        
        if not created:
            google_app.client_id = client_id
            google_app.secret = client_secret
            google_app.save()
            self.stdout.write(
                self.style.SUCCESS('Updated existing Google OAuth application')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Created new Google OAuth application')
            )
        
        # Add the site to the app
        google_app.sites.add(site)
        
        self.stdout.write(
            self.style.SUCCESS(f'Google OAuth setup complete for site: {site.domain}')
        )
        self.stdout.write('You can now use Google login in your DeathClock application!')