from django.db import models

# Create your models here.
class Quizzes(models.Model):
    id=models.IntegerField(primary_key=True)
    points=models.IntegerField(default=0)
    def __str__(self):
        return self.id
    
import quiz as q
from django import template

register=template.Library()
@register.tag_function
def getQuiz():
    #perform some random computation
    myQ= q.load(1)
    return myQ.getQA(0),myQ.getCorrect(0)
