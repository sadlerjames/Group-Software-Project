from django.shortcuts import render,redirect
from treasurehunt.views import activityFinished

# Create your views here.
def game(request):
    if request.method == 'GET':
        hunt = request.GET.get('hunt')
        return render(request,"game.html",{'hunt':hunt})
    else:
        score = int(request.POST.get('score')) #CURRENTLY BLANK
        if score>200:
            return activityFinished(request,score/1000)
        else:
            return redirect("/treasurehunt/fail")