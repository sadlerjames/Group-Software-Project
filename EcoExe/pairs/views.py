from django.shortcuts import render

# Create your views here.
def play_game(request):
    return render(request, 'pairs/game.html')