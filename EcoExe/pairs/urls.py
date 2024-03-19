from django.urls import path
from . import views

urlpatterns = [
    path('pairs/', views.play_game, name='pairs'),
]