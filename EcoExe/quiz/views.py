from django.shortcuts import render
<<<<<<< HEAD
from django.http import JsonResponse, HttpResponse
import json
import ast
=======
from quiz.templatetags.quiz import Quiz, load
# Create your views here.
>>>>>>> 2be866cdc4c145ecdba944b25ba25cd05305cac6


def quizzes(request):
<<<<<<< HEAD
    return render(request, 'quiz/quiznew.html')

def get_quiz(request):
    if request.method == "GET":
        data = request.GET.get('getdata',None)
        print(ast.literal_eval(data))
        with open("quiz/templatetags/quizzes/"+ast.literal_eval(data)+'.json') as inf:
            question = json.load(inf)
            print(question)
        return JsonResponse(question)
=======
    context = {}
    quiz = load(1)
    context['id'] = quiz.id
    context['questions'] = quiz.getQuestion()
    context['total_questions'] = range(len(quiz.getQuestion()))

    options = [
        [],
        [],
        [],
        []
    ]
    for answer_set in quiz.getAnswer():
        for i in range(0, 4):
            try:
                options[i].append(answer_set[i])
            except:
                options[i].append("EMPTY ANSWER")

    context['answer0'] = options[0]
    context['answer1'] = options[1]
    context['answer2'] = options[2]
    context['answer3'] = options[3]

    correct = []
    for i in range(0, len(quiz.getQuestion())):
        correct.append(quiz.getCorrect(i))

    context['correct'] = correct
    return render(request, 'quizzes.html', context)
>>>>>>> 2be866cdc4c145ecdba944b25ba25cd05305cac6
