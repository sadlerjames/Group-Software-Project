from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.shortcuts import render

def leaderboard(request):
    return render(request, "leaderboard.html")
