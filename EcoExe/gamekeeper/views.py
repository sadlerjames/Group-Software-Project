from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate,login
from accounts.models import User
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def loginpage(request):
    return render(request, "gamekeeper/login.html")


def dashboard(request):
    
    return render(request, "gamekeeper/dashboard.html")

@csrf_protect
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None and user.is_gamekeeper:
                login(request,user)
                return redirect('/gamekeeper/dashboard')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request,'gamekeeper/login.html',{'form':form,'msg':msg})