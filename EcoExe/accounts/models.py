from django.db import models
from django.contrib.auth.models import User
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#extending-the-existing-user-model
# https://docs.djangoproject.com/en/5.0/ref/signals/#django.db.models.signals.post_save