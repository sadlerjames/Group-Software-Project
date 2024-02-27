from django.db import models
from django.utils import timezone

class Points(models.Model):
    user_id = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    quiz_id = models.ForeignKey("quiz.Quizzes", related_name="quiz_id", on_delete=models.SET_NULL, null=True)
    points = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now())

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'quiz_id'], name='composite_primary_key')
        ]
