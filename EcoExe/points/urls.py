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
from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('leaderboard/', views.leaderboard, name="leaderboard"),
    path('get_points/', views.get_points, name='get_points'),
    #path('sort_leaderboard_by_user/', views.sort_leaderboard_by_user, name='sort_leaderboard_by_user'),
    path('fetch_options/', views.fetch_options, name='fetch_options'),
]
