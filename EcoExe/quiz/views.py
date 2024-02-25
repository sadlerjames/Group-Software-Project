from django.shortcuts import render
# Create your views here.

def quizzes(request):
    return render(request, 'quizzes.html')
