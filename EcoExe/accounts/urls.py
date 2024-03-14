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


urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('login/', views.login_view, name="loginpage"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('signup/', views.signup, name='signup'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('logout/', views.logoutview, name='logout'),
    path('profile/', views.userprofile, name='profile'),
    path('update-password/', UpdatePasswordView.as_view(), name='password_update')
]

