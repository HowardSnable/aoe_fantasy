from django.template.defaulttags import register
import datetime

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='subtract_date')
def subtract_date(value, arg):
    return (value - arg).days