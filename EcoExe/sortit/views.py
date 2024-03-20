#Authored by George Piper

from django.shortcuts import render,redirect
from treasurehunt.views import activityFinished

# Create your views here.
def game(request):
    if request.method == 'GET':
        hunt = request.GET.get('hunt')
        return render(request,"game.html",{'hunt':hunt}) #load the game page
    else:
        score = int(request.POST.get('score'))
        if score>200: #if the user has passed
            return activityFinished(request,score/1000)
        else:
            return redirect("/treasurehunt/fail")