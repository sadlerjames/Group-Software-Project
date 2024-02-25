from django.shortcuts import render

# Create your views here.
def loginpage(request):
    return render(request, "gamekeeper/login.html")


def dashboard(request):
    return render(request, "gamekeeper/dashboard.html")

def modify(request):
    return render(request,"gamekeeper/modify.html")

def create(request):
    return render(request,"gamekeeper/create.html")