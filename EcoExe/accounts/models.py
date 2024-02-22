from django.db import models

class User(models.Model):
    username = models.CharField(max_length=16)
    birthday = models.DateField()
    points = models.IntegerField(default=0)
    def __str__(self):
        return self.username