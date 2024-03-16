from django.shortcuts import render,redirect
import json
from matplotlib.patches import Circle
from treasurehunt.treasure import Treasure
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from quiz.templatetags.quiz import load


# Create your views here.
@login_required
def scan(request):
    return render(request, "scan.html")

def quiz(request):
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
            stage = 2

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
            name = "Kamal"
            if Treasure.getStageNo(player_name=name,hunt_id=huntID) == stage-1:
                #render the activity
                hunt = Treasure.getTreasure(id=huntID)
                activityID = hunt.getStageActivity(stage)
                activity = Treasure.getActivities()[activityID]
                extra =  activity['info']

                if(activity['type'] == "Quiz"):
                    return JsonResponse({'redirect':'/treasurehunt/quiz','extra':extra})
                #show the user the location of the next stage
            else:
                print("No")
                #verify the user is on the correct stage
                #show a message about being on the wrong stage
            return render(request,"scan.html")
    else:
        return redirect(request,"/accounts/login.html")