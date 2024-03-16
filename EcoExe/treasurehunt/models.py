#Authored by Finn Ashby
from django.db import models
#from treasurehunt import treasure
# Create your models here.
from django.db import models

from django import template

from django.db import models

class TreasureHunt(models.Model):
    hunt_id = models.AutoField(primary_key=True)
    points = models.IntegerField()
    name=models.CharField(max_length=100,unique=True)
    #location = models.CharField(max_length=100)
    image=models.TextField(default='/img/Default.png')

    def __str__(self):
        return f"Treasure Hunt {self.hunt_id}"

class Activities(models.Model):
    act_id=models.AutoField(primary_key=True)
    type=models.TextField()
    name=models.TextField()
    info=models.TextField()
    location=models.TextField()
    location_name=models.TextField(default="Parker moot room!")

class Stage(models.Model):
    hunt = models.ForeignKey(TreasureHunt, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    activity_id=models.ForeignKey(Activities,on_delete=models.CASCADE,default=1)
    no_points = models.IntegerField()
    information = models.TextField()

    class Meta:
        unique_together = ('hunt', 'order')

    def __str__(self):
        return f"Slot {self.order} of Treasure Hunt {self.hunt.hunt_id}"
    


    

class UserTreasure(models.Model):
    hunt = models.ForeignKey(TreasureHunt, on_delete=models.CASCADE)
    player = models.CharField(max_length=100)
    stage_completed = models.IntegerField(default=False)
    no_points = models.IntegerField()

    class Meta:
        # Define composite primary key
        unique_together = ('hunt', 'player')

    def __str__(self):
        return f"{self.player.username}'s Progress in Treasure Hunt {self.hunt.hunt_id}"