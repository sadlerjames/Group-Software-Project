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
from django.contrib.auth import authenticate,login

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

def loginpage(request):
    return render(request, "index.html")

def dashboard(request):
    return render(request, "dashboard.html")

def userprofile(request):
    return render(request, "../userprofile/templates/userprofile.html")

def signup(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'registration/signup.html',{'form':form,'msg':msg})

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('dashboard')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request,'login.html',{'form':form,'msg':msg})