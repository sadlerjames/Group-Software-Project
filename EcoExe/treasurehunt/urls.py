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
from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('status/',views.status,name="status"),
    path('scan/', views.scan, name='scan'),
    path('verify/',views.verify,name='verify'),
    path('validate/',views.validatePage,name='validate'),
    path('quiz/',views.quiz,name="quiz"),
    path('trivia/',views.trivia,name="trivia"),
    path('wrong/',views.wrong,name="wrong"),
    path('next_locations/',views.getPins,name="next_locations"),
    path('wronglocation/',views.wronglocation,name="wronglocation"),
    path('finish',views.finish,name="finish"),
    path('fail',views.fail,name="fail"),
]
