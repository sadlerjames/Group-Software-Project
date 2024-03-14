# Authored by Jack Hales, George Piper, James Sadler

from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

# Create your models here.

class User(AbstractUser):
    is_gamekeeper = models.BooleanField('Is game keeper', default=False)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(blank=True, null=True)

    # Override the save method of the model
    def save(self):
        super().save()

        img = Image.open(self.avatar.path) # Open image

        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resize image
            img.save(self.avatar.path) # Save it again and override the larger image
            print("resized")

        print("saved")

   
