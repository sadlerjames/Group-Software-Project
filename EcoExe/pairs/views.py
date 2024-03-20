from django.shortcuts import render
from treasurehunt.views import activityFinished

def play_game(request):
    if request.method == 'GET':
        hunt = request.GET.get('hunt')
        return render(request, 'pairs/game.html',{'hunt':hunt})
    else:
        return activityFinished(request)