#Authored by George Piper and James Sadler

from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate,login
from accounts.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .forms import QuizCreationForm
from quiz.templatetags.quiz import Quiz


# Create your views here.
@login_required(login_url = '/gamekeeper/login')
def dashboard(request):
    if getattr(request.user,'is_gamekeeper'): #check the user is allowed to access the webpage
        return render(request, "gamekeeper/dashboard.html")
    else:
        return redirect('/accounts/dashboard') #send a player user to their dashboard

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password) #log the user in
            if user is not None and user.is_gamekeeper: #check the user has the correct access level
                login(request,user)
                return redirect('/gamekeeper/dashboard')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request,'gamekeeper/login.html',{'form':form,'msg':msg}) #send the user back to the 
    
@login_required(login_url = '/gamekeeper/login')
def creation_view(request):
    if getattr(request.user,'is_gamekeeper'):
        if request.method == 'POST':
            #get the number of questions from the post request
            form = QuizCreationForm(request.POST,extra= request.POST.get('extra_field_count'))  

            if form.is_valid():
                quizName = request.POST.get('quiz_name')
                quizPoints = request.POST.get('number_of_points')
                formCount = int(request.POST.get('extra_field_count'))

                #cycle through the forms and split them into questions and answers
                questions = []
                answers = []
                i = 1
                while i < formCount + 1:

                    questions.append(request.POST.get('extra_field_{index}'.format(index=i)))
                    qAnswers = []
                    for j in range(4):
                        i+=1
                        qAnswers.append(request.POST.get('extra_field_{index}'.format(index=i)))
                    answers.append(qAnswers)
                    i+=1

                #call the quiz class to save the quiz to json file
                Quiz(quizName, questions, answers,correct=[],noPoints= quizPoints)
                return redirect('/gamekeeper/quiz/create')

            else:
                form = QuizCreationForm()
            return render(request,"gamekeeper/quiz/create.html",{'form':form})
        else:
            form = QuizCreationForm()
            return render(request,"gamekeeper/quiz/create.html",{'form':form})
    else:
        return redirect('/account/dashboard')
