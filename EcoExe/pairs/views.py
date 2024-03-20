from django.shortcuts import render
from treasurehunt.views import activityFinished

def play_game(request):
    if request.method == 'GET':
        hunt = request.GET.get('hunt')
        return render(request, 'pairs/game.html',{'hunt':hunt}) #load the game page
    else:
        score = int(request.POST.get('score'))
        if(score>2000): #if the user has passed
            return activityFinished(request,score/4000)
        else:
            return render(request,"/treasurehunt/fail.html")
