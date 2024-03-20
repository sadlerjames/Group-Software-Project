from django.shortcuts import render,redirect
import json
from matplotlib.patches import Circle
from treasurehunt.treasure import Treasure
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from quiz.templatetags.quiz import load
from quiz.models import Quizzes
from django.utils import timezone
from points.models import DailyPoints
from django.core.exceptions import ObjectDoesNotExist
from treasurehunt.models import Stage
from urllib.parse import urlparse, parse_qs


# Create your views here.
@login_required
def scan(request):
    return render(request, "scan.html")

def wrong(request):
    return render(request,"wrong.html",{'location':request.GET.get('extra')})

def wronglocation(request):
    return render(request,"wronglocation.html",{'location':request.GET.get('extra')})

def finish(request):
    return render(request,"finish.html")

def fail(request):
    return render(request,"fail.html")

def quiz(request):
    if request.method == "POST":
        # Load quiz and get questions and points per question
        quiz_id = request.POST.get("quiz_id")
        quiz_id = int(quiz_id)
        quiz = load(quiz_id)
        quizObj = Quizzes.objects.get(pk=quiz_id)
        questions = quiz.getQuestion(-1)
        pointsPerQuestion = quizObj.points

        # Set default values
        score = 0
        wrong = 0
        correct = 0
        total = 0

        # Get the time remaining
        time_remaining = request.POST.get("timer")
        time_remaining = int(time_remaining)

        # Iterate through each question and get the correct answer
        for q in questions:
            answer = quiz.getCorrect(total)
            total = total + 1

            # Check if user answer is correct
            if answer == request.POST.get(q):
                score = score + pointsPerQuestion
                correct = correct + 1
            else:
                wrong = wrong + 1
        
        # Calculate final score and percent
        percent = (correct/total) * 100
        percent = round(percent, 2)
        if percent % 1 == 0:
            percent = int(percent)
        if(percent > 50): #the player has passed
            return activityFinished(request,percent/100)
        else:
            return render(request,"fail.html")

    
    # User is loading quiz
    else:
        hunt = request.GET.get('hunt')
        quizID = request.GET.get('extra')
        quiz = load(int(quizID))
        context = {}
        time_limit = quiz.getTime()

        # Load quiz and get questions and answers
        questions = quiz.getQuestion(-1)
        answers = quiz.getAnswer(-1)

        # Change into form required for displaying quiz
        data = []
        i = 0
        for option in questions:
            if len(answers[i]) == 2:
                data.append({
                    'question': option,
                    'op1': answers[i][0],
                    'op2': answers[i][1],
                })
            elif len(answers[i]) == 3:
                data.append({
                    'question': option,
                    'op1': answers[i][0],
                    'op2': answers[i][1],
                    'op3': answers[i][2],
                })
            elif len(answers[i]) == 4:
                data.append({
                    'question': option,
                        'op1': answers[i][0],
                        'op2': answers[i][1],
                        'op3': answers[i][2],
                        'op4': answers[i][3],
                    })
            i = i + 1

        # Set context for quiz page
        context = {
            'hunt' : hunt,
            'questions': data,
            'quiz_id': quizID,
            'time_limit': time_limit
        }
        return render(request, "quiz.html", context)

def trivia(request):
    if request.method == 'GET':
        hunt = request.GET.get('hunt')
        return render(request,"trivia.html",{'fact':request.GET.get('extra'),'hunt':hunt})
    else:
        return activityFinished(request,1)

def verify(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            data = json.loads(request.body.decode('utf-8'))

            url = data['extra']         

            # Parse the URL
            parsed_url = urlparse(url)

            # Extract query parameters
            query_params = parse_qs(parsed_url.query)

            # Get huntID and stage_id from the query parameters
            huntID = query_params.get('huntID', [None])[0]
            stage = query_params.get('stage_id', [None])[0]

            longitude = data['longitude']
            latitude = data['latitude']
            
            #get the location of the qr code
            activitiesID = Treasure.getTreasure(huntID).getStageActivity(stage)
            location = Treasure.getActivities()[activitiesID]['location']
            x,y = location.split(",")
            print(x,latitude)
            print(y,longitude)

            circle = Circle((float(x),float(y)),radius = 0.001) #a circle centering on the qr code with about a 40m radius
            if(circle.contains_point([latitude,longitude])):
                name =  request.user.username
                #check the user has scanned the qr code for the stage after the last one they completed
                if Treasure.getStageNo(player_name=name,hunt_id=huntID) == int(stage)-1:
                    #render the activity
                    hunt = Treasure.getTreasure(id=huntID)
                    activityID = hunt.getStageActivity(stage)
                    activity = Treasure.getActivities()[activityID]
                    extra =  activity['info']
                    #render a different page based on the activity type
                    if(activity['type'] == "quiz"):
                        return JsonResponse({'redirect':'/treasurehunt/quiz','extra':extra,'hunt':huntID})
                    elif(activity['type'] == "trivia"):
                        return JsonResponse({'redirect':'/treasurehunt/trivia','extra':extra,'hunt':huntID})
                    elif(activity['type'] == "sortit"):
                        return JsonResponse({'redirect':'/sortit/game','extra':extra,'hunt':huntID})
                    elif(activity['type'] == "pairs"):
                        return JsonResponse({'redirect':'/pairs/game','extra':extra,'hunt':huntID})
                    #show the user the location of the next stage
                else:
                    #show a message about being on the wrong stage
                    try:
                        hunt = Treasure.getTreasure(id=huntID)
                        print(Treasure.getStageNo(request.user.username,huntID))
                        if Treasure.getStageNo(request.user.username,huntID) == 0:
                            #if the user has not started, show the location of the first page
                            activityID = hunt.getStageActivity(1)
                            activity = Treasure.getActivities()[activityID]
                        else:
                            #or else show the next stage from them
                            activityID = hunt.getStageActivity(Treasure.getStageNo(request.user.username,huntID)+1)
                            activity = Treasure.getActivities()[activityID]
                        return JsonResponse({'redirect':'/treasurehunt/wrong','extra':activity['location_name']})
                    except Stage.DoesNotExist:
                        #this means the next stage doesn't exist, so the treasure hunt is finished
                        return JsonResponse({'redirect':'/treasurehunt/finish'})
                return render(request,"scan.html")
            else:
                try:
                    #show the user that they are in the wrong location
                    hunt = Treasure.getTreasure(id=huntID)
                    activityID = hunt.getStageActivity(Treasure.getStageNo(request.user.username,huntID)+1)
                    activity = Treasure.getActivities()[activityID]
                    return JsonResponse({'redirect':'/treasurehunt/wronglocation','extra':activity['location_name']})
                except Stage.DoesNotExist:
                    #this means the next stage doesn't exist, so the treasure hunt is finished
                    return JsonResponse({'redirect':'/treasurehunt/finish'})
    else:
        return redirect(request,"/accounts/login.html",context={'extra':activity['location_name']})
    
def activityFinished(request,multiplier):
    huntID = request.POST.get('hunt')

    #add the points to the database
    stage = Treasure.getStageNo(request.user.username,huntID)
    hunt = Treasure.getTreasure(id=huntID)
    activityID = hunt.getStageActivity(stage+1)
    points = Treasure.getActivities()[activityID]['points']

    Treasure.incrementStage(request.user.username,huntID,points*multiplier)

    try: #if the user has not finished the treasure hunt
        stage += 1 #get the next stage
        activityID = hunt.getStageActivity(stage+1)
        activity = Treasure.getActivities()[activityID]
        return render(request,"next.html",{'location':activity['location_name']})
    except Stage.DoesNotExist: #if the user has finished the treasure hunt, there is no next stage
        points = hunt.getPoints()
        #add the bonus points for completing the treasure hunt
        Treasure.incrementStage(request.user.username,huntID,points*multiplier)
        return render(request,"finish.html")
    
def validatePage(request):
    return render(request,"validate.html")

def status(request):
    hunts = Treasure.getUserStages(request.user.username)
    notStarted = Treasure.getNewHunts(request.user.username)
    finished = []
    unfinished = []
    unstarted = []

    for treasure in notStarted:
        activityID = treasure.getStageActivity(1)
        location = Treasure.getActivities()[activityID]['location_name']
        unstarted.append([treasure.getName(), location])
        
    
    for hunt in hunts:
        if hunt[1] == -1:
            finished.append(hunt)
        else:
            unfinished.append(hunt)
    return render(request,"status.html",context={'finished':finished,'unfinished':unfinished, 'notStarted':unstarted})

 
def getPins(request):
    user = request.user.username
    locations = {}
    stages = Treasure.getUserStages(user)
    i=0
    for stage in stages:
        try:
            hunt = Treasure.getTreasure(stage[0])
            activityID = hunt.getStageActivity(stage[1])
            name = Treasure.getActivities()[activityID]['name']
            location = Treasure.getActivities()[activityID]['location']
            #pass in the name and location of any unfinished treasure hunt
            locations[i] = [name, location]
            i+=1
            
        except Stage.DoesNotExist: #occurs when user has finished the treasure hunt
            pass
        
    return JsonResponse(locations)
    