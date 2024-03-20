from django.shortcuts import render
from treasurehunt.views import activityFinished

def play_game(request):
    if request.method == 'GET':
        hunt = request.GET.get('hunt')
        return render(request, 'pairs/game.html',{'hunt':hunt})
    else:
        score = int(request.POST.get('score'))
        if(score>2000):
            return activityFinished(request,score/4000)
        else:
            return render(request,"/treasurehunt/fail.html")
