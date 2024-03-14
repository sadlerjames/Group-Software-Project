#Authored by George Piper and James Sadler

from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate,login,logout
from accounts.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .forms import QuizCreationForm,QRCreationForm,TreasureHuntCreationForm,SetDailyForm
from quiz.templatetags.quiz import Quiz
from .models import DailyQuizzes
from quiz.models import Quizzes
from quiz.templatetags import quiz
import os
import datetime


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
                msg = 'Invalid Credentials'
        else:
            msg = 'Error validating form'
    return render(request,'gamekeeper/login.html',{'form':form,'msg':msg}) #send the user back to the 
    
@login_required(login_url = '/gamekeeper/login')
def creation_view(request):
    if getattr(request.user,'is_gamekeeper'):
        if request.method == 'POST':
            #get the number of questions from the post request
            form = QuizCreationForm(request.POST,extra= request.POST.get('extra_field_count'))
            if form.is_valid():
                quizName = request.POST.get('quiz_name')
                quizPoints = request.POST.get('points_per_question')
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
                Quiz(quizName, questions, answers,correct=[],noPoints= quizPoints,loading=False)
                return redirect('/gamekeeper/quiz/create')

            else:
                form = QuizCreationForm()
            return render(request,"gamekeeper/quiz/create.html",{'form':form})
        else:
            form = QuizCreationForm()
            return render(request,"gamekeeper/quiz/create.html",{'form':form})
    else:
        return redirect('/account/dashboard')

@login_required(login_url = 'gamekeeper/login')  
def logoutview(request):
    logout(request)
    return redirect('/gamekeeper/login/')

@login_required(login_url = '/gamekeeper/login')
@csrf_protect
def create_activity(request):
    if getattr(request.user,'is_gamekeeper'):
        contextVars = {}
        # Fetch all quizzes from database
        options = Quizzes.objects.values_list('id', flat=True)
        # Iterate through each quiz object and store the id and name
        data = []
        for option in options:
            data.append({
                'quiz_id': option,
                'quiz_name': quiz.load(option).getName(),
            })
        # Add to contextVars
        contextVars['quiz_files'] = list(data)

        contextVars['form'] = ""
        if request.method == 'POST':
            form = QRCreationForm(request.POST)
            contextVars['form'] = form
            if form.is_valid():
                activityType = request.POST.get('activity_type')
                activityName = request.POST.get('qr_name')
                location = request.POST.get('location')
                extraInfo = request.POST.get('extra')
                #save this to the database
                return redirect('/gamekeeper/treasurehunt/create', context=contextVars)
            else:
                form = QRCreationForm()
            return render(request,"gamekeeper/treasurehunt/create-activity.html",context=contextVars)
        else:
            form = QRCreationForm()
            return render(request,"gamekeeper/treasurehunt/create-activity.html",context=contextVars)
    else:
        return redirect('/account/dashboard')
    
@login_required(login_url = '/gamekeeper/login')
@csrf_protect
def create_treasure(request):
    if request.method == 'POST':
        #get the number of questions from the post request
        form = TreasureHuntCreationForm(request.POST,extra= request.POST.get('extra_field_count'))
        if form.is_valid():
            name = request.POST.get('treasure_hunt_name')
            points = request.POST.get('bonus_points')
            activities = []
            for i in range(1,int(request.POST.get('extra_field_count'))+1):
                activities.append(request.POST.get('extra_field_{index}'.format(index=i)))
        return render(request,"gamekeeper/treasurehunt/create-treasure-hunt.html")
    else:
        return render(request,"gamekeeper/treasurehunt/create-treasure-hunt.html")

@login_required(login_url = '/gamekeeper/login')
def set_daily(request):
    if getattr(request.user,'is_gamekeeper'):
        contextVars = {}
        # Fetch all quizzes from database
        options = Quizzes.objects.values_list('id', flat=True)
        # Iterate through each quiz object and store the id and name
        data = []
        for option in options:
            data.append({
                'quiz_id': option,
                'quiz_name': quiz.load(option).getName(),
            })
        # Add to contextVars
        contextVars['quiz_files'] = list(data)

        # Fetch all daily quizzes from database
        dailyQuizzes = DailyQuizzes.objects.all()
        # Iterate through each daily quiz object and store the date, ID and name
        # Only show present/future daily quizzes
        timeNow = datetime.date.today()
        data = []
        for option in dailyQuizzes:
            if option.date >= timeNow:
                data.append({
                    'date': option.date,
                    'quiz_id': option.quiz_id.id,
                    'quiz_name': quiz.load(option.quiz_id.id).getName(),
                    'time_limit': option.time_limit
                })
        # Add to contextVars
        contextVars['daily_quizzes'] = list(data)
        contextVars['form'] = ""

        # POST request for form
        if request.method == 'POST':
            form = SetDailyForm(request.POST)
            contextVars['form'] = form
            if form.is_valid():
                date = request.POST.get('date')
                quizID = request.POST.get('quiz')
                quizID = int(quizID)
                time = request.POST.get('time')
                time = int(time)
                
                # Get quiz object for chosen quiz
                options = Quizzes.objects.values_list('id', flat=True)
                for option in options:
                    if (quiz.load(option).getId() == quizID):
                        quizObj = Quizzes.objects.get(pk=quizID)

                # Save this to the database
                db = DailyQuizzes(date=date, quiz_id=quizObj, time_limit=time)
                db.save()
                return redirect('/gamekeeper/quiz/set_daily', context=contextVars)
            else:
                form = SetDailyForm()
            return render(request,"gamekeeper/quiz/set_daily.html",context=contextVars)
        else:
            form = SetDailyForm()
            return render(request,"gamekeeper/quiz/set_daily.html",context=contextVars)
    else:
        return redirect('/account/dashboard')

@login_required(login_url = '/gamekeeper/login')
def drop_row(request, id):
    if request.method == 'POST':
        DailyQuizzes.objects.filter(date=id).delete()
    
    return redirect('/gamekeeper/quiz/set_daily')