from django.shortcuts import render
from treasurehunt.views import activityFinished

# Create your views here.
def game(request):
    if request.method == 'GET':
        hunt = request.GET.get('hunt')
        return render(request,"game.html",{'hunt':hunt})
    else:
        return activityFinished(request)