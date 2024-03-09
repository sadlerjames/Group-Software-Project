from django import template
from quiz.templatetags.quiz import load

register = template.Library()

@register.filter
def getName(x):
    return load(x[:-5]).getName()