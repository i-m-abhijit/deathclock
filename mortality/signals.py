from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import redirect
from allauth.socialaccount.signals import pre_social_login
from django.contrib import messages

@receiver(user_logged_in)
def redirect_to_profile_setup(sender, request, user, **kwargs):
    """Redirect new users to profile setup after login"""
    if not hasattr(user, 'userprofile'):
        messages.success(request, 'Welcome to your mortality journey. Let\'s set up your death clock.')

@receiver(pre_social_login)
def populate_profile_from_social(sender, request, sociallogin, **kwargs):
    """Populate user profile from social login data"""
    if sociallogin.account.provider == 'google':
        user_data = sociallogin.account.extra_data
        user = sociallogin.user
        
        # Set first name and last name from Google data
        if not user.first_name and 'given_name' in user_data:
            user.first_name = user_data['given_name']
        if not user.last_name and 'family_name' in user_data:
            user.last_name = user_data['family_name']