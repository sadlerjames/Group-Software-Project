from django import template
from quiz.templatetags.quiz import load
from treasurehunt.treasure import Treasure

register = template.Library()

@register.filter
def getName(x):
    return load(x['quiz_id']).getName()

@register.filter
def getID(x):
    return x['quiz_id']

@register.filter
def getTreasureName(x):
    return Treasure.getTreasure(x[0]).getName()

@register.filter
def getStage(x):
    return x[1]

@register.filter
def length(x):
    return len(x)>0