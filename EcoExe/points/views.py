# Authored by Jack Hales

from django.shortcuts import render
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from operator import itemgetter
from .models import Points
from quiz.models import Quizzes
from quiz.templatetags import quiz
from treasurehunt.models import TreasureHunt
from treasurehunt.treasure import Treasure
from treasurehunt.models import UserTreasure

def leaderboard(request):
    return render(request, "leaderboard.html")

# Function to populate drop down of available leaderboards
def fetch_options(request):
    # Throw 404 error if user tries to access URL
    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        raise Http404()
    
    # Is this for treasure hunts or quizzes?
    leaderboard_type = request.GET.get('type')

    if leaderboard_type == "treasure_hunt":
        # Fetch all quizzes from database
        options = TreasureHunt.objects.values_list('hunt_id', flat=True)
        # Iterate through each quiz object and store the id and name
        data = []
        for option in options:
            data.append({
                'quiz_id': option,
                'quiz_name': Treasure.getTreasure(option).getName(),
            })
            
    elif leaderboard_type == "quiz":
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
    
    # Is this for treasure hunts or quizzes?
    leaderboard_type = request.GET.get('type')

    # Get options from AJAX request and fetch points from the database
    quiz_id = request.GET.get('quiz_id')
    filter = request.GET.get('filter')
    if leaderboard_type == "treasure_hunt":
        points = UserTreasure.objects.all()
        print(points)
            
    elif leaderboard_type == "quiz":
        points = Points.objects.all().select_related('quiz_id', 'user_id')
    
    data = []

    # If points table isn't empty, convert objects into a list of dictionaries
    if points.exists():
        points_data = []
        for point in points:
            if leaderboard_type == "treasure_hunt":
                point_dict = {
                    'username': point.player,
                    'quiz_id': point.hunt_id,
                    'points': point.no_points,
                    'timestamp': timezone.now(),
                }
            elif leaderboard_type == "quiz":
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
