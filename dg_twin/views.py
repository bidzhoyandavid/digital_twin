from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
import uuid

# Create your views here.

def welcome(request):
    if request.user.is_authenticated:
        return redirect('dg_twin:avatar')
    return render(request, 'welcome.html')

def google_login(request):
    if request.user.is_authenticated:
        return redirect('dg_twin:avatar')
    return redirect('account_google_login')

def guest_login(request):
    if request.user.is_authenticated:
        return redirect('dg_twin:avatar')
    
    # Generate a unique guest username
    guest_username = f"{settings.GUEST_USERNAME_PREFIX}{uuid.uuid4().hex[:8]}"
    
    # Create a new guest user
    guest_user = User.objects.create_user(
        username=guest_username,
        email=None,
        password=None
    )
    
    # Log in the guest user
    login(request, guest_user)
    
    return redirect('dg_twin:avatar')

@login_required
def avatar(request):
    return render(request, 'avatar.html')
