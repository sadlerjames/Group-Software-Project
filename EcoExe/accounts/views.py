# Authored by Jack Hales, George Piper, James Sadler

from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import LoginForm, SignUpForm
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from .forms import CustomPasswordChangeForm, UpdateUserForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from treasurehunt.treasure import Treasure

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.html'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('password_reset_done')

class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('password_change_done')

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'change_password.html'

class PasswordChangeDoneView(TemplateView):
    template_name = 'change_password_complete.html'

@login_required()    
def dashboard(request):
    return render(request, "dashboard.html")
       
#process the POST request and create the user 
def signup(request):
    #if the user is already signed in take them to dashboard
    if request.user.is_authenticated:
        return redirect('/accounts/dashboard')
    else:
        msg = None
        if request.method == 'POST':
            form = SignUpForm(request.POST)

            #check the inputted form is valid, create user if so
            if form.is_valid():
                form.save()
                msg = 'user created'
                return redirect('/accounts/login')
            else:
                msg = form.errors
        else:
            form = SignUpForm()
        return render(request,'registration/signup.html',{'form':form,'msg':msg})

#process the login request and sign the user in if checks pass
def login_view(request):
    #if the user is already signed in take them to dashboard
    if request.user.is_authenticated:
        return redirect('/accounts/dashboard')
    else:
        form = LoginForm(request.POST or None)
        msg = None
        if request.method == 'POST':
            #check the form is valid
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


@login_required
def userprofile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        
        if user_form.is_valid():
            user_form.save()
            # messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'profile.html', {'user_form': user_form})


@login_required
def delete_account(request):
    if request.method == 'POST':
        # Delete the user account
        request.user.delete()
        # Log out the user
        logout(request)
        # Redirect to a success page or any other page
        return redirect('/accounts/delete_account_success')
    return render(request, 'registration/delete_account_confirmation.html')

def delete_account_success(request):
    return render(request, 'registration/delete_account_success.html')

def password_reset_done(request):
    return render(request, 'password_reset_done.html')


