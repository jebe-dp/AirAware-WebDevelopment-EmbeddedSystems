from django import template

register = template.Library()

@register.filter
def yes_no(value):
    return "Yes" if value else "No"

@register.filter
def getattribute(obj, attr):
    return getattr(obj, attr)