from django.urls import path
from . import views

app_name = 'dg_twin'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('google-login/', views.google_login, name='google_login'),
    path('guest-login/', views.guest_login, name='guest_login'),
    path('avatar/', views.avatar, name='avatar'),
] 