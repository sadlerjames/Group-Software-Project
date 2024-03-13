# Authored by Jack Hales

from django.db import models

# Create DailyQuizzes model for the database with required fields
class DailyQuizzes(models.Model):
    date = models.DateField(primary_key=True)
    quiz_id = models.ForeignKey("quiz.Quizzes", related_name="daily_quiz_id", on_delete=models.SET_NULL, null=True)