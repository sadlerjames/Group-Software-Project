# Authored by Jack Hales, George Piper, James Sadler

"""
URL configuration for EcoExe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('login/', views.login_view, name="loginpage"),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('password_reset_confirmed/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirmed'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('signup/', views.signup, name='signup'),
    path('password_change/', ChangePasswordView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('logout/', views.logoutview, name='logout'),
    path('profile/', views.userprofile, name='profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('delete_account_success/', views.delete_account_success, name='delete_account_success')
]

