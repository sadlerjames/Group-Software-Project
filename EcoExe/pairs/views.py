from django.shortcuts import render
from treasurehunt.views import activityFinished

def play_game(request):
    if request.method == 'GET':
        hunt = request.GET.get('hunt')
        return render(request, 'pairs/game.html',{'hunt':hunt}) #load the game page
    else:
<<<<<<< HEAD
        return activityFinished(request)

def view_sources(request):
    return render(request, 'pairs/sources.html')
=======
        score = int(request.POST.get('score'))
        if(score>2000): #if the user has passed
            return activityFinished(request,score/4000)
        else:
            return render(request,"/treasurehunt/fail.html")
>>>>>>> 3ece69c8d0fad66a8249253ead07f77a9d5ea714
