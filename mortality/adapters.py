from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_callback_url(self, request, app):
        """Force HTTPS for OAuth callbacks in production"""
        callback_url = super().get_callback_url(request, app)
        if not settings.DEBUG and callback_url.startswith('http://'):
            callback_url = callback_url.replace('http://', 'https://', 1)
        return callback_url
