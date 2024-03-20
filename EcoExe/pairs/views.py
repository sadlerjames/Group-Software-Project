from django.shortcuts import render
from treasurehunt.views import activityFinished

# Create view for playing the pairs game
def play_game(request):
    # Play game
    if request.method == 'GET':
        hunt = request.GET.get('hunt')
        return render(request, 'pairs/game.html',{'hunt':hunt})
    # Game complete so show score
    else:
        score = int(request.POST.get('score'))
        if(score>2000):
            return activityFinished(request,score/4000)
        else:
            return render(request,"/treasurehunt/fail.html")

# Create view for game image asset sources
def view_sources(request):
    return render(request, 'pairs/sources.html')
