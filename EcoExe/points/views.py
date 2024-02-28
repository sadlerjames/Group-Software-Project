# Authored by Jack Hales

from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from operator import itemgetter
from .models import Points
from quiz.models import Quizzes
from quiz.templatetags import quiz

def leaderboard(request):
    return render(request, "leaderboard.html")

# Function to populate drop down of available leaderboards
def fetch_options(request):
    # Throw 404 error if user tries to access URL
    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        raise Http404()
    
    # Fetch all quizzes from database
    options = Quizzes.objects.values_list('id', flat=True)
    
    # Iterate through each quiz object and store the id and name
    data = []
    for option in options:
        data.append({
            'quiz_id': option,
            'quiz_name': quiz.load(option).getName(),
        })

    return JsonResponse(list(data), safe=False)

def get_points(request):
    # Throw 404 error if user tries to access URL
    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        raise Http404()
    
    # Get options from AJAX request and fetch points from the database
    quiz_id = request.GET.get('quiz_id')
    filter = request.GET.get('filter')
    points = Points.objects.all().select_related('quiz_id', 'user_id')
    data = []

    # If points table isn't empty, convert objects into a list of dictionaries
    if points.exists():
        points_data = []
        for point in points:
            point_dict = {
                'username': point.user_id.username,
                'quiz_id': point.quiz_id.id,
                'points': point.points,
                'timestamp': point.timestamp,
            }
            points_data.append(point_dict)

        # Filter out points that match the timestamp filter selected
        if filter != "all-time":
            time_now = timezone.now()

            if filter == "past-year":
                time = time_now - relativedelta(years=1)
            elif filter == "past-month":
                time = time_now - relativedelta(months=1)
            elif filter == "past-week":
                time = time_now - relativedelta(weeks=1)
            elif filter == "past-day":
                time = time_now - relativedelta(days=1)
            
            points_data = [point for point in points_data if point.get('timestamp', 0) >= time]

        # Check again that this filtering hasn't made an empty list
        if points_data:
            # Sum points for each user when the overall leaderboard is selected
            if quiz_id == "overall":
                user_points = defaultdict(int)
                for point in points_data:
                    user_points[point['username']] += point['points']
                
                data = [{'username': username, 'points': points} for username, points in user_points.items()]
                
                # Sort the leaderboard into descending order
                data.sort(key=itemgetter('points'), reverse=True)
            
            # Otherwise, iterate through the points for the chosen quiz
            else:
                for point in points_data:
                    if point['quiz_id'] == int(quiz_id):
                        data.append({
                            'username': point['username'],
                            'points': point['points']
                        })

                # Sort the leaderboard into descending order
                data.sort(key=itemgetter('points'), reverse=True)

    return JsonResponse(list(data), safe=False)
