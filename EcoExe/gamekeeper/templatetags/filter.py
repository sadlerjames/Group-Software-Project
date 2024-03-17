from django import template
from quiz.templatetags.quiz import load

register = template.Library()

@register.filter
def getName(x):
    return load(x['quiz_id']).getName()

@register.filter
def getID(x):
    return x['quiz_id']