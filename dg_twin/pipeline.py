from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from social_core.pipeline.user import get_username

def save_profile(backend, user, response, *args, **kwargs):
    """
    Save additional user profile information after Google login
    """
    if backend.name == 'google-oauth2':
        if response.get('picture'):
            user.profile.avatar_url = response['picture']
        if response.get('email'):
            user.email = response['email']
        user.save() 