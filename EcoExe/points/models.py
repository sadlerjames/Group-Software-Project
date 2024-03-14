# Authored by Jack Hales

from django.db import models
from django.utils import timezone

# Create Points model for the database with required fields
class Points(models.Model):
    user_id = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    quiz_id = models.ForeignKey("quiz.Quizzes", related_name="quiz_id", on_delete=models.SET_NULL, null=True)
    points = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now())

    # Add constraint that user_id and quiz_id act as a composite primary key
    # This prevents the user having two scores for the same quiz
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'quiz_id'], name='composite_primary_key')
        ]

# Create DailyPoints model for the database with required fields
class DailyPoints(models.Model):
    user_id = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    quiz_id = models.ForeignKey("quiz.Quizzes", related_name="daily_quiz_id_points", on_delete=models.SET_NULL, null=True)
    points = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now())

    # Add constraint that user_id and quiz_id act as a composite primary key
    # This prevents the user having two scores for the same quiz
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'quiz_id'], name='composite_primary_key_2')
        ]