from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.shortcuts import render
from collections import defaultdict
from operator import itemgetter
from .models import Points

def leaderboard(request):
    return render(request, "leaderboard.html")

def get_points(request):
    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        raise Http404()
    
    points = Points.objects.all().select_related('quiz_id', 'user_id')

    return points

    """data = []
    for point in points:
        data.append({
            'quiz_id': point.quiz_id.id,
            #'quiz_name': point.quiz_id.name,       NEEDS FUNCTION TO GET NAME FROM JSON
            'username': point.user_id.username,
            'points': point.points
        })

    return JsonResponse(list(data), safe=False)"""

def sort_leaderboard_by_user(request):
    points = get_points(request)

    user_points = defaultdict(int)
    for point in points:
        user_points[point.user_id.username] += point.points
    
    leaderboard = [{'username': username, 'points': points} for username, points in user_points.items()]
    
    leaderboard.sort(key=itemgetter('points'), reverse=True)

    return JsonResponse(leaderboard, safe=False)