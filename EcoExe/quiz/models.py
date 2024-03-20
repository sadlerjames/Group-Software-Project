#Authored by Finn
from django.db import models
import quiz as q
from django import template

# Create your models here.
class Quizzes(models.Model):
    #id=models.AutoField(primary_key=True)
    points=models.IntegerField(default=0)
    time=models.IntegerField(default=60)
    def __str__(self):
        return str(self.id)

register=template.Library()
@register.tag_function
def getQ(a):
    #perform some random computation
    myQ= q.load(1)
    return myQ.getQ(a)

@register.tag_function
def getA(a):
    myQ=q.load(1)
    return myQ.get
