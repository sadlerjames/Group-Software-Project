from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import ast

def quizzes(request):
    return render(request, 'quiz/quizzes.html')

def get_quiz(request):
    if request.method == "GET":
        data = request.GET.get('getdata',None)
        print(ast.literal_eval(data))
        with open("quiz/templatetags/quizzes/"+ast.literal_eval(data)+'.json') as inf:
            question = json.load(inf)
            print(question)
        return JsonResponse(question)