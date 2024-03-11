# Authored by Jack Hales, George Piper, James Sadler

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_gamekeeper = models.BooleanField('Is game keeper', default=False)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(blank=True, null=True)
   
