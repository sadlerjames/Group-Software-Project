from django import template
from treasurehunt.treasure import Treasure

register = template.Library()

@register.filter
def getName(x):
    return Treasure.getTreasure(x[0]).getName()

@register.filter
def getStage(x):
    return x[1]

@register.filter
def length(x):
    return len(x)>0