from django.shortcuts import get_object_or_404,render
from django.template import loader
# Create your views here.
from django.http import HttpResponse
from django.http import Http404



def profile(request):
    return render(request, "profile.html")
