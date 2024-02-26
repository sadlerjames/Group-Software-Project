from django.shortcuts import render

# Create your views here.
def userprofile(request):
    return render(request, "userprofile.html")