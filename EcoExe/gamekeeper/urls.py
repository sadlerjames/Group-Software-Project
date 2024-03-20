#Authored by George Piper and James Sadler
"""
URL configuration for EcoExe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, register_converter
from . import views
from .views import *
from gamekeeper.converters import DateConverter

register_converter(DateConverter, 'date')

urlpatterns = [
    path('', views.dashboard,  name='dashboard'),
    path('login/', views.login_view,  name='login'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('quiz/create/', views.creation_view, name="create"),
    path('quiz/set_daily/', views.set_daily, name="set_daily"),
    path('quiz/drop_row/<date:id>/', views.drop_row, name="drop_row"),
    path('treasurehunt/create_activity/', views.create_activity, name="create_activity"),
    path('treasurehunt/create/', views.create_treasure, name="create_treasure"),
    path('treasurehunt/get_activities/', views.get_activities, name="get_activities"),
    path('logout/', views.logoutview, name='logout'),
    path('info/',views.info,name="info"),
]

