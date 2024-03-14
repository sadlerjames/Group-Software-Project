#Authored by Sam Arrowsmith, Finn Ashby, Dan Harkness-Moore

from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
import json
import ast
from quiz.templatetags.quiz import load
from gamekeeper.models import DailyQuizzes
from quiz.models import Quizzes
from points.models import DailyPoints
import datetime


def quizzes(request):
    return render(request, 'quiz/quiznew.html')

def get_quiz(request):
    if request.method == "GET":
        data = request.GET.get('getdata',None)
        #print(ast.literal_eval(data))
        with open("quiz/templatetags/quizzes/"+ast.literal_eval(data)+'.json') as inf:
            question = json.load(inf)
            #print(question)
        return JsonResponse(question)

def daily_quiz(request):
    # User has submitted quiz
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
        return render(request, "daily_quiz_result.html", context)
    
    # User is loading quiz
    else:
        context = {}
        # Check if user has already completed the daily quiz
        today = datetime.date.today()
        quizzesToday = DailyPoints.objects.filter(timestamp__date=today)
        for quiz in quizzesToday:
            if quiz.user_id == request.user:
                return render(request, "daily_quiz.html", context)

        # Fetch all daily quizzes from database
        dailyQuizzes = DailyQuizzes.objects.all()
            
        # Default quiz and time limit if not set for today
        quiz_id = 1
        time_limit = 30

        # Get today's daily quiz
        for option in dailyQuizzes:
            if option.date == today:
                quiz_id = option.quiz_id.id
                quiz_id = int(quiz_id)
                time_limit = option.time_limit
                time_limit = int(time_limit)

        # Load quiz and get questions and answers
        quiz = load(quiz_id)
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
            'quiz_id': quiz_id,
            'time_limit': time_limit
        }
        return render(request, "daily_quiz.html", context)
    
def daily_quiz_result(request):
    return render(request, "daily_quiz_result.html")
