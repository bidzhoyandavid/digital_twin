from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AvatarForm
from .models import Avatar
from .services import generate_avatar
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
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = form.save(commit=False)
            avatar.user = request.user
            avatar.save()
            
            # Generate avatar using D-ID
            avatar_url = generate_avatar(avatar.original_photo.path)
            if avatar_url:
                avatar.generated_avatar_url = avatar_url
                avatar.save()
                messages.success(request, 'Avatar generated successfully!')
            else:
                messages.error(request, 'Failed to generate avatar. Please try again.')
            
            return redirect('dg_twin:avatar')
    else:
        form = AvatarForm()
    
    # Get existing avatar if any
    try:
        existing_avatar = request.user.avatar
    except Avatar.DoesNotExist:
        existing_avatar = None
    
    return render(request, 'avatar.html', {
        'form': form,
        'avatar': existing_avatar
    })
