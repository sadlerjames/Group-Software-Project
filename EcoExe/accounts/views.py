# Authored by Jack Hales, George Piper, James Sadler

from django.shortcuts import get_object_or_404, render,redirect
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, LoginForm, SignUpForm
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import CreateView
from .forms import CustomPasswordChangeForm
from django.views.generic import TemplateView
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change_form.html'

class PasswordChangeDoneView(TemplateView):
    template_name = 'registration/password_change_done.html'


@login_required()    
def dashboard(request):
    return render(request, "dashboard.html")
    
def userprofile(request):
    return render(request, "../userprofile/templates/userprofile.html")
    
def signup(request):
    if request.user.is_authenticated:
        return redirect('/accounts/dashboard')
    else:
        msg = None
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                msg = 'user created'
                return redirect('/accounts/login')
            else:
                print(form.errors)
                msg = form.errors
        else:
            form = SignUpForm()
        return render(request,'registration/signup.html',{'form':form,'msg':msg})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/accounts/dashboard')
    else:
        form = LoginForm(request.POST or None)
        msg = None
        if request.method == 'POST':
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username,password=password)
                if user is not None and not user.is_gamekeeper:
                    login(request,user)
                    return redirect('dashboard')
                else:
                    msg = 'Invalid Credentials'
            else:
                msg = 'Error validating form'
        return render(request,'registration/login.html',{'form':form,'msg':msg})

@login_required()  
def logoutview(request):
    logout(request)
    return redirect('/accounts/login')