from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_player = models.BooleanField('Is player', default=False)
    is_gamekeeper = models.BooleanField('Is game keeper', default=False)
