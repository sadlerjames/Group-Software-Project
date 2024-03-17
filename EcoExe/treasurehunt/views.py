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


# Create your views here.
@login_required
def scan(request):
    return render(request, "scan.html")

def wrong(request):
    return render(request,"wrong.html",{'location':request.GET.get('extra')})

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
        final_score = score + time_remaining
        percent = (correct/total) * 100
        percent = round(percent, 2)
        if percent % 1 == 0:
            percent = int(percent)
        
        # Get current date
        timestamp = timezone.now()

        # Save this to the database
        try:
            db = DailyPoints(points=final_score, timestamp=timestamp, quiz_id=quizObj, user_id=request.user)
            db.save()
        except:
            pass

        # Set context for results page
        context = {
            'score': score,
            'time': time_remaining,
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'final_score': final_score
        }

        if(score > 2): #the player has passed
            huntID = request.POST.get('hunt')
            Treasure.incrementStage(request.user.username,huntID)
            try: #if the user has not finished the treasure hunt
                stage = Treasure.getStageNo(request.user.username,huntID) + 1 #get the next stage
                hunt = Treasure.getTreasure(id=huntID)
                activityID = hunt.getStageActivity(stage)
                activity = Treasure.getActivities()[activityID]
                return render(request,"next.html",{'location':activity['location_name']})
            except Stage.DoesNotExist: #if the user has finished the treasure hunt, there is no next stage
                return render(request,"finish.html")
        return render(request, "quiz_result.html", context)
    
    # User is loading quiz
    else:
        hunt = request.GET.get('hunt')
        quizID = request.GET.get('extra')
        quiz = load(quizID)
        context = {}
        time_limit = 30

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


def validate(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            #read these in from the qr code
            huntID = 1
            stage = 1
            data = json.loads(request.body.decode('utf-8'))
            longitude = data['longitude']
            latitude = data['latitude']
            x =  -3.5146264011643513 #need to be based on the qr code coordinates
            y = 50.73719035512385
            circle = Circle((x,y),radius = 0.001) #a circle centering on the qr code with about a 40m radius
            if(circle.contains_point([longitude,latitude])):
                print("Within radius")
            else:
                print("Not within radius")
            #PUT BACK IN LOCATION CHECK
            name =  request.user.username
            #name = "Kamal" #hardcoded for testing
            if Treasure.getStageNo(player_name=name,hunt_id=huntID) == stage-1:
                #render the activity
                hunt = Treasure.getTreasure(id=huntID)
                activityID = hunt.getStageActivity(stage)
                activity = Treasure.getActivities()[activityID]
                extra =  activity['info']
                if(activity['type'] == "Quiz"):
                    return JsonResponse({'redirect':'/treasurehunt/quiz','extra':extra,'hunt':huntID})
                #show the user the location of the next stage
            else:
                #show a message about being on the wrong stage
                hunt = Treasure.getTreasure(id=huntID)
                activityID = hunt.getStageActivity(stage)
                activity = Treasure.getActivities()[activityID]
                return JsonResponse({'redirect':'/treasurehunt/wrong','extra':activity['location_name']})
            return render(request,"scan.html")
    else:
        return redirect(request,"/accounts/login.html")