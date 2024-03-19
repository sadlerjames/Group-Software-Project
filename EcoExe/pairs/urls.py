from django.urls import path
from . import views

urlpatterns = [
    path('game/', views.play_game, name='game'),
]