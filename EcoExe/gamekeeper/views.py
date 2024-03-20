#Authored by George Piper and James Sadler

from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import QuizCreationForm,QRCreationForm,TreasureHuntCreationForm,SetDailyForm
from quiz.templatetags.quiz import Quiz
from .models import DailyQuizzes
from quiz.models import Quizzes
from quiz.templatetags import quiz
import datetime
import segno
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from treasurehunt.treasure import Treasure
from django.http import JsonResponse
from django.db import IntegrityError
import os
from django.core.files.storage import FileSystemStorage
from pypdf import PdfMerger


@login_required(login_url = '/gamekeeper/login')
def dashboard(request):
    #if gamekeeper take them to their dashboard
    if getattr(request.user,'is_gamekeeper'): 
        return render(request, "gamekeeper/dashboard.html")
    #if player them them to their dashboard
    else:
        return redirect('/accounts/dashboard')
    
@login_required(login_url = '/gamekeeper/login')
def info(request):
    #if gamekeeper render info
    if getattr(request.user,'is_gamekeeper'): 
        return render(request, "gamekeeper/info.html")
    else:
        # if player user send to their dashboard
        return redirect('/accounts/dashboard')

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username,password=password) #log the user in

            #check the user has the correct access level
            if user is not None and user.is_gamekeeper: 
                login(request,user)
                return redirect('/gamekeeper/dashboard')
            else:
                msg = 'Invalid Credentials'

        else:
            msg = 'Error validating form'

    return render(request,'gamekeeper/login.html',{'form':form,'msg':msg}) #send the user back to the login
    
@login_required(login_url = '/gamekeeper/login')
def creation_view(request):
    if getattr(request.user,'is_gamekeeper'):
        if request.method == 'POST':
            #get the number of questions from post request
            form = QuizCreationForm(request.POST,extra= request.POST.get('extra_field_count'))

            if form.is_valid():
                quizName = request.POST.get('quiz_name')
                quizPoints = request.POST.get('points_per_question')
                formCount = int(request.POST.get('extra_field_count'))
                time = int(request.POST.get('time'))

                #cycle through the forms and split them into questions and answers
                questions = []
                answers = []
                i = 1

                #cycle through and add question + comments to respective array
                while i < formCount + 1:
                    questions.append(request.POST.get('extra_field_{index}'.format(index=i)))
                    
                    #add answers to question specfic answer array
                    qAnswers = []
                    for j in range(4):
                        i+=1
                        qAnswers.append(request.POST.get('extra_field_{index}'.format(index=i)))

                    #add question answer array to main answer arrays
                    answers.append(qAnswers)
                    i+=1

                #save quiz to database + json
                Quiz(quizName, questions, answers, correct=[], noPoints=quizPoints, loading=False, time_limit=time)

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
                #get information from the post request
                activityType = request.POST.get('activity_type')
                activityName = request.POST.get('qr_name')
                latitude = request.POST.get('latitude')
                longitude = request.POST.get('longitude')
                location = str(latitude) +","+str(longitude) 
                extraInfo = request.POST.get('extra')
                points = request.POST.get('points')
                locationName = request.POST.get('location_name')

                #Save activity in the database
                Treasure.addActivity(activityName,location,activityType,extraInfo,points,locationName)

                return redirect('/gamekeeper/treasurehunt/create_activity', context=contextVars)
            else:
                #if form is invalid, display this to the user
                contextVars['message'] = "There was an error in your form, please try again "
                form = QRCreationForm()

            return render(request,"gamekeeper/treasurehunt/create-activity.html",context=contextVars)
        
        else:
            form = QRCreationForm()
            return render(request,"gamekeeper/treasurehunt/create-activity.html",context=contextVars)
        
    else:
        return redirect('/account/dashboard')
    
@login_required(login_url = '/gamekeeper/login')
def create_treasure(request):
    if request.method == 'POST':
        form = TreasureHuntCreationForm(request.POST, request.FILES, extra= request.POST.get('extra_field_count'))
        context = {}

        if form.is_valid():
            name = request.POST.get('treasure_hunt_name')
            points = request.POST.get('bonus_points')

            #will throw an error if treasurehunt with same name already exists
            try: 
                #if the user uploaded a photo
                if 'avatar' in request.FILES:
                    avatar = request.FILES['avatar']
                    
                    fs = FileSystemStorage()

                    _, file_extension = os.path.splitext(avatar.name)
                    filename = fs.save('treasure_hunt/' + name + file_extension, avatar) #save the uploaded user file

                    treasure = Treasure(name, points, img = filename) #save treasure hunt to database
                else:
                    treasure = Treasure(name, points) #save treasure hunt to database

                #cycle through the activities that were submitted
                for i in range(1,int(request.POST.get('extra_field_count'))+1):
                    activity_ID = request.POST.get('extra_field_{index}'.format(index=i))
                    
                    #create a qr code for the activity
                    url = "/treasurehunt/validate/?huntID={hunt_id}&stage_id={stage_id}".format(hunt_id = treasure.getId(), stage_id = i)
                    qr = segno.make(url)

                    #temporarily save the qr code
                    qr.save("gamekeeper/templatetags/qrcodes/{treasurename}_{index}.png".format(treasurename=name,index=i), scale=13)
                    
                    treasure.addStage(i, activity_ID) #create a stage in the treasure hunt
            
            #if same name treasure hunt exists error to user
            except IntegrityError:
                return render(request,"gamekeeper/treasurehunt/create-treasure-hunt.html",context={'message':'A treasure hunt with this name already exists'})
            
            
            #call makePDF to create the PDF of QR codes
            makePDF(name,request.POST.get('extra_field_count'))

            context['pdf'] = name #provide a link to the pdf on the DOM

            #delete all the temp qr codes files
            for i in range(1,int(request.POST.get('extra_field_count'))+1): #for each activity
                os.remove("gamekeeper/templatetags/qrcodes/{treasurename}_{index}.png".format(treasurename=name,index=i))

        return render(request,"gamekeeper/treasurehunt/create-treasure-hunt.html",context=context)
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

        # Add to contextVars to display on DOM
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

        # Add to contextVars on DOM
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

def makePDF(name,extra):
    images = []
    #cycle through the temp qr codes and add to array
    for i in range(1,int(extra)+1):
        path = "gamekeeper/templatetags/qrcodes/{treasurename}_{index}.png".format(treasurename=name,index=i)
        images.append([Image.open(path), path, i])

    pdf_path = "media/pdfs/{name}temp.pdf".format(name=name)

    #create a canvas of A4 size
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    #cycle through each qr code and create new page for each + add to it
    for img in images:
        image = img[0]

        #Resize the image to fit within the A4 page
        image.thumbnail((width, height))

        #Calculate the position to center the image on the page
        x = (width - image.width) / 2
        y = (height - image.height) / 2

        #Add title to page
        title = "Stage " + str(img[2])
        c.setFont("Helvetica-Bold", 22)  # Set font and size for the title
        c.drawCentredString(width / 2, height - 50, title)

        #Draw the qr code on centre of page
        c.drawImage(img[1], x, y, width=image.width, height=image.height)

        #Add a new page for the next qr code
        c.showPage()

    merged = PdfMerger()

    c.save() #save the pdf

    #merge the instructions page to the beginning of the qr pdf
    merged.append('gamekeeper/templatetags/basepage.pdf')
    merged.append("media/pdfs/{name}temp.pdf".format(name=name))
    merged.write("media/pdfs/{name}.pdf".format(name=name))
    merged.close()

    os.remove("media/pdfs/{name}temp.pdf".format(name=name)) #remove the temp qr pdf

def get_activities(request):
    return JsonResponse(Treasure.getActivities())