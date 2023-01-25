from django.template.defaulttags import register
from django.utils import timezone

@register.filter
def get_item(dictionary, key):
    if dictionary:
        return dictionary.get(key)

@register.filter(name='subtract_date')
def subtract_date(value, arg):
    return (value - arg).days