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
    if getattr(request.user,'is_gamekeeper'):
        return render(request, "gamekeeper/dashboard.html")
    
    else:
        return redirect('/accounts/dashboard')

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

@login_required(login_url = '/gamekeeper/login')
def creation_view(request):
    if getattr(request.user,'is_gamekeeper'):
        if request.method == 'POST':
            form = QuizCreationForm(request.POST,extra= request.POST.get('extra_field_count'))

            if form.is_valid():
                quizName = request.POST.get('quiz_name')
                quizPoints = request.POST.get('number_of_points')
                formCount = int(request.POST.get('extra_field_count'))

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

                Quiz(quizName, questions, answers, 8, [], quizPoints)
                return redirect('/gamekeeper/quiz/create')

            else:
                form = QuizCreationForm()
            return render(request,"gamekeeper/quiz/create.html",{'form':form})
        else:
            form = QuizCreationForm()
            return render(request,"gamekeeper/quiz/create.html",{'form':form})
    else:
        return redirect('/account/dashboard')