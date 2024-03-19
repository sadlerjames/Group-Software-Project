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
def getLocation(x):
    hunt = Treasure.getTreasure(x[0])
    activityID = hunt.getStageActivity(x[1])
    return Treasure.getActivities()[activityID]['location_name']

@register.filter
def length(x):
    return len(x)>0

@register.filter
def getUnstartedHuntName(x):
    return x[0]

@register.filter
def getUnstartedHuntLocation(x):
    return x[1]
 
@register.filter
def exists(x):
    return x!= None
